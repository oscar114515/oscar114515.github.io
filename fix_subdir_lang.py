#!/usr/bin/env python3
"""修复子目录文件中的韩文/日文选项 - 使用正则匹配"""
import os
import re

BASE = 'C:/Users/Administrator/WorkBuddy/2026-09-04-21-32-11/repo'

# 匹配整个 lang-inline <li> 块
pattern = re.compile(
    r'(<li class="lang-inline">\s*'
    r'<select id="langSwitcherInline" class="lang-switcher-inline" onchange="switchLanguageInline\(this\.value\)">\s*'
    r'<option value="zh"[^>]*>繁體中文</option>\s*'
    r'<option value="cn"[^>]*>简体中文</option>\s*'
    r'<option value="en"[^>]*>English</option>\s*'
    r'<option value="ko"[^>]*>한국어</option>\s*'
    r'<option value="ja"[^>]*>日本語</option>\s*'
    r'</select>\s*'
    r'</li>)'
)

replacement = '''<li class="lang-inline">
                        <select id="langSwitcherInline" class="lang-switcher-inline" onchange="switchLanguageInline(this.value)">
                            <option value="zh">繁體中文</option>
                            <option value="cn">简体中文</option>
                            <option value="en">English</option>
                        </select>
                    </li>'''

# Also fix the JS langOrder
old_js_pattern = re.compile(r"const langOrder = \['zh', 'cn', 'en', 'ko', 'ja'\];")
new_js = "const langOrder = ['zh', 'cn', 'en'];"

old_js_pattern2 = re.compile(r'const langOrder = \["zh", "cn", "en", "ko", "ja"\];')
new_js2 = 'const langOrder = ["zh", "cn", "en"];'

modified = []

for d in ['zh', 'cn', 'en']:
    subdir = os.path.join(BASE, d)
    if not os.path.isdir(subdir):
        continue
    for fname in sorted(os.listdir(subdir)):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(subdir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'langSwitcherInline' not in content:
            continue

        changed = False

        # 替换下拉菜单 HTML
        new_content, count = pattern.subn(replacement, content)
        if count > 0:
            content = new_content
            changed = True
            print(f'✓ {d}/{fname}: 替换 {count} 处下拉菜单')

        # 替换 JS langOrder
        new_content, count = old_js_pattern.subn(new_js, content)
        if count > 0:
            content = new_content
            changed = True
            print(f'✓ {d}/{fname}: 替换 {count} 处 JS langOrder')

        new_content, count = old_js_pattern2.subn(new_js2, content)
        if count > 0:
            content = new_content
            changed = True
            print(f'✓ {d}/{fname}: 替换 {count} 处 JS langOrder (双引号)')

        if changed:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            modified.append(f'{d}/{fname}')

print(f'\n总共修改: {len(modified)} 个文件')