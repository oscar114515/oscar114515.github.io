# -*- coding: utf-8 -*-
"""Add CAPTCHA to all tool HTML files that have register panels."""
import os
import re

BASE_DIR = '.'

SKIP_FILES = {'login.html', 'captcha_test.html', 'TEMPLATE.html', 'airscan.html', 'htmlrunner.html'}

CAPTCHA_CSS = """
        /* CAPTCHA 驗證碼 */
        .captcha-row {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 1rem;
        }
        .captcha-label {
            font-weight: 500;
            color: #5c5c5c;
            font-size: 0.8rem;
            min-width: 44px;
        }
        .captcha-input {
            flex: 0 0 140px;
            padding: 0.55rem 0.7rem;
            border: 1px solid #e5e7eb;
            border-radius: 1rem;
            font-size: 0.85rem;
            outline: none;
            font-family: sans-serif;
        }
        .captcha-input:focus { border-color: #b0b0b0; }
        .captcha-image {
            width: 110px;
            height: 36px;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
            cursor: pointer;
            background: #f9f9f9;
        }
        .captcha-refresh {
            background: none;
            border: none;
            color: #999;
            cursor: pointer;
            font-size: 0.9rem;
            padding: 2px 6px;
            border-radius: 4px;
        }
        .captcha-refresh:hover { background: #f0f0f0; color: #555; }
"""

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

files_processed = 0
files_skipped = 0
files_failed = 0

for fname in sorted(os.listdir(BASE_DIR)):
    if not fname.endswith('.html'):
        continue
    if fname in SKIP_FILES:
        files_skipped += 1
        continue

    fpath = os.path.join(BASE_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'regConfirmPassword' not in content or 'registerSubmitBtn' not in content:
        print(f'SKIP {fname}: no register panel')
        files_skipped += 1
        continue

    if 'captcha-row' in content:
        print(f'SKIP {fname}: already has CAPTCHA')
        files_skipped += 1
        continue

    changes = 0

    # 1. Add CAPTCHA CSS before </style>
    if '</style>' in content:
        content = content.replace('</style>', CAPTCHA_CSS + '</style>', 1)
        changes += 1

    # 2. Add CAPTCHA HTML - find regConfirmPassword line and insert after it
    # Look for the pattern: regConfirmPassword input div followed by registerSubmitBtn
    idx = content.find('id="regConfirmPassword"')
    if idx >= 0:
        # Find the end of this div
        div_end = content.find('</div>', idx) + len('</div>')
        # Find the next line (registerSubmitBtn)
        next_line_start = content.find('\n', div_end) + 1
        next_line_end = content.find('\n', next_line_start)

        captcha_html = """                    <div class="captcha-row">
                        <label class="captcha-label">驗證碼</label>
                        <input type="text" id="registerCaptcha" class="captcha-input" placeholder="請輸入驗證碼" autocomplete="off">
                        <img id="registerCaptchaImg" class="captcha-image" alt="驗證碼" onclick="refreshRegisterCaptcha()">
                        <button class="captcha-refresh" onclick="refreshRegisterCaptcha()" title="重新生成">↻</button>
                    </div>
"""
        content = content[:next_line_start] + captcha_html + content[next_line_start:]
        changes += 1
    else:
        print(f'  {fname}: regConfirmPassword not found')
        files_failed += 1
        continue

    # 3. Add CAPTCHA JS before event binding
    if '事件綁定' in content:
        content = content.replace('        // ===== 事件綁定 =====', CAPTCHA_JS + '        // ===== 事件綁定 =====', 1)
        changes += 1
    else:
        # Try alternate marker
        if 'registerSubmitBtn.addEventListener' in content:
            # Find the event binding section
            idx = content.find('registerSubmitBtn.addEventListener')
            # Go back to find a good insertion point
            line_start = content.rfind('\n', 0, idx) + 1
            # Go back further to find a blank line or comment
            prev_line = content.rfind('\n', 0, line_start - 1) + 1
            content = content[:prev_line] + CAPTCHA_JS + content[prev_line:]
            changes += 1

    # 4. Modify handleRegister - add CAPTCHA check after password validation
    # Find: if (pw !== cf) ... return; }  followed by showLoading
    pw_idx = content.find('if (pw !== cf)')
    if pw_idx >= 0:
        # Find the closing } of this if block
        if_end = content.find('return; }', pw_idx) + len('return; }')
        # Find showLoading after this
        sl_idx = content.find('showLoading', if_end)
        if sl_idx >= 0:
            # Insert CAPTCHA check between the if block and showLoading
            captcha_check = "\n            if (!checkCaptcha('registerCaptcha', 'registerExpectedCaptcha')) { showMsg(registerMessage, '驗證碼錯誤，請重新獲取', 'error'); return; }"
            content = content[:if_end] + captcha_check + content[if_end:]
            changes += 1
    else:
        print(f'  {fname}: pw check not found')

    # 5. Clear CAPTCHA after successful register
    # Find: regName.value = ''; regPassword.value = ''; regConfirmPassword.value = '';
    reg_clear_idx = content.find("regConfirmPassword.value = ''")
    if reg_clear_idx >= 0:
        # Find the end of this line
        line_end = content.find('\n', reg_clear_idx)
        # Insert CAPTCHA clear after this line
        captcha_clear = "\n                document.getElementById('registerCaptcha').value = '';"
        content = content[:line_end] + captcha_clear + content[line_end:]
        changes += 1

    if changes >= 3:  # At minimum: CSS + HTML + JS
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'OK {fname}: {changes} changes')
        files_processed += 1
    else:
        print(f'FAIL {fname}: only {changes} changes (need at least 3)')
        files_failed += 1

print(f'\nProcessed: {files_processed}, Skipped: {files_skipped}, Failed: {files_failed}')