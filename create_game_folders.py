#!/usr/bin/env python3
"""
为每个游戏创建独立文件夹结构：
  games/{slug}/
    cover.jpg          # 封面图
    screenshots/        # 截图
    README.md           # 介绍（中文）
    downloads.md        # 下载地址
    info.json           # 元数据
"""
import json, os, re, urllib.request, time, shutil

BASE = "/root/Projects/20260724-awesome-gaming/games/"
PAGES = "/root/Projects/20260724-awesome-gaming/games_html/"

with open("/root/games_data.json") as f:
    games = json.load(f)

def slugify(en):
    s = en.lower().replace(" ", "-").replace(":", "").replace("'", "").replace(".", "").replace(",", "").replace("--", "-")
    return re.sub(r'[^a-z0-9-]', '', s)[:50]

def download(url, path, timeout=10):
    if not url:
        return False
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=timeout)
        with open(path, "wb") as f:
            f.write(resp.read())
        return True
    except:
        return False

# 创建文件夹结构
for i, g in enumerate(games):
    cn = g["cn"]
    en = g["en"]
    slug = slugify(en)
    folder = os.path.join(BASE, slug)
    ss_dir = os.path.join(folder, "screenshots")
    os.makedirs(ss_dir, exist_ok=True)
    
    print(f"[{i+1}/{len(games)}] {cn}...", end=" ", flush=True)
    
    # 1. 下载封面图
    poster_url = g.get("poster", "")
    cover_path = os.path.join(folder, "cover.jpg")
    if poster_url and not os.path.exists(cover_path):
        ok = download(poster_url, cover_path)
        if not ok:
            print("⚠️ 封面下载失败", end=" ")
    
    # 2. 下载截图（从详情页提取）
    # 查找对应的详情页HTML
    detail_path = os.path.join(PAGES, f"{slug}.html")
    screenshots = []
    if os.path.exists(detail_path):
        with open(detail_path) as fh:
            detail = fh.read()
        # 提取截图URL
        ss_urls = re.findall(r'<img src="(https://shared\.akamai\.steamstatic\.com/store_item_assets/steam/apps/\d+/[^"]+\.jpg)"', detail)
        # 过滤掉封面图
        ss_urls = [u for u in ss_urls if "library_600x900" not in u and "header" not in u]
        for j, url in enumerate(ss_urls[:6]):
            ss_path = os.path.join(ss_dir, f"ss{j+1}.jpg")
            if not os.path.exists(ss_path):
                download(url, ss_path)
                screenshots.append(url)
    
    # 3. 生成README.md
    readme = f"""# {cn} ({en})

{'> 评分: ' + g['score'] + ' | 年份: ' + g['year'] + ' | ' + g['tags'] if g.get('tags') else ''}

## 封面

![{cn}](cover.jpg)

## 介绍

{cn}（{en}）是一款{g['year']}年发行的游戏，媒体评分{g['score']}分。

> 游戏详情和介绍请参考 [Steam 商店页](https://store.steampowered.com/)。

## 截图

"""
    for j in range(1, 7):
        ss_path = f"screenshots/ss{j}.jpg"
        if os.path.exists(os.path.join(ss_dir, f"ss{j}.jpg")):
            readme += f"![截图{j}]({ss_path})\n\n"
    
    with open(os.path.join(folder, "README.md"), "w") as fh:
        fh.write(readme)
    
    # 4. 生成downloads.md
    dl_md = f"""# {cn} - 下载地址

## 下载链接

| 来源 | 链接 | 说明 |
|------|------|------|
"""
    for url in g.get("links", []):
        if "gamer520.com" in url:
            dl_md += f"| 🎮 gamer520 | [{url[:50]}...]({url}) | PC破解版，需点'立即获取' |\n"
        elif "x6d.com" in url:
            dl_md += f"| 📦 x6d | [{url[:50]}...]({url}) | 多网盘下载 |\n"
        elif "cloud.189.cn" in url:
            dl_md += f"| ☁️ 天翼云 | [{url[:50]}...]({url}) | 高速下载 |\n"
        elif "pan.baidu.com" in url:
            dl_md += f"| 📀 百度网盘 | [{url[:50]}...]({url}) | 需提取码 |\n"
        elif "magnet:" in url:
            dl_md += f"| 🧲 磁力链 | `{url[:60]}...` | BT下载 |\n"
        elif "fitgirl" in url:
            dl_md += f"| 📀 FitGirl | [{url[:50]}...]({url}) | 高压版 |\n"
        else:
            dl_md += f"| 📎 下载 | [{url[:50]}...]({url}) | |\n"
    
    dl_md += "\n## 解压密码\n- gamer520.com: `laoquzhang.com`\n- x6d.com: 见页面说明\n"
    with open(os.path.join(folder, "downloads.md"), "w") as fh:
        fh.write(dl_md)
    
    # 5. 生成info.json
    info = {
        "name_cn": cn,
        "name_en": en,
        "year": g.get("year", ""),
        "score": g.get("score", ""),
        "tags": g.get("tags", "").split(","),
        "poster": poster_url,
        "downloads": g.get("links", []),
        "screenshots": screenshots
    }
    with open(os.path.join(folder, "info.json"), "w") as fh:
        json.dump(info, fh, ensure_ascii=False, indent=2)
    
    print("✅")

print(f"\n全部完成! 共 {len(games)} 个游戏文件夹")