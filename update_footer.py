#!/usr/bin/env python3
"""將關於這個网站文字移到聯繫我們區塊。"""
import os

BASE = r"C:\Users\Administrator\Desktop\oscar114515.github.io"

OLD = '''        <div class="footer-col">
            <h4>關於這個网站</h4>
            <p>這是梁喆同學的個人作品集网站，上面所有工具均由原創開發。网站使用 GitHub Pages 托管，並整合了 Firebase 認證功能。</p>
            <p>聯繫我們：QQ: 1962487792 | 郵箱: oscarmtr114514@gmail.com</p>
        </div>
        <div class="footer-col">
            <h4>隐私政策</h4>
            <p>本站不收集任何個人數據。所有工具均在本地浏览器運行，不會將你的數據上傳至任何服務器。我們不使用 Cookie 追踪，也不與第三方共享數據。</p>
        </div>'''

NEW = '''        <div class="footer-col">
            <h4>隐私政策</h4>
            <p>本站不收集任何個人數據。所有工具均在本地浏览器運行，不會將你的數據上傳至任何服務器。我們不使用 Cookie 追踪，也不與第三方共享數據。</p>
        </div>
        <div class="footer-col">
            <h4>聯繫我們</h4>
            <p>這是梁喆同學的個人作品集网站，上面所有工具均由原創開發。网站使用 GitHub Pages 托管，並整合了 Firebase 認證功能。</p>
            <p>QQ: 1962487792 | 郵箱: oscarmtr114514@gmail.com</p>
        </div>'''

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
    if OLD in content:
        content = content.replace(OLD, NEW)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f"  ✅ {f}")
    else:
        print(f"  ⏭️  {f}")

print("Done!")