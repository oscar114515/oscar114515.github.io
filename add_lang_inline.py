#!/usr/bin/env python3
"""Add inline language switcher to all HTML pages in all language dirs"""
import os, re

BASE = r'C:\Users\Administrator\WorkBuddy\2026-09-04-21-32-11\repo'

# Language switcher HTML + JS to insert before </ul> in nav-right
LANG_SWITCHER = '''                    <li class="lang-inline">
                        <select id="langSwitcherInline" class="lang-switcher-inline" onchange="switchLanguageInline(this.value)">
                            <option value="zh" >繁體中文</option>
                            <option value="cn" >简体中文</option>
                            <option value="en" >English</option>
                            <option value="ko" >한국어</option>
                            <option value="ja" >日本語</option>
                        </select>
                    </li>'''

LANG_JS = '''
<script>
function switchLanguageInline(targetLang) {
    const path = window.location.pathname;
    const langOrder = ['zh', 'cn', 'en', 'ko', 'ja'];
    let pagePath = 'index.html';
    for (const lang of langOrder) {
        const prefix = '/' + lang + '/';
        if (path.includes(prefix)) {
            pagePath = path.substring(path.indexOf(prefix) + prefix.length);
            break;
        }
    }
    window.location.href = '/' + targetLang + '/' + pagePath;
}
document.addEventListener('DOMContentLoaded', function() {
    const sel = document.getElementById('langSwitcherInline');
    if (sel) {
        const path = window.location.pathname;
        const langOrder = ['zh', 'cn', 'en', 'ko', 'ja'];
        for (const lang of langOrder) {
            if (path.includes('/' + lang + '/')) {
                sel.value = lang;
                break;
            }
        }
    }
});
</script>'''

LANG_CSS = '''
        .lang-switcher-inline {
            padding: 6px 10px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 0.9rem;
            background: #fff;
            cursor: pointer;
            color: #333;
            max-width: 140px;
        }
        .lang-switcher-inline:focus {
            outline: none;
            border-color: #007bff;
        }
        .lang-inline {
            display: flex;
            align-items: center;
        }
'''

dirs = ['zh', 'cn', 'en', 'ko', 'ja']
total = 0

for lang in dirs:
    lang_dir = os.path.join(BASE, lang)
    for f in sorted(os.listdir(lang_dir)):
        if not f.endswith('.html'):
            continue
        path = os.path.join(lang_dir, f)
        with open(path, 'r', encoding='utf-8') as fh:
            content = fh.read()
        
        # Skip if already has inline switcher
        if 'langSwitcherInline' in content:
            continue
        
        # Add CSS before </style>
        if '</style>' in content and '.lang-switcher-inline' not in content:
            content = content.replace('</style>', LANG_CSS + '</style>')
        
        # Add JS before </body>
        if '</body>' in content:
            content = content.replace('</body>', LANG_JS + '</body>')
        
        # Insert switcher before </ul> in nav-right
        # Find the last </ul> before </body> (the nav-links one)
        nav_pattern = r'(<div class="nav-right">.*?<ul class="nav-links">)'
        match = re.search(nav_pattern, content, re.DOTALL)
        if match:
            insert_pos = match.end()
            # Insert the switcher li right after <ul class="nav-links">
            content = content[:insert_pos] + LANG_SWITCHER + content[insert_pos:]
        
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(content)
        total += 1
        print(f'  {lang}/{f}: added inline switcher')

print(f'Total: {total} files updated')