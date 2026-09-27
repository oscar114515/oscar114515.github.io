#!/usr/bin/env python3
"""Regenerate all language dirs from zh with T2S, then apply EN dict to en"""
import os, re

BASE = r'C:\Users\Administrator\WorkBuddy\2026-09-04-21-32-11\repo'

T2S = {
    '聯':'联','繫':'系','彈':'弹','驭':'驭','證':'证','導':'导','欄':'栏',
    '無':'无','紅':'红','畫':'画','頁':'页','聖':'圣','誕':'诞','勢':'势',
    '陸':'陆','鈕':'钮','車':'车','資':'资','訊':'讯','數':'数','繪':'绘',
    '庫':'库','簡':'简','網':'网','總':'总','關':'关','開':'开','門':'门',
    '電':'电','話':'话','視':'视','聽':'听','員':'员','師':'师',
    '經':'经','結':'结','鐵':'铁','臨':'临','屬':'属','術':'术',
    '衛':'卫','運':'运','遠':'远','進':'进','退':'退',
    '應':'应','備':'备','營':'营','銷':'销',
    '廠':'厂','場':'场','適':'适','貴':'贵','貨':'货','費':'费',
    '貼':'贴','買':'买','賣':'卖','贊':'赞','贈':'赠',
    '購':'购','銷':'销','錢':'钱','銀':'银','鏡':'镜',
    '顯':'显','隱':'隐','願':'愿',
    '團':'团','體':'体','議':'议',
    '護':'护','計':'计','記':'记','紀':'纪','訪':'访',
    '評':'评','訴':'诉',
    '讀':'读',
    '輸':'输','輪':'轮','傳':'传',
    '編':'编','樣':'样',
    '極':'极','樓':'楼','樹':'树','歡':'欢','權':'权',
    '廳':'厅','廣':'广','條':'条',
    '親':'亲','邊':'边','裏':'里','為':'为',
    '舊':'旧','醫':'医','藥':'药',
}

def t2s(text):
    for k, v in T2S.items():
        text = text.replace(k, v)
    return text

def apply_dict(content, dictionary):
    for k in sorted(dictionary.keys(), key=len, reverse=True):
        content = content.replace(k, dictionary[k])
    return content

# Step 1: Regenerate all from zh with T2S
for lang in ['cn', 'en', 'ko', 'ja']:
    src = os.path.join(BASE, 'zh')
    dst = os.path.join(BASE, lang)
    for f in sorted(os.listdir(src)):
        if not f.endswith('.html') and f != 'lang-switch.js':
            continue
        spath = os.path.join(src, f)
        dpath = os.path.join(dst, f)
        with open(spath, 'r', encoding='utf-8') as fh:
            content = fh.read()
        content = t2s(content)
        content = content.replace('zh-CN', lang).replace('zh-TW', lang).replace('zh', lang)
        with open(dpath, 'w', encoding='utf-8') as fh:
            fh.write(content)
    print(f'{lang} regenerated with T2S')

# Step 2: Count
for lang in ['cn', 'en', 'ko', 'ja']:
    total = 0
    lang_dir = os.path.join(BASE, lang)
    for f in sorted(os.listdir(lang_dir)):
        if not f.endswith('.html') and f != 'lang-switch.js':
            continue
        with open(os.path.join(lang_dir, f), 'r', encoding='utf-8') as fh:
            total += len(re.findall(r'[\u4e00-\u9fff\uf900-\ufaff]', fh.read()))
    print(f'  {lang}: {total} Chinese chars')
print('Done!')