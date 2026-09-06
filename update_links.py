content = open('C:/Users/Administrator/Desktop/oscar114515.github.io/index.html', 'r', encoding='utf-8').read()

# 在footer前添加工具链接
old_footer = '        <footer class="site-footer">\n            <p>© 2026 梁喆同学 · 用 ❤️ 制作</p>\n        </footer>'
new_footer = '''        <!-- 工具链接 -->
        <section class="tools-section">
            <h2 class="tools-title">我的工具</h2>
            <div class="tools-grid">
                <a href="/calculator.html" class="tool-link">计算器</a>
                <a href="/converter.html" class="tool-link">单位转换器</a>
                <a href="/htmlrunner.html" class="tool-link">HTML运行器</a>
                <a href="/paint.html" class="tool-link">画板</a>
                <a href="/password.html" class="tool-link">密码生成器</a>
                <a href="/qinqi.html" class="tool-link">亲戚计算器</a>
                <a href="/qr.html" class="tool-link">QR码生成器</a>
                <a href="/spinner.html" class="tool-link">抽签转盘</a>
                <a href="/timer.html" class="tool-link">秒表</a>
                <a href="/tomato.html" class="tool-link">番茄钟</a>
                <a href="/worldclock.html" class="tool-link">世界时钟</a>
                <a href="/crack.html" class="tool-link">源码抓取</a>
                <a href="/emoji.html" class="tool-link">Emoji字符画</a>
                <a href="/login.html" class="tool-link">登录按钮生成器</a>
                <a href="/mtr.html" class="tool-link">港铁实时状况</a>
                <a href="/weather.html" class="tool-link">天文台数据看板</a>
                <a href="/xmas.html" class="tool-link">圣诞树</a>
            </div>
        </section>

        <footer class="site-footer">
            <p>© 2026 梁喆同学 · 用 ❤️ 制作</p>
        </footer>'''

if old_footer in content:
    content = content.replace(old_footer, new_footer)
    print('添加工具链接成功')
else:
    print('未找到footer，尝试其他匹配')
    idx = content.find('site-footer')
    if idx != -1:
        print('找到site-footer在位置:', idx)
        print(repr(content[idx-50:idx+100]))

# 在CSS末尾添加工具链接样式
old_css_end = '        }\\n    </style>'
new_css_end = '''        }
        /* ===== 工具链接 ===== */
        .tools-section { width: 100%; max-width: 900px; margin: 40px 0; }
        .tools-title { color: rgba(255,255,255,0.8); font-size: 1.2rem; margin-bottom: 20px; text-align: center; }
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 12px;
        }
        .tool-link {
            display: block;
            padding: 12px 16px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            color: rgba(255,255,255,0.8);
            text-align: center;
            text-decoration: none;
            font-size: 0.9rem;
            transition: all 0.2s;
        }
        .tool-link:hover {
            background: rgba(255,107,53,0.15);
            border-color: rgba(255,107,53,0.4);
            color: #ffb347;
            transform: translateY(-2px);
        }
    </style>'''

if old_css_end in content:
    content = content.replace(old_css_end, new_css_end)
    print('添加CSS样式成功')
else:
    print('未找到CSS结束位置')

open('C:/Users/Administrator/Desktop/oscar114515.github.io/index.html', 'w', encoding='utf-8').write(content)
print('完成')
