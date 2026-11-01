"""Build complete digital VI delivery packages, without modifying approved artwork.

Run after build_vi_boards.py. Uses existing Pillow/resvg dependencies only.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET
import hashlib
import json
import shutil
import zipfile

from PIL import Image, ImageFont
import resvg_py
from build_vi_boards import BRANDS, Board, SOURCE, OUT, NS

VERSION = '1.0'
FOLDERS = ['00-使用说明', '01-品牌规范', '02-品牌标识', '03-应用图标', '04-色彩与字体', '05-辅助视觉', '06-应用模板', '07-源文件']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contrast(a, b):
    def light(color):
        values = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
        return sum((v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4) * w for v, w in zip(values, [.2126, .7152, .0722]))
    x, y = sorted([light(a), light(b)])
    return (y + .05) / (x + .05)


class Canvas(Board):
    def art(self, variant, x, y, w, h, reverse=False):
        super().art(variant, x, y, w, h, reverse)
        # Fit the actual image rather than the presentation canvas's large margins.
        node = ET.fromstring(self.parts[-1])
        with Image.open(SOURCE / f'{self.b["id"]}-{variant}.png') as image:
            box = image.convert('RGBA').getchannel('A').getbbox()
            if box:
                vb = [float(v) for v in node.get('viewBox').split()]
                sx, sy = vb[2] / image.width, vb[3] / image.height
                node.set('viewBox', f'{box[0]*sx} {box[1]*sy} {(box[2]-box[0])*sx} {(box[3]-box[1])*sy}')
        self.parts[-1] = ET.tostring(node, encoding='unicode')

    def paragraph(self, x, y, value, width=1000, size=24, color='#252C29'):
        font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', size)
        line = ''
        for char in value:
            if char == '\n' or font.getlength(line + char) > width:
                self.text(x, y, line, size, color)
                y += size * 1.65
                line = ''
            if char != '\n':
                line += char
        if line:
            self.text(x, y, line, size, color)
            y += size * 1.65
        return y

    def svg(self, width, height, title):
        from html import escape
        return f'<svg xmlns="{NS}" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><title>{escape(title)}</title>' + ''.join(self.parts) + '</svg>'


def save_pair(folder, stem, canvas, width, height):
    folder.mkdir(parents=True, exist_ok=True)
    svg = canvas.svg(width, height, stem)
    (folder / (stem + '.svg')).write_text(svg, encoding='utf-8')
    (folder / (stem + '.png')).write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=svg)))


def colored(brand, variant):
    return brand['colors'][0] if variant == 'color' else '#242725' if variant == 'mono' else '#FFFFFF'


def lockups(brand, folder):
    for variant in ['color', 'mono', 'reverse']:
        ink = colored(brand, variant)
        for form, width, height in [('symbol', 840, 760), ('horizontal', 1440, 480), ('vertical', 840, 960), ('wordmark', 1100, 260)]:
            c = Canvas(brand)
            if form == 'symbol':
                # Copy the approved source without changing its canvas or geometry.
                if variant != 'reverse':
                    source = 'mark' if variant == 'color' else 'mono'
                    for ext in ['svg', 'png']:
                        shutil.copyfile(SOURCE / f'{brand["id"]}-{source}.{ext}', folder / f'{form}-{variant}.{ext}')
                    continue
                Board.art(c, 'mono', 0, 0, 840, 760, reverse=True)
            elif form == 'horizontal':
                c.art('mark' if variant == 'color' else 'mono', 60, 70, 480, 340, reverse=variant == 'reverse')
                c.text(610, 285, brand['name'], 140, ink, 600)
            elif form == 'vertical':
                c.art('mark' if variant == 'color' else 'mono', 90, 80, 660, 550, reverse=variant == 'reverse')
                c.text(420, 810, brand['name'], 125, ink, 600)
                c.parts[-1] = c.parts[-1].replace('<text ', '<text text-anchor="middle" ', 1)
            else:
                c.text(550, 177, brand['name'], 160, ink, 600)
                c.parts[-1] = c.parts[-1].replace('<text ', '<text text-anchor="middle" ', 1)
            save_pair(folder, form + '-' + variant, c, width, height)


def tokens(brand, folder):
    primary, accent, paper, bg = brand['colors']
    colors = dict(primary=primary, accent=accent, paper=paper, surface=bg, ink=brand['dark'], onPrimary='#FFFFFF')
    pairs = [(key, foreground, background) for key, foreground, background in [('body',brand['dark'],bg), ('button','#FFFFFF',primary), ('accent-text',accent,bg)]]
    measures = {name: dict(ratio=round(contrast(fg, back),2), normalTextAA=contrast(fg,back)>=4.5, foreground=fg, background=back) for name, fg, back in pairs}
    value = dict(brand=brand['name'], signature='卓越构建', version=VERSION, status='New layouts and usage rules pending owner approval', colorSpace='sRGB', colors=colors,
                 typography=dict(family='"Segoe UI", "Microsoft YaHei", system-ui, sans-serif', display=dict(size=48,lineHeight=1.2,weight=600), heading=dict(size=32,lineHeight=1.3,weight=600), body=dict(size=16,lineHeight=1.6,weight=400), caption=dict(size=14,lineHeight=1.5,weight=400)), contrast=measures)
    (folder/'design-tokens.json').write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
    css = ':root {\n' + ''.join(f'  --{brand["id"]}-{key}: {color};\n' for key,color in colors.items())
    css += f'  --{brand["id"]}-font: "Segoe UI", "Microsoft YaHei", system-ui, sans-serif;\n'
    for name, spec in value['typography'].items():
        if isinstance(spec, dict):
            css += f'  --{brand["id"]}-{name}-size: {spec["size"]}px;\n  --{brand["id"]}-{name}-line-height: {spec["lineHeight"]};\n  --{brand["id"]}-{name}-weight: {spec["weight"]};\n'
    (folder/'variables.css').write_text(css+'}\n',encoding='utf-8')
    lines = [f'# {brand["name"]} 色彩与字体', '', '颜色为 sRGB；RGB 数值由 HEX 直接换算。不包含 CMYK/Pantone。', '']
    for name, color in colors.items():
        lines.append(f'- {name}: {color} / RGB ' + ', '.join(str(int(color[i:i+2],16)) for i in (1,3,5)))
    lines += ['', '## 文本对比度', '普通文字 AA 以 4.5:1 为下限。强调色只作图形点缀，除非对应背景通过检测。']
    for name, spec in measures.items():
        lines.append(f'- {name}: {spec["ratio"]}:1 / 普通文字 AA：{spec["normalTextAA"]}')
    lines += ['', '## 字体', '英文 Segoe UI，中文微软雅黑；不随包分发字体。系统回退字体会改变字宽。', '标题 48/32 px，正文 16 px，辅助 14 px；组合字标使用 Semibold。', '精确复现 SVG 前请安装合法字体，或在有授权的设计软件内转曲。现有 PNG 已固化外观。']
    (folder/'色彩与字体.md').write_text('\n'.join(lines),encoding='utf-8')
    return value


def icons(brand, folder):
    id = brand['id']
    for variant in ['app']:
        for ext in ['svg','png']:
            shutil.copyfile(SOURCE/f'{id}-{variant}.{ext}',folder/f'{variant}.{ext}')
    for size in [16,32,48,64,180,192,512]:
        shutil.copyfile(SOURCE/f'{id}-icon-{size}.png',folder/f'icon-{size}.png')
    for ext in ['svg','png','ico']:
        shutil.copyfile(SOURCE/f'{id}-favicon.{ext}',folder/f'favicon.{ext}')
    shutil.copyfile(SOURCE/f'{id}-icon-180.png',folder/'apple-touch-icon.png')
    # The entire symbol fits inside the central safe circle (radius 40% of width).
    c = Canvas(brand); c.rect(0,0,512,512,brand['colors'][3]); c.art('mark',128,128,256,256)
    save_pair(folder,'maskable-512',c,512,512)
    data = dict(name=brand['name'],short_name=brand['name'],id='./',start_url='./',scope='./',display='standalone',background_color=brand['colors'][3],theme_color=brand['colors'][0],icons=[dict(src=f'icon-{s}.png',sizes=f'{s}x{s}',type='image/png',purpose='any') for s in [192,512]]+[dict(src='maskable-512.png',sizes='512x512',type='image/png',purpose='maskable')])
    (folder/'site.webmanifest').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    (folder/'接入示例.html').write_text('''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>图标接入示例</title>
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon.ico" sizes="any"><link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="manifest" href="site.webmanifest"></head>
<body><h1>图标接入示例</h1><p>将此目录文件放在实际站点资源目录，并调整 manifest 的 id、start_url、scope 和图标路径。本示例不包含 Service Worker，也不承诺离线可用或商店上架合规。</p><img src="icon-192.png" alt="应用图标" width="192" height="192"></body></html>''',encoding='utf-8')


def templates(brand, folder, auxiliary):
    primary, accent, paper, bg = brand['colors']; dark = brand['dark']
    specs = [('avatar',1024,1024),('social-share',1200,630),('presentation-cover',1920,1080),('welcome-screen',1440,900),('business-card-front',1050,600),('business-card-back',1050,600)]
    for name,w,h in specs:
        c = Canvas(brand); c.rect(0,0,w,h,bg)
        if name == 'avatar':
            c.art('mark',160,160,704,704)
        elif name == 'social-share':
            c.text(64,120,brand['name'],72,primary,600); c.text(68,180,'卓越构建 · '+brand['role'],24,dark)
            c.paragraph(68,310,brand['line'],width=510,size=36,color=dark)
            c.art('mark',650,130,490,350); c.text(68,555,brand['id']+'.cn',24,dark)
        elif name == 'presentation-cover':
            c.text(100,160,brand['name'],100,primary,600); c.text(105,235,'卓越构建',32,dark)
            c.paragraph(100,490,brand['line'],width=840,size=64,color=dark)
            c.text(100,680,'演示主题 / 请替换',32,dark)
            c.text(100,980,brand['id']+'.cn',30,dark); c.art('mark',1050,230,770,590)
        elif name == 'welcome-screen':
            c.text(70,110,brand['name'],52,primary,600)
            c.art('mark',540,185,360,270)
            c.text(720,550,brand['title'],48,dark,600); c.parts[-1]=c.parts[-1].replace('<text ','<text text-anchor="middle" ',1)
            c.text(720,620,brand['text'],26,dark); c.parts[-1]=c.parts[-1].replace('<text ','<text text-anchor="middle" ',1)
            c.rect(520,690,400,76,primary,8); c.text(720,740,brand['action'],28,'#FFFFFF',600); c.parts[-1]=c.parts[-1].replace('<text ','<text text-anchor="middle" ',1)
            c.text(70,845,'卓越构建 · 欢迎页视觉模板，不含功能实现',22,dark)
        elif name == 'business-card-front':
            c.rect(0,0,w,h,primary); c.art('mono',80,120,350,300,reverse=True)
            c.text(500,260,brand['name'],65,'#FFFFFF',600); c.text(505,330,'卓越构建',28,'#FFFFFF'); c.text(505,460,brand['id']+'.cn',27,'#FFFFFF')
        else:
            c.text(70,110,brand['name'],48,primary,600); c.text(70,270,'姓名 / 请替换',38,dark,600)
            c.text(70,335,'职位 / 请替换',27,dark); c.text(70,430,'邮箱 / 请替换',27,dark); c.text(70,490,'联系方式 / 请替换',27,dark)
            c.art('mark',670,190,300,240)
        save_pair(folder,name,c,w,h)
    c=Canvas(brand); c.rect(0,0,1600,900,bg)
    for row in range(3):
        for col in range(5):
            c.art('mark',40+col*320,30+row*300,230,220)
    save_pair(auxiliary,'brand-pattern',c,1600,900)
    c=Canvas(brand); c.rect(0,0,1600,400,primary)
    c.art('mono',70,65,350,270,reverse=True); c.text(500,195,brand['name'],100,'#FFFFFF',600); c.text(505,275,'卓越构建',32,'#FFFFFF')
    save_pair(auxiliary,'brand-banner',c,1600,400)
    (folder/'模板说明.md').write_text('''# 模板使用

所有 SVG 可编辑，PNG 可直接使用。文字使用系统字体，未转曲；模板中的“请替换”是明确的编辑字段，发布前必须替换。

- avatar：1024×1024，圆形/方形头像均保留核心图形。
- social-share：1200×630，网页 Open Graph 分享图，发布前检查标题和链接。
- presentation-cover：1920×1080，演示封面，替换主题文字。
- welcome-screen：1440×900，产品欢迎页视觉示意，不提供按钮逻辑或真实产品功能。
- business-card-front/back：1050×600，约 1.75:1 比例，仅 RGB 数字示意，无出血、无裁切线；打印前需设计师重新设定成品尺寸、出血、CMYK 配置和字体转曲。

辅助纹样来自原品牌标志，仅用于背景，不替代主标识。全部模板需要结合实际用途验收，不表示界面已经上线。
''',encoding='utf-8')


def manual(brand, folder, token):
    primary, accent, paper, bg=brand['colors']; dark=brand['dark']
    titles=['品牌识别','标识与背景','空间与正确使用','色彩与字体','平台图标与辅助视觉','应用与交付说明']
    pages=[]
    for page,title in enumerate(titles):
        c=Canvas(brand); c.rect(0,0,1200,1600,'#F8FAF7')
        c.text(70,95,brand['name']+' / 卓越构建',30,primary,600)
        c.text(70,200,title,58,dark,600)
        if page==0:
            c.rect(70,260,1060,680,bg); c.art('mark',200,320,800,520)
            c.text(70,1040,brand['role'],42,dark,600)
            y=c.paragraph(70,1120,brand['line']+'\n'+brand['desc'],size=32,color=dark)
            c.paragraph(70,y+50,'沿用现有图标。标准双眼、原有轮廓与标志性切角不可擅自修改。本手册新增组合、净空、字号和应用模板为本轮建议，待品牌方验收。',size=25,color=dark)
        elif page==1:
            for idx,(variant,label,color,rev) in enumerate([('mark','彩色 / 推荐浅色背景',bg,False),('mono','单色 / 印记与简洁界面','#E9ECE8',False),('mono','反白 / 深色背景',dark,True)]):
                y=275+idx*290; c.rect(70,y,460,245,color); c.art(variant,120,y+25,350,190,reverse=rev)
                c.text(580,y+90,label,28,dark,600)
            c.paragraph(70,1220,'02-品牌标识提供独立图形、横向、纵向及文字标志，各含彩色、单色、反白三套 SVG/PNG。反白文件透明底，必须放在深色背景。禁止用截图代替源标识。',size=27,color=dark)
            c.paragraph(70,1390,'图形为既有资产；组合字标使用 Segoe UI Semibold，保留可编辑文字。',size=24,color=dark)
        elif page==2:
            # Exact diagram: W=640, margin x=W/8=80, visible image inside 640x400 box.
            c.rect(70,280,800,560,'none',stroke='#7F8A83'); c.rect(150,360,640,400,'none',stroke='#B2B9B4')
            c.art('mono',150,360,640,400); c.text(900,430,'x = W / 8',25,dark); c.text(900,480,'四周净空',25,dark)
            c.paragraph(70,920,'净空按完整图形可见宽度 W 计算，不含 SVG 画布空白；推荐四周至少 W/8。横向组合可见宽度建议不小于 160 px；独立复杂图形建议不小于 64 px。更小尺寸改用专用微型图标，并在实际屏幕检查。',size=25,color=dark)
            for i,label in enumerate(['禁止非等比拉伸','禁止旋转主标识','禁止低对比背景']):
                x=70+i*365; c.rect(x,1150,330,220,primary if i==2 else bg)
                if i==0:
                    c.art('mono',x+30,1190,270,130); c.parts[-1]=c.parts[-1].replace('preserveAspectRatio="xMidYMid meet"','preserveAspectRatio="none"')
                elif i==1:
                    c.parts.append(f'<g transform="rotate(22 {x+165} 1260)">'); c.art('mono',x+65,1195,200,130); c.parts.append('</g>')
                else:
                    c.art('mono',x+65,1195,200,130); c.parts[-1]=c.parts[-1].replace('#242725',primary).replace('#222822',primary)
                c.text(x,1425,label,24,dark,600)
        elif page==3:
            for i,(color,label) in enumerate(zip(brand['colors'],['主色','强调色','角色浅色','场景底色'])):
                x=70+i*270; c.rect(x,280,250,180,color); c.text(x,510,label,26,dark,600); c.text(x,555,color,26,dark)
                rgb='/'.join(str(int(color[n:n+2],16)) for n in (1,3,5)); c.text(x,600,'RGB '+rgb,21,dark)
            c.text(70,720,'Segoe UI / 微软雅黑',44,dark,600)
            for i,(label,size) in enumerate([('展示标题 48 px',48),('章节标题 32 px',32),('正文 16 px · 行高 1.6',26),('辅助说明 14 px · 行高 1.5',24)]):
                c.text(70,810+i*95,label,size,dark)
            y=1230
            for name,spec in token['contrast'].items():
                c.text(70,y,f'{name}: {spec["ratio"]}:1 / 普通文字 AA ' + ('通过' if spec['normalTextAA'] else '不通过，仅作图形点缀'),25,dark); y+=48
            c.paragraph(70,1440,'数值按 sRGB 计算；无 CMYK/Pantone 承诺。字体授权和安装说明见 00-使用说明。',size=23,color=dark)
        elif page==4:
            c.art('app',80,280,420,420)
            c.text(580,330,'优先复用平台专用文件',32,dark,600)
            c.paragraph(580,395,'16 / 32 / 48 / 64 px：微型图标\n180 px：Apple Touch\n192 / 512 px：Web / PWA\nSVG / ICO：浏览器 favicon',width=500,size=27,color=dark)
            for i,size in enumerate([16,32,48,64]):
                c.small(size,600+i*125,650-size); c.text(600+i*125,700,str(size)+' px',22,dark)
            c.rect(70,800,450,450,bg); c.art('mark',182.5,912.5,225,225)
            c.parts.append('<circle cx="295" cy="1025" r="180" fill="none" stroke="#7F8A83" stroke-width="2" stroke-dasharray="10 10"/>')
            c.paragraph(580,870,'Maskable 图标使用不透明底色，主体保持在中心安全圆内。不要直接把带圆角的 app 图标标记为 maskable。',width=500,size=27,color=dark)
            c.paragraph(580,1070,'Web manifest 是接入示例，部署时修改路径与作用域。不包含离线逻辑或移动应用商店提交清单。',width=500,size=25,color=dark)
            c.paragraph(70,1360,'辅助纹样与品牌横幅位于 05-辅助视觉，使用同一标志衍生。它们用于背景与展示，不替代主标识，也不在主体上叠加新装饰。',size=26,color=dark)
        else:
            c.text(70,300,'独立模板，可直接编辑',34,dark,600)
            rows=[('社交头像','1024 × 1024'),('分享图','1200 × 630'),('演示封面','1920 × 1080'),('产品欢迎页','1440 × 900'),('名片正反面','1050 × 600 · RGB 示意')]
            for i,(label,dim) in enumerate(rows):
                y=390+i*90; c.text(70,y,label,29,dark); c.text(550,y,dim,27,dark)
            c.rect(70,860,1060,270,bg); c.art('mark',100,890,330,210); c.text(490,980,brand['name'],65,primary,600); c.text(495,1050,'卓越构建',30,dark)
            c.paragraph(70,1210,'发布前替换模板中的姓名、联系方式与演示主题。欢迎页与物料是视觉模板，不表示产品功能已实现。打印前另做尺寸、出血、字体及色彩管理。',size=26,color=dark)
            c.paragraph(70,1390,'SVG 为可编辑源文件；PNG 固化外观；本 PDF 是高清栅格页。完整文件索引与 SHA256 校验清单位于 00-使用说明。',size=24,color=dark)
        c.text(70,1540,f'{brand["name"]} · 数字产品 VI / v{VERSION}',21,dark); c.text(1050,1540,f'{page+1} / 6',21,dark)
        save_pair(folder,f'manual-{page+1:02d}',c,1200,1600)
        with Image.open(folder/f'manual-{page+1:02d}.png') as im:
            pages.append(im.convert('RGB'))
    target=folder/'品牌规范手册.pdf'
    pages[0].save(target,'PDF',resolution=150,save_all=True,append_images=pages[1:])
    shutil.copyfile(target,OUT/f'{brand["id"]}-vi-guidelines.pdf')


def instructions(brand, package, source_hashes):
    folder=package/FOLDERS[0]
    (folder/'README.md').write_text(f'''# {brand['name']} 完整 VI 资产交付包

版本 {VERSION} / 卓越构建 / 数字产品 RGB 交付

## 从这里开始

1. 阅读 01-品牌规范/品牌规范手册.pdf；原展板提供总览，手册补全规则。
2. 网站或文档优先选 02-品牌标识/horizontal-color.svg；只需图形选 symbol-color.svg。
3. 深色背景选 *-reverse.svg，反白透明 PNG 在白色查看器中看起来是空白，属正常情况。
4. 应用图标使用 03-应用图标；Web 接入示例可本地打开，部署时调整路径。
5. 开发使用 04-色彩与字体/design-tokens.json 或 variables.css。
6. 模板 SVG 可直接在支持 SVG 的编辑器中打开；修改文字后检查字体与排版，再输出 PNG。

## 目录

'''+'\n'.join('- '+name for name in FOLDERS)+'''

## 决策与适用范围

现有图形和配色沿用已确认文件；新增组合、字体层级、净空、模板是本轮建议，待所有者验收。正式包只含当前方案，不混入历史探索和 BenchGo 其他研究色。
所有模板均为数字示意，不是印刷就绪稿。未提供 CMYK、Pantone、出血、原生 AI/PSD/Figma 工程或移动应用商店上架认证。PDF 为高清栅格页，SVG 为矢量图形与可编辑文字，未做字体转曲。
不包含用户项目数据库、API 密钥、外部图片或字体二进制。域名来自现有品牌资产，发布前自行确认部署与链接。

## 源文件与复现

所有目录中的 SVG 均为相应可编辑源文件，不重复存放一份。07-源文件保留官方原标识和来源哈希。
在本项目根目录依次执行：
python scripts/build_vi_boards.py
python scripts/build_vi_packages.py
python scripts/build_asset_library.py
字体环境：Windows Segoe UI、微软雅黑。依赖：Python、Pillow、resvg-py。重新生成后校验和会随 PDF 元数据变化，不要求跨次构建逐字节一致。

## 校验

00-使用说明/manifest.json 列出全部交付文件（不含清单自身）的路径、字节数、SHA256；checksums.sha256 包含 manifest.json。清单不自签名，供检查传输完整性使用。
''',encoding='utf-8')
    (folder/'字体与授权说明.md').write_text('''# 字体与授权边界

- 英文：Microsoft Segoe UI，使用系统已安装的 Regular / Semibold。
- 中文：Microsoft YaHei（微软雅黑），使用系统已安装字体。
- 字体文件不随包分发，不提供 WebFont 转换文件。
- 合法安装操作系统或桌面字体，不等于拥有字体文件再分发、Web 嵌入或服务器部署许可。商用部署请按自己的使用场景核对授权。
- SVG 保留文字，未嵌入字体。没有相应字体时会回退并改变版式；PNG 与 PDF 固化构建时的外观。
- 可以在具备合法字体授权的设计环境中将字标转曲后交付；本包不宣称字体许可或品牌法律权属已审查。
- 小角图形来自项目既有资产。外部使用和授权由资产所有者决定，本文件不新增或推定开放源代码授权。

官方参考：
https://learn.microsoft.com/en-us/typography/font-list/segoe-ui
https://learn.microsoft.com/en-us/typography/font-list/microsoft-yahei
https://learn.microsoft.com/en-us/typography/fonts/font-faq
''',encoding='utf-8')
    for variant in ['mark','app','mono']:
        shutil.copyfile(SOURCE/f'{brand["id"]}-{variant}.svg',package/FOLDERS[7]/f'{brand["id"]}-{variant}-original.svg')
    (package/FOLDERS[7]/'provenance.json').write_text(json.dumps(dict(brand=brand['name'],signature='卓越构建',sourceRoot='frontend/public/logos/go/v2',sources=source_hashes,generatedBy='scripts/build_vi_packages.py',editableSources='SVG files in folders 01 through 07',status='Existing symbols retained; new usage rules and templates proposed'),ensure_ascii=False,indent=2),encoding='utf-8')


def index_package(package, brand):
    records=[]
    for path in sorted(package.rglob('*')):
        if path.is_file():
            record=dict(path=path.relative_to(package).as_posix(),bytes=path.stat().st_size,sha256=digest(path))
            if path.suffix=='.png':
                with Image.open(path) as image:
                    record['width'],record['height']=image.size
            records.append(record)
    manifest=package/FOLDERS[0]/'manifest.json'
    manifest.write_text(json.dumps(dict(product=brand['name'],version=VERSION,files=records),ensure_ascii=False,indent=2),encoding='utf-8')
    lines=[f'{r["sha256"]}  {r["path"]}' for r in records]+[f'{digest(manifest)}  {manifest.relative_to(package).as_posix()}']
    (package/FOLDERS[0]/'checksums.sha256').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return len(records)+2


def main():
    sources={p:digest(p) for p in SOURCE.rglob('*') if p.is_file()}
    delivery=[]
    with TemporaryDirectory(prefix='xiaojiao-vi-') as temp:
        root=Path(temp)
        for brand in BRANDS:
            package=root/(brand['name']+'-VI')
            for name in FOLDERS:
                (package/name).mkdir(parents=True)
            lockups(brand,package/FOLDERS[2])
            token=tokens(brand,package/FOLDERS[4])
            icons(brand,package/FOLDERS[3])
            templates(brand,package/FOLDERS[6],package/FOLDERS[5])
            manual(brand,package/FOLDERS[1],token)
            for ext in ['svg','png','pdf']:
                shutil.copyfile(OUT/f'{brand["id"]}-vi.{ext}',package/FOLDERS[1]/f'{brand["id"]}-vi-board.{ext}')
            hashes={p.name:sha for p,sha in sources.items() if p.parent==SOURCE and p.name.startswith(brand['id']+'-') and any(p.name==f'{brand["id"]}-{v}.{ext}' for v in ['mark','mono','app','favicon'] for ext in ['svg','png','ico'])}
            instructions(brand,package,hashes)
            count=index_package(package,brand)
            archive=OUT/f'{brand["id"]}-vi-assets.zip'
            with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
                for path in sorted(package.rglob('*')):
                    if path.is_file():
                        z.write(path,path.relative_to(root))
            delivery.append(dict(id=brand['id'],name=brand['name'],version=VERSION,files=count,bytes=archive.stat().st_size,sha256=digest(archive),bundle='/logos/vi/'+archive.name,guide=f'/logos/vi/{brand["id"]}-vi-guidelines.pdf'))
            print(f'{brand["name"]}: {count} files')
        with zipfile.ZipFile(OUT/'go-family-vi-assets.zip','w',zipfile.ZIP_DEFLATED) as z:
            for path in sorted(root.rglob('*')):
                if path.is_file():
                    z.write(path,path.relative_to(root))
    assert all(digest(p)==sha for p,sha in sources.items()), 'Original assets changed'
    (OUT/'delivery-catalog.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Four complete packages and family archive built; original assets unchanged.')


if __name__=='__main__':
    main()
