#!/usr/bin/env python3
"""
下载游戏封面图（600x900）
来源：Steam CDN (library_600x900_2x.jpg)
"""
import requests
import time
import re
import struct
from pathlib import Path

OUTPUT_DIR = Path("/root/Projects/20260724-awesome-gaming/pics/poster")
MD_FILE = OUTPUT_DIR / "games-205-to-374.md"

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})

# ── 已知 Steam App ID ─────────────────────────────────────────────────────
KNOWN_APPIDS = {
    "Diablo III": 545120,
    "Bastion": 107100,
    "Call of Duty: Black Ops III": 311210,
    "Human: Fall Flat": 477160,
    "Halo Infinite": 1240440,
    "The Callisto Protocol": 1259420,
    "Plants vs. Zombies": 3590,
    "Heroes of Might and Magic III": 297000,
    "No Man's Sky": 275850,
    "PUBG: Battlegrounds": 578080,
    "Helldivers 2": 553850,
    "Final Fantasy VII Rebirth": 2909400,
    "Path of Exile 2": 2694490,
    "The First Descendant": 2074920,
    "Resident Evil 4 (2023)": 2050650,
    "Lethal Company": 1966720,
    "Pizza Tower": 2231450,
    "Cocoon": 1497840,
    "Sifu": 2138710,
    "Monster Hunter Rise: Sunbreak": 1446780,
    "NARAKA: BLADEPOINT": 1166370,
    "Fall Guys": 1097150,
    "Genshin Impact": 1971870,
    "Marvel's Spider-Man": 1817070,
    "Prey": 480490,
    "Uncharted 4: A Thief's End": 1659420,
    "DOOM (2016)": 379720,
    "Inside": 304430,
    "Civilization VI": 289070,
    "Rocket League": 252950,
    "Shovel Knight": 250760,
    "Alien: Isolation": 214490,
    "Transistor": 237930,
    "Path of Exile": 238960,
    "Rayman Legends": 273166,
    "Risk of Rain 1": 248820,
    "Tomb Raider (2013)": 203160,
    "CS:GO": 730,
    "Guild Wars 2": 1284210,
    "Red Dead Redemption": 2668510,
    "StarCraft II: Wings of Liberty": 208480,
    "Dead Space 1": 1693980,
    "Left 4 Dead 1": 500,
    "Portal 1": 400,
    "Call of Duty 4: Modern Warfare": 7940,
    "The Witcher 1": 20900,
    "Crysis 1": 1715760,
    "The Elder Scrolls IV: Oblivion": 2623190,
    "Okami": 587620,
    "Resident Evil 4 (Original)": 254700,
    "Devil May Cry 3": 689740,
    "Civilization IV": 3830,
    "Metal Gear Solid 3: Snake Eater": 2131630,
    "Halo 2": 1064270,
    "Grand Theft Auto III": 12100,
    "Silent Hill 2": 2124490,
    "Deus Ex 1": 6910,
    "Counter-Strike 1.6": 10,
    "Baldur's Gate II: Shadows of Amn": 257350,
    "Age of Empires II: The Age of Kings": 813780,
    "Half-Life": 70,
    "Metal Gear Solid 1": 2131630,
    "Fallout 2": 38220,
    "Final Fantasy VII (Original)": 39140,
    "Chrono Trigger": 613830,
    "DOOM (1993)": 2280,
    "Street Fighter II": 586200,
    "The Witcher 2: Assassins of Kings": 20920,
    "Split Fiction": 2456290,
    "Assassin's Creed Origins": 582160,
    "Assassin's Creed Valhalla": 2208920,
    "Assassin's Creed Mirage": 2266760,
    "Assassin's Creed Syndicate": 368500,
    "Assassin's Creed Unity": 289650,
    "Far Cry 4": 298110,
    "Far Cry 5": 552520,
    "Far Cry 6": 1339820,
    "Assassin's Creed": 15100,
    "Assassin's Creed II": 48190,
    "Assassin's Creed III Remastered": 891290,
    "Assassin's Creed IV: Black Flag": 242050,
    "Call of Duty: Black Ops 6": 2933620,
    "Call of Duty: Modern Warfare II": 1938090,
    "Call of Duty: Vanguard": 1085660,
    "Call of Duty: WWII": 476600,
    "Call of Duty: Infinite Warfare": 292730,
    "Call of Duty: Advanced Warfare": 209160,
    "Call of Duty: Ghosts": 209160,
    "Call of Duty: Modern Warfare 2": 10180,
    "Call of Duty: World at War": 10090,
    "Call of Duty 2": 2630,
    "Call of Duty": 2620,
    "Monster Hunter Wilds": 2246340,
    "The Last of Us Part II": 2334260,
    "The Last of Us": 1888930,
    "Persona 5 (JP)": 1687950,
    "The Witcher 3 - Blood and Wine": 292030,
    "Schedule I": 3164500,
    "PEAK": 3527320,
    "R.E.P.O.": 3241660,
    "ARC Raiders": 2465660,
}

# ── 不在 Steam 上的游戏 ───────────────────────────────────────────────────
NOT_ON_STEAM = {
    "LittleBigPlanet", "Metroid Prime Remastered", "Demon's Souls",
    "Demon's Souls Remake", "Shadow of the Colossus", "Astro Bot",
    "Bayonetta 3", "Metroid Dread", "Luigi's Mansion 3", "Bayonetta 2",
    "Uncharted 3: Drake's Deception", "Uncharted 2: Among Thieves",
    "Metal Gear Solid 4: Guns of the Patriots", "World of Warcraft",
    "God of War 1", "God of War III", "The Sims 1", "Vagrant Story",
    "Soulcalibur", "Xenogears", "Resident Evil 2 (1998)",
    "Grand Theft Auto 1", "Castlevania: Symphony of the Night",
    "GoldenEye 007", "Diablo 1", "Resident Evil 1 (1996)", "Super Metroid",
    "Tetris (1984/1989)", "Pac-Man", "Super Mario Odyssey",
    "The Legend of Zelda: Breath of the Wild",
    "The Legend of Zelda: Tears of the Kingdom",
    "Super Smash Bros. Ultimate", "Super Mario 3D World",
    "Mario Kart 8 Deluxe", "Animal Crossing: New Horizons", "Wii Sports",
    "Super Mario Bros.", "Pokemon Red/Blue",
    "Paper Mario: The Thousand-Year Door (Remake)",
    "Super Mario Bros. Wonder", "Gran Turismo 7", "Xenoblade Chronicles 3",
    "Fire Emblem: Three Houses", "Bloodborne", "Super Mario Maker",
    "Mario Kart 8 (Wii U)", "Super Mario Galaxy 2", "Super Mario Galaxy 1",
    "Super Smash Bros. Melee", "The Legend of Zelda: Majora's Mask",
    "The Legend of Zelda: Ocarina of Time", "Super Mario 64",
    "Pokemon Red / Blue", "Super Mario World 2: Yoshi's Island",
    "Super Mario Kart", "Super Mario World",
    "The Legend of Zelda: A Link to the Past", "Super Mario Bros. 3",
    "Super Mario Bros. 1", "Call of Duty: Black Ops Cold War",
    "Silent Hill f", "Marvel Snap", "Diablo II: Lord of Destruction",
}

def get_jpg_dimensions(data):
    i = 0
    while i < len(data) - 9:
        if data[i] == 0xFF and data[i+1] == 0xC0:
            h, w = struct.unpack(">HH", data[i+5:i+9])
            return w, h
        i += 1
    return None, None

def is_valid_cover(data, min_size=30000):
    return len(data) >= min_size and data[:3] == b'\xff\xd8\xff'

def steam_search(name):
    try:
        resp = SESSION.get(
            "https://store.steampowered.com/api/storesearch/",
            params={"term": name, "l": "english", "cc": "US"},
            timeout=10
        )
        items = resp.json().get("items", [])
        return items[0]["id"] if items else None
    except Exception as e:
        print(f"  [搜索失败] {e}")
        return None

def download_steam_cover(appid):
    url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/library_600x900_2x.jpg"
    try:
        resp = SESSION.get(url, timeout=15)
        if resp.status_code == 200 and is_valid_cover(resp.content):
            return resp.content
    except Exception as e:
        print(f"  [下载失败] {e}")
    return None

def parse_md(md_path):
    games = []
    pattern = re.compile(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|")
    with open(md_path, encoding="utf-8") as f:
        for line in f:
            m = pattern.match(line)
            if m:
                num, zh, en = m.group(1), m.group(2).strip(), m.group(3).strip()
                if zh == "中文名":
                    continue
                games.append({"num": int(num), "zh": zh, "en": en})
    return games

def safe_filename(en, num):
    name = re.sub(r'[^\w\s-]', '', en)
    name = re.sub(r'\s+', '_', name.strip())[:60]
    return f"{num:03d}_{name}.jpg"

def main():
    games = parse_md(MD_FILE)
    print(f"共 {len(games)} 款游戏\n")
    success, skipped, failed = [], [], []

    for i, game in enumerate(games):
        num, zh, en = game["num"], game["zh"], game["en"]
        fname = safe_filename(en, num)
        fpath = OUTPUT_DIR / fname

        if fpath.exists() and fpath.stat().st_size > 30000:
            print(f"[{i+1}/{len(games)}] #{num} {en} — 已存在")
            success.append((num, en, fname))
            continue

        print(f"[{i+1}/{len(games)}] #{num} {en}", end=" ... ", flush=True)

        if en in NOT_ON_STEAM or zh in NOT_ON_STEAM:
            print("⚠ 非Steam独占，跳过")
            skipped.append((num, en))
            continue

        appid = KNOWN_APPIDS.get(en) or KNOWN_APPIDS.get(zh)
        if not appid:
            appid = steam_search(en)
            time.sleep(0.5)

        if not appid:
            print("✗ 未找到AppID")
            failed.append((num, en, "未找到AppID"))
            continue

        data = download_steam_cover(appid)
        if data:
            fpath.write_bytes(data)
            w, h = get_jpg_dimensions(data)
            print(f"✓ {w}x{h} {len(data)//1024}KB → {fname}")
            success.append((num, en, fname))
        else:
            print(f"✗ 下载失败 (appid={appid})")
            failed.append((num, en, f"appid={appid}"))

        time.sleep(0.3)

    print("\n" + "="*60)
    print(f"✅ 成功: {len(success)}")
    print(f"⚠ 跳过(非Steam): {len(skipped)}")
    print(f"❌ 失败: {len(failed)}")

    if failed:
        print("\n失败列表:")
        for num, en, reason in failed:
            print(f"  #{num} {en} — {reason}")
    if skipped:
        print("\n非Steam游戏（需手动处理）:")
        for num, en in skipped:
            print(f"  #{num} {en}")

if __name__ == "__main__":
    main()
