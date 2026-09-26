# -*- coding: utf-8 -*-
"""Fix ai-web.html specifically - different structure from other files."""
FPATH = 'ai-web.html'

with open(FPATH, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# 1. Add escapeHtml function before loadUserTable
if 'escapeHtml' not in content:
    escape_fn = """
        // ===== HTML 轉義（防止 XSS） =====
        function escapeHtml(str) {
            if (str == null) return '';
            const div = document.createElement('div');
            div.textContent = str;
            return div.innerHTML;
        }

"""
    marker = '      let allUsers = [];'
    if marker in content:
        content = content.replace(marker, escape_fn + marker, 1)
        changes += 1
        print('1: escapeHtml added')
    else:
        print('1: marker not found, trying alternate')
        # Try to find loadUserTable
        idx = content.find('function loadUserTable')
        if idx > 0:
            # Insert before this function
            content = content[:idx] + escape_fn + content[idx:]
            changes += 1
            print('1: escapeHtml added before loadUserTable')

# 2. XSS fix in loadUserTable - ai-web uses string concatenation
if 'escapeHtml(user.name)' not in content:
    old_line = """      html += '<tr><td>' + (user.name || '-') + '</td><td>' + (user.email || '-') + '</td><td>' + pwDisplay + '</td><td>' + d + '</td><td><button class="delete-user-btn" onclick="window._deleteUser(\'' + key + '\',\'' + safeName + '\')"><i class="fas fa-trash"></i> 刪除</button></td></tr>';"""
    new_line = """      html += '<tr><td>' + (escapeHtml(user.name) || '-') + '</td><td>' + (escapeHtml(user.email) || '-') + '</td><td>' + escapeHtml(pwDisplay) + '</td><td>' + d + '</td><td><button class="delete-user-btn" onclick="window._deleteUser(\'' + key + '\',\'' + escapeHtml(safeName) + '\')"><i class="fas fa-trash"></i> 刪除</button></td></tr>';"""
    if old_line in content:
        content = content.replace(old_line, new_line, 1)
        changes += 1
        print('2: XSS fixed in loadUserTable')
    else:
        print('2: old line not found')
        # Try to find it
        idx = content.find('html += ')
        if idx > 0:
            end = content.find(';', idx) + 1
            print('  Found:', repr(content[idx:end][:100]))

# 3. safeName for Firebase key in register
if 'const safeName = name.replace' not in content:
    # Fix duplicate check
    old_dup = "    const snap = await db.ref('users').orderByChild('name').equalTo(name).once('value');"
    new_dup = "    const safeName = name.replace(/[.#$\\[\\]]/g, '_');\n    const snap = await db.ref('users/' + safeName).once('value');"
    if old_dup in content:
        content = content.replace(old_dup, new_dup, 1)
        changes += 1
        print('3a: duplicate check fixed')

    # Fix register write
    old_write = "    const ref = db.ref('users').push();"
    new_write = "    const ref = db.ref('users/' + safeName);"
    if old_write in content:
        content = content.replace(old_write, new_write, 1)
        changes += 1
        print('3b: register write fixed')

    # Fix uid
    old_uid = "    const ud = { name, email: '', photo: avatar, uid: ref.key, displayName: name };"
    new_uid = "    const ud = { name, email: '', photo: avatar, uid: safeName, displayName: name };"
    if old_uid in content:
        content = content.replace(old_uid, new_uid, 1)
        changes += 1
        print('3c: uid fixed')

    # Fix localStorage
    old_local = "    localStorage.setItem('_localUid', ref.key);"
    new_local = "    localStorage.setItem('_localUid', safeName);"
    if old_local in content:
        content = content.replace(old_local, new_local, 1)
        changes += 1
        print('3d: localStorage fixed')

with open(FPATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nTotal: {changes}')