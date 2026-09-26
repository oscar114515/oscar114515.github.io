# -*- coding: utf-8 -*-
"""Fix logo link to point to index.html instead of #"""
import os

skip = {'captcha_test.html', 'TEMPLATE.html'}

for f in sorted(os.listdir('.')):
    if not f.endswith('.html') or f in skip:
        continue
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()

    old = 'href="#"><img src="https://i.postimg.cc/HxVC7TcN/IMG-8863.png" alt="Logo"></a>'
    new = 'href="index.html"><img src="https://i.postimg.cc/HxVC7TcN/IMG-8863.png" alt="Logo"></a>'

    if old in content:
        content = content.replace(old, new, 1)
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f'OK {f}')
    else:
        print(f'SKIP {f}')