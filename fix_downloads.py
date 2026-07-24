#!/usr/bin/env python3
"""
使用 FastAPI 通道修复 games.json 中的下载链接
"""

import json
import requests
import time
from typing import Dict, List, Optional

# FastAPI 服务地址
API_BASE = "http://127.0.0.1:8001"

# 错误的链接（需要修复）
WRONG_GAMER520 = "https://www.gamer520.com/61541.html"
WRONG_X6D = "https://www.x6d.com/i-wz-8398.html"

def search_gamer520(query: str) -> Optional[str]:
    """通过 FastAPI 搜索 gamer520"""
    try:
        response = requests.get(
            f"{API_BASE}/gamer520/search",
            params={"q": query},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("results"):
                # 返回第一个结果的 URL
                return data["results"][0]["url"]
    except Exception as e:
        print(f"  搜索 gamer520 失败: {e}")
    return None

def search_x6d(query: str) -> Optional[str]:
    """通过 FastAPI 搜索 x6d"""
    try:
        response = requests.get(
            f"{API_BASE}/x6d/search",
            params={"q": query},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("results"):
                # 返回第一个结果的 URL
                return data["results"][0]["url"]
    except Exception as e:
        print(f"  搜索 x6d 失败: {e}")
    return None

def fix_game_downloads(game: Dict) -> bool:
    """修复单个游戏的下载链接"""
    fixed = False
    downloads = game.get("downloads", [])
    
    for i, dl in enumerate(downloads):
        url = dl.get("url", "")
        dl_type = dl.get("type", "")
        
        # 检查是否是错误链接
        if url == WRONG_GAMER520 or url == WRONG_X6D:
            print(f"  发现错误链接: {dl_type} -> {url}")
            
            # 根据类型搜索正确的链接
            if dl_type == "gamer520":
                new_url = search_gamer520(game["cn_name"])
                time.sleep(0.5)  # 避免请求过快
            elif dl_type == "x6d":
                new_url = search_x6d(game["cn_name"])
                time.sleep(0.5)
            else:
                continue
            
            if new_url:
                downloads[i]["url"] = new_url
                print(f"  ✓ 更新为: {new_url}")
                fixed = True
            else:
                print(f"  ✗ 未找到正确的链接")
    
    return fixed

def main():
    # 检查 FastAPI 服务是否运行
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code != 200:
            print("FastAPI 服务未运行，请先启动:")
            print("  cd /root/.hermes/services/game-resources-api")
            print("  bash start.sh")
            return
    except:
        print("FastAPI 服务未运行，请先启动:")
        print("  cd /root/.hermes/services/game-resources-api")
        print("  bash start.sh")
        return
    
    # 读取 games.json
    games_file = "/root/Projects/20260724-awesome-gaming/games.json"
    with open(games_file, "r", encoding="utf-8") as f:
        games = json.load(f)
    
    print(f"共 {len(games)} 个游戏")
    
    # 找出需要修复的游戏
    wrong_games = []
    for game in games:
        downloads = game.get("downloads", [])
        for dl in downloads:
            if dl.get("url") in [WRONG_GAMER520, WRONG_X6D]:
                wrong_games.append(game)
                break
    
    print(f"发现 {len(wrong_games)} 个游戏有错误链接\n")
    
    # 修复每个游戏
    fixed_count = 0
    for i, game in enumerate(wrong_games, 1):
        print(f"[{i}/{len(wrong_games)}] {game['cn_name']} ({game['en_name']})")
        
        if fix_game_downloads(game):
            fixed_count += 1
        
        print()
    
    # 保存更新后的 games.json
    with open(games_file, "w", encoding="utf-8") as f:
        json.dump(games, f, ensure_ascii=False, indent=2)
    
    print(f"\n修复完成: {fixed_count}/{len(wrong_games)} 个游戏")
    print(f"已保存到: {games_file}")

if __name__ == "__main__":
    main()
