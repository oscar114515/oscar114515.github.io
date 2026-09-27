#!/usr/bin/env python3
"""Add inline language switcher to root index.html"""
import os, re

BASE = r'C:\Users\Administrator\WorkBuddy\2026-09-04-21-32-11\repo'

LANG_SWITCHER = (
    '                    <li class="lang-inline">\n'
    '                        <select id="langSwitcherInline" class="lang-switcher-inline" '
    'onchange="switchLanguageInline(this.value)">\n'
    '                            <option value="zh">繁體中文</option>\n'
    '                            <option value="cn">简体中文</option>\n'
    '                            <option value="en">English</option>\n'
    '                            <option value="ko">한국어</option>\n'
    '                            <option value="ja">日本語</option>\n'
    '                        </select>\n'
    '                    </li>'
)

LANG_JS = (
    '<script>\n'
    'function switchLanguageInline(targetLang) {\n'
    '    const path = window.location.pathname;\n'
    '    const langOrder = ["zh", "cn", "en", "ko", "ja"];\n'
    '    let pagePath = "index.html";\n'
    '    for (const lang of langOrder) {\n'
    '        const prefix = "/" + lang + "/";\n'
    '        if (path.includes(prefix)) {\n'
    '            pagePath = path.substring(path.indexOf(prefix) + prefix.length);\n'
    '            break;\n'
    '        }\n'
    '    }\n'
    '    window.location.href = "/" + targetLang + "/" + pagePath;\n'
    '}\n'
    'document.addEventListener("DOMContentLoaded", function() {\n'
    '    const sel = document.getElementById("langSwitcherInline");\n'
    '    if (sel) {\n'
    '        const path = window.location.pathname;\n'
    '        const langOrder = ["zh", "cn", "en", "ko", "ja"];\n'
    '        for (const lang of langOrder) {\n'
    '            if (path.includes("/" + lang + "/")) {\n'
    '                sel.value = lang;\n'
    '                break;\n'
    '            }\n'
    '        }\n'
    '    }\n'
    '});\n'
    '</script>'
)

LANG_CSS = (
    '        .lang-switcher-inline {\n'
    '            padding: 6px 10px;\n'
    '            border: 1px solid #ddd;\n'
    '            border-radius: 6px;\n'
    '            font-size: 0.9rem;\n'
    '            background: #fff;\n'
    '            cursor: pointer;\n'
    '            color: #333;\n'
    '            max-width: 140px;\n'
    '        }\n'
    '        .lang-switcher-inline:focus {\n'
    '            outline: none;\n'
    '            border-color: #007bff;\n'
    '        }\n'
    '        .lang-inline {\n'
    '            display: flex;\n'
    '            align-items: center;\n'
    '        }\n'
)

path = os.path.join(BASE, 'index.html')
with open(path, 'r', encoding='utf-8') as fh:
    content = fh.read()

if 'langSwitcherInline' not in content:
    if '</style>' in content:
        content = content.replace('</style>', LANG_CSS + '</style>')
    if '</body>' in content:
        content = content.replace('</body>', LANG_JS + '</body>')

    nav_pattern = r'(<div class="nav-right">.*?<ul class="nav-links">)'
    match = re.search(nav_pattern, content, re.DOTALL)
    if match:
        insert_pos = match.end()
        content = content[:insert_pos] + LANG_SWITCHER + content[insert_pos:]

    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(content)
    print('Root index.html: added inline switcher')
else:
    print('Root index.html: already has inline switcher')