# -*- coding: utf-8 -*-
"""Fix remaining XSS and modal issues in login.html"""
FPATH = 'login.html'

with open(FPATH, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# Fix 1b: XSS in loadUserTable
idx = content.find('`<tr><td>${u.name}</td>')
if idx > 0:
    end = content.find('`;', idx) + 2
    old = content[idx:end]
    print('1b old len:', len(old))

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
        print('1b: XSS fixed')
    else:
        print('1b: no change')
else:
    print('1b: marker not found')

# Fix 3d: Modal override
idx = content.find('_origOpenAuthModal')
if idx > 0:
    close_idx = content.find('};', idx)
    if close_idx > 0:
        old = content[idx:close_idx+2]
        print('3d old:', repr(old[:100]))

        new = old.replace(
            'if (!window.registerExpectedCaptcha) refreshRegisterCaptcha();',
            'if (!window.loginExpectedCaptcha) refreshLoginCaptcha();\n            if (!window.registerExpectedCaptcha) refreshRegisterCaptcha();'
        )

        if old != new:
            content = content.replace(old, new, 1)
            changes += 1
            print('3d: Modal override updated')
        else:
            print('3d: no change')
    else:
        print('3d: closing not found')
else:
    print('3d: marker not found')

with open(FPATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nTotal: {changes}')