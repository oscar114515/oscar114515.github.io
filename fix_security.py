# -*- coding: utf-8 -*-
"""Fix security vulnerabilities in login.html"""
import os

FPATH = 'login.html'

with open(FPATH, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ============================================================
# FIX 1: XSS - Add escapeHtml function before loadUserTable
# ============================================================
escape_fn = """
        // ===== HTML 轉義（防止 XSS） =====
        function escapeHtml(str) {
            if (str == null) return '';
            const div = document.createElement('div');
            div.textContent = str;
            return div.innerHTML;
        }

"""
marker = '        let allUsers = [];'
if marker in content:
    content = content.replace(marker, escape_fn + marker, 1)
    changes += 1
    print('Fix 1a: escapeHtml function added')

# ============================================================
# FIX 1b: Use escapeHtml in loadUserTable
# ============================================================
old_table = """                        `<tr><td>${u.name}</td><td>${u.email || '-'}</td><td>${pwDisplay}</td><td>${d}</td><td><button class="delete-user-btn" onclick="window._deleteUser('${u.key}','${u.name.replace(/'/g, "\\'")}')"><i class="fas fa-trash"></i> 刪除</button></td></tr>`;"""
new_table = """                        `<tr><td>${escapeHtml(u.name)}</td><td>${escapeHtml(u.email || '-')}</td><td>${escapeHtml(pwDisplay)}</td><td>${d}</td><td><button class="delete-user-btn" onclick="window._deleteUser('${u.key}','${escapeHtml(u.name).replace(/'/g, "\\'")}')"><i class="fas fa-trash"></i> 刪除</button></td></tr>`;"""
if old_table in content:
    content = content.replace(old_table, new_table, 1)
    changes += 1
    print('Fix 1b: loadUserTable XSS fixed')
else:
    print('Fix 1b: old table string not found')

# ============================================================
# FIX 2: Duplicate name - Use name as Firebase key
# ============================================================
old_reg_write = """                const avatar = generateIdenticon(name);
                const ref = db.ref('users').push();
                await ref.set({ name, password: pw, photo: avatar, createdAt: Date.now() });
                const ud = { name, email: '', photo: avatar, uid: ref.key };"""
new_reg_write = """                const avatar = generateIdenticon(name);
                // 使用姓名作為 Firebase key（防止重複姓名）
                const safeName = name.replace(/[.#$\\[\\]]/g, '_');
                const ref = db.ref('users/' + safeName);
                await ref.set({ name, password: pw, photo: avatar, createdAt: Date.now() });
                const ud = { name, email: '', photo: avatar, uid: safeName };"""
if old_reg_write in content:
    content = content.replace(old_reg_write, new_reg_write, 1)
    changes += 1
    print('Fix 2: Register uses name as unique key')
else:
    print('Fix 2: old register write not found')

# Fix duplicate check
old_dup_check = """                const snap = await db.ref('users').orderByChild('name').equalTo(name).once('value');
                if (snap.exists()) { showMsg(registerMessage, '此姓名已被使用', 'error');"""
new_dup_check = """                const safeName = name.replace(/[.#$\\[\\]]/g, '_');
                const snap = await db.ref('users/' + safeName).once('value');
                if (snap.exists()) { showMsg(registerMessage, '此姓名已被使用', 'error');"""
if old_dup_check in content:
    content = content.replace(old_dup_check, new_dup_check, 1)
    changes += 1
    print('Fix 2b: Duplicate check uses safeName')
else:
    print('Fix 2b: old dup check not found')

# ============================================================
# FIX 3: Add CAPTCHA to login panel (rate limiting)
# ============================================================
old_login_form = """<div class="input-group"><input type="password" id="loginPassword" class="input-field" placeholder="密码"></div>
                    <button class="action-btn" id="loginSubmitBtn">登入</button>"""
new_login_form = """<div class="input-group"><input type="password" id="loginPassword" class="input-field" placeholder="密码"></div>
                    <div class="captcha-row">
                        <label class="captcha-label">驗證碼</label>
                        <input type="text" id="loginCaptcha" class="captcha-input" placeholder="請輸入驗證碼" autocomplete="off">
                        <img id="loginCaptchaImg" class="captcha-image" alt="驗證碼" onclick="refreshLoginCaptcha()">
                        <button class="captcha-refresh" onclick="refreshLoginCaptcha()" title="重新生成">↻</button>
                    </div>
                    <button class="action-btn" id="loginSubmitBtn">登入</button>"""
if old_login_form in content:
    content = content.replace(old_login_form, new_login_form, 1)
    changes += 1
    print('Fix 3a: Login CAPTCHA HTML added')
else:
    print('Fix 3a: old login form not found')

# Add CAPTCHA check to handleLogin
old_login_check = """            if (!name || !pw) { showMsg(loginMessage, '請輸入姓名和密码', 'error'); return; }
            showLoading('登入中...');"""
new_login_check = """            if (!name || !pw) { showMsg(loginMessage, '請輸入姓名和密码', 'error'); return; }
            if (!checkCaptcha('loginCaptcha', 'loginExpectedCaptcha')) { showMsg(loginMessage, '驗證碼錯誤，請重新獲取', 'error'); return; }
            showLoading('登入中...');"""
if old_login_check in content:
    content = content.replace(old_login_check, new_login_check, 1)
    changes += 1
    print('Fix 3b: Login CAPTCHA check added')
else:
    print('Fix 3b: old login check not found')

# Add refreshLoginCaptcha function
old_refresh = """        function refreshRegisterCaptcha() {
            loadCaptcha('registerCaptchaImg', 'registerExpectedCaptcha');
        }"""
new_refresh = """        function refreshLoginCaptcha() {
            loadCaptcha('loginCaptchaImg', 'loginExpectedCaptcha');
        }

        function refreshRegisterCaptcha() {
            loadCaptcha('registerCaptchaImg', 'registerExpectedCaptcha');
        }"""
if old_refresh in content:
    content = content.replace(old_refresh, new_refresh, 1)
    changes += 1
    print('Fix 3c: refreshLoginCaptcha added')
else:
    print('Fix 3c: old refresh not found')

# Update modal override
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
    print('Fix 3d: old modal not found')

# Clear login CAPTCHA after successful login
old_login_clear = """                        loginName.value = '';
                        loginPassword.value = '';"""
new_login_clear = """                        loginName.value = '';
                        loginPassword.value = '';
                        document.getElementById('loginCaptcha').value = '';"""
if old_login_clear in content:
    content = content.replace(old_login_clear, new_login_clear, 1)
    changes += 1
    print('Fix 3e: Login CAPTCHA clear added')
else:
    print('Fix 3e: old login clear not found')

# ============================================================
# FIX 4: Add note about Firebase rules
# ============================================================
note = """
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
marker2 = '        // ===== CAPTCHA 驗證碼 ====='
if marker2 in content:
    content = content.replace(marker2, note + marker2, 1)
    changes += 1
    print('Fix 4: Firebase rules note added')
else:
    print('Fix 4: marker not found')

with open(FPATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nTotal changes: {changes}')