#!/usr/bin/env python3
"""
用Steam风格模板重新生成所有游戏详情页
"""
import json
import os
import requests
import time
from pathlib import Path

# 读取游戏数据
with open('games.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

# 读取模板
with open('steam-template.html', 'r', encoding='utf-8') as f:
    template = f.read()

def get_steam_data(appid):
    """从Steam API获取完整数据"""
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=schinese"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get(str(appid), {}).get('success'):
            return data[str(appid)]['data']
    except Exception as e:
        print(f"  获取Steam数据失败: {e}")
    return None

def render_template(tpl, data):
    """简单模板渲染"""
    result = tpl
    
    # 简单替换
    for key, value in data.items():
        if isinstance(value, str):
            result = result.replace('{{' + key + '}}', value)
    
    # 处理条件块 {{#if KEY}}...{{/if}}
    import re
    
    # {{#if KEY}}...{{/if}}
    def replace_if(match):
        key = match.group(1)
        content = match.group(2)
        if data.get(key):
            return content
        return ''
    
    result = re.sub(r'\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}', replace_if, result, flags=re.DOTALL)
    
    # {{#unless KEY}}...{{/unless}}
    def replace_unless(match):
        key = match.group(1)
        content = match.group(2)
        if not data.get(key):
            return content
        return ''
    
    result = re.sub(r'\{\{#unless\s+(\w+)\}\}(.*?)\{\{/unless\}\}', replace_unless, result, flags=re.DOTALL)
    
    # {{#each ARRAY}}...{{/each}}
    def replace_each(match):
        key = match.group(1)
        content = match.group(2)
        arr = data.get(key, [])
        if not isinstance(arr, list):
            return ''
        
        items = []
        for item in arr:
            item_content = content
            if isinstance(item, dict):
                for k, v in item.items():
                    item_content = item_content.replace('{{' + k + '}}', str(v))
            else:
                item_content = item_content.replace('{{this}}', str(item))
            items.append(item_content)
        
        return ''.join(items)
    
    result = re.sub(r'\{\{#each\s+(\w+)\}\}(.*?)\{\{/each\}\}', replace_each, result, flags=re.DOTALL)
    
    # 处理数组索引 {{ARRAY.[0]}}
    def replace_array_index(match):
        key = match.group(1)
        idx = int(match.group(2))
        arr = data.get(key, [])
        if isinstance(arr, list) and idx < len(arr):
            return str(arr[idx])
        return ''
    
    result = re.sub(r'\{\{(\w+)\.\[(\d+)\]\}\}', replace_array_index, result)
    
    return result

def generate_detail_page(game):
    """生成单个游戏详情页"""
    appid = game.get('appid')
    slug = game.get('detail', '').replace('games/', '').replace('/', '')
    
    if not slug:
        return None
    
    # 获取Steam数据
    steam_data = None
    if appid:
        steam_data = get_steam_data(appid)
        time.sleep(0.3)
    
    # 准备模板数据
    data = {
        'GAME_NAME': game.get('cn_name', ''),
        'GAME_NAME_EN': game.get('en_name', ''),
        'COVER_IMAGE': game.get('cover', ''),
        'RELEASE_DATE': game.get('year', ''),
        'GENRES': ', '.join(game.get('genres', [])),
        'SCORE': str(game.get('score', '')),
        'SHORT_DESCRIPTION': game.get('description', ''),
        'DEVELOPERS': game.get('developers', [''])[0] if game.get('developers') else '',
        'PUBLISHERS': game.get('publishers', [''])[0] if game.get('publishers') else '',
        'ABOUT_GAME': game.get('about_game', game.get('description', '')),
        'STEAM_APPID': str(appid or ''),
        'VIDEO_URL': '',
        'SCREENSHOTS': game.get('screenshots', []),
        'DOWNLOADS': game.get('downloads', []),
        'PC_REQUIREMENTS': game.get('pc_requirements', {})
    }
    
    # 从Steam数据补充
    if steam_data:
        data['GENRES'] = ', '.join([g['description'] for g in steam_data.get('genres', [])])
        data['DEVELOPERS'] = ', '.join(steam_data.get('developers', []))
        data['PUBLISHERS'] = ', '.join(steam_data.get('publishers', []))
        data['ABOUT_GAME'] = steam_data.get('about_the_game', data['ABOUT_GAME'])
        data['SHORT_DESCRIPTION'] = steam_data.get('short_description', data['SHORT_DESCRIPTION'])
        data['RELEASE_DATE'] = steam_data.get('release_date', {}).get('date', data['RELEASE_DATE'])
        
        # 视频
        movies = steam_data.get('movies', [])
        if movies:
            data['VIDEO_URL'] = movies[0].get('mp4', {}).get('480', '')
        
        # 截图
        data['SCREENSHOTS'] = [s['path_full'] for s in steam_data.get('screenshots', [])]
        
        # 系统需求
        pc_req = steam_data.get('pc_requirements', {})
        if isinstance(pc_req, dict):
            data['PC_REQUIREMENTS'] = pc_req
    
    # 渲染模板
    html = render_template(template, data)
    
    # 保存文件
    output_dir = Path('games') / slug
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_dir / 'index.html'

# 批量生成
print(f"开始生成 {len(games)} 个游戏详情页...")
success = 0

for i, game in enumerate(games):
    if i % 50 == 0:
        print(f"进度: {i}/{len(games)}")
    
    try:
        result = generate_detail_page(game)
        if result:
            success += 1
    except Exception as e:
        print(f"生成失败 {game.get('cn_name')}: {e}")

print(f"\n完成！成功生成 {success}/{len(games)} 个详情页")
