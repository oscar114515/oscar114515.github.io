# -*- coding: utf-8 -*-
import sys

with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# Fix 1: Make captcha-input not flex:1, give it a fixed width
old_css = '.captcha-input {\n            flex: 1;\n            padding: 0.55rem 0.7rem;'
new_css = '.captcha-input {\n            flex: 0 0 140px;\n            padding: 0.55rem 0.7rem;'
if old_css in content:
    content = content.replace(old_css, new_css, 1)
    changes += 1
    print('CSS fixed')

# Fix 2: Remove CAPTCHA row from login panel
old_login_captcha = '''<div class="captcha-row">
                        <label class="captcha-label">验证码</label>
                        <input type="text" id="loginCaptcha" class="captcha-input" placeholder="请输入验证码" autocomplete="off">
                        <img id="loginCaptchaImg" class="captcha-image" alt="验证码" onclick="refreshLoginCaptcha()">
                        <button class="captcha-refresh" onclick="refreshLoginCaptcha()" title="重新生成">↻</button>
                    </div>
                    <button class="action-btn" id="loginSubmitBtn">登录</button>'''
new_login = '<button class="action-btn" id="loginSubmitBtn">登录</button>'
if old_login_captcha in content:
    content = content.replace(old_login_captcha, new_login, 1)
    changes += 1
    print('Login CAPTCHA HTML removed')
else:
    print('Login CAPTCHA HTML not found, trying alternate...')
    # Try with traditional Chinese
    old_login_captcha2 = '''<div class="captcha-row">
                        <label class="captcha-label">驗證碼</label>
                        <input type="text" id="loginCaptcha" class="captcha-input" placeholder="請輸入驗證碼" autocomplete="off">
                        <img id="loginCaptchaImg" class="captcha-image" alt="驗證碼" onclick="refreshLoginCaptcha()">
                        <button class="captcha-refresh" onclick="refreshLoginCaptcha()" title="重新生成">↻</button>
                    </div>
                    <button class="action-btn" id="loginSubmitBtn">登入</button>'''
    if old_login_captcha2 in content:
        content = content.replace(old_login_captcha2, new_login, 1)
        changes += 1
        print('Login CAPTCHA HTML removed (traditional)')

# Fix 3: Remove CAPTCHA check from handleLogin
old_login_check = "if (!name || !pw) { showMsg(loginMessage, '请输入姓名和密码', 'error'); return; }\n            if (!checkCaptcha('loginCaptcha', 'loginExpectedCaptcha', '验证码错误')) { showMsg(loginMessage, '验证码错误，请重新获取', 'error'); return; }\n            showLoading('登录中...');"
new_login_check = "if (!name || !pw) { showMsg(loginMessage, '请输入姓名和密码', 'error'); return; }\n            showLoading('登录中...');"
if old_login_check in content:
    content = content.replace(old_login_check, new_login_check, 1)
    changes += 1
    print('Login CAPTCHA check removed')
else:
    # Try traditional
    old_login_check2 = "if (!name || !pw) { showMsg(loginMessage, '請輸入姓名和密码', 'error'); return; }\n            if (!checkCaptcha('loginCaptcha', 'loginExpectedCaptcha', '驗證碼錯誤')) { showMsg(loginMessage, '驗證碼錯誤，請重新獲取', 'error'); return; }\n            showLoading('登入中...');"
    if old_login_check2 in content:
        content = content.replace(old_login_check2, new_login_check, 1)
        changes += 1
        print('Login CAPTCHA check removed (traditional)')

# Fix 4: Remove login CAPTCHA clear
old_login_clear = "loginName.value = '';\n                        loginPassword.value = '';\n                        document.getElementById('loginCaptcha').value = '';"
new_login_clear = "loginName.value = '';\n                        loginPassword.value = '';"
if old_login_clear in content:
    content = content.replace(old_login_clear, new_login_clear, 1)
    changes += 1
    print('Login CAPTCHA clear removed')

# Fix 5: Remove refreshLoginCaptcha function
old_login_js = "        function refreshLoginCaptcha() {\n            loadCaptcha('loginCaptchaImg', 'loginExpectedCaptcha');\n        }\n        \n"
if old_login_js in content:
    content = content.replace(old_login_js, '', 1)
    changes += 1
    print('Login refresh function removed')

# Fix 6: Update modal override
old_modal = "        const originalOpenAuthModal = openAuthModal;\n        openAuthModal = function() {\n            originalOpenAuthModal();\n            if (!window.loginExpectedCaptcha) refreshLoginCaptcha();\n            if (!window.registerExpectedCaptcha) refreshRegisterCaptcha();\n        };\n"
new_modal = "        const originalOpenAuthModal = openAuthModal;\n        openAuthModal = function() {\n            originalOpenAuthModal();\n            if (!window.registerExpectedCaptcha) refreshRegisterCaptcha();\n        };\n"
if old_modal in content:
    content = content.replace(old_modal, new_modal, 1)
    changes += 1
    print('Modal override updated')

with open('login.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nTotal changes: {changes}')