#!/usr/bin/env python3
"""为每个游戏生成Steam风格详情页"""
import json, os, urllib.request, time, re

GAMES_DIR = "/root/Projects/20260724-awesome-gaming/games/"
INDEX = "/root/Projects/20260724-awesome-gaming/index.html"
STEAM_API = "https://store.steampowered.com/api/appdetails?appids={}&cc=cn&l=schinese"

os.makedirs(GAMES_DIR, exist_ok=True)

with open("/root/games_data.json", "r") as f:
    games = json.load(f)

steam_games = [g for g in games if g["appid"] > 0]

def gen_page(game, steam_data):
    cn = game["cn"]
    en = game["en"]
    year = game["year"]
    score = game["score"]
    tags = game["tags"]
    links = game["links"]
    appid = game["appid"]
    
    # 下载按钮
    dl_btns = ""
    for url in links:
        if "gamer520.com" in url:
            dl_btns += f'<a href="{url}" class="dl-btn gamer520" target="_blank">🎮 gamer520</a>\n'
        elif "x6d.com" in url:
            dl_btns += f'<a href="{url}" class="dl-btn x6d" target="_blank">📦 x6d</a>\n'
        elif "cloud.189.cn" in url:
            dl_btns += f'<a href="{url}" class="dl-btn tianyi" target="_blank">☁️ 天翼云</a>\n'
        elif "pan.baidu.com" in url:
            dl_btns += f'<a href="{url}" class="dl-btn baidu" target="_blank">📀 百度网盘</a>\n'
        elif "magnet:" in url:
            dl_btns += f'<a href="{url}" class="dl-btn magnet" target="_blank">🧲 磁力链</a>\n'
        elif "fitgirl" in url:
            dl_btns += f'<a href="{url}" class="dl-btn fitgirl" target="_blank">📀 FitGirl</a>\n'
        elif "steamzg" in url:
            dl_btns += f'<a href="{url}" class="dl-btn steamzg" target="_blank">🧲 steamzg</a>\n'
        elif "crotorrents" in url:
            dl_btns += f'<a href="{url}" class="dl-btn crotorrents" target="_blank">🧲 CroTorrents</a>\n'
        else:
            dl_btns += f'<a href="{url}" class="dl-btn gamer520" target="_blank">📎 下载</a>\n'
    
    if not dl_btns:
        dl_btns = '<p style="color:#999;font-size:13px">暂无下载链接</p>'
    
    # Steam数据
    desc = steam_data.get("short_description", "暂无简介") if steam_data else "暂无简介"
    header = steam_data.get("header_image", "") if steam_data else ""
    devs = ", ".join(steam_data.get("developers", [])) if steam_data else ""
    pubs = ", ".join(steam_data.get("publishers", [])) if steam_data else ""
    genres = ", ".join(g["description"] for g in steam_data.get("genres", [])) if steam_data else ""
    metacritic = steam_data.get("metacritic", {}).get("score", "") if steam_data else ""
    release = steam_data.get("release_date", {}).get("date", "") if steam_data else ""
    screenshots = steam_data.get("screenshots", []) if steam_data else []
    about = steam_data.get("about_the_game", "") if steam_data else ""
    # 清理about的HTML，只保留纯文本
    about_clean = re.sub(r'<[^>]+>', '', about)[:800] if about else ""
    reqs = steam_data.get("pc_requirements", {})
    min_req = reqs.get("minimum", "")
    rec_req = reqs.get("recommended", "")
    
    tag_html = "".join(f'<span class="tag {("mc" if "口碑" in t else "sales")}">{t}</span>' for t in tags.split(","))
    
    steam_url = f"https://store.steampowered.com/app/{appid}" if appid > 0 else ""
    
    # 截图
    ss_html = ""
    for s in screenshots[:6]:
        img = s.get("path_full", "")
        if img:
            ss_html += f'<img src="{img}" alt="" loading="lazy">\n'
    
    # 配置要求
    reqs_html = ""
    if min_req:
        reqs_html += f'<div class="req-item"><h3>最低配置</h3><div class="req-text">{min_req}</div></div>'
    if rec_req:
        reqs_html += f'<div class="req-item"><h3>推荐配置</h3><div class="req-text">{rec_req}</div></div>'
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{cn} - {en} - 游戏详情</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',sans-serif;background:#f5f5f7;color:#1a1a2e;line-height:1.6}}
.topbar{{background:#ffffff;border-bottom:1px solid #e0e0e4;padding:12px 0;position:sticky;top:0;z-index:100}}
.topbar .container{{display:flex;align-items:center;gap:16px}}
.container{{max-width:1200px;margin:0 auto;padding:0 20px}}
.back{{color:#6d28d9;text-decoration:none;font-size:14px;font-weight:500;display:flex;align-items:center;gap:4px}}
.back:hover{{text-decoration:underline}}
.back-btn{{background:#6d28d9;color:#fff;padding:6px 14px;border-radius:4px;text-decoration:none;font-size:13px}}
.back-btn:hover{{background:#5b21b6}}

/* Steam风格头部 */
.hero{{background:linear-gradient(180deg,#f0f0f5 0%,#e8e8f0 100%);color:#1a1a2e;padding:30px 0 0;border-bottom:1px solid #e0e0e4}}
.hero .container{{display:flex;gap:30px;flex-wrap:wrap}}
.hero-info{{flex:1;min-width:280px}}
.hero-info h1{{font-size:26px;margin-bottom:4px}}
.hero-info .en{{color:#888;font-size:14px;margin-bottom:12px}}
.hero-info .meta{{display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap}}
.hero .tag{{font-size:12px;padding:3px 10px;border-radius:4px;background:#e8e8ec;color:#555}}
.hero .tag.mc{{background:#6d28d922;color:#6d28d9}}
.hero .tag.sales{{background:#e11d4822;color:#e11d48}}
.hero-img{{width:460px;max-width:100%;border-radius:8px;flex-shrink:0;box-shadow:0 2px 12px rgba(0,0,0,0.08)}}

/* Steam风格内容区 */
.content{{padding:24px 0}}
.section{{background:#fff;border-radius:8px;border:1px solid #e0e0e4;padding:24px;margin-bottom:16px}}
.section h2{{font-size:18px;color:#1a1a2e;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid #e0e0e4}}

/* 简介 */
.desc{{font-size:15px;color:#444;line-height:1.7}}
.desc a{{color:#6d28d9}}

/* 下载区 */
.dl-section{{background:#fff;border-radius:8px;border:1px solid #e0e0e4;padding:24px;margin-bottom:16px}}
.dl-section h2{{font-size:18px;color:#1a1a2e;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid #e0e0e4}}
.dl-buttons{{display:flex;flex-wrap:wrap;gap:8px}}
.dl-btn{{display:inline-flex;align-items:center;gap:5px;padding:8px 16px;border-radius:6px;font-size:13px;text-decoration:none;color:#fff;transition:all .2s;font-weight:500}}
.dl-btn:hover{{filter:brightness(1.1);transform:translateY(-1px)}}
.dl-btn.gamer520{{background:#10b981}}
.dl-btn.x6d{{background:#3b82f6}}
.dl-btn.tianyi{{background:#6366f1}}
.dl-btn.baidu{{background:#2563eb}}
.dl-btn.magnet{{background:#ef4444}}
.dl-btn.fitgirl{{background:#f59e0b}}
.dl-btn.steamzg{{background:#8b5cf6}}
.dl-btn.crotorrents{{background:#ec4899}}

/* Steam信息网格 */
.info-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:16px}}
.info-item{{}}
.info-item .label{{font-size:12px;color:#888;text-transform:uppercase;letter-spacing:0.5px}}
.info-item .value{{font-size:14px;color:#1a1a2e;margin-top:2px}}
.info-item .value a{{color:#6d28d9;text-decoration:none}}
.info-item .value a:hover{{text-decoration:underline}}

/* 截图 */
.ss-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:8px}}
.ss-grid img{{width:100%;border-radius:6px;cursor:pointer;transition:transform .2s}}
.ss-grid img:hover{{transform:scale(1.02)}}

/* 配置要求 */
.reqs{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
@media(max-width:768px){{.reqs{{grid-template-columns:1fr}}}}
.req-item{{}}
.req-item h3{{font-size:14px;color:#1a1a2e;margin-bottom:8px;padding-bottom:4px;border-bottom:1px solid #e0e0e4}}
.req-text{{font-size:13px;color:#555;line-height:1.6}}
.req-text ul{{list-style:none;padding:0}}
.req-text li{{padding:2px 0}}
.req-text strong{{color:#1a1a2e}}

@media(max-width:768px){{.hero-img{{width:100%}}.ss-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>

<div class="topbar">
  <div class="container">
    <a href="../../index.html" class="back">← 返回游戏榜单</a>
    <a href="https://store.steampowered.com/app/{appid}" target="_blank" class="back-btn" style="margin-left:auto">Steam 商店页</a>
  </div>
</div>

<div class="hero">
  <div class="container">
    <img src="https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/library_600x900.jpg" alt="{en}" class="hero-img" onerror="this.style.display='none'">
    <div class="hero-info">
      <h1>{cn}</h1>
      <div class="en">{en}</div>
      <div class="meta">
        <span class="tag">{year}</span>
        <span class="tag mc">评分 {score}</span>
        {tag_html}
        <span class="tag">{genres or "待补充"}</span>
      </div>
      <div class="desc">{desc}</div>
    </div>
  </div>
</div>

<div class="content">
  <div class="container">

    <div class="dl-section">
      <h2>📥 下载链接</h2>
      <div class="dl-buttons">
{dl_btns}
      </div>
    </div>

    <div class="section">
      <h2>📋 游戏信息</h2>
      <div class="info-grid">
        <div class="info-item"><div class="label">开发商</div><div class="value">{devs or "待补充"}</div></div>
        <div class="info-item"><div class="label">发行商</div><div class="value">{pubs or "待补充"}</div></div>
        <div class="info-item"><div class="label">发行日期</div><div class="value">{release or year}</div></div>
        <div class="info-item"><div class="label">类型</div><div class="value">{genres or "待补充"}</div></div>
        <div class="info-item"><div class="label">Metacritic</div><div class="value">{metacritic or "待补充"}</div></div>
        <div class="info-item"><div class="label">Steam</div><div class="value"><a href="{steam_url}" target="_blank">查看商店页 →</a></div></div>
      </div>
    </div>

    {f'''
    <div class="section">
      <h2>📖 关于这款游戏</h2>
      <div class="desc">{about_clean}</div>
    </div>''' if about_clean else ''}

    {f'''
    <div class="section">
      <h2>📸 游戏截图</h2>
      <div class="ss-grid">
        {ss_html}
      </div>
    </div>''' if ss_html else ''}

    {f'''
    <div class="section">
      <h2>💻 系统配置要求</h2>
      <div class="reqs">
        {reqs_html}
      </div>
    </div>''' if reqs_html else ''}

  </div>
</div>
</body>
</html>"""
    
    return html

# 分批处理
success = 0
errors = []

for i, game in enumerate(steam_games):
    appid = game["appid"]
    cn = game["cn"]
    en = game["en"]
    filename = en.lower().replace(" ", "-").replace(":", "").replace("'", "").replace(".", "").replace(",", "")[:50]
    filename = re.sub(r'[^a-z0-9-]', '', filename)
    filepath = os.path.join(GAMES_DIR, f"{filename}.html")
    
    print(f"[{i+1}/{len(steam_games)}] {cn}...", end=" ", flush=True)
    
    try:
        url = STEAM_API.format(appid)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        steam_data = data.get(str(appid), {}).get("data", {})
        
        if not steam_data:
            print("⚠️ 无数据")
            errors.append(cn)
            continue
        
        html = gen_page(game, steam_data)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        
        success += 1
        print("✅")
        time.sleep(0.3)
    except Exception as e:
        print(f"❌ {e}")
        errors.append(cn)

print(f"\n完成: {success}/{len(steam_games)} 页")
if errors:
    print(f"失败: {len(errors)} 个: {', '.join(errors[:10])}")