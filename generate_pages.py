#!/usr/bin/env python3
"""Generate game detail pages from Steam API data."""
import json
import time
import re
import urllib.request
import urllib.error
import os
import html as html_mod

# --- CONFIG ---
BASE_DIR = "/root/Projects/20260724-awesome-gaming"

# slug mapping: appid -> slug
SLUG_MAP = {
    "1774580": "star-wars-jedi-survivor",
    "241930": "middle-earth-shadow-of-mordor",
    "812140": "assassins-creed-odyssey",
    "20920": "the-witcher-2",
    "2001120": "split-fiction",
    "582160": "assassins-creed-origins",
    "2208920": "assassins-creed-valhalla",
    "3035570": "assassins-creed-mirage",
    "368500": "assassins-creed-syndicate",
    "289650": "assassins-creed-unity",
    "298110": "far-cry-4",
    "552520": "far-cry-5",
    "2369390": "far-cry-6",
    "15100": "assassins-creed-1",
    "33230": "assassins-creed-2",
    "911400": "assassins-creed-3",
    "242050": "assassins-creed-4",
    "4384550": "call-of-duty-black-ops-6",
    "3595230": "call-of-duty-modern-warfare-ii",
}

# cn_name mapping
CN_NAME = {
    "1774580": "星球大战：绝地武士幸存者",
    "241930": "中土世界：暗影魔多",
    "812140": "刺客信条：奥德赛",
    "20920": "巫师2：国王刺客",
    "2001120": "双影奇境",
    "582160": "刺客信条：起源",
    "2208920": "刺客信条：英灵殿",
    "3035570": "刺客信条：幻景",
    "368500": "刺客信条：枭雄",
    "289650": "刺客信条：大革命",
    "298110": "孤岛惊魂 4",
    "552520": "孤岛惊魂 5",
    "2369390": "孤岛惊魂 6",
    "15100": "刺客信条1",
    "33230": "刺客信条2",
    "911400": "刺客信条3：高清重制版",
    "242050": "刺客信条4：黑旗",
    "4384550": "使命召唤：黑色行动 6",
    "3595230": "使命召唤：现代战争 II 2022",
}

# Partial genre mapping for known appids (fallback if API fails)
GENRE_FALLBACK = {
    "1774580": "动作, 冒险",
    "241930": "动作, 冒险, 角色扮演",
    "812140": "动作, 角色扮演, 冒险",
    "20920": "角色扮演",
    "2001120": "动作, 冒险",
    "582160": "动作, 角色扮演, 冒险",
    "2208920": "动作, 角色扮演, 冒险",
    "3035570": "动作, 冒险",
    "368500": "动作, 冒险",
    "289650": "动作, 冒险",
    "298110": "动作, 冒险",
    "552520": "动作, 冒险",
    "2369390": "动作, 冒险",
    "15100": "动作, 冒险",
    "33230": "动作, 冒险",
    "911400": "动作, 冒险",
    "242050": "动作, 冒险",
    "4384550": "动作, 第一人称射击",
    "3595230": "动作, 第一人称射击",
}

# Metacritic fallback scores
SCORE_FALLBACK = {
    "1774580": 82,
    "241930": 84,
    "812140": 84,
    "20920": 88,
    "2001120": 91,
    "582160": 81,
    "2208920": 80,
    "3035570": 77,
    "368500": 74,
    "289650": 75,
    "298110": 80,
    "552520": 81,
    "2369390": 72,
    "15100": 81,
    "33230": 90,
    "911400": 80,
    "242050": 86,
    "4384550": 80,
    "3595230": 76,
}


def fetch_json(url, retries=3):
    """Fetch JSON from URL with retries."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(1)
    return None


def extract_plain_text(html_content):
    """Extract plain text from Steam bbcode-like HTML content."""
    # Remove script/style tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    # Remove HTML tags but keep text
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = html_mod.unescape(text)
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_steam_description(about_the_game_html):
    """Extract a clean description from Steam's about_the_game HTML."""
    if not about_the_game_html:
        return ""
    text = extract_plain_text(about_the_game_html)
    # Take first paragraph (up to ~200 chars)
    if len(text) > 300:
        text = text[:300] + "..."
    return text


def generate_header(appid, slug, cn_name, data):
    """Generate the HTML header and hero section."""
    game_data = data.get(appid, {})
    success = game_data.get("success", False)
    game = game_data.get("data", {}) if success else {}

    en_name = game.get("name", cn_name)
    release_date = game.get("release_date", {}).get("date", "待公布") if isinstance(game.get("release_date"), dict) else "待公布"
    
    # Genres
    genres_raw = game.get("genres", [])
    if genres_raw:
        genres = ", ".join(g.get("description", "") for g in genres_raw)
    else:
        genres = GENRE_FALLBACK.get(appid, "动作, 冒险")
    
    # Metacritic
    metacritic = game.get("metacritic", {})
    if isinstance(metacritic, dict) and metacritic.get("score"):
        score = metacritic["score"]
    else:
        score = SCORE_FALLBACK.get(appid, 80)
    
    # Developers / Publishers
    developers = game.get("developers", [])
    publishers = game.get("publishers", [])
    developer_str = ", ".join(developers) if developers else "待补充"
    publisher_str = ", ".join(publishers) if publishers else "待补充"
    
    # Short description
    short_desc = game.get("short_description", "")
    if not short_desc:
        short_desc = extract_steam_description(game.get("about_the_game", ""))
    if not short_desc:
        short_desc = f"《{cn_name}》是一款精彩的游戏作品。"
    
    # Cover image
    header_image = game.get("header_image", "")
    if not header_image:
        header_image = f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/library_600x900.jpg"
    else:
        # Use library_600x900 for better cover
        header_image = f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/library_600x900.jpg"
    
    # Escape values for HTML
    cn_name_e = html_mod.escape(cn_name)
    en_name_e = html_mod.escape(en_name)
    short_desc_e = html_mod.escape(short_desc)
    developer_str_e = html_mod.escape(developer_str)
    publisher_str_e = html_mod.escape(publisher_str)
    genres_e = html_mod.escape(genres)
    release_date_e = html_mod.escape(release_date)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{cn_name_e} - 游戏详情</title>
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
  <a href="https://store.steampowered.com/app/{appid}/" target="_blank">Steam 商店页 →</a>
</nav>

<!-- 游戏头部 -->
<section class="hero">
  <div class="container">
    <div class="hero-cover">
      <img src="{header_image}" alt="{cn_name_e}">
    </div>
    <div class="hero-info">
      <h1>{cn_name_e}</h1>
      <div class="en-name">{en_name_e}</div>
      
      <div class="meta-tags">
        <span class="meta-tag year">{release_date_e}</span>
        <span class="meta-tag">{genres_e}</span>
      </div>
      
      <div class="info-row">
        <div class="info-item">
          <span class="label">开发者</span>
          <span class="value">{developer_str_e}</span>
        </div>
        <div class="info-item">
          <span class="label">发行商</span>
          <span class="value">{publisher_str_e}</span>
        </div>
      </div>
      
      <div class="hero-desc">
        {short_desc_e}
      </div>
    </div>
  </div>
</section>

<!-- 媒体区域 -->
<section class="media-section">
  <div class="media-gallery">
    <!-- 主图显示区域 -->
    <div class="media-main" id="mediaMain">
      <iframe src="https://store.steampowered.com/app/{appid}/" frameborder="0" allowfullscreen allow="autoplay; fullscreen"></iframe>
    </div>
    
    <!-- 缩略图bar -->
    <div class="media-thumbnails" id="mediaThumbnails">
'''
    return html


def generate_media_thumbnails(appid, data):
    """Generate media thumbnails HTML."""
    game_data = data.get(appid, {})
    success = game_data.get("success", False)
    game = game_data.get("data", {}) if success else {}
    
    screenshots = game.get("screenshots", [])
    movies = game.get("movies", [])
    
    thumbnails = []
    
    # Add movies first
    for i, movie in enumerate(movies):
        thumb_url = movie.get("thumbnail", "")
        if not thumb_url:
            continue
        # Get the actual mp4/webm URL for the video
        video_urls = movie.get("mp4", {})
        if isinstance(video_urls, dict):
            video_url = video_urls.get("max", "") or video_urls.get("480", "")
        else:
            video_url = ""
        if not video_url:
            video_url = thumb_url
        thumbnails.append({
            "type": "video",
            "url": video_url,
            "thumb": thumb_url,
        })
    
    # Add screenshots
    for i, ss in enumerate(screenshots):
        thumb_url = ss.get("path_thumbnail", "")
        full_url = ss.get("path_full", "")
        if not thumb_url or not full_url:
            continue
        thumbnails.append({
            "type": "image",
            "url": full_url,
            "thumb": thumb_url,
        })
    
    # If no media found, add placeholder
    if not thumbnails:
        thumbnails.append({
            "type": "image",
            "url": f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/library_600x900.jpg",
            "thumb": f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/library_600x900.jpg",
        })
    
    # Limit to 30 items
    thumbnails = thumbnails[:30]
    
    html = ""
    for i, item in enumerate(thumbnails):
        active = " active" if i == 0 else ""
        if item["type"] == "video":
            html += f'      <div class="media-thumb{active}" data-index="{i}"><div class="play-icon">▶</div><img src="{item["thumb"]}" alt="Video"></div>\n'
        else:
            html += f'      <div class="media-thumb{active}" data-index="{i}"><img src="{item["thumb"]}" alt="Screenshot"></div>\n'
    
    html += '''    </div>
  </div>
</section>

<!-- 关于此游戏 -->
<section class="content-section">
  <div class="content-block">
    <h2>关于此游戏</h2>
    <div>
'''
    
    # Add the about_the_game content
    about_html = game.get("about_the_game", "")
    if about_html:
        # Clean up the HTML a bit - replace relative URLs etc.
        about_html = re.sub(r'src="/', 'src="https://store.steampowered.com/', about_html)
        about_html = re.sub(r'href="/', 'href="https://store.steampowered.com/', about_html)
        html += about_html
    else:
        html += f'<p>{html_mod.escape(extract_steam_description("")) or "暂无详细介绍。"}</p>'
    
    html += '''    </div>
  </div>
</section>

<!-- 下载区域 -->
<section class="download-section">
  <div class="download-block">
    <h2>📥 下载链接</h2>
    <div class="download-buttons">
      <a href="#" class="download-btn magnet" target="_blank">🧲磁力</a>
      <a href="#" class="download-btn fitgirl" target="_blank">FitGirl</a>
      <a href="#" class="download-btn gamer520" target="_blank">gamer520</a>
      <a href="#" class="download-btn x6d" target="_blank">x6d</a>
    </div>
  </div>
</section>

<!-- 系统需求 -->
<section class="content-section">
  <div class="content-block">
    <h2>系统需求</h2>
    <div class="sys-req">
'''
    
    # System requirements
    pc_req = game.get("pc_requirements", {})
    if isinstance(pc_req, dict):
        minimum = pc_req.get("minimum", "")
        recommended = pc_req.get("recommended", "")
        
        if minimum:
            html += f'      <div class="sys-req-col"><h4>最低配置</h4><div>{minimum}</div></div>\n'
        else:
            html += '      <div class="sys-req-col"><h4>最低配置</h4><div><ul><li>待补充</li></ul></div></div>\n'
        
        if recommended:
            html += f'      <div class="sys-req-col"><h4>推荐配置</h4><div>{recommended}</div></div>\n'
        else:
            html += '      <div class="sys-req-col"><h4>推荐配置</h4><div><ul><li>待补充</li></ul></div></div>\n'
    else:
        html += '''      <div class="sys-req-col"><h4>最低配置</h4><div><ul><li>待补充</li></ul></div></div>
      <div class="sys-req-col"><h4>推荐配置</h4><div><ul><li>待补充</li></ul></div></div>
'''
    
    html += '''    </div>
  </div>
</section>

<script>
// 媒体数据
const mediaItems = [
'''
    
    # Media items JSON
    for i, item in enumerate(thumbnails):
        comma = "," if i < len(thumbnails) - 1 else ""
        html += f'  {{"type": "{item["type"]}", "url": "{html_mod.escape(item["url"])}", "thumb": "{html_mod.escape(item["thumb"])}"}}{comma}\n'
    
    html += '''];

let currentIndex = 0;

// 切换到指定媒体
function switchMedia(index) {
  if (index < 0 || index >= mediaItems.length) return;
  
  currentIndex = index;
  const item = mediaItems[index];
  const mainEl = document.getElementById('mediaMain');
  
  if (item.type === 'video') {
    // 使用Steam视频嵌入
    mainEl.innerHTML = `<iframe src="${item.url}" frameborder="0" allowfullscreen allow="autoplay; fullscreen"></iframe>`;
  } else {
    mainEl.innerHTML = `<img src="${item.url}" alt="Screenshot">`;
  }
  
  // 更新缩略图active状态
  document.querySelectorAll('.media-thumb').forEach((thumb, i) => {
    thumb.classList.toggle('active', i === index);
  });
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
  // 绑定缩略图点击事件
  document.querySelectorAll('.media-thumb').forEach((thumb, index) => {
    thumb.addEventListener('click', () => switchMedia(index));
  });
  
  // 设置初始状态
  if (mediaItems.length > 0) {
    switchMedia(0);
  }
});
</script>

</body>
</html>'''
    
    return html


def main():
    # Fetch all appids from Steam API
    appids = list(SLUG_MAP.keys())
    all_data = {}
    
    print(f"Fetching data for {len(appids)} games from Steam API...")
    for i, appid in enumerate(appids):
        slug = SLUG_MAP[appid]
        cn_name = CN_NAME[appid]
        print(f"  [{i+1}/{len(appids)}] {cn_name} (appid={appid}, slug={slug})...", end=" ", flush=True)
        
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=schinese"
        result = fetch_json(url)
        
        if result and appid in result:
            game_data = result[appid]
            if game_data.get("success") and game_data.get("data"):
                all_data[appid] = game_data
                game = game_data["data"]
                print(f"OK - {game.get('name', 'N/A')}")
            else:
                print(f"FAIL - API returned success=false or no data")
                # Still store the result so we can use fallback data
                all_data[appid] = game_data if game_data else {}
        else:
            print(f"FAIL - No response")
            all_data[appid] = {}
        
        # 0.5 second delay between requests
        if i < len(appids) - 1:
            time.sleep(0.5)
    
    print(f"\nGenerating pages...")
    for appid in appids:
        slug = SLUG_MAP[appid]
        cn_name = CN_NAME[appid]
        
        game_dir = os.path.join(BASE_DIR, "games", slug)
        os.makedirs(game_dir, exist_ok=True)
        
        # Generate header
        header_html = generate_header(appid, slug, cn_name, all_data)
        
        # Generate media + content + footer
        rest_html = generate_media_thumbnails(appid, all_data)
        
        full_html = header_html + rest_html
        
        filepath = os.path.join(game_dir, "index.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_html)
        
        print(f"  ✓ {slug}/index.html")
    
    print(f"\nDone! Generated {len(appids)} game pages.")


if __name__ == "__main__":
    main()