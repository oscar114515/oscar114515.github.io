#!/usr/bin/env python3
"""Extract all unique Chinese text segments from zh/ HTML files."""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
zh_dir = os.path.join(BASE, 'zh')

all_text = set()
for fname in sorted(os.listdir(zh_dir)):
    if not fname.endswith('.html'):
        continue
    with open(os.path.join(zh_dir, fname), 'r', encoding='utf-8') as fh:
        content = fh.read()
    # Find all Chinese text segments
    texts = re.findall(r'[\u4e00-\u9fff\u3000-\u9fff]+', content)
    all_text.update(texts)

print(f'Total unique Chinese text segments: {len(all_text)}')
print()
for t in sorted(all_text, key=len, reverse=True):
    print(repr(t))