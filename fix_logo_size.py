#!/usr/bin/env python3
"""修复 Logo 尺寸：固定像素大小，任何设备都不缩放"""
import os

BASE = 'C:/Users/Administrator/WorkBuddy/2026-09-04-21-32-11/repo'

# 旧 CSS（允许缩放）
OLD_LOGO_CSS = '.logo img { height: 50px; width: auto; display: block; }'

# 新 CSS（固定尺寸，禁止缩放）
# 图片原始尺寸 864x266，高度 50px 时宽度 = 50 * 864/266 ≈ 162px
NEW_LOGO_CSS = '.logo img { width: 162px; height: 50px; display: block; flex-shrink: 0; min-width: 162px; min-height: 50px; }'

modified = []

# 处理根目录
for fname in sorted(os.listdir(BASE)):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if OLD_LOGO_CSS not in content:
        continue

    content = content.replace(OLD_LOGO_CSS, NEW_LOGO_CSS)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    modified.append(fname)
    print(f'✓ {fname}')

# 处理子目录
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

        if OLD_LOGO_CSS not in content:
            continue

        content = content.replace(OLD_LOGO_CSS, NEW_LOGO_CSS)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        modified.append(f'{d}/{fname}')
        print(f'✓ {d}/{fname}')

print(f'\n总共修改: {len(modified)} 个文件')
print(f'Logo 固定尺寸: 162px × 50px（原始比例 864×266）')