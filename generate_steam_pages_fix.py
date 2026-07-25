#!/usr/bin/env python3
"""
Steam风格详情页生成器 - 视频修复版
"""
import json
import os
import re
import requests
import time
from pathlib import Path

with open('games.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

def get_steam_data(appid):
    """从Steam API获取数据"""
    if not appid:
        return None
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=schinese"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get(str(appid), {}).get('success'):
            return data[str(appid)]['data']
    except Exception as e:
        pass
    return None

def render_template(tpl, data):
    """模板渲染"""
    result = tpl
    
    # 处理 {{#each ARRAY}}...{{/each}}
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
                    item_content = item_content.replace('{{' + k + '}}', str(v) if v else '')
            else:
                item_content = item_content.replace('{{this}}', str(item))
            items.append(item_content)
        return ''.join(items)
    
    result = re.sub(r'\{\{#each\s+(\w+)\}\}(.*?)\{\{/each\}\}', replace_each, result, flags=re.DOTALL)
    
    # 处理 {{#unless KEY}}...{{/unless}}
    def replace_unless(match):
        key = match.group(1)
        content = match.group(2)
        if not data.get(key):
            return content
        return ''
    result = re.sub(r'\{\{#unless\s+(\w+)\}\}(.*?)\{\{/unless\}\}', replace_unless, result, flags=re.DOTALL)
    
    # 处理 {{#if KEY}}...{{/if}}
    def replace_if(match):
        key = match.group(1)
        content = match.group(2)
        if data.get(key):
            return content
        return ''
    for _ in range(3):
        result = re.sub(r'\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}', replace_if, result, flags=re.DOTALL)
    
    # 处理 {{{KEY}}} 和 {{KEY}}
    for key, value in data.items():
        if isinstance(value, str):
            result = result.replace('{{{' + key + '}}}', value)
            result = result.replace('{{' + key + '}}', value)
    
    # 清理残留模板语法
    result = re.sub(r'\{\{/?if[^}]*\}\}', '', result)
    result = re.sub(r'\{\{#each[^}]*\}\}', '', result)
    result = re.sub(r'\{\{/each\}\}', '', result)
    result = re.sub(r'\{\{#unless[^}]*\}\}', '', result)
    result = re.sub(r'\{\{/unless\}\}', '', result)
    
    return result

def generate_detail_page(game):
    """生成详情页"""
    appid = game.get('appid')
    slug = game.get('detail', '').replace('games/', '').replace('/', '')
    if not slug:
        return None
    
    # 获取Steam数据
    steam_data = get_steam_data(appid)
    if steam_data:
        time.sleep(0.3)
    
    # 获取视频缩略图（从API）
    movie_thumbnails = []
    if steam_data:
        movies = steam_data.get('movies', [])
        movie_thumbnails = [m.get('thumbnail', '') for m in movies if m.get('thumbnail')]
    
    # 获取截图
    screenshots = []
    if steam_data:
        screenshots = [s['path_full'] for s in steam_data.get('screenshots', [])]
    else:
        screenshots = game.get('screenshots', [])
    
    # 构建媒体列表：视频 + 截图
    media_items = []
    
    # 添加视频（使用Steam官方iframe嵌入）
    for movie in movie_thumbnails:
        media_items.append({
            'type': 'video',
            'url': movie,  # 使用缩略图作为placeholder
            'thumb': movie
        })
    
    # 添加截图
    for ss in screenshots:
        media_items.append({
            'type': 'image',
            'url': ss,
            'thumb': ss.replace('.jpg', '.600x338.jpg') if ss.endswith('.jpg') else ss
        })
    
    # 生成主图HTML
    main_media_html = ''
    if media_items:
        first_item = media_items[0]
        if first_item['type'] == 'video':
            # 视频：使用iframe嵌入Steam视频页面
            video_url = f"https://store.steampowered.com/app/{appid}/"
            main_media_html = f'<iframe src="{video_url}" frameborder="0" allowfullscreen allow="autoplay; fullscreen"></iframe>'
        else:
            main_media_html = f'<img src="{first_item["url"]}" alt="Screenshot">'
    else:
        main_media_html = f'<img src="{game.get("cover", "")}" alt="Cover">'
    
    # 生成缩略图HTML
    thumbnails_html = ''
    for i, item in enumerate(media_items):
        active_class = 'active' if i == 0 else ''
        if item['type'] == 'video':
            # 视频缩略图带播放图标
            thumbnails_html += f'<div class="media-thumb {active_class}" data-index="{i}"><div class="play-icon">▶</div><img src="{item["thumb"]}" alt="Video"></div>\n'
        else:
            thumbnails_html += f'<div class="media-thumb {active_class}" data-index="{i}"><img src="{item["thumb"]}" alt="Screenshot"></div>\n'
    
    # 生成媒体数据JSON
    media_data_json = ',\n  '.join([
        json.dumps(item, ensure_ascii=False) for item in media_items
    ])
    
    # 生成下载链接
    downloads = game.get('downloads', [])
    downloads_html = ''
    if downloads:
        for dl in downloads:
            dl_type = dl.get('type', '')
            dl_url = dl.get('url', '')
            dl_name = dl.get('name', dl_type)
            downloads_html += f'<a href="{dl_url}" class="download-btn {dl_type}" target="_blank">{dl_name}</a>\n'
    else:
        downloads_html = '<p style="color:#8f98a0;">暂无下载链接</p>'
    
    # 生成系统需求
    pc_req_html = ''
    if steam_data:
        pc_req = steam_data.get('pc_requirements', {})
        if isinstance(pc_req, dict):
            minimum = pc_req.get('minimum', '')
            recommended = pc_req.get('recommended', '')
            if minimum or recommended:
                pc_req_html = f'''
<section class="content-section">
  <div class="content-block">
    <h2>系统需求</h2>
    <div class="sys-req">
      {f'<div class="sys-req-col"><h4>最低配置</h4><div>{minimum}</div></div>' if minimum else ''}
      {f'<div class="sys-req-col"><h4>推荐配置</h4><div>{recommended}</div></div>' if recommended else ''}
    </div>
  </div>
</section>'''
    
    # 准备模板数据
    data = {
        'GAME_NAME': game.get('cn_name', ''),
        'GAME_NAME_EN': game.get('en_name', ''),
        'COVER_IMAGE': game.get('cover', ''),
        'RELEASE_DATE': game.get('year', ''),
        'GENRES': ', '.join(game.get('genres', [])) if game.get('genres') else '',
        'SCORE': str(game.get('score', '')) if game.get('score') else '',
        'SHORT_DESCRIPTION': game.get('description', ''),
        'DEVELOPERS': '',
        'PUBLISHERS': '',
        'ABOUT_GAME': game.get('about_game', game.get('description', '')),
        'STEAM_APPID': str(appid or ''),
        'MAIN_MEDIA_HTML': main_media_html,
        'THUMBNAILS_HTML': thumbnails_html,
        'MEDIA_DATA_JSON': media_data_json,
        'DOWNLOADS_HTML': downloads_html,
        'PC_REQ_HTML': pc_req_html
    }
    
    # 从Steam数据补充
    if steam_data:
        data['GENRES'] = ', '.join([g['description'] for g in steam_data.get('genres', [])])
        data['DEVELOPERS'] = ', '.join(steam_data.get('developers', []))
        data['PUBLISHERS'] = ', '.join(steam_data.get('publishers', []))
        data['ABOUT_GAME'] = steam_data.get('about_the_game', data['ABOUT_GAME'])
        data['SHORT_DESCRIPTION'] = steam_data.get('short_description', data['SHORT_DESCRIPTION'])
        data['RELEASE_DATE'] = steam_data.get('release_date', {}).get('date', data['RELEASE_DATE'])
    
    # 读取模板
    with open('steam-template-v4.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
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
