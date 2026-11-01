"""Original vector brand studies based on XiaoJiao's 600 x 380 geometry."""
from pathlib import Path
import json
import resvg_py

ROOT = Path(__file__).resolve().parents[1] / 'frontend/public/logos'
ROOT.mkdir(parents=True, exist_ok=True)
DESIGNS = [
    dict(id='terracotta', name='赤陶原点', english='TERRA', category='生活方式 / 创意品牌', background='#E9D8C4', body='#F9F2E8', corner='#C84630', eyes='#422D25', light='#F8EDDB', dark='#C7A587', mood='温润、有分量，保留小角最本真的亲切。', kind='plain'),
    dict(id='mint', name='薄荷信笺', english='MINT', category='笔记 / 效率工具', background='#123D35', body='#D9F5D6', corner='#6DAF80', eyes='#173E33', light='#397965', dark='#092B26', mood='深绿与嫩芽色，让记录成为安静的日常。', kind='plain'),
    dict(id='aurora', name='午夜极光', english='AURA', category='AI / 数字产品', background='#15172F', body='#E4E3FF', corner='#8279E8', eyes='#302F61', light='#464B89', dark='#0C1027', mood='冷静的紫，藏着一点来自未来的光。', kind='plain'),
    dict(id='sunny', name='日光俱乐部', english='SUNNY', category='社区 / 灵感产品', background='#F5BE45', body='#FFF4CD', corner='#EA732E', eyes='#78401E', light='#FFE7A0', dark='#DD8F24', mood='像一个好天气，把轻快放进每次打开。', kind='plain'),
    dict(id='berry', name='莓果电台', english='BERRY', category='音乐 / 社交产品', background='#662F4B', body='#FFDCE6', corner='#D95F85', eyes='#692B4A', light='#AD5976', dark='#40243E', mood='柔软的粉与浓郁莓色，亲密而不甜腻。', kind='plain'),
    dict(id='mono', name='墨白之间', english='MONO', category='设计 / 专业工具', background='#DDDCD5', body='#272A28', corner='#8C9589', eyes='#F3F1E8', light='#F5F4ED', dark='#B4B7AE', mood='去掉多余的声音，让轮廓自己说话。', kind='plain'),
]
BODY='M95 0H505A95 95 0 0 1 600 95V285A95 95 0 0 1 505 380H95A95 95 0 0 1 0 285V95A95 95 0 0 1 95 0Z'
CORNER='M410 380H505A95 95 0 0 0 600 285V190Z'

def make(d, icon=False):
    defs=f'''<linearGradient id="body" x1="0" y1="0" x2=".65" y2="1"><stop stop-color="{d['body']}"/><stop offset="1" stop-color="{d['body']}"/></linearGradient>
    <radialGradient id="bg" cx=".25" cy=".05" r="1.15"><stop stop-color="{d['light']}"/><stop offset=".53" stop-color="{d['background']}"/><stop offset="1" stop-color="{d['dark']}"/></radialGradient>
    <linearGradient id="fold" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{d['corner']}"/><stop offset="1" stop-color="{d['corner']}"/></linearGradient>
    <filter id="shadow" x="-30%" y="-40%" width="160%" height="200%"><feDropShadow dx="0" dy="19" stdDeviation="16" flood-color="{d['dark']}" flood-opacity=".25"/><feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#000" flood-opacity=".1"/></filter>'''
    eyes='<rect x="123" y="125" width="90" height="130" rx="45"/><rect x="261" y="125" width="90" height="130" rx="45"/>'
    opening='<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">' if icon else '<svg xmlns="http://www.w3.org/2000/svg" width="780" height="560" viewBox="0 0 780 560">'
    bg='<rect width="1024" height="1024" rx="224" fill="url(#bg)"/>' if icon else ''
    transform='translate(140 276) scale(1.24)' if icon else 'translate(90 90)'
    return opening+f'<title>小角 · {d["name"]}</title><defs>{defs}</defs>'+bg+f'<g transform="{transform}"><path d="{BODY}" fill="url(#body)"'+(' filter="url(#shadow)"' if icon else '')+f'/><path d="{CORNER}" fill="url(#fold)"/><g fill="{d["eyes"]}">{eyes}</g></g></svg>'

for design in DESIGNS:
    for variant in ('mark','icon'):
        svg=make(design, variant=='icon')
        (ROOT/f'{design["id"]}-{variant}.svg').write_text(svg,encoding='utf-8')
        (ROOT/f'{design["id"]}-{variant}.png').write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=svg)))
(ROOT/'collection.json').write_text(json.dumps(DESIGNS,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Created {len(DESIGNS)} logo families in {ROOT}')
