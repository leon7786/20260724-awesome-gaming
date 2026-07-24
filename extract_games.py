#!/usr/bin/env python3
"""提取所有游戏数据并生成专属页面"""
import re, json, os, subprocess, sys, time, urllib.request

INDEX = "/root/Projects/20260724-awesome-gaming/index.html"
GAMES_DIR = "/root/Projects/20260724-awesome-gaming/games/"
STEAM_API = "https://store.steampowered.com/api/appdetails?appids={}&cc=cn&l=zh"

# 读取HTML
with open(INDEX, "r") as f:
    content = f.read()

# 提取所有游戏卡片数据 - 更精确的方法
# 按card分割
card_blocks = content.split('<div class="card" data-tags="')
games = []

for block in card_blocks[1:]:  # 跳过第一个(头部)
    try:
        # 提取标签
        tags = block.split('"')[0]
        
        # 提取cn
        cn_match = re.search(r'<div class="cn">([^<]+)</div>', block)
        en_match = re.search(r'<div class="en">([^<]+)</div>', block)
        year_match = re.search(r'<span class="tag">(\d{4})</span>', block)
        score_match = re.search(r'<span class="tag mc">(\d+)</span>', block)
        
        # 提取下载链接
        dl_links = re.findall(r'<a href="([^"]+)" class="dl-btn', block)
        
        # 提取appid - 从Steam图片URL中
        appid_match = re.search(r'steam/apps/(\d+)/', block)
        appid = int(appid_match.group(1)) if appid_match else 0
        
        cn = cn_match.group(1) if cn_match else ""
        en = en_match.group(1) if en_match else ""
        year = year_match.group(1) if year_match else ""
        score = score_match.group(1) if score_match else ""
        
        games.append({
            "cn": cn, "en": en, "year": year, "score": score,
            "tags": tags, "appid": appid, "links": dl_links
        })
    except Exception as e:
        print(f"解析错误: {e}")

print(f"解析出 {len(games)} 个游戏")

# 有Steam App ID的游戏
steam_games = [g for g in games if g["appid"] > 0]
print(f"有Steam App ID: {len(steam_games)} 个")

# 保存游戏数据到JSON，供后续使用
with open("/root/games_data.json", "w", encoding="utf-8") as f:
    json.dump(games, f, ensure_ascii=False, indent=2)

print("游戏数据已保存到 /root/games_data.json")