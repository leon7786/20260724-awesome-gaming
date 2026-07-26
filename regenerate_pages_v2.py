#!/usr/bin/env python3
"""用 template-detail.html 的完整 CSS + HTML 结构重做详情页，替换旧脚本。"""
import json, os, urllib.request
from html import escape

PROXY = "http://admin12:Dd--2131801@127.0.0.1:2022"
ph = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
opener = urllib.request.build_opener(ph)
urllib.request.install_opener(opener)

ROOT = "/root/Projects/20260724-awesome-gaming"
TEMPLATE = os.path.join(ROOT, "template-detail.html")

games = json.load(open(os.path.join(ROOT, "games.json")))

# --- Fetch Steam details ---
all_appids = set()
for x in games:
    if x.get("appid"):
        all_appids.add(int(x["appid"]))
print(f"Fetching Steam details for {len(all_appids)} appids...")
steam_data = {}
for i, appid in enumerate(sorted(all_appids), 1):
    try:
        req = urllib.request.Request(
            f"https://store.steampowered.com/api/appdetails?appids={appid}&l=schinese",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        data = json.loads(opener.open(req, timeout=15).read())
        if data.get(str(appid), {}).get("success"):
            steam_data[appid] = data[str(appid)]["data"]
    except Exception:
        pass
    if i % 50 == 0:
        print(f"  fetched {len(steam_data)}/{len(all_appids)}")

# --- Extract CSS from template ---
with open(TEMPLATE) as f:
    tpl_full = f.read()
css_start = tpl_full.find("<style>")
css_end = tpl_full.find("</style>")
css_block = tpl_full[css_start:css_end + len("</style>")]


def get_videos(appid):
    d = steam_data.get(appid, {})
    out = []
    for v in d.get("movies", []):
        mp4 = v.get("mp4", {})
        if mp4.get("movie_max"):
            out.append({"type": "video", "url": mp4["movie_max"], "thumb": v["thumbnail"]})
    return out[:3]


def get_screenshots(appid, n=18):
    d = steam_data.get(appid, {})
    return [s["path_full"] for s in d.get("screenshots", [])][:n]


def get_sysreq(appid):
    d = steam_data.get(appid, {})
    pc = d.get("pc_requirements")
    mac = d.get("mac_requirements")
    if not pc and not mac:
        return None
    return (
        pc.get("minimum", "无数据") if pc else mac.get("minimum", "无数据"),
        pc.get("recommended", "无数据") if pc else mac.get("recommended", "无数据"),
    )


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
    screenshots_json = g.get("screenshots", []) or []
    downloads = g.get("downloads", [])

    # Metacritic link - use metacritic_url from Steam API, fallback to constructed URL
    mc_url = ""
    if meta:
        mc_url = g.get("metacritic_url", "")
        if not mc_url:
            sn = g.get("steam_name", "").lower()
            if sn:
                mc_url = f"https://www.metacritic.com/game/pc/{sn.replace(' ', '-')}"

    videos = get_videos(appid) if appid else []
    screenshots_steam = get_screenshots(appid) if appid else []
    screenshots_used = screenshots_steam if screenshots_steam else screenshots_json

    # --- Media ---
    media_items_js = []
    thumb_html_lines = []
    all_media = list(videos)
    for s in screenshots_used:
        all_media.append({"type": "image", "url": s, "thumb": s})

    main_html = '<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:#9ca3af;font-size:0.9rem">暂无媒体</div>'
    if all_media:
        main_item = all_media[0]
        if main_item["type"] == "video":
            main_html = f'<video controls playsinline poster="{main_item["thumb"]}" src="{main_item["url"]}" style="width:100%;height:100%;object-fit:contain;background:#000"></video>'
        else:
            main_html = f'<img src="{main_item["url"]}" alt="Screenshot">'

    for i, m in enumerate(all_media):
        cls = f'media-thumb {"active" if i == 0 else ""}'
        idx = f'data-index="{i}"'
        icon = '<div class="play-icon">▶</div>' if m["type"] == "video" else ""
        src = m["thumb"] if m["type"] == "video" else m["url"]
        thumb_html_lines.append(f'<div class="{cls}" {idx}>{icon}<img src="{src}" alt="Media"></div>')

    thumb_block = "\n      ".join(thumb_html_lines)
    media_js = json.dumps([{
        "type": m["type"],
        "url": m["url"],
        "thumb": m["thumb"],
    } for m in all_media], ensure_ascii=False) if all_media else "[]"

    media_section = f'''<!-- 媒体区域 -->
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

    # --- Download pills ---
    dl_pills = ""
    for d in downloads:
        t = d.get("type", "")
        if t in ("gamer520", "x6d", "fitgirl", "steamzg", "tianyi", "baidu", "crotorrents"):
            dl_pills += f'<a href="{escape(d["url"])}" class="download-pill" target="_blank">{t}</a>\n'

    if dl_pills:
        download_section = f'''<section class="download-section">
  <div class="download-block">
    <span class="download-label">Download</span>
    <div class="download-pills">
{dl_pills}    </div>
  </div>
</section>'''
    else:
        download_section = ""

    # --- Description (about this game) ---
    # 优先用 Steam API 的 about_the_game（含视频动图），否则用 games.json 的 description
    steam_about = ""
    if appid and appid in steam_data:
        steam_about = steam_data[appid].get("about_the_game", "")
    desc_html = steam_about if steam_about else escape(desc) if desc else ""
    if desc_html:
        desc_section = f'''<section class="content-section">
  <div class="content-block">
    <h2>关于此游戏</h2>
    {desc_html}
  </div>
</section>'''
    else:
        desc_section = ""

    # --- System requirements (translate Steam English labels to Chinese) ---
    SYS_LABEL_MAP = {
        "Minimum:": "最低配置:",
        "Recommended:": "推荐配置:",
        "OS:": "操作系统:",
        "Processor:": "处理器:",
        "Memory:": "内存:",
        "Graphics:": "显卡:",
        "DirectX:": "DirectX 版本:",
        "DirectX Version:": "DirectX 版本:",
        "Storage:": "存储空间:",
        "Sound Card:": "声卡:",
        "Additional Notes:": "备注:",
        "Requires a 64-bit processor and operating system": "需要 64 位处理器和操作系统",
        "available space": "可用空间",
    }
    def translate_sys(html):
        for en, zh in SYS_LABEL_MAP.items():
            # match both "<strong>Label:</strong>" and inline text
            html = html.replace(f"<strong>{en}</strong>", f"<strong>{zh}</strong>")
        # Inline replacements for non-tag text
        for en, zh in SYS_LABEL_MAP.items():
            if en.startswith(("Requires", "available")):
                html = html.replace(en, zh)
        return html

    if appid:
        sr = get_sysreq(appid)
        if sr:
            sys_section = f'''<!-- 系统需求 -->
<section class="sys-req-section">
  <div class="sys-req-block">
    <h2>💻 系统配置要求</h2>
    <div class="sys-req-grid">
      <div class="sys-req-col minimum">
        <h4>最低配置</h4>
        {translate_sys(sr[0])}
      </div>
      <div class="sys-req-col recommended">
        <h4>推荐配置</h4>
        {translate_sys(sr[1])}
      </div>
    </div>
  </div>
</section>'''
        else:
            sys_section = ""
    else:
        sys_section = ""

    # --- Info row ---
    info_items = ""
    if dev:
        info_items += f'''<div class="info-item">
          <span class="label">开发商</span>
          <span class="value">{escape(dev)}</span>
        </div>'''
    if pub:
        info_items += f'''<div class="info-item">
          <span class="label">发行商</span>
          <span class="value">{escape(pub)}</span>
        </div>'''
    if sz:
        info_items += f'''<div class="info-item">
          <span class="label">存储需求</span>
          <span class="value">约 {sz} GB</span>
        </div>'''

    # --- Metacritic tag ---
    if meta and mc_url:
        mc_tag = f'''<a href="{mc_url}" class="mc-inline" target="_blank">
          <span class="mc-num">{meta}</span>
          <span class="mc-label">Metacritic</span>
        </a>'''
    else:
        mc_tag = ""

    tags_str = " · ".join(tags) if tags else ""
    steam_url = f"https://store.steampowered.com/app/{appid}/" if appid else "#"

    # --- Build HTML ---
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(cn)} - 游戏详情</title>
{css_block}
</head>
<body>

<!-- 顶部导航 -->
<nav class="topbar">
  <a href="../../index.html">← 返回游戏榜单</a>
  <a href="{steam_url}" target="_blank">Steam 商店页 →</a>
</nav>

<!-- 游戏头部 -->
<section class="hero">
  <div class="container">
    <div class="hero-cover">
      <img src="{cover}" alt="{escape(cn)}">
    </div>
    <div class="hero-info">
      <h1>{escape(cn)}</h1>
      <div class="en-name">{escape(en)}</div>

      <div class="meta-tags">
        <span class="meta-tag year">{year}</span>
        <span class="meta-tag">{escape(tags_str)}</span>
{mc_tag}      </div>

      <div class="info-row">
{info_items}      </div>

      <div class="hero-desc">
        {escape(desc)}
      </div>
    </div>
  </div>
</section>

{media_section}

{desc_section}{download_section}
{sys_section}
<script>
// 媒体数据
const mediaItems = {media_js};

let currentIndex = 0;

// 切换到指定媒体
function switchMedia(index) {{
  if (index < 0 || index >= mediaItems.length) return;
  currentIndex = index;
  const item = mediaItems[index];
  const mainEl = document.getElementById('mediaMain');
  if (item.type === 'video') {{
    mainEl.innerHTML = '<video controls autoplay playsinline poster="' + item.thumb + '" src="' + item.url + '" style="width:100%;height:100%;object-fit:contain;background:#000"></video>';
  }} else {{
    mainEl.innerHTML = '<img src="' + item.url + '" alt="Screenshot">';
  }}
  document.querySelectorAll('.media-thumb').forEach((thumb, i) => {{
    thumb.classList.toggle('active', i === index);
  }});
  const bar = document.getElementById('mediaThumbnails');
  const active = document.querySelector('.media-thumb[data-index="'+index+'"]');
  if (bar && active) {{
    active.scrollIntoView({{ behavior: 'smooth', block: 'nearest', inline: 'center' }});
  }}
}}

document.addEventListener('DOMContentLoaded', () => {{
  document.querySelectorAll('.media-thumb').forEach((thumb, index) => {{
    thumb.addEventListener('click', () => switchMedia(index));
  }});
  if (mediaItems.length > 0) {{
    switchMedia(0);
  }}
  // 滚动箭头
  const thumbsWrap = document.getElementById('mediaThumbnailsWrap');
  const bar = document.getElementById('mediaThumbnails');
  if (bar && thumbsWrap) {{
    const leftArrow = thumbsWrap.querySelector('.media-arrow.left') || (() => {{
      const el = document.createElement('div');
      el.className = 'media-arrow left';
      el.innerHTML = '\\u2039';
      thumbsWrap.appendChild(el);
      return el;
    }})();
    const rightArrow = thumbsWrap.querySelector('.media-arrow.right') || (() => {{
      const el = document.createElement('div');
      el.className = 'media-arrow right';
      el.innerHTML = '\\u203A';
      thumbsWrap.appendChild(el);
      return el;
    }})();
    function updateArrows() {{
      const maxLeft = Math.max(0, bar.scrollWidth - bar.clientWidth);
      leftArrow.classList.toggle('show', bar.scrollLeft > 1);
      rightArrow.classList.toggle('show', bar.scrollLeft < maxLeft - 1);
    }}
    bar.addEventListener('scroll', updateArrows);
    window.addEventListener('resize', updateArrows);
    updateArrows();
  }}
}});
</script>

</body>
</html>
'''


done = skipped = 0
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
        with open(path, "w") as f:
            f.write(build_page(g))
        done += 1
    except Exception as e:
        print(f"ERROR {detail_dir}: {e}")

print(f"\nDone: {done} updated, {skipped} skipped")
