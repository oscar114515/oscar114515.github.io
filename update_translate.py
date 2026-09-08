import os
import re

LANG_SELECTOR_HTML = '''<div class="lang-selector">
                        <button class="lang-btn" id="langBtn">
                            <span>🌐</span>
                            <span id="currentLang">中文(繁)</span>
                            <i class="fas fa-chevron-down" style="font-size: 0.7rem;"></i>
                        </button>
                        <div class="lang-dropdown" id="langDropdown">
                            <div class="lang-option active" data-lang="zh-TW" data-flag="🇹🇼">
                                <span>🇹🇼</span>
                                <span>中文(繁)</span>
                            </div>
                            <div class="lang-option" data-lang="zh-CN" data-flag="🇨🇳">
                                <span>🇨🇳</span>
                                <span>中文(简)</span>
                            </div>
                            <div class="lang-option" data-lang="en" data-flag="🇺🇸">
                                <span>🇺🇸</span>
                                <span>English</span>
                            </div>
                            <div class="lang-option" data-lang="ko" data-flag="🇰🇷">
                                <span>🇰🇷</span>
                                <span>한국어</span>
                            </div>
                            <div class="lang-option" data-lang="ja" data-flag="🇯🇵">
                                <span>🇯🇵</span>
                                <span>日本語</span>
                            </div>
                        </div>
                    </div>'''

TRANSLATE_INIT = '''
        // 初始化 translate.js
        translate.selectLanguageTag.languages = 'zh-TW,zh-CN,ko,ja,en';
        translate.language.setLocal('zh-TW');
        translate.selectLanguageTag.show = false;'''

for filename in os.listdir('.'):
    if filename.endswith('.html') and filename not in ['TEMPLATE.html', 'index.html']:
        filepath = os.path.join('.', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # 1. 移除 Google Translate 脚本
        content = re.sub(r'<script type="text/javascript" src="//translate\.google\.com/translate_a/element\.js\?cb=googleTranslateElementInit"></script>\s*', '', content)
        content = re.sub(r'<script\s+type="text/javascript"\s+src="//translate\.google\.com/translate_a/element\.js[^"]*"[^>]*>\s*</script>', '', content)

        # 2. 移除 Google Translate 初始化函数
        content = re.sub(r'\s*function\s+googleTranslateElementInit\s*\(\s*\)\s*\{[^}]*\}\s*', '', content)

        # 3. 替换 google_translate_element 为 lang-selector
        content = re.sub(
            r'<div\s+id="google_translate_element"\s*>',
            LANG_SELECTOR_HTML,
            content
        )

        # 4. 移除 autoDisplay 相关
        content = content.replace('autoDisplay: true', '// translate.js 自动翻译')
        content = content.replace('autoDisplay: false', '// translate.js 自动翻译')

        # 5. 添加 translate.js 脚本（在 </body> 前）
        if 'translate.min.js' not in content:
            content = content.replace('</body>', '''    <!-- translate.js 自动翻译 -->
    <script src="https://cdn.jsdelivr.net/npm/translate.js@2.0.2/translate.min.js"></script>
</body>''')

        # 6. 添加 translate.js 初始化代码（在 </script> 前）
        if 'translate.selectLanguageTag' not in content:
            # 在最后一个 </script> 前插入
            last_script = content.rfind('</script>')
            if last_script > 0:
                content = content[:last_script] + TRANSLATE_INIT + content[last_script:]

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Updated: {filename}')
        else:
            print(f'No change: {filename}')
