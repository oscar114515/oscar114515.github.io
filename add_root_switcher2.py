#!/usr/bin/env python3
"""Add inline language switcher to all root-level HTML files."""
import os

BASE = 'C:/Users/Administrator/WorkBuddy/2026-09-04-21-32-11/repo'

# CSS to add before </style>
LANG_CSS = """
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
"""

# HTML to insert after <ul class="nav-links">
LANG_HTML = """                    <li class="lang-inline">
                        <select id="langSwitcherInline" class="lang-switcher-inline" onchange="switchLanguageInline(this.value)">
                            <option value="zh">繁體中文</option>
                            <option value="cn">简体中文</option>
                            <option value="en">English</option>
                            <option value="ko">한국어</option>
                            <option value="ja">日本語</option>
                        </select>
                    </li>"""

# JS to add before </script> (or before </head>)
LANG_JS = """
function switchLanguageInline(targetLang) {
    const path = window.location.pathname;
    const langOrder = ["zh", "cn", "en", "ko", "ja"];
    let pagePath = "index.html";
    for (const lang of langOrder) {
        const prefix = "/" + lang + "/";
        if (path.includes(prefix)) {
            pagePath = path.substring(path.indexOf(prefix) + prefix.length);
            break;
        }
    }
    window.location.href = "/" + targetLang + "/" + pagePath;
}
document.addEventListener("DOMContentLoaded", function() {
    const sel = document.getElementById("langSwitcherInline");
    if (sel) {
        const path = window.location.pathname;
        const langOrder = ["zh", "cn", "en", "ko", "ja"];
        for (const lang of langOrder) {
            if (path.includes("/" + lang + "/")) {
                sel.value = lang;
                break;
            }
        }
    }
});
"""

# Files to skip
SKIP = {'index.html', 'TEMPLATE.html', 'captcha_test.html'}

modified = []
skipped = []

for fname in sorted(os.listdir(BASE)):
    if not fname.endswith('.html'):
        continue
    if fname in SKIP:
        skipped.append(fname)
        continue

    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has it
    if 'langSwitcherInline' in content:
        skipped.append(fname + ' (already)')
        continue

    # Check for nav-links
    if '<ul class="nav-links"' not in content:
        skipped.append(fname + ' (no nav-links)')
        continue

    changes = 0

    # 1. Insert HTML after <ul class="nav-links">
    nav_marker = '<ul class="nav-links">'
    if nav_marker in content:
        # Find the position right after the opening tag
        idx = content.find(nav_marker)
        insert_pos = idx + len(nav_marker)
        # Check if there's already content right after (the existing <li> tags)
        content = content[:insert_pos] + '\n' + LANG_HTML + content[insert_pos:]
        changes += 1

    # 2. Insert CSS before </style>
    if '</style>' in content and '.lang-switcher-inline' not in content:
        idx = content.find('</style>')
        content = content[:idx] + LANG_CSS + content[idx:]
        changes += 1

    # 3. Insert JS before </script> (the last one before </body>)
    if '</script>' in content and 'function switchLanguageInline' not in content:
        # Find the last </script> before </body>
        body_idx = content.find('</body>')
        if body_idx > 0:
            script_section = content[:body_idx]
            last_script = script_section.rfind('</script>')
            if last_script > 0:
                content = content[:last_script] + LANG_JS + content[last_script:]
                changes += 1

    if changes >= 2:  # At least HTML + one of CSS/JS
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        modified.append(fname)
        print(f'✓ {fname}: {changes} changes')
    else:
        skipped.append(fname + f' (only {changes} changes)')
        print(f'✗ {fname}: only {changes} changes - skipping')

print(f'\nModified: {len(modified)}')
print(f'Skipped: {len(skipped)}')
for s in skipped:
    print(f'  - {s}')