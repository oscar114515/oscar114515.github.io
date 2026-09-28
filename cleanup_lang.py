#!/usr/bin/env python3
"""清理：删除韩文/日文，只保留繁中/简中/英文，修复双下拉菜单问题"""
import os
import shutil

BASE = 'C:/Users/Administrator/WorkBuddy/2026-09-04-21-32-11/repo'

# 1. 删除 ko/ 和 ja/ 目录
for d in ['ko', 'ja']:
    dirpath = os.path.join(BASE, d)
    if os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
        print(f'✓ 已删除目录: {d}/')
    else:
        print(f'✗ 目录不存在: {d}/')

# 2. 定义替换规则
# 移除 lang-switch.js 引用（它会动态创建第二个下拉菜单）
# 更新 inline 下拉菜单 HTML：只保留 zh/cn/en
# 更新 inline JS：langOrder 只保留三种

OLD_LANG_HTML = """                    <li class="lang-inline">
                        <select id="langSwitcherInline" class="lang-switcher-inline" onchange="switchLanguageInline(this.value)">
                            <option value="zh">繁體中文</option>
                            <option value="cn">简体中文</option>
                            <option value="en">English</option>
                            <option value="ko">한국어</option>
                            <option value="ja">日本語</option>
                        </select>
                    </li>"""

NEW_LANG_HTML = """                    <li class="lang-inline">
                        <select id="langSwitcherInline" class="lang-switcher-inline" onchange="switchLanguageInline(this.value)">
                            <option value="zh">繁體中文</option>
                            <option value="cn">简体中文</option>
                            <option value="en">English</option>
                        </select>
                    </li>"""

# root index.html uses slightly different format (no extra spaces)
OLD_LANG_HTML_ROOT = """                <ul class="nav-links">                    <li class="lang-inline">
                        <select id="langSwitcherInline" class="lang-switcher-inline" onchange="switchLanguageInline(this.value)">
                            <option value="zh">繁體中文</option>
                            <option value="cn">简体中文</option>
                            <option value="en">English</option>
                            <option value="ko">한국어</option>
                            <option value="ja">日本語</option>
                        </select>
                    </li>"""

NEW_LANG_HTML_ROOT = """                <ul class="nav-links">                    <li class="lang-inline">
                        <select id="langSwitcherInline" class="lang-switcher-inline" onchange="switchLanguageInline(this.value)">
                            <option value="zh">繁體中文</option>
                            <option value="cn">简体中文</option>
                            <option value="en">English</option>
                        </select>
                    </li>"""

OLD_JS = """function switchLanguageInline(targetLang) {
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
});"""

NEW_JS = """function switchLanguageInline(targetLang) {
    const path = window.location.pathname;
    const langOrder = ['zh', 'cn', 'en'];
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
        const langOrder = ['zh', 'cn', 'en'];
        for (const lang of langOrder) {
            if (path.includes('/' + lang + '/')) {
                sel.value = lang;
                break;
            }
        }
    }
});"""

# root index.html uses double quotes
OLD_JS_ROOT = """function switchLanguageInline(targetLang) {
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
});"""

NEW_JS_ROOT = """function switchLanguageInline(targetLang) {
    const path = window.location.pathname;
    const langOrder = ["zh", "cn", "en"];
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
        const langOrder = ["zh", "cn", "en"];
        for (const lang of langOrder) {
            if (path.includes("/" + lang + "/")) {
                sel.value = lang;
                break;
            }
        }
    }
});"""

modified = []
errors = []

# 3. 处理根目录 HTML 文件
for fname in sorted(os.listdir(BASE)):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'langSwitcherInline' not in content:
        continue

    changed = False

    # 移除 lang-switch.js 引用（防止双下拉菜单）
    if '<script src="lang-switch.js"></script>' in content:
        content = content.replace('<script src="lang-switch.js"></script>', '')
        changed = True

    # 替换下拉菜单 HTML
    if OLD_LANG_HTML_ROOT in content:
        content = content.replace(OLD_LANG_HTML_ROOT, NEW_LANG_HTML_ROOT)
        changed = True
    elif OLD_LANG_HTML in content:
        content = content.replace(OLD_LANG_HTML, NEW_LANG_HTML)
        changed = True

    # 替换 inline JS
    if OLD_JS_ROOT in content:
        content = content.replace(OLD_JS_ROOT, NEW_JS_ROOT)
        changed = True
    elif OLD_JS in content:
        content = content.replace(OLD_JS, NEW_JS)
        changed = True

    if changed:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        modified.append(fname)
        print(f'✓ {fname}')

# 4. 处理子目录 HTML 文件
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

        # 移除 lang-switch.js 引用
        if 'lang-switch.js' in content:
            # Try different patterns
            for pattern in ['<script src="lang-switch.js"></script>', '<script src="lang-switch.js">']:
                if pattern in content:
                    content = content.replace(pattern, '')
                    changed = True
                    break

        # 替换下拉菜单 HTML
        if OLD_LANG_HTML in content:
            content = content.replace(OLD_LANG_HTML, NEW_LANG_HTML)
            changed = True

        # 替换 inline JS
        if OLD_JS in content:
            content = content.replace(OLD_JS, NEW_JS)
            changed = True

        if changed:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            modified.append(f'{d}/{fname}')
            print(f'✓ {d}/{fname}')

print(f'\n总共修改: {len(modified)} 个文件')

# 5. 删除 lang-switch.js（不再需要）
js_path = os.path.join(BASE, 'lang-switch.js')
if os.path.exists(js_path):
    os.remove(js_path)
    print('✓ 已删除 lang-switch.js')

# 6. 也删除子目录中的 lang-switch.js
for d in ['zh', 'cn', 'en']:
    js_path = os.path.join(BASE, d, 'lang-switch.js')
    if os.path.exists(js_path):
        os.remove(js_path)
        print(f'✓ 已删除 {d}/lang-switch.js')