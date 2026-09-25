#!/usr/bin/env python3
"""將 CDN 圖片改為 inline SVG，避免外部加載問題。"""
import os, re, urllib.request

BASE = r"C:\Users\Administrator\Desktop\oscar114515.github.io"

# 下載 SVG 內容
CDN_URLS = {
    "bili": "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/bilibili.svg",
    "xhs": "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/xiaohongshu.svg",
    "douyin": "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/tiktok.svg",
    "yt": "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/youtube.svg",
}

SVG_CONTENT = {}
for key, url in CDN_URLS.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            svg = resp.read().decode('utf-8')
            # 移除 XML declaration 和 svg 标籤，只保留內部內容
            svg = svg.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
            SVG_CONTENT[key] = svg.strip()
            print(f"  ✅ {key}: {len(svg)} bytes")
    except Exception as e:
        print(f"  ❌ {key}: {e}")

# 替換映射
REPLACEMENTS = {
    # calculator.html 等：class 方式的按鈕
    '<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/bilibili.svg" alt="Bilibili" style="height:22px;width:22px;vertical-align:middle;">':
        f'<span style="display:inline-block;vertical-align:middle;">{SVG_CONTENT["bili"]}</span>',
    '<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/xiaohongshu.svg" alt="Xiaohongshu" style="height:22px;width:22px;vertical-align:middle;">':
        f'<span style="display:inline-block;vertical-align:middle;">{SVG_CONTENT["xhs"]}</span>',
    '<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/tiktok.svg" alt="Douyin" style="height:22px;width:22px;vertical-align:middle;">':
        f'<span style="display:inline-block;vertical-align:middle;">{SVG_CONTENT["douyin"]}</span>',
    '<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/youtube.svg" alt="YouTube" style="height:22px;width:22px;vertical-align:middle;">':
        f'<span style="display:inline-block;vertical-align:middle;">{SVG_CONTENT["yt"]}</span>',
    # ai-web.html：沒有 vertical-align
    '<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/bilibili.svg" alt="Bilibili" style="height:22px;width:22px;">':
        f'<span style="display:inline-block;vertical-align:middle;">{SVG_CONTENT["bili"]}</span>',
    '<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/xiaohongshu.svg" alt="Xiaohongshu" style="height:22px;width:22px;">':
        f'<span style="display:inline-block;vertical-align:middle;">{SVG_CONTENT["xhs"]}</span>',
    '<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/tiktok.svg" alt="Douyin" style="height:22px;width:22px;">':
        f'<span style="display:inline-block;vertical-align:middle;">{SVG_CONTENT["douyin"]}</span>',
    '<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/youtube.svg" alt="YouTube" style="height:22px;width:22px;">':
        f'<span style="display:inline-block;vertical-align:middle;">{SVG_CONTENT["yt"]}</span>',
    # convert.html：沒有 vertical-align，沒有 height/width
    '<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/bilibili.svg" alt="Bilibili" style="height:22px;width:22px;">':
        f'<span style="display:inline-block;vertical-align:middle;">{SVG_CONTENT["bili"]}</span>',
    '<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/xiaohongshu.svg" alt="Xiaohongshu" style="height:22px;width:22px;">':
        f'<span style="display:inline-block;vertical-align:middle;">{SVG_CONTENT["xhs"]}</span>',
    '<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/tiktok.svg" alt="Douyin" style="height:22px;width:22px;">':
        f'<span style="display:inline-block;vertical-align:middle;">{SVG_CONTENT["douyin"]}</span>',
    '<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/youtube.svg" alt="YouTube" style="height:22px;width:22px;">':
        f'<span style="display:inline-block;vertical-align:middle;">{SVG_CONTENT["yt"]}</span>',
}

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
    for old, new in REPLACEMENTS.items():
        if old in content:
            content = content.replace(old, new)
            changed = True
    if changed:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f"  ✅ {f}")
    else:
        print(f"  ⏭️  {f}")

print("Done!")