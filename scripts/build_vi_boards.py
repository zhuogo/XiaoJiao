"""Four self-contained VI boards using existing, unchanged product artwork."""
from pathlib import Path
from xml.etree import ElementTree as ET
from html import escape
import hashlib
import io
import json
import re
import zipfile

import resvg_py
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'frontend/public/logos/go/v2'
OUT = ROOT / 'frontend/public/logos/vi'
OUT.mkdir(parents=True, exist_ok=True)
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
W, H = 2400, 3400
BRANDS = [
    dict(id='draftgo', name='DraftGo', role='开发底座', line='让创造，有自己的运行空间。', desc='轨道连接模块，承托从想法到系统的每一次搭建。', colors=['#244DE0','#EE9853','#F1F5FF','#E9EEFA'], dark='#172B61', action='创建工作空间', ui=['工作空间','应用容器','开发环境'], title='从一个想法开始', text='把代码与工具，放进自己的空间。'),
    dict(id='routergo', name='RouterGo', role='模型连接', line='一个入口，连接更多可能。', desc='暖红线路从同一个入口分流，连接不同模型与服务。', colors=['#B94332','#F08D70','#FFF6EE','#F6EAE3'], dark='#351F1B', action='配置模型连接', ui=['模型连接','路由配置','API 密钥'], title='让连接更直接', text='在一个入口，管理你的模型服务。'),
    dict(id='selfgo', name='SelfGo', role='思考画布', line='把思绪，一页页收好。', desc='松绿画布在小角身后叠起，容纳笔记、闪念与思考。', colors=['#265B4C','#80A68C','#F1F3E7','#E6EDE3'], dark='#193E33', action='写下一个想法', ui=['我的画布','日常笔记','灵感收藏'], title='给想法一个位置', text='记录此刻，也为下一次灵感留白。'),
    dict(id='benchgo', name='BenchGo', role='全天候助手', line='想法就绪，随时开工。', desc='暖米白的小角保留编辑器标签与光标，陪伴办公与开发。', colors=['#222222','#D44A36','#F3EBDF','#E8EAE5'], dark='#222222', action='开始新的对话', ui=['对话','本地文件','开发任务'], title='今天，一起做点什么', text='整理文件、梳理思路，或开始一段代码。'),
]


class Board:
    def __init__(self, brand):
        self.b = brand
        self.parts = []
        self.n = 0

    def rect(self, x, y, w, h, color, radius=0, stroke=None):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{color}"' + (f' stroke="{stroke}" stroke-width="2" stroke-dasharray="10 10"' if stroke else '') + '/>')

    def text(self, x, y, text, size=28, color='#252C29', weight=400):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(text)}</text>')

    def art(self, variant, x, y, w, h, reverse=False):
        self.n += 1
        source = ET.fromstring((SOURCE / f'{self.b["id"]}-{variant}.svg').read_text(encoding='utf-8'))
        prefix = f'art-{self.n}-'
        for el in source.iter():
            if 'id' in el.attrib:
                el.set('id', prefix + el.get('id'))
            for key, value in list(el.attrib.items()):
                value = re.sub(r'url\(#([^)]*)\)', lambda m: 'url(#' + prefix + m[1] + ')', value)
                if key.endswith('href') and value.startswith('#'):
                    value = '#' + prefix + value[1:]
                # Monochrome files use #242725 for the artwork; masks must remain unchanged.
                if reverse and value.lower() in {'#242725', '#222222', '#222822'} and key in {'fill', 'stroke'}:
                    value = '#FFFFFF'
                el.set(key, value)
        source.set('x', str(x)); source.set('y', str(y))
        source.set('width', str(w)); source.set('height', str(h))
        source.set('preserveAspectRatio', 'xMidYMid meet')
        self.parts.append(ET.tostring(source, encoding='unicode'))

    def small(self, size, x, y):
        # Raster micro-icons preserve the actual production pixels.
        import base64
        data = base64.b64encode((SOURCE / f'{self.b["id"]}-icon-{size}.png').read_bytes()).decode()
        self.parts.append(f'<image x="{x}" y="{y}" width="{size}" height="{size}" href="data:image/png;base64,{data}"/>')

    def build(self):
        b = self.b
        c, accent, paper, bg = b['colors']
        dark = b['dark']
        self.rect(0,0,W,H,'#F8FAF7')
        self.rect(0,0,W,900,bg)
        self.text(100,145,b['name'],110,c,600)
        self.text(105,210,b['role'] + ' / 卓越构建',30,dark)
        self.text(105,365,b['line'],49,dark,600)
        self.text(105,430,b['desc'],25,dark)
        self.text(105,780,b['id'] + '.cn',28,dark)
        self.text(105,833,'Visual identity · 品牌视觉识别',24,dark)
        self.art('mark',1070,70,1250,770)
        # Identity system: three complementary formats.
        self.text(100,1000,'标识系统',44,dark,600)
        self.text(1850,998,'共同基准，不同性格。',24,dark)
        self.rect(100,1040,1040,440,'#FFFFFF')
        self.art('mark',120,1050,400,290)
        self.text(520,1230,b['name'],80,c,600)
        self.text(145,1435,'横向组合 · 图形与字标保持独立',24,dark)
        self.rect(1180,1040,540,440,bg)
        self.art('app',1280,1065,340,310)
        self.text(1220,1435,'应用图标',24,dark)
        self.rect(1760,1040,540,220,'#E9ECE8')
        self.rect(1760,1260,540,220,dark)
        self.art('mono',1810,1038,440,220)
        self.art('mono',1810,1260,440,220,reverse=True)
        # Core colour system.
        self.text(100,1590,'品牌色',44,dark,600)
        for i, (color, label) in enumerate(zip(b['colors'],['主色 / 文字','强调色','角色 / 浅色','场景底色'])):
            x = 100 + i * 560
            self.rect(x,1630,520,150,color)
            self.text(x,1825,label,25,dark)
            self.text(x,1870,color,30,dark,600)
            rgb = ' · '.join(str(int(color[n:n+2],16)) for n in (1,3,5))
            self.text(x,1910,'RGB ' + rgb,22,dark)
        # Typography and clear-space guidance.
        self.text(100,2025,'字体与层级',44,dark,600)
        self.text(100,2100,'Aa  ' + b['name'],63,c,600)
        self.text(100,2160,'Segoe UI / Semibold · Regular',27,dark)
        self.text(100,2225,'让想法，有自己的样子。',43,dark,600)
        self.text(100,2280,'微软雅黑 / 标题 32–48 · 正文 16 · 辅助 14 px',24,dark)
        self.text(100,2330,'建议组合；系统字体不随资产包分发。',22,dark)
        self.text(1250,2025,'空间与尺寸',44,dark,600)
        self.rect(1250,2060,440,260,'none',stroke='#8A948D')
        self.art('mono',1300,2090,340,200)
        self.text(1740,2105,'建议净空 ≥ 图形宽度的 1/8',25,dark)
        self.text(1740,2155,'保持比例，不裁切、不变形。',24,dark)
        self.text(1740,2200,'小尺寸使用专用文件。',24,dark)
        for i, size in enumerate([16,32,48,64]):
            x = 1740 + i * 135
            self.small(size,x,2240 + 64-size)
            self.text(x,2340,str(size) + ' px',20,dark)
        self.text(1250,2380,'净空与字号为本轮使用建议；屏幕 RGB 展示稿。',21,dark)
        # Real content, explicitly proposed product UI and print applications.
        self.text(100,2500,'品牌应用',44,dark,600)
        self.text(1840,2495,'界面与物料均为应用示意',22,dark)
        self.rect(100,2540,1390,650,'#FFFFFF')
        self.rect(100,2540,300,650,bg)
        self.text(140,2615,b['name'],38,c,600)
        for i, label in enumerate(b['ui']):
            if i == 0:
                self.rect(125,2670,250,62,c,8)
            self.text(150,2710+i*95,label,24,'#FFFFFF' if i == 0 else dark)
        self.text(460,2645,b['title'],41,dark,600)
        self.text(460,2700,b['text'],24,dark)
        self.art('mark',730,2710,550,330)
        self.rect(470,3070,300,65,c,8)
        self.text(500,3113,b['action'],25,'#FFFFFF')
        self.text(1010,3135,'产品欢迎页示意',21,dark)
        self.rect(1530,2540,770,300,c)
        self.art('mono',1545,2570,300,210,reverse=True)
        self.text(1850,2675,b['name'],45,'#FFFFFF',600)
        self.text(1850,2735,b['id']+'.cn',25,'#FFFFFF')
        self.rect(1530,2880,770,310,bg)
        self.art('app',1580,2920,220,220)
        self.text(1850,2990,b['name'],44,c,600)
        self.text(1850,3050,b['role'],28,dark)
        self.text(1850,3120,'启动页 / 名片应用示意',22,dark)
        self.text(100,3320,'XiaoJiao · ' + b['name'] + ' 品牌视觉识别',26,dark)
        self.text(1550,3320,'标准双眼 / 原有轮廓 / 标志性切角',24,dark)
        return f'<svg xmlns="{NS}" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><title>{b["name"]} 完整 VI 展板</title>' + ''.join(self.parts) + '</svg>'


def main():
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCE.glob('*') if p.is_file()}
    manifest, images = [], []
    for brand in BRANDS:
        stem = brand['id'] + '-vi'
        svg = Board(brand).build()
        doc = ET.fromstring(svg)
        ids = [e.get('id') for e in doc.iter() if e.get('id')]
        assert len(ids) == len(set(ids))
        (OUT / (stem+'.svg')).write_text(svg,encoding='utf-8')
        png = bytes(resvg_py.svg_to_bytes(svg_string=svg))
        (OUT / (stem+'.png')).write_bytes(png)
        image = Image.open(io.BytesIO(png)).convert('RGB')
        assert image.size == (W,H)
        image.save(OUT / (stem+'.pdf'),'PDF',resolution=150)
        preview = image.copy(); preview.thumbnail((900,1275))
        preview.save(OUT / (stem+'-preview.jpg'), quality=88, optimize=True)
        images.append(image)
        with zipfile.ZipFile(OUT / (stem+'.zip'),'w',zipfile.ZIP_DEFLATED) as z:
            for ext in ['svg','png','pdf']:
                z.write(OUT / (stem+'.'+ext),stem+'.'+ext)
        manifest.append(dict(id=brand['id'],name=brand['name']+' · 完整 VI 展板',stem=stem,width=W,height=H))
    images[0].save(OUT/'go-family-vi.pdf','PDF',save_all=True,append_images=images[1:],resolution=150)
    (OUT/'catalog.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'README.md').write_text('# 小角四产品 VI\n\n四张 2400 × 3400 px 展板，沿用现有图标。\n\nSVG 内嵌矢量图形与微型 PNG 图标，文字可编辑；需安装 Segoe UI 与微软雅黑。PNG 固化外观，PDF 为 150 dpi 栅格嵌入。屏幕 RGB 展示，不是印刷打样。\n\n横向组合、字体层级、净空为本轮建议；产品界面和物料均为应用示意。原标识文件未修改。\n\n重新生成：python scripts/build_vi_boards.py\n',encoding='utf-8')
    with zipfile.ZipFile(OUT/'go-family-vi.zip','w',zipfile.ZIP_DEFLATED) as z:
        board_files = ['README.md', 'catalog.json', 'go-family-vi.pdf']
        board_files += [b['id'] + '-vi' + suffix for b in BRANDS for suffix in ['.svg', '.png', '.pdf', '-preview.jpg']]
        for filename in board_files:
            z.write(OUT / filename, filename)
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == sha for p,sha in before.items())
    print('Built four VI boards; SVG IDs, dimensions and source preservation verified.')


if __name__ == '__main__':
    main()
