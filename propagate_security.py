# -*- coding: utf-8 -*-
"""Propagate all security fixes to all tool HTML files."""
import os

SKIP_FILES = {'login.html', 'captcha_test.html', 'TEMPLATE.html', 'airscan.html', 'htmlrunner.html', 'convert.html'}

escape_fn = """
        // ===== HTML 轉義（防止 XSS） =====
        function escapeHtml(str) {
            if (str == null) return '';
            const div = document.createElement('div');
            div.textContent = str;
            return div.innerHTML;
        }

"""

captcha_login_html = """                    <div class="captcha-row">
                        <label class="captcha-label">驗證碼</label>
                        <input type="text" id="loginCaptcha" class="captcha-input" placeholder="請輸入驗證碼" autocomplete="off">
                        <img id="loginCaptchaImg" class="captcha-image" alt="驗證碼" onclick="refreshLoginCaptcha()">
                        <button class="captcha-refresh" onclick="refreshLoginCaptcha()" title="重新生成">↻</button>
                    </div>"""

login_captcha_check = "if (!checkCaptcha('loginCaptcha', 'loginExpectedCaptcha')) { showMsg(loginMessage, '驗證碼錯誤，請重新獲取', 'error'); return; }\n            "

login_refresh_fn = """        function refreshLoginCaptcha() {
            loadCaptcha('loginCaptchaImg', 'loginExpectedCaptcha');
        }

"""

modal_override_login = """            if (!window.loginExpectedCaptcha) refreshLoginCaptcha();
            if (!window.registerExpectedCaptcha) refreshRegisterCaptcha();"""

safeName_dup = """                const safeName = name.replace(/[.#$\\[\\]]/g, '_');
                const snap = await db.ref('users/' + safeName).once('value');"""

safeName_write = "                const ref = db.ref('users/' + safeName);"

safeName_uid = "const ud = { name, email: '', photo: avatar, uid: safeName };"

firebase_note = """
        // ===== 安全注意 =====
        // Firebase Realtime Database 規則請設定為：
        // {
        //   "rules": {
        //     ".read": "auth != null",
        //     ".write": "auth != null"
        //   }
        // }
        // 或更嚴格的規則以保護用户數據
"""

files_ok = 0
files_skip = 0

for fname in sorted(os.listdir('.')):
    if not fname.endswith('.html'):
        continue
    if fname in SKIP_FILES:
        files_skip += 1
        continue

    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'escapeHtml' in content and 'loginCaptcha' in content and 'safeName' in content:
        print(f'SKIP {fname}: already fixed')
        files_skip += 1
        continue

    changes = 0

    # 1. Add escapeHtml before loadUserTable
    if 'escapeHtml' not in content:
        marker = '        let allUsers = [];'
        if marker in content:
            content = content.replace(marker, escape_fn + marker, 1)
            changes += 1

    # 2. XSS fix in loadUserTable
    if 'escapeHtml(u.name)' not in content:
        idx = content.find('`<tr><td>${u.name}</td>')
        if idx > 0:
            end = content.find('`;', idx) + 2
            old = content[idx:end]
            new = old.replace('${u.name}', '${escapeHtml(u.name)}')
            new = new.replace("${u.email || '-'}", "${escapeHtml(u.email || '-')}")
            new = new.replace('${pwDisplay}', '${escapeHtml(pwDisplay)}')
            new = new.replace(
                "${u.name.replace(/'/g, \"\\\\'\")}",
                "${escapeHtml(u.name).replace(/'/g, \"\\\\'\")}"
            )
            if old != new:
                content = content.replace(old, new, 1)
                changes += 1

    # 3. safeName for duplicate name prevention
    if 'safeName' not in content:
        old_dup = "const snap = await db.ref('users').orderByChild('name').equalTo(name).once('value');"
        if old_dup in content:
            content = content.replace(old_dup, safeName_dup, 1)
            changes += 1

        old_write = "const ref = db.ref('users').push();"
        if old_write in content:
            content = content.replace(old_write, safeName_write, 1)
            changes += 1

        old_uid = "const ud = { name, email: '', photo: avatar, uid: ref.key };"
        if old_uid in content:
            content = content.replace(old_uid, safeName_uid, 1)
            changes += 1

    # 4. Login CAPTCHA
    if 'loginCaptcha' not in content:
        old_form = """<div class="input-group"><input type="password" id="loginPassword" class="input-field" placeholder="密码"></div>
                    <button class="action-btn" id="loginSubmitBtn">登录</button>"""
        new_form = """<div class="input-group"><input type="password" id="loginPassword" class="input-field" placeholder="密码"></div>
""" + captcha_login_html + """
                    <button class="action-btn" id="loginSubmitBtn">登录</button>"""
        if old_form in content:
            content = content.replace(old_form, new_form, 1)
            changes += 1

        old_check = "if (!name || !pw) { showMsg(loginMessage, '請輸入姓名和密码', 'error'); return; }\n            showLoading('登入中...');"
        new_check = "if (!name || !pw) { showMsg(loginMessage, '請輸入姓名和密码', 'error'); return; }\n            " + login_captcha_check + "showLoading('登入中...');"
        if old_check in content:
            content = content.replace(old_check, new_check, 1)
            changes += 1

        old_refresh = "function refreshRegisterCaptcha() {"
        if old_refresh in content and 'refreshLoginCaptcha' not in content:
            content = content.replace(old_refresh, login_refresh_fn + old_refresh, 1)
            changes += 1

        old_modal = "if (!window.registerExpectedCaptcha) refreshRegisterCaptcha();"
        if old_modal in content:
            content = content.replace(old_modal, modal_override_login, 1)
            changes += 1

        old_clear = "loginName.value = '';\n                        loginPassword.value = '';"
        new_clear = "loginName.value = '';\n                        loginPassword.value = '';\n                        document.getElementById('loginCaptcha').value = '';"
        if old_clear in content and "document.getElementById('loginCaptcha')" not in content:
            content = content.replace(old_clear, new_clear, 1)
            changes += 1

    # 5. Firebase rules note
    if '安全注意' not in content:
        marker = '        // ===== CAPTCHA 驗證碼 ====='
        if marker in content:
            content = content.replace(marker, firebase_note + marker, 1)
            changes += 1

    if changes > 0:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'OK {fname}: {changes} changes')
        files_ok += 1
    else:
        print(f'FAIL {fname}: no changes')
        files_skip += 1

print(f'\nProcessed: {files_ok}, Skipped: {files_skip}')