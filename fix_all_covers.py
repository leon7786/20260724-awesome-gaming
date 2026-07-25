#!/usr/bin/env python3
"""
批量修复所有游戏海报
"""
import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 游戏名称到Steam appid的映射（需要手动补充的）
MANUAL_APPID_MAP = {
    '心灵杀手2': 2915520,
    '我的世界': 1672980,
    '光环：战斗进化': 718130,
    '控制': 870780,
    '旅途': 638230,
    '蔚蓝': 504230,
    '森林': 242760,
    '极限竞速：地平线4': 1293830,
    '死亡搁浅': 1850570,
    '仁王 1': 485510,
    '守望先锋2': 2357570,
    '使命召唤：现代战争': 1962663,
    'XCOM 2：选民之战': 261410,
    '上古卷轴 4：湮没': 22330,
    '使命召唤 4：现代战争': 7940,
    '使命召唤：现代战争3': 1938090,
    '光环 2': 1064191,
    '刀魂 / 剑魂 1': 1775820,
    '反恐精英：全球攻势': 730,
    '大神': 2508860,
    '宇宙机器人': 2462060,
    '师父': 2138710,
    '异形：隔离': 214490,
    '战神 1': 1593500,
    '战神 3': 1922520,
    '披萨塔': 1702320,
    '文明 6': 289070,
    '晶体管': 2379780,
    '暗黑破坏神 II': 1369630,
    '最终幻想 VII (原版)': 39140,
    '植物大战僵尸': 3590,
    '求生之路 1': 500,
    '潜龙谍影 4': 1938090,
    '生化危机 1 (原版)': 304240,
    '生化危机 2 (原版)': 883710,
    '生化危机 4 (原版)': 2523470,
    '街头霸王 II': 1365760,
    '雷曼：传奇': 207490,
    '鬼泣 3': 260230,
}

def search_steam_appid(game_name, en_name):
    """搜索Steam API获取appid"""
    search_terms = [en_name, game_name]
    
    for term in search_terms:
        if not term:
            continue
        
        try:
            url = f"https://store.steampowered.com/api/storesearch/?term={requests.utils.quote(term)}&l=schinese&cc=CN"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            
            if data.get('total', 0) > 0:
                # 返回第一个匹配结果
                return data['items'][0]['id']
        except Exception as e:
            print(f"  搜索 '{term}' 失败: {e}")
    
    return None

def get_steam_cover(appid):
    """从Steam API获取海报URL"""
    if not appid:
        return None
    
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=schinese"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        
        if data.get(str(appid), {}).get('success'):
            # 尝试获取竖版海报
            header = data[str(appid)]['data'].get('header_image', '')
            if header:
                # 转换为竖版海报格式
                # header_image: https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1245620/header.jpg
                # library_600x900: https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1245620/library_600x900.jpg
                cover = header.replace('/header.jpg', '/library_600x900.jpg')
                return cover
    except Exception as e:
        print(f"  获取 appid={appid} 海报失败: {e}")
    
    return None

def fix_game_cover(game):
    """修复单个游戏的海报"""
    cn_name = game.get('cn_name', '')
    en_name = game.get('en_name', '')
    current_cover = game.get('cover', '')
    appid = game.get('appid')
    
    # 1. 检查当前海报是否可用
    if current_cover:
        try:
            resp = requests.head(current_cover, timeout=5, allow_redirects=True)
            if resp.status_code == 200:
                return None  # 海报正常，无需修复
        except:
            pass  # 海报不可用，需要修复
    
    # 2. 尝试从手动映射获取appid
    if cn_name in MANUAL_APPID_MAP:
        appid = MANUAL_APPID_MAP[cn_name]
        game['appid'] = appid
        print(f"  {cn_name}: 使用手动映射 appid={appid}")
    
    # 3. 如果没有appid，尝试搜索
    if not appid:
        appid = search_steam_appid(cn_name, en_name)
        if appid:
            game['appid'] = appid
            print(f"  {cn_name}: 搜索到 appid={appid}")
            time.sleep(0.3)  # 避免请求过快
    
    # 4. 获取海报
    if appid:
        cover = get_steam_cover(appid)
        if cover:
            game['cover'] = cover
            return ('fixed', cn_name, cover)
    
    return ('failed', cn_name, '无法获取海报')

def main():
    # 加载游戏数据
    with open('/root/Projects/20260724-awesome-gaming/games.json', 'r', encoding='utf-8') as f:
        games = json.load(f)
    
    print(f"开始修复 {len(games)} 个游戏的海报...\n")
    
    fixed_count = 0
    failed_count = 0
    failed_games = []
    
    # 并行修复（限制并发数避免被封）
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fix_game_cover, game): game for game in games}
        
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            
            if result:
                status, name, info = result
                if status == 'fixed':
                    fixed_count += 1
                    print(f"[{i}/{len(games)}] ✓ {name}: {info}")
                else:
                    failed_count += 1
                    failed_games.append(name)
                    print(f"[{i}/{len(games)}] ✗ {name}: {info}")
            
            if i % 50 == 0:
                print(f"\n进度: {i}/{len(games)}\n")
    
    # 保存修复后的数据
    with open('/root/Projects/20260724-awesome-gaming/games.json', 'w', encoding='utf-8') as f:
        json.dump(games, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"修复完成！")
    print(f"✓ 成功修复: {fixed_count} 个")
    print(f"✗ 修复失败: {failed_count} 个")
    
    if failed_games:
        print(f"\n失败的游戏列表:")
        for name in failed_games:
            print(f"  - {name}")

if __name__ == '__main__':
    main()
