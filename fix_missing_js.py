# -*- coding: utf-8 -*-
"""Add missing CAPTCHA JS to files that have CSS but no JS."""
import os

CAPTCHA_JS = """
        // ===== CAPTCHA 驗證碼 =====
        const captchaChars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';

        function generateCaptchaText() {
            let result = '';
            for (let i = 0; i < 4; i++) {
                result += captchaChars.charAt(Math.floor(Math.random() * captchaChars.length));
            }
            return result;
        }

        function loadCaptcha(imgId, expectedVar) {
            const text = generateCaptchaText();
            window[expectedVar] = text;
            const img = document.getElementById(imgId);
            img.src = 'https://api.opencaptcha.io/captcha?text=' + encodeURIComponent(text) + '&t=' + Date.now();
        }

        function refreshRegisterCaptcha() {
            loadCaptcha('registerCaptchaImg', 'registerExpectedCaptcha');
        }

        function checkCaptcha(inputId, expectedVar) {
            const input = document.getElementById(inputId).value.trim().toUpperCase();
            const expected = window[expectedVar];
            if (!expected) return true;
            return input === expected;
        }

        // Initialize CAPTCHA when modal opens
        const _origOpenAuthModal = openAuthModal;
        openAuthModal = function() {
            _origOpenAuthModal();
            if (!window.registerExpectedCaptcha) refreshRegisterCaptcha();
        };

"""

missing_files = ['ai-web.html', 'index.html', 'mtr.html', 'weather.html']

for fname in missing_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'generateCaptchaText' in content:
        print(f'SKIP {fname}: already has JS')
        continue

    # Find the event binding section - try different markers
    markers = [
        '        // ===== 事件綁定 =====',
        '        // 9. 事件綁定',
        '        // 事件綁定',
        '// 事件綁定',
        'registerSubmitBtn.addEventListener',
        'registerSubmit.addEventListener',
    ]

    inserted = False
    for marker in markers:
        if marker in content:
            content = content.replace(marker, CAPTCHA_JS + marker, 1)
            inserted = True
            print(f'OK {fname}: JS inserted before marker')
            break

    if not inserted:
        # Try to find registerSubmitBtn.addEventListener and insert before it
        idx = content.find('registerSubmitBtn.addEventListener')
        if idx >= 0:
            line_start = content.rfind('\n', 0, idx) + 1
            content = content[:line_start] + CAPTCHA_JS + content[line_start:]
            inserted = True
            print(f'OK {fname}: JS inserted before registerSubmitBtn.addEventListener')
        else:
            print(f'FAIL {fname}: could not find insertion point')
            continue

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)