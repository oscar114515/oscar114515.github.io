import os
import re

for filename in os.listdir('.'):
    if filename.endswith('.html') and filename not in ['TEMPLATE.html', 'index.html']:
        filepath = os.path.join('.', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # 1. 移除 translate.js 相关代码
        content = re.sub(r'<script src=[^>]*translate\.js[^>]*></script>', '', content)
        content = re.sub(r'<script>[\s\S]*?translate\.selectLanguageTag[\s\S]*?</script>', '', content)
        content = re.sub(r'<!-- translate\.js[^>]*-->\s*', '', content)

        # 2. 替换 translate.execute() 为 MyMemory API 调用
        content = content.replace('translate.language.setLocal(lang);\n                translate.execute();', '''// 使用 MyMemory API 翻译
                if (lang === 'zh-TW') {
                    restoreOriginal();
                } else {
                    translatePage(lang);
                }''')

        # 3. 添加翻译函数
        if 'async function translatePage' not in content:
            translate_code = '''
        // 语言代码映射 (MyMemory API)
        const langCodeMap = {
            'zh-TW': 'zh-TW',
            'zh-CN': 'zh',
            'en': 'en',
            'ko': 'ko',
            'ja': 'ja'
        };

        // 翻译状态
        let isTranslating = false;
        let originalTexts = new Map();

        // 翻译页面
        async function translatePage(targetLang) {
            if (isTranslating) return;
            isTranslating = true;
            localStorage.setItem('selectedLang', targetLang);
            originalTexts.clear();

            // 获取所有可翻译的文本元素
            const excludeSelectors = '.lang-selector, .lang-btn, .lang-option, #langBtn, #langDropdown, #currentLang, button, input, textarea, select';
            const elements = Array.from(document.querySelectorAll('*'))
                .filter(el => {
                    if (el.closest(excludeSelectors)) return false;
                    if (!el.textContent.trim()) return false;
                    if (el.children.length > 0) return false;
                    return true;
                });

            // 保存原文
            elements.forEach(el => {
                originalTexts.set(el, el.textContent.trim());
            });

            const sourceLang = 'zh-TW';
            const targetCode = langCodeMap[targetLang];

            // 逐个翻译
            for (const el of elements) {
                const text = originalTexts.get(el);
                if (!text) continue;
                try {
                    const response = await fetch('https://api.mymemory.translated.net/get?q=' + encodeURIComponent(text) + '&langpair=' + sourceLang + '|' + targetCode);
                    const data = await response.json();
                    if (data.responseStatus === 200 && data.responseData.translatedText) {
                        el.textContent = data.responseData.translatedText;
                    }
                } catch (e) {
                    console.error('Translation error:', e);
                }
            }
            isTranslating = false;
        }

        // 恢复原文
        function restoreOriginal() {
            originalTexts.forEach((text, el) => {
                el.textContent = text;
            });
            originalTexts.clear();
            localStorage.removeItem('selectedLang');
        }'''

            # 在 </script> 前插入
            content = content.replace('</script>', translate_code + '\n    </script>')

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Updated: {filename}')
        else:
            print(f'No change: {filename}')
