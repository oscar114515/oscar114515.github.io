import os
import re

for filename in os.listdir('.'):
    if filename.endswith('.html') and filename not in ['TEMPLATE.html', 'index.html']:
        filepath = os.path.join('.', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # 移除重复的 restoreOriginal 函数
        pattern = r'\s*function restoreOriginal\(\) \{[\s\S]*?localStorage\.removeItem\('selectedLang'\);[\s\S]*?\}'
        matches = list(re.finditer(pattern, content))

        if len(matches) > 1:
            # 保留最后一个（因为它在最后）
            # 删除前面的重复
            for match in matches[:-1]:
                content = content[:match.start()] + content[match.end():]
            print(f'Fixed restoreOriginal: {filename}')

        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print('Done')
