import os
import re

for filename in os.listdir('.'):
    if filename.endswith('.html') and filename not in ['TEMPLATE.html', 'index.html']:
        filepath = os.path.join('.', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # 移除重复的 translatePage 函数（保留第一个）
        # 找到第一个 translatePage 函数的结束位置
        first_match = re.search(r'async function translatePage\(targetLang\) \{', content)
        if first_match:
            # 找到对应的结束括号
            start = first_match.start()
            brace_count = 0
            end = start
            for i in range(start, len(content)):
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end = i + 1
                        break

            # 查找后续的重复函数
            remaining = content[end:]
            duplicate_pattern = r'\s*async function translatePage\(targetLang\) \{[\s\S]*?\n        \}'
            remaining_clean = re.sub(duplicate_pattern, '', remaining)

            if len(remaining_clean) < len(remaining):
                content = content[:end] + remaining_clean
                print(f'Cleaned: {filename}')

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
