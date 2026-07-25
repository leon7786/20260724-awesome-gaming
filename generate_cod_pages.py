#!/usr/bin/env python3
"""Generate COD game detail pages from Steam API data."""

import json
import os
import time
import urllib.request
import urllib.error
import urllib.parse
import re

BASE = "/root/Projects/20260724-awesome-gaming"

# Game config
GAMES = [
    {"appid": 2620, "slug": "call-of-duty-1", "cn_name": "使命召唤 1"},
    {"appid": 2630, "slug": "call-of-duty-2", "cn_name": "使命召唤 2"},
    {"appid": 10090, "slug": "call-of-duty-world-at-war", "cn_name": "使命召唤：战争世界"},
    {"appid": 10180, "slug": "call-of-duty-modern-warfare-2", "cn_name": "使命召唤：现代战争 2"},
    {"appid": 209160, "slug": "call-of-duty-ghosts", "cn_name": "使命召唤：幽灵"},
    {"appid": 209650, "slug": "call-of-duty-advanced-warfare", "cn_name": "使命召唤：高级战争"},
    {"appid": 292730, "slug": "call-of-duty-infinite-warfare", "cn_name": "使命召唤：无限战争"},
    {"appid": 476600, "slug": "call-of-duty-wwii", "cn_name": "使命召唤：二战"},
    {"appid": 1985810, "slug": "call-of-duty-black-ops-cold-war", "cn_name": "使命召唤：黑色行动 冷战"},
    {"appid": 1985820, "slug": "call-of-duty-vanguard", "cn_name": "使命召唤：先锋"},
]


def fetch_steam_api(appid):
    """Fetch game details from Steam API with Chinese language."""
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=schinese"
    print(f"Fetching appid {appid}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if str(appid) in data and data[str(appid)].get("success"):
            return data[str(appid)]["data"]
        else:
            print(f"  API returned success=false for appid {appid}")
            return None
    except Exception as e:
        print(f"  Error fetching appid {appid}: {e}")
        return None


def get_en_name(data):
    """Get English name from Steam data."""
    # Try to get from the data directly
    name = data.get("name", "")
    # If the name is Chinese, we need to get the English name
    # Steam API with l=schinese returns Chinese name in 'name' field
    return name


def get_release_date(data):
    """Get formatted release date."""
    rd = data.get("release_date", {})
    date_str = rd.get("date", "")
    if date_str:
        # Try to parse and format nicely
        parts = date_str.split(" ")
        if len(parts) >= 3:
            # Already in a nice format like "15 Nov, 2010"
            return date_str
        # Try to convert YYYY-MM-DD
        m = re.match(r"(\d{4})-(\d{2})-(\d{2})", date_str)
        if m:
            months = ["", "1 月", "2 月", "3 月", "4 月", "5 月", "6 月",
                      "7 月", "8 月", "9 月", "10 月", "11 月", "12 月"]
            month_num = int(m.group(2))
            month_name = months[month_num] if month_num < len(months) else m.group(2)
            return f"{m.group(3)} {month_name}, {m.group(1)}"
        return date_str
    return ""


def get_metacritic(data):
    """Get metacritic score."""
    mc = data.get("metacritic", {})
    return mc.get("score", None)


def get_genres(data):
    """Get genre names."""
    genres = data.get("genres", [])
    return [g.get("description", "") for g in genres]


def get_screenshots(data):
    """Get screenshots."""
    return data.get("screenshots", [])


def get_developers(data):
    """Get developers."""
    return data.get("developers", [])


def get_publishers(data):
    """Get publishers."""
    return data.get("publishers", [])


def clean_html(html_content):
    """Clean and normalize HTML content from Steam."""
    if not html_content:
        return ""
    return html_content


def escape_for_js(s):
    """Escape string for embedding in JavaScript."""
    if not s:
        return ""
    s = s.replace("\\", "\\\\")
    s = s.replace("'", "\\'")
    s = s.replace("\n", "\\n")
    s = s.replace("\r", "")
    return s


def escape_for_json(s):
    """Escape string for JSON."""
    if not s:
        return ""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "")


def generate_page(game, data):
    """Generate index.html for a game."""
    appid = game["appid"]
    slug = game["slug"]
    cn_name = game["cn_name"]
    en_name = data.get("name", cn_name)
    
    # Header image
    header_image = data.get("header_image", "")
    # Use library_600x900 for cover
    cover_image = f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/library_600x900.jpg"
    # Also get capsule for gallery
    capsule_image = f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/capsule_616x353.jpg"
    
    # Release date
    release_date = get_release_date(data)
    
    # Genres
    genres = get_genres(data)
    genre_tags = "".join([f'<span class="meta-tag">{g}</span>\n' for g in genres])
    
    # Metacritic
    mc_score = get_metacritic(data)
    mc_tag = f'<span class="meta-tag score">⭐ {mc_score}</span>' if mc_score else ""
    
    # Developers / Publishers
    developers = get_developers(data)
    publishers = get_publishers(data)
    dev_str = ", ".join(developers) if developers else "N/A"
    pub_str = ", ".join(publishers) if publishers else "N/A"
    
    # Description
    about_text = data.get("short_description", "")
    # Escape for HTML
    about_text_escaped = about_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    # Download search URLs
    gamer520_url = urllib.parse.quote(en_name)
    x6d_url = urllib.parse.quote(en_name)
    
    # About the game HTML content
    about_game = data.get("about_the_game", "")
    
    # Screenshots
    screenshots = get_screenshots(data)
    
    # Media items - try to get movies first, then screenshots
    movies = data.get("movies", [])
    media_items = []
    
    for m in movies:
        # Get the mp4 or webm source
        video_url = ""
        thumb_url = m.get("thumbnail", "")
        # Try to get the best quality video
        if "mp4" in m.get("webm", {}):
            video_url = m["webm"]["max"]
        elif "mp4" in m:
            video_url = m["mp4"].get("max", "")
        
        # If no video URL, use the thumbnail as placeholder
        if not video_url:
            video_url = thumb_url
        
        media_items.append({
            "type": "video",
            "url": video_url,
            "thumb": thumb_url
        })
    
    for s in screenshots:
        full_url = s.get("path_full", "")
        thumb_url = s.get("path_thumbnail", "")
        media_items.append({
            "type": "image",
            "url": full_url,
            "thumb": thumb_url
        })
    
    # System requirements
    pc_req = data.get("pc_requirements", {})
    min_req = pc_req.get("minimum", "")
    rec_req = pc_req.get("recommended", "")
    
    # Build media thumbnails HTML
    thumbs_html = ""
    for i, item in enumerate(media_items):
        active = "active" if i == 0 else ""
        play_icon = '<div class="play-icon">▶</div>' if item["type"] == "video" else ""
        thumbs_html += f'<div class="media-thumb {active}" data-index="{i}">{play_icon}<img src="{item["thumb"]}" alt="Media"></div>\n'
    
    # Build media items JS array
    media_js_items = []
    for item in media_items:
        media_js_items.append(f'{{"type":"{item["type"]}","url":"{escape_for_json(item["url"])}","thumb":"{escape_for_json(item["thumb"])}"}}')
    media_js = "[\n" + ",\n".join(media_js_items) + "\n]"
    
    # Determine first media display
    first_media = media_items[0] if media_items else {"type": "image", "url": cover_image}
    first_media_display = ""
    if first_media["type"] == "video":
        first_media_display = f'<iframe src="{first_media["url"]}" frameborder="0" allowfullscreen allow="autoplay; fullscreen"></iframe>'
    else:
        first_media_display = f'<img src="{first_media["url"]}" alt="Screenshot">'
    
    # Steam store URL
    steam_url = f"https://store.steampowered.com/app/{appid}/"
    
    # Build the HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{cn_name} - 游戏详情</title>
<style>
:root {{
  --bg: #fafbfc;
  --surface: #ffffff;
  --border: #e5e7eb;
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --accent: #3b82f6;
  --accent-light: #dbeafe;
  --success: #10b981;
  --warning: #f59e0b;
  --radius: 12px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
  --shadow: 0 4px 12px rgba(0,0,0,0.06);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.08);
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg);
  color: var(--text-primary);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}}

/* 顶部导航 */
.topbar {{
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 0.75rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
}}

.topbar a {{
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.2s;
}}

.topbar a:hover {{
  background: var(--accent-light);
  color: var(--accent);
}}

/* 游戏头部 */
.hero {{
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 2rem;
}}

.hero .container {{
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2.5rem;
  align-items: start;
}}

.hero-cover {{
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  aspect-ratio: 3/4;
}}

.hero-cover img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
}}

.hero-info {{
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-top: 0.5rem;
}}

.hero-info h1 {{
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}}

.hero-info .en-name {{
  font-size: 1.125rem;
  color: var(--text-secondary);
  font-weight: 400;
}}

.meta-tags {{
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}}

.meta-tag {{
  font-size: 0.8125rem;
  font-weight: 500;
  padding: 0.375rem 0.75rem;
  border-radius: 8px;
  background: #f3f4f6;
  color: var(--text-secondary);
}}

.meta-tag.score {{
  background: var(--accent-light);
  color: var(--accent);
  font-weight: 600;
}}

.meta-tag.year {{
  background: #fef3c7;
  color: #92400e;
}}

.info-row {{
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}}

.info-item {{
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}}

.info-item .label {{
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}}

.info-item .value {{
  font-size: 0.9375rem;
  color: var(--text-primary);
  font-weight: 500;
}}

.hero-desc {{
  font-size: 1rem;
  color: var(--text-secondary);
  line-height: 1.75;
  max-width: 640px;
}}

/* 媒体区域 - Steam风格 */
.media-section {{
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem;
}}

.media-gallery {{
  background: var(--surface);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  overflow: hidden;
}}

/* 主图显示区域 */
.media-main {{
  position: relative;
  width: 100%;
  aspect-ratio: 16/9;
  background: #000;
  overflow: hidden;
}}

.media-main img,
.media-main video,
.media-main iframe {{
  width: 100%;
  height: 100%;
  object-fit: contain;
  border: none;
}}

/* 媒体控制按钮 */
.media-controls {{
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  display: flex;
  gap: 0.5rem;
  z-index: 10;
}}

.media-control-btn {{
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}}

.media-control-btn:hover {{
  background: rgba(0, 0, 0, 0.9);
}}

/* 缩略图bar */
.media-thumbnails {{
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  overflow-x: auto;
  background: #f9fafb;
  border-top: 1px solid var(--border);
}}

.media-thumbnails::-webkit-scrollbar {{
  height: 6px;
}}

.media-thumbnails::-webkit-scrollbar-track {{
  background: #f3f4f6;
}}

.media-thumbnails::-webkit-scrollbar-thumb {{
  background: #d1d5db;
  border-radius: 3px;
}}

.media-thumb {{
  flex-shrink: 0;
  width: 120px;
  height: 67.5px;
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s;
  position: relative;
}}

.media-thumb:hover {{
  border-color: var(--accent);
  transform: scale(1.05);
}}

.media-thumb.active {{
  border-color: var(--accent);
}}

.media-thumb img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
}}

.media-thumb .play-icon {{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.7);
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}}

/* 内容区域 */
.content-section {{
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem 2rem;
}}

.content-block {{
  background: var(--surface);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  padding: 2rem;
  margin-bottom: 1.5rem;
}}

.content-block h2 {{
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}}

.content-block p {{
  color: var(--text-secondary);
  font-size: 0.9375rem;
  line-height: 1.75;
  margin-bottom: 0.75rem;
}}

.content-block h2.bb_tag {{
  font-size: 1.125rem;
  color: var(--accent);
  margin: 1.5rem 0 0.75rem;
  padding-bottom: 0;
  border-bottom: none;
}}

/* Steam 内嵌媒体 */
.content-block .bb_img_ctn {{
  display: block;
  max-width: 100%;
  margin: 1rem 0;
  overflow: hidden;
  border-radius: 8px;
  background: #000;
}}

.content-block .bb_img {{
  max-width: 100% !important;
  width: 100% !important;
  height: auto !important;
  display: block;
  border-radius: 8px;
}}

.content-block video.bb_img {{
  width: 100% !important;
  height: auto !important;
  max-height: 500px;
  object-fit: contain;
  background: #000;
}}

/* 下载区域 */
.download-section {{
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem 2rem;
}}

.download-block {{
  background: var(--surface);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  padding: 2rem;
}}

.download-block h2 {{
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}}

.download-buttons {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}}

.download-btn {{
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  text-decoration: none;
  color: #fff;
  font-size: 0.9375rem;
  font-weight: 500;
  transition: all 0.2s;
  box-shadow: var(--shadow-sm);
}}

.download-btn:hover {{
  transform: translateY(-2px);
  box-shadow: var(--shadow);
}}

.download-btn.gamer520 {{ background: linear-gradient(135deg, #10b981, #059669); }}
.download-btn.x6d {{ background: linear-gradient(135deg, #3b82f6, #2563eb); }}
.download-btn.magnet {{ background: linear-gradient(135deg, #f59e0b, #d97706); }}
.download-btn.fitgirl {{ background: linear-gradient(135deg, #8b5cf6, #7c3aed); }}
.download-btn.tianyi {{ background: linear-gradient(135deg, #6366f1, #4f46e5); }}
.download-btn.baidu {{ background: linear-gradient(135deg, #06b6d4, #0891b2); }}
.download-btn.crotorrents {{ background: linear-gradient(135deg, #ec4899, #db2777); }}

/* 系统需求 */
.sys-req {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}}

.sys-req-col h4 {{
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--accent);
  margin-bottom: 1rem;
}}

.sys-req-col ul {{
  list-style: none;
}}

.sys-req-col li {{
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
  padding-left: 1.25rem;
  position: relative;
  line-height: 1.6;
}}

.sys-req-col li:before {{
  content: "•";
  position: absolute;
  left: 0;
  color: var(--accent);
  font-weight: bold;
}}

/* 响应式 */
@media (max-width: 900px) {{
  .hero .container {{
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }}
  .hero-cover {{
    max-width: 280px;
    margin: 0 auto;
  }}
  .hero-info h1 {{
    font-size: 1.75rem;
  }}
  .sys-req {{
    grid-template-columns: 1fr;
  }}
  .media-thumb {{
    width: 100px;
    height: 56.25px;
  }}
}}

@media (max-width: 640px) {{
  .hero {{
    padding: 1.5rem 1rem;
  }}
  .media-section,
  .content-section,
  .download-section {{
    padding: 0 1rem 1.5rem;
  }}
  .content-block,
  .download-block {{
    padding: 1.5rem;
  }}
  .media-thumb {{
    width: 80px;
    height: 45px;
  }}
}}
</style>
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
      <img src="{cover_image}" alt="{cn_name}">
    </div>
    <div class="hero-info">
      <h1>{cn_name}</h1>
      <div class="en-name">{en_name}</div>
      
      <div class="meta-tags">
        <span class="meta-tag year">{release_date}</span>
{genre_tags}        {mc_tag}
      </div>
      
      <div class="info-row">
        <div class="info-item">
          <span class="label">开发者</span>
          <span class="value">{dev_str}</span>
        </div>
        <div class="info-item">
          <span class="label">发行商</span>
          <span class="value">{pub_str}</span>
        </div>
      </div>
      
      <div class="hero-desc">
        {about_text_escaped}
      </div>
    </div>
  </div>
</section>

<!-- 媒体区域 -->
<section class="media-section">
  <div class="media-gallery">
    <div class="media-main" id="mediaMain">
      {first_media_display}
    </div>
    <div class="media-thumbnails" id="mediaThumbnails">
{thumbs_html}
    </div>
  </div>
</section>

<!-- 关于此游戏 -->
<section class="content-section">
  <div class="content-block">
    <h2>关于此游戏</h2>
    <div>{about_game}</div>
  </div>
</section>

<!-- 下载区域 -->
<section class="download-section">
  <div class="download-block">
    <h2>📥 下载链接</h2>
    <div class="download-buttons">
      <a href="https://www.gamer520.com/?s={gamer520_url}" class="download-btn gamer520" target="_blank">gamer520</a>
      <a href="https://www.x6d.com/search/?searchkey={x6d_url}" class="download-btn x6d" target="_blank">x6d</a>
    </div>
  </div>
</section>

<!-- 系统需求 -->
<section class="content-section">
  <div class="content-block">
    <h2>系统需求</h2>
    <div class="sys-req">
      <div class="sys-req-col"><h4>最低配置</h4><div>{min_req}</div></div>
      <div class="sys-req-col"><h4>推荐配置</h4><div>{rec_req}</div></div>
    </div>
  </div>
</section>

<script>
// 媒体数据
const mediaItems = {media_js};

let currentIndex = 0;

function switchMedia(index) {{
  if (index < 0 || index >= mediaItems.length) return;
  currentIndex = index;
  const item = mediaItems[index];
  const mainEl = document.getElementById('mediaMain');
  
  if (item.type === 'video') {{
    mainEl.innerHTML = `<iframe src="${{item.url}}" frameborder="0" allowfullscreen allow="autoplay; fullscreen"></iframe>`;
  }} else {{
    mainEl.innerHTML = `<img src="${{item.url}}" alt="Screenshot">`;
  }}
  
  document.querySelectorAll('.media-thumb').forEach((thumb, i) => {{
    thumb.classList.toggle('active', i === index);
  }});
}}

document.addEventListener('DOMContentLoaded', () => {{
  document.querySelectorAll('.media-thumb').forEach((thumb, index) => {{
    thumb.addEventListener('click', () => switchMedia(index));
  }});
  if (mediaItems.length > 0) {{
    switchMedia(0);
  }}
}});
</script>

</body>
</html>'''
    
    return html


def main():
    os.chdir(BASE)
    
    for game in GAMES:
        appid = game["appid"]
        slug = game["slug"]
        
        print(f"\n{'='*60}")
        print(f"Processing: {game['cn_name']} (appid={appid}, slug={slug})")
        
        # Fetch data from Steam API
        data = fetch_steam_api(appid)
        
        if not data:
            print(f"  SKIPPED: API returned no data for appid {appid}")
            continue
        
        # Create directory
        game_dir = os.path.join(BASE, "games", slug)
        os.makedirs(game_dir, exist_ok=True)
        print(f"  Created directory: {game_dir}")
        
        # Generate HTML
        html = generate_page(game, data)
        
        # Write file
        filepath = os.path.join(game_dir, "index.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Written: {filepath} ({len(html)} bytes)")
        
        # Wait 0.5s between requests
        if game != GAMES[-1]:
            print(f"  Waiting 0.5s...")
            time.sleep(0.5)
    
    print(f"\n{'='*60}")
    print("Done!")


if __name__ == "__main__":
    main()