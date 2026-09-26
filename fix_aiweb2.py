# -*- coding: utf-8 -*-
"""Fix XSS in ai-web.html table line."""
FPATH = 'ai-web.html'

with open(FPATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the table line
idx = content.find("html += '<tr><td>' + (user.name")
if idx > 0:
    end = content.find(';', idx) + 1
    old = content[idx:end]
    print('Old:', repr(old[:80]))

    # Replace user.name, user.email, pwDisplay with escapeHtml versions
    new = old
    new = new.replace("(user.name || '-')", "(escapeHtml(user.name) || '-')")
    new = new.replace("(user.email || '-')", "(escapeHtml(user.email) || '-')")
    new = new.replace("+ pwDisplay +", "+ escapeHtml(pwDisplay) +")
    new = new.replace("+ safeName +'", "+ escapeHtml(safeName) +'")

    if old != new:
        content = content.replace(old, new, 1)
        with open(FPATH, 'w', encoding='utf-8') as f:
            f.write(content)
        print('SUCCESS: XSS fixed')
    else:
        print('No change needed')
else:
    print('FAILED: marker not found')
    # Try alternate
    idx2 = content.find("html += '<tr>")
    if idx2 > 0:
        end2 = content.find(';', idx2) + 1
        print('Found at', idx2, repr(content[idx2:end2][:100]))