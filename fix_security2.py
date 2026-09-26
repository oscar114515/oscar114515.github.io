# -*- coding: utf-8 -*-
"""Fix remaining security issues in login.html"""
FPATH = 'login.html'

with open(FPATH, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ============================================================
# FIX 1b: XSS in loadUserTable - use escapeHtml
# ============================================================
old_table = """                        `<tr><td>${u.name}</td><td>${u.email || '-'}</td><td>${pwDisplay}</td><td>${d}</td><td><button class="delete-user-btn" onclick="window._deleteUser('${u.key}','${u.name.replace(/'/g, "\\'")}')"><i class="fas fa-trash"></i> 刪除</button></td></tr>`;"""
new_table = """                        `<tr><td>${escapeHtml(u.name)}</td><td>${escapeHtml(u.email || '-')}</td><td>${escapeHtml(pwDisplay)}</td><td>${d}</td><td><button class="delete-user-btn" onclick="window._deleteUser('${u.key}','${escapeHtml(u.name).replace(/'/g, "\\'")}')"><i class="fas fa-trash"></i> 刪除</button></td></tr>`;"""
if old_table in content:
    content = content.replace(old_table, new_table, 1)
    changes += 1
    print('Fix 1b: XSS fixed in loadUserTable')
else:
    print('Fix 1b: FAILED')
    # Debug
    idx = content.find('delete-user-btn')
    if idx > 400:
        # Find the actual line
        start = content.rfind('`<tr>', 0, idx)
        end = content.find('`;', idx) + 2
        print('Actual:', repr(content[start:end]))

# ============================================================
# FIX 3a: Add CAPTCHA to login panel
# ============================================================
old_login = """                    <div class="input-group"><input type="password" id="loginPassword" class="input-field" placeholder="密码"></div>
                    <button class="action-btn" id="loginSubmitBtn">登录</button>"""
new_login = """                    <div class="input-group"><input type="password" id="loginPassword" class="input-field" placeholder="密码"></div>
                    <div class="captcha-row">
                        <label class="captcha-label">驗證碼</label>
                        <input type="text" id="loginCaptcha" class="captcha-input" placeholder="請輸入驗證碼" autocomplete="off">
                        <img id="loginCaptchaImg" class="captcha-image" alt="驗證碼" onclick="refreshLoginCaptcha()">
                        <button class="captcha-refresh" onclick="refreshLoginCaptcha()" title="重新生成">↻</button>
                    </div>
                    <button class="action-btn" id="loginSubmitBtn">登录</button>"""
if old_login in content:
    content = content.replace(old_login, new_login, 1)
    changes += 1
    print('Fix 3a: Login CAPTCHA HTML added')
else:
    print('Fix 3a: FAILED')
    idx = content.find('loginPassword')
    if idx > 0:
        start = content.rfind('<div', 0, idx)
        end = content.find('</button>', idx) + 10
        print('Actual:', repr(content[start:end]))

# ============================================================
# FIX 3b: Add CAPTCHA check to handleLogin
# ============================================================
old_check = """            if (!name || !pw) { showMsg(loginMessage, '請輸入姓名和密码', 'error'); return; }
            showLoading('登入中...');"""
new_check = """            if (!name || !pw) { showMsg(loginMessage, '請輸入姓名和密码', 'error'); return; }
            if (!checkCaptcha('loginCaptcha', 'loginExpectedCaptcha')) { showMsg(loginMessage, '驗證碼錯誤，請重新獲取', 'error'); return; }
            showLoading('登入中...');"""
if old_check in content:
    content = content.replace(old_check, new_check, 1)
    changes += 1
    print('Fix 3b: Login CAPTCHA check added')
else:
    print('Fix 3b: FAILED')
    idx = content.find("if (!name || !pw)")
    if idx > 0:
        end = content.find('showLoading', idx) + 30
        print('Actual:', repr(content[idx:end]))

# ============================================================
# FIX 3d: Update modal override
# ============================================================
old_modal = """        const _origOpenAuthModal = openAuthModal;
        openAuthModal = function() {
            _origOpenAuthModal();
            if (!window.registerExpectedCaptcha) refreshRegisterCaptcha();
        };"""
new_modal = """        const _origOpenAuthModal = openAuthModal;
        openAuthModal = function() {
            _origOpenAuthModal();
            if (!window.loginExpectedCaptcha) refreshLoginCaptcha();
            if (!window.registerExpectedCaptcha) refreshRegisterCaptcha();
        };"""
if old_modal in content:
    content = content.replace(old_modal, new_modal, 1)
    changes += 1
    print('Fix 3d: Modal override updated')
else:
    print('Fix 3d: FAILED')
    idx = content.find('_origOpenAuthModal')
    if idx > 0:
        end = content.find(';', idx) + 200
        print('Actual:', repr(content[idx:end]))

with open(FPATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nTotal changes: {changes}')