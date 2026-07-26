#!/usr/bin/env python3
"""用 witcher3 模板重做所有详情页——保持同一套 CSS 风格。"""
import json, os, re, glob
import urllib.request
from html import escape

PROXY = "http://admin12:Dd--2131801@127.0.0.1:2022"
ph = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
opener = urllib.request.build_opener(ph)
urllib.request.install_opener(opener)

ROOT = "/root/Projects/20260724-awesome-gaming"
TEMPLATE = os.path.join(ROOT, "template-detail.html")

games = json.load(open(os.path.join(ROOT, "games.json")))

# Fetch Steam details for all unique appids (videos + sysreq)
all_appids = set()
for x in games:
    if x.get("appid"):
        all_appids.add(int(x["appid"]))

print(f"Fetching Steam details for {len(all_appids)} appids...")
steam_data = {}
for appid in all_appids:
    try:
        req = urllib.request.Request(
            f"https://store.steampowered.com/api/appdetails?appids={appid}",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        data = json.loads(opener.open(req, timeout=15).read())
        if data.get(str(appid), {}).get("success"):
            steam_data[appid] = data[str(appid)]["data"]
    except Exception:
        pass
    if len(steam_data) % 50 == 0:
        print(f"  fetched {len(steam_data)}/{len(all_appids)}")

with open(TEMPLATE) as f:
    tpl = f.read()


def get_videos(appid):
    """Return video thumbnail+url pairs from Steam."""
    d = steam_data.get(appid, {})
    videos = []
    for v in d.get("movies", []):
        if "movie_max" in v.get("mp4", {}):
            videos.append({
                "type": "video",
                "url": v["mp4"]["movie_max"],
                "thumb": v["thumbnail"],
            })
    return videos[:3]


def get_screenshots(appid, max_n=18):
    """Return screenshot urls from Steam."""
    d = steam_data.get(appid, {})
    return [s["path_full"] for s in d.get("screenshots", [])][:max_n]


def get_sysreq(appid):
    d = steam_data.get(appid, {})
    pc = d.get("pc_requirements")
    mac = d.get("mac_requirements")
    if not pc and not mac:
        return None
    min_html = escape(pc.get("minimum", "无数据") if pc else (mac.get("minimum", "无数据") if mac else "无数据"))
    rec_html = escape(pc.get("recommended", "无数据") if pc else (mac.get("recommended", "无数据") if mac else "无数据"))
    return min_html, rec_html


def build_page(g):
    appid = g.get("appid")
    cn = g.get("cn_name", "")
    en = g.get("en_name", "")
    year = g.get("year", "")
    tags = g.get("tags", [])
    cover = g.get("cover", "")
    desc = g.get("description", "")
    dev = g.get("developer", "")
    pub = g.get("publisher", "")
    sz = g.get("size_gb")
    meta = g.get("metacritic")
    detail_dir = g.get("detail", "")
    screenshots_from_json = g.get("screenshots", []) or []
    downloads = g.get("downloads", [])

    # Metacritic URL
    mc_url = ""
    if meta:
        # Try to build from appid or use steam_name
        sn = g.get("steam_name", "").lower()
        if sn:
            # Use the metacritic URL format
            mc_url = f"https://www.metacritic.com/game/pc/{sn.replace(' ', '-')}"

    # Build media section: videos first, then screenshots
    videos = get_videos(appid) if appid else []
    screenshots_steam = get_screenshots(appid) if appid else []
    # Prefer screenshots from games.json if no Steam screenshots
    screenshots_used = screenshots_steam if screenshots_steam else screenshots_from_json

    # Build mediaItems JS array
    media_items = []
    thumb_html = []
    main_html = ""

    all_media = []
    for v in videos:
        all_media.append(v)
    for s in screenshots_used[:18]:
        all_media.append({"type": "image", "url": s, "thumb": s})

    for i, m in enumerate(all_media):
        idx = f'data-index="{i}"'
        cls = f'media-thumb {"active" if i == 0 else ""} {idx}'
        if m["type"] == "video":
            icon = '<div class="play-icon">▶</div>'
            thumb_src = m["thumb"]
            main_html = f'<video controls playsinline poster="{m["thumb"]}" src="{m["url"]}" style="width:100%;height:100%;object-fit:contain;background:#000"></video>'
        else:
            icon = ""
            thumb_src = m["url"]
            if i == 0:
                main_html = f'<img src="{m["url"]}" alt="Screenshot">'
        thumb_html.append(f'<div class="{cls}">{icon}<img src="{thumb_src}" alt="Media"></div>')
        media_items.append(f'{{"type":"{m["type"]}","url":"{m["url"]}","thumb":"{m["thumb"]}"}},')

    if not all_media:
        # No media: hide media section with a placeholder
        main_html = '<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:#9ca3af;font-size:0.9rem">暂无媒体</div>'
        thumb_html = []

    media_js = "[" + "".join(media_items) + "]" if media_items else "[]"
    thumb_block = "\n".join(thumb_html)

    # Downloads
    dl_pills = ""
    for d in downloads:
        t = d.get("type", "")
        url = d.get("url", "")
        if t in ("gamer520", "x6d", "fitgirl", "steamzg", "tianyi", "baidu", "crotorrents"):
            dl_pills += f'<a href="{escape(url)}" class="download-pill" target="_blank">{t}</a>\n'

    if dl_pills:
        download_html = f'''<section class="download-section">
  <div class="download-block">
    <span class="download-label">Download</span>
    <div class="download-pills">
{dl_pills}    </div>
  </div>
</section>'''
    else:
        download_html = ""

    # System requirements
    sys_html = ""
    if appid:
        sr = get_sysreq(appid)
        if sr:
            min_h, rec_h = sr
            sys_html = f'''<!-- 系统需求 -->
<section class="sys-req-section">
  <div class="sys-req-block">
    <h2>💻 系统配置要求</h2>
    <div class="sys-req-grid">
      <div class="sys-req-col minimum">
        <h4>最低配置</h4>
        {min_h}
      </div>
      <div class="sys-req-col recommended">
        <h4>推荐配置</h4>
        {rec_h}
      </div>
    </div>
  </div>
</section>'''

    # Metacritic inline badge
    if meta:
        mc_tag = f'<a href="{mc_url}" class="mc-inline" target="_blank"><span class="mc-num">{meta}</span><span class="mc-label">Metacritic</span></a>'
    else:
        mc_tag = ""

    # Tags
    tags_str = " · ".join(tags) if tags else ""

    # Info row
    info_row = ""
    if dev:
        info_row += f'''<div class="info-item">
          <span class="label">开发商</span>
          <span class="value">{escape(dev)}</span>
        </div>'''
    if pub:
        info_row += f'''<div class="info-item">
          <span class="label">发行商</span>
          <span class="value">{escape(pub)}</span>
        </div>'''
    if sz:
        info_row += f'''<div class="info-item">
          <span class="label">存储需求</span>
          <span class="value">约 {sz} GB</span>
        </div>'''

    # Description
    desc_html = escape(desc) if desc else ""

    # Description section (Steam HTML)
    desc_block = ""
    if desc:
        desc_block = f'''<section class="content-section">
  <div class="content-block">
    <h2>关于此游戏</h2>
    {desc_html}
  </div>
</section>'''

    # Topbar links
    steam_url = f"https://store.steampowered.com/app/{appid}/" if appid else "#"

    # Build the final HTML — extract CSS from template
    # Find the template's structural sections and replace placeholders
    html = tpl

    # Replace title
    html = html.replace("<title>巫师3：狂猎 - 游戏详情</title>", f"<title>{escape(cn)} - 游戏详情</title>")

    # Topbar
    html = html.replace('<a href="../../index.html">← 返回游戏榜单</a>', f'<a href="../../index.html">← 返回游戏榜单</a>')
    html = html.replace('<a href="https://store.steampowered.com/app/292030/" target="_blank">Steam 商店页 →</a>', f'<a href="{steam_url}" target="_blank">Steam 商店页 →</a>')

    # Hero
    html = html.replace('<img src="https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/292030/library_600x900.jpg" alt="巫师3：狂猎">', f'<img src="{cover}" alt="{escape(cn)}">')
    html = html.replace("<h1>巫师3：狂猎</h1>", f"<h1>{escape(cn)}</h1>")
    html = html.replace("<div class=\"en-name\">The Witcher 3: Wild Hunt</div>", f"<div class=\"en-name\">{escape(en)}</div>")
    html = html.replace("<span class=\"meta-tag year\">2015</span>", f"<span class=\"meta-tag year\">{year}</span>")
    html = html.replace("<span class=\"meta-tag\">口碑Top · 销量Top</span>", f"<span class=\"meta-tag\">{tags_str}</span>")
    html = html.replace('<a href="https://www.metacritic.com/game/pc/the-witcher-3-wild-hunt" class="mc-inline" target="_blank">\n          <span class="mc-num">93</span>\n          <span class="mc-label">Metacritic</span>\n        </a>', mc_tag)

    # Info row
    old_info = '''      <div class="info-row">
        <div class="info-item">
          <span class="label">开发商</span>
          <span class="value">CD PROJEKT RED</span>
        </div>
        <div class="info-item">
          <span class="label">发行商</span>
          <span class="value">CD PROJEKT RED</span>
        </div>
        <div class="info-item">
          <span class="label">存储需求</span>
          <span class="value">约 50 GB</span>
        </div>
      </div>'''
    html = html.replace(old_info, f'''      <div class="info-row">
{info_row}      </div>''')

    # Desc
    html = html.replace("您是利维亚的杰洛特，收钱办事的怪物杀手。您可以在眼前这片怪物横行、饱受战火摧残的土地上尽情探索。您手上的委托？追踪预言之子——希里，一件足以改变世界面貌的活生生的武器。", desc_html)

    # Media section - replace between <!-- 媒体区域 --> and <!-- 下载区域 --> / </section>
    # Find media section boundaries
    media_start = html.find("<!-- 媒体区域 -->")
    media_end = html.find("<!-- 下载区域 -->")
    if media_start == -1 or media_end == -1:
        media_end = html.find("<section class=\"content-section\">")
    if media_start != -1 and media_end != -1:
        new_media = f'''<!-- 媒体区域 -->
<section class="media-section">
  <div class="media-gallery">
    <div class="media-main" id="mediaMain">
      {main_html}
    </div>
    <div class="media-thumbnails-wrap" id="mediaThumbnailsWrap">
      <div class="media-thumbnails" id="mediaThumbnails">
      {thumb_block}
      </div>
    </div>
  </div>
</section>'''
        html = html[:media_start] + new_media + html[media_end:]

    # Desc block
    old_desc_section = html.find("<section class=\"content-section\">")
    # Find the one with 关于此游戏
    desc_idx = html.find("<h2>关于此游戏</h2>")
    if desc_idx != -1:
        # Find matching section end
        sect_start = html.rfind("<section", 0, desc_idx)
        sect_end = html.find("</section>", desc_idx) + len("</section>")
        if desc_block:
            html = html[:sect_start] + desc_block + html[sect_end:]

    # Downloads
    old_dl = html[html.find("<!-- 下载区域 -->"):html.find("</section>", html.find("<!-- 下载区域 -->")) + 12]
    if download_html:
        dl_start = html.find("<!-- 下载区域 -->")
        dl_end = html.find("</section>", dl_start) + 12
        if dl_start != -1:
            html = html[:dl_start] + download_html + html[dl_end:]
    else:
        # Remove download section
        dl_start = html.find("<!-- 下载区域 -->")
        dl_end = html.find("</section>", dl_start) + 12
        if dl_start != -1:
            html = html[:dl_start] + html[dl_end:]

    # Sysreq
    old_sys = html[html.find("<!-- 系统需求 -->"):html.find("</section>", html.find("<!-- 系统需求 -->")) + 12]
    sys_start = html.find("<!-- 系统需求 -->")
    sys_end = html.find("</section>", sys_start) + 12
    if sys_start != -1 and sys_end != -1:
        if sys_html:
            html = html[:sys_start] + sys_html + html[sys_end:]
        else:
            # Remove sysreq section if no data
            html = html[:sys_start] + html[sys_end:]

    # Media JS
    old_media_js = html.find("const mediaItems = ")
    new_js_line = f"const mediaItems = {media_js}"
    if old_media_js != -1:
        js_start = html.rfind("<script>", 0, old_media_js) + len("<script>")
        js_line_end = html.find("\n", old_media_js)
        html = html[:old_media_js] + new_js_line + html[js_line_end:]

    return html


# Skip witcher3 itself — it's already the template
done = 0
skipped = 0
for g in games:
    detail_dir = g.get("detail", "")
    if not detail_dir:
        continue
    path = os.path.join(ROOT, detail_dir, "index.html")
    if not os.path.exists(path):
        continue
    if detail_dir.startswith("games/the-witcher-3-wild-hunt/"):
        skipped += 1
        continue
    try:
        html = build_page(g)
        with open(path, "w") as f:
            f.write(html)
        done += 1
    except Exception as e:
        print(f"ERROR {detail_dir}: {e}")

print(f"\nDone: {done} updated, {skipped} skipped")
