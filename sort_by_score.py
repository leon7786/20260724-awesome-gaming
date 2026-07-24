#!/usr/bin/env python3
"""按评分降序排序 games.json"""
import json

# 读取游戏数据
with open('games.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

print(f"排序前总数: {len(games)}")

# 按评分降序排序，无评分的放最后
def get_score(game):
    score = game.get('score', 0)
    if isinstance(score, str):
        try:
            return int(score)
        except:
            return 0
    return score if isinstance(score, (int, float)) else 0

# 排序
games_sorted = sorted(games, key=lambda g: get_score(g), reverse=True)

# 统计
with_score = sum(1 for g in games_sorted if get_score(g) > 0)
print(f"有评分: {with_score}")
print(f"无评分: {len(games_sorted) - with_score}")

# 显示前10和后10
print("\n前10名:")
for i, g in enumerate(games_sorted[:10], 1):
    print(f"{i}. {g['cn_name']} - {get_score(g)}分")

print("\n后10名:")
for i, g in enumerate(games_sorted[-10:], len(games_sorted)-9):
    print(f"{i}. {g['cn_name']} - {get_score(g)}分")

# 保存
with open('games.json', 'w', encoding='utf-8') as f:
    json.dump(games_sorted, f, ensure_ascii=False, indent=2)

print(f"\n✓ 已保存排序后的 games.json")
