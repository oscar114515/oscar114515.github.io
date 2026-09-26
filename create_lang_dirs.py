#!/usr/bin/env python3
"""Create language directory copies with lang-switch.js integration."""
import os
import shutil
import re

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
LANGS = ['zh', 'cn', 'en', 'ko', 'ja']

# Files to exclude (templates, test files)
EXCLUDE = {'TEMPLATE.html', 'captcha_test.html', 'lang-switch.js', 'create_lang_dirs.py'}

# Internal links that need to be prefixed with language path
# These are relative links within the site
INTERNAL_LINKS = [
    'privacy.html', 'login.html', '404.html',
    'emoji.html', 'crack.html', 'xmas.html', 'mtr.html',
    'weather.html', 'tomato.html', 'paint.html', 'worldclock.html',
    'password.html', 'converter.html', 'spinner.html', 'qr.html',
    'calculator.html', 'qinqi.html', 'timer.html', 'htmlrunner.html',
    'ai-web.html', 'airscan.html', 'convert.html', 'converter.html',
    'index.html'
]

def process_file(src_path, dst_path, lang):
    """Copy and modify a file for a specific language."""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add lang-switch.js before closing </head>
    lang_script = '    <script src="lang-switch.js"></script>\n'
    if lang_script not in content:
        content = content.replace('</head>', lang_script + '</head>')

    # 2. Update html lang attribute
    lang_map = {'zh': 'zh-TW', 'cn': 'zh-CN', 'en': 'en', 'ko': 'ko', 'ja': 'ja'}
    content = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang_map[lang]}"', content)

    # 3. Update internal links to include language prefix
    for link in INTERNAL_LINKS:
        # href="privacy.html" → href="/lang/privacy.html"
        content = content.replace(f'href="{link}"', f'href="/{lang}/{link}"')
        # Also handle href='privacy.html' (single quotes)
        content = content.replace(f"href='{link}'", f"href='/{lang}/{link}'")

    # 4. Update title suffix for non-zh languages
    if lang != 'zh':
        lang_names = {'cn': ' · 简体中文', 'en': ' · English', 'ko': ' · 한국어', 'ja': ' · 日本語'}
        content = content.replace(
            '<title>梁喆同學 · 作品集</title>',
            f'<title>梁喆同學 · 作品集{lang_names[lang]}</title>'
        )

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    # Get all HTML files from root (excluding special ones)
    html_files = []
    for f in os.listdir(REPO_DIR):
        if f.endswith('.html') and f not in EXCLUDE:
            html_files.append(f)

    print(f"Found {len(html_files)} HTML files to process")

    for lang in LANGS:
        lang_dir = os.path.join(REPO_DIR, lang)
        os.makedirs(lang_dir, exist_ok=True)
        count = 0
        for html_file in html_files:
            src = os.path.join(REPO_DIR, html_file)
            dst = os.path.join(lang_dir, html_file)
            process_file(src, dst, lang)
            count += 1
        print(f"  {lang}/: {count} files")

    # Copy lang-switch.js to root (already done)
    print("\nDone! Language directories created.")

if __name__ == '__main__':
    main()