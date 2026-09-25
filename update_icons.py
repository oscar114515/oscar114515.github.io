#!/usr/bin/env python3
"""將聯繫彈窗中的文字平台按鈕替換為真實 logo 圖片。"""
import os, re

BASE = r"C:\Users\Administrator\Desktop\oscar114515.github.io"

# CDN logo URLs (SVG, transparent background)
LOGOS = {
    "bili": "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/bilibili.svg",
    "xhs": "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/xiaohongshu.svg",
    "douyin": "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/tiktok.svg",
    "yt": "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/youtube.svg",
}

# Old button HTML (text-based)
OLD_BUTTONS = '''<div class="platform-grid-small">
                <button class="platform-btn-small bili" onclick="window.open('https://space.bilibili.com/3632309945239723','_blank')">嗶哩嗶哩</button>
                <button class="platform-btn-small xhs" onclick="window.open('https://xhslink.com/m/5aECPzZiqGQ','_blank')">小紅書</button>
                <button class="platform-btn-small douyin" onclick="window.open('https://v.douyin.com/HDdZvMmGXwU/','_blank')">抖音</button>
                <button class="platform-btn-small yt" onclick="window.open('https://www.youtube.com/@%E6%A2%81%E5%96%86%E5%90%8C%E5%AD%B8','_blank')">YouTube</button>
            </div>'''

# New button HTML (image-based, same dimensions)
NEW_BUTTONS = '''<div class="platform-grid-small">
                <button class="platform-btn-small bili" onclick="window.open('https://space.bilibili.com/3632309945239723','_blank')"><img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/bilibili.svg" alt="Bilibili" style="height:22px;width:22px;vertical-align:middle;"></button>
                <button class="platform-btn-small xhs" onclick="window.open('https://xhslink.com/m/5aECPzZiqGQ','_blank')"><img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/xiaohongshu.svg" alt="Xiaohongshu" style="height:22px;width:22px;vertical-align:middle;"></button>
                <button class="platform-btn-small douyin" onclick="window.open('https://v.douyin.com/HDdZvMmGXwU/','_blank')"><img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/tiktok.svg" alt="Douyin" style="height:22px;width:22px;vertical-align:middle;"></button>
                <button class="platform-btn-small yt" onclick="window.open('https://www.youtube.com/@%E6%A2%81%E5%96%86%E5%90%8C%E5%AD%B8','_blank')"><img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/youtube.svg" alt="YouTube" style="height:22px;width:22px;vertical-align:middle;"></button>
            </div>'''

# Also need to update the CSS to make images fit properly
OLD_CSS = '''.platform-btn-small {
            display: block; width: 100%; padding: 12px 0;
            border: 1px solid #dce3ed; border-radius: 40px; background: #ffffff;
            font-size: 0.95rem; font-weight: 500; color: #1a1a1a;
            cursor: pointer; text-align: center; transition: 0.15s;
            font-family: sans-serif;
        }
        .platform-btn-small:active { background: #f0f0f0; transform: scale(0.97); }
        .platform-btn-small.bili { color: #00a1d6; }
        .platform-btn-small.xhs { color: #ff2442; }
        .platform-btn-small.douyin { color: #000000; }
        .platform-btn-small.yt { color: #ff0000; }'''

NEW_CSS = '''.platform-btn-small {
            display: flex; align-items: center; justify-content: center; width: 100%; padding: 12px 0;
            border: 1px solid #dce3ed; border-radius: 40px; background: #ffffff;
            cursor: pointer; text-align: center; transition: 0.15s;
        }
        .platform-btn-small:active { background: #f0f0f0; transform: scale(0.97); }
        .platform-btn-small img { display: block; }'''

FILES = [
    "calculator.html", "converter.html", "crack.html", "emoji.html",
    "htmlrunner.html", "login.html", "mtr.html", "paint.html",
    "password.html", "qinqi.html", "qr.html", "spinner.html",
    "timer.html", "tomato.html", "weather.html", "worldclock.html",
    "xmas.html", "airscan.html", "ai-web.html", "convert.html",
]

for f in FILES:
    path = os.path.join(BASE, f)
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()

    changed = False

    # Replace buttons
    if OLD_BUTTONS in content:
        content = content.replace(OLD_BUTTONS, NEW_BUTTONS)
        changed = True

    # Replace CSS
    if OLD_CSS in content:
        content = content.replace(OLD_CSS, NEW_CSS)
        changed = True

    if changed:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f"  ✅ {f}")
    else:
        print(f"  ⏭️  {f}")

print("Done!")