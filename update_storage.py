#!/usr/bin/env python3
"""
批量获取游戏存储需求并更新games.json
"""
import json
import requests
import re
import time

def get_storage_requirement(appid):
    """从Steam API获取存储需求"""
    if not appid:
        return None
    
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=schinese"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        
        if data.get(str(appid), {}).get('success'):
            game_data = data[str(appid)]['data']
            pc_req = game_data.get('pc_requirements', {})
            
            if isinstance(pc_req, dict):
                minimum = pc_req.get('minimum', '')
                recommended = pc_req.get('recommended', '')
                
                # 优先从推荐配置获取
                storage_text = recommended or minimum
                
                # 匹配 "需要 XX GB 可用空间"
                match = re.search(r'需要\s*(\d+)\s*GB\s*可用空间', storage_text)
                if match:
                    return int(match.group(1))
                
                # 匹配 "XX GB available space"
                match = re.search(r'(\d+)\s*GB\s*available\s*space', storage_text, re.IGNORECASE)
                if match:
                    return int(match.group(1))
        
        return None
    except Exception as e:
        return None

def main():
    # 读取games.json
    with open('games.json', 'r', encoding='utf-8') as f:
        games = json.load(f)
    
    print(f"总共 {len(games)} 个游戏\n")
    
    # 批量获取存储需求
    updated = 0
    for i, game in enumerate(games):
        if i % 50 == 0 and i > 0:
            print(f"进度: {i}/{len(games)}")
        
        appid = game.get('appid')
        if appid and 'size_gb' not in game:
            size = get_storage_requirement(appid)
            if size:
                game['size_gb'] = size
                updated += 1
                if size >= 20:
                    print(f"  ✓ {game['cn_name']}: {size}GB")
            time.sleep(0.2)
    
    print(f"\n更新完成: {updated} 个游戏添加了存储需求")
    
    # 保存
    with open('games.json', 'w', encoding='utf-8') as f:
        json.dump(games, f, ensure_ascii=False, indent=2)
    
    print("✓ 已保存到 games.json")
    
    # 统计超过20GB的游戏
    large_games = [g for g in games if g.get('size_gb', 0) >= 20]
    print(f"\n超过20GB的游戏: {len(large_games)} 个")
    for g in large_games:
        print(f"  {g['cn_name']}: {g['size_gb']}GB")

if __name__ == '__main__':
    main()
