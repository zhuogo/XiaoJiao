"""生成正式完整交付。"""
from pathlib import Path
from copy import deepcopy
from io import BytesIO
import json
import xml.etree.ElementTree as ET
import resvg_py
from PIL import Image, ImageFilter, ImageChops

HERE = Path(__file__).resolve().parent.parent
SOURCE = HERE
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
GRAY, PANEL, INK = '#C8CAC7', '#FFFFFF', '#222222'
BODY = '#F3EBDF'
WINK = 'M338 151 L281 190 L338 229'
FONT_FILES = ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/msyhbd.ttc']


def tag(name):
    return '{' + NS + '}' + name


def shadow_defs():
    defs = ET.Element(tag('defs'))
    for sid, blur in [('soft-shadow', 12), ('contact-shadow', 2.5)]:
        f = ET.SubElement(defs, tag('filter'), {
            'id': sid, 'filterUnits': 'userSpaceOnUse', 'x': '-80', 'y': '-80',
            'width': '760', 'height': '540', 'color-interpolation-filters': 'sRGB'})
        ET.SubElement(f, tag('feGaussianBlur'), {'stdDeviation': str(blur)})
    return defs


def shadows():
    return [ET.Element(tag('rect'), {
        'x': '0', 'y': str(y), 'width': '600', 'height': '380', 'rx': '95',
        'fill': '#252825', 'opacity': str(op), 'filter': 'url(#' + sid + ')'})
        for sid, y, op in [('soft-shadow', 8, .14), ('contact-shadow', 2, .045)]]


def is_body(e):
    return e.get('fill', '').upper() == BODY and (
        e.tag == tag('path') and e.get('d', '').startswith('M95 0H505')
        or e.tag == tag('rect') and e.get('width') == '600' and e.get('height') == '380')


def style_svg(r, board=False, favicon=False):
    # Only source body silhouettes get shadows; facial strokes remain unchanged.
    for e in r.iter():
        if e.tag == tag('path') and e.get('d') == 'M269 184Q306 220 343 184':
            e.set('d', WINK)
            e.set('stroke-width', '17')
    if not favicon:
        groups = [e for e in r.iter() if any(is_body(c) for c in e)]
        # Root-level logos need a local group so background remains flat.
        if r in groups:
            content = [e for e in r if e.tag != tag('defs') and
                       not (e.tag == tag('rect') and
                            e.get('width') == '780' and e.get('height') == '560')]
            if content:
                g = ET.Element(tag('g'))
                for e in content:
                    r.remove(e)
                    g.append(e)
                r.append(g)
                groups[groups.index(r)] = g
        if groups:
            r.insert(0, shadow_defs())
            for g in groups:
                for i, e in enumerate(shadows()):
                    g.insert(i, e)
    if board:
        for e in r:
            if e.tag in (tag('rect'), tag('circle')):
                color = e.get('fill', '').upper()
                if color == BODY and e.get('width') == '1920':
                    e.set('fill', '#FFFFFF')
                elif color == '#FAF6EF':
                    e.set('fill', '#FFFFFF')
                elif color == '#EDE4D3':
                    e.set('fill', '#FFFFFF')
                elif color == '#222222' and e.tag == tag('circle'):
                    e.set('fill', GRAY)
                elif color == '#222222' and e.tag == tag('rect'):
                    # Keep the monochrome white sample on its dark background.
                    if not ((e.get('x') == '1430' and e.get('y') == '815') or
                            (e.get('x') == '1156' and e.get('y') == '229')):
                        e.set('fill', GRAY)
            if e.tag == tag('polyline'):
                if e.get('stroke') == '#D9D0C2':
                    e.set('stroke', '#ACB0AC')
        for e in r.iter(tag('text')):
            text = e.text or ''
            e.text = {
                '小角 · 视觉形象规范': '小角 · 视觉形象规范 正式',
                '禁止拉伸、描边、渐变、阴影': '允许轻阴影；禁止描边、拉伸、渐变',
                '保持比例与标准色': '轻阴影：向下 8 / 模糊 12 / 14%',
                '深墨底 · 暖米白体': '浅灰底 · 暖米白体 · 轻阴影',
                '白体保持不动，表情由双眼变化。': '身体保持不动；眨眼为左眼睁开、右眼＜形。',
                '统一配色与标准轮廓': '微型图标用平面版，保证边缘清晰',
            }.get(text, text)
            if text == '双眼 90 × 130 / APP 占比 74%':
                e.text = '灰底 #C8CAC7 · 轻阴影'
            if e.get('fill') == '#777167':
                e.set('fill', '#606560')
        # Replace auxiliary beige palette with new primary gray; keep beige as auxiliary.
        if any(e.text == '基础规范' for e in r.iter(tag('text'))):
            for e in r:
                if e.tag == tag('rect') and e.get('x') == '1496' and e.get('y') == '229':
                    e.set('fill', GRAY)
                if e.tag == tag('rect') and e.get('x') == '1666' and e.get('y') == '229':
                    e.set('fill', '#EDE4D3')
                if e.tag == tag('text'):
                    if e.text == '浅米': e.text = '主背景灰'
                    elif e.text == '#EDE4D3': e.text = GRAY
                    elif e.text == '功能蓝': e.text = '辅助浅米'
                    elif e.text == '#6EC6E8': e.text = '#EDE4D3'
                    elif e.text == '功能蓝仅用于表情辅助，不进入标准主标识。':
                        e.text = '灰色为主背景；浅米为辅助；功能蓝 #6EC6E8 仅用于表情。'
                        e.set('font-size', '17')
            # White support example next to the gray primary presentation.
            for e in r:
                if e.tag == tag('rect') and e.get('x') in ('94', '606') and e.get('y') == '226':
                    e.set('fill', '#FFFFFF')
    return r


def save_svg(r, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(r).write(path, encoding='utf-8', xml_declaration=True)
    return path


def render(path, width=None, height=None):
    kwargs = {'svg_path': str(path), 'font_files': FONT_FILES,
              'skip_system_fonts': True, 'font_family': 'Microsoft YaHei'}
    if width: kwargs['width'] = width
    if height: kwargs['height'] = height
    return Image.open(BytesIO(resvg_py.svg_to_bytes(**kwargs))).convert('RGBA')


def png(path, destination, width=None, height=None):
    im = render(path, width, height)
    destination.parent.mkdir(parents=True, exist_ok=True)
    im.save(destination)
    return im


def convert_assets():
    # Base master.
    p = save_svg(style_svg(ET.parse(SOURCE/'00-基板/小角-标准基板.svg').getroot()),
                 HERE/'00-基板/小角-标准基板.svg')
    im = png(p, p.with_suffix('.png'), 1584, 1144)
    bg = Image.new('RGBA', im.size, GRAY); bg.alpha_composite(im)
    bg.convert('RGB').save(HERE/'00-基板/小角-灰底效果.png')
    for folder in ['01-主标识', '02-应用图标', '03-社交头像', '04-表情包', '06-网站favicon']:
        for p in sorted((SOURCE/folder/'SVG').glob('*.svg')):
            r = ET.parse(p).getroot()
            is_favicon = folder == '06-网站favicon'
            if folder in ['02-应用图标', '03-社交头像']:
                for e in r:
                    if e.get('fill') == INK and e.tag in [tag('rect'), tag('circle')]:
                        e.set('fill', GRAY)
            p2 = save_svg(style_svg(r, favicon=is_favicon), HERE/folder/'SVG'/p.name)
            if folder == '01-主标识':
                sizes = [1024, 512, 256] if p.stem == '小角-主标识' else [1024]
                for size in sizes:
                    png(p2, HERE/folder/'PNG'/f'{p.stem}-{size}px.png', size)
            elif folder == '02-应用图标':
                for size in [1024, 512, 192, 180]:
                    png(p2, HERE/folder/'PNG'/f'{p.stem}-{size}px.png', size, size)
            elif folder == '03-社交头像':
                for size in [1024, 512, 256]:
                    png(p2, HERE/folder/'PNG'/f'{p.stem}-{size}px.png', size, size)
            elif folder == '04-表情包':
                for size in [512, 240]:
                    # Square sticker canvases preserve standard width and safe margins.
                    square = deepcopy(r)
                    square.set('viewBox', '0 -110 780 780')
                    square.set('width', '780'); square.set('height', '780')
                    data = ET.tostring(square, encoding='unicode')
                    im = Image.open(BytesIO(resvg_py.svg_to_bytes(svg_string=data,width=size,height=size)))
                    d = HERE/folder/f'PNG-{size}'/p.with_suffix('.png').name
                    d.parent.mkdir(parents=True, exist_ok=True); im.save(d)
            elif is_favicon:
                for size in [16, 32, 48]:
                    png(p2, HERE/folder/f'favicon-{size}x{size}.png', size, size)
                im = render(p2, 256, 256)
                im.save(HERE/folder/'favicon.ico', sizes=[(16,16),(32,32),(48,48),(256,256)])
    # Deliver gray-background and auxiliary-beige logo exports as well.
    mark = ET.parse(HERE/'01-主标识/SVG/小角-主标识.svg').getroot()
    for suffix, color in [('灰底', GRAY), ('辅助米底', '#EDE4D3')]:
        r = deepcopy(mark)
        r.insert(1, ET.Element(tag('rect'), {'x':'-90','y':'-90','width':'780','height':'560','fill':color}))
        p = save_svg(r, HERE/'01-主标识/SVG'/f'小角-主标识-{suffix}.svg')
        png(p, HERE/'01-主标识/PNG'/f'小角-主标识-{suffix}-1024px.png',1024)


def convert_gifs():
    dest = HERE/'04-表情包/GIF'; dest.mkdir(parents=True, exist_ok=True)
    for p in (SOURCE/'04-表情包/GIF').glob('*.gif'):
        old = Image.open(p)
        frames, durations = [], []
        for i in range(old.n_frames):
            old.seek(i); im = old.convert('RGBA')
            alpha = im.getchannel('A')
            shadow = Image.new('L', im.size, 0)
            shadow.paste(alpha.filter(ImageFilter.GaussianBlur(3.7)), (0, 2))
            shadow = shadow.point(lambda v: round(v*.14))
            back = Image.new('RGBA', im.size, GRAY)
            layer = Image.new('RGBA',im.size,'#252825'); layer.putalpha(shadow)
            back.alpha_composite(layer); back.alpha_composite(im)
            if p.stem == 'sticker-03-wink':
                filename = 'sticker-01-standard' if i == 0 else 'sticker-03-wink'
                im2 = Image.open(HERE/f'04-表情包/PNG-240/{filename}.png').convert('RGBA')
                back = Image.new('RGBA', im2.size, GRAY); back.alpha_composite(im2)
            frames.append(back.convert('RGB'))
            durations.append(old.info.get('duration', 200))
        frames[0].save(dest/p.name, save_all=True, append_images=frames[1:],
                       duration=durations, loop=0, disposal=2, optimize=False)


def boards():
    dest = HERE/'05-VI展板'; dest.mkdir(parents=True,exist_ok=True)
    roots, images = [], []
    for name in ['01-基础规范-4K', '02-表情体系-4K', '03-应用体系-4K']:
        r = style_svg(ET.parse(SOURCE/f'05-VI展板/{name}.svg').getroot(),board=True)
        if name == '03-应用体系-4K':
            import re
            for g in r.iter(tag('g')):
                m = re.search(r'translate\(([-\d.]+)',g.get('transform',''))
                if m and float(m.group(1)) >= 1300:
                    for child in list(g):
                        if child.get('filter','').startswith('url(#soft-'):
                            g.remove(child)
        roots.append(r)
        p = save_svg(r, dest/(name+'.svg'))
        im = png(p, dest/(name+'.png'))
        im.convert('RGB').resize((1920,1080),Image.Resampling.LANCZOS).save(dest/(name+'-预览.jpg'),quality=92)
        images.append(im)
        print('Rendered board:', name, flush=True)
    full = ET.Element(tag('svg'), {'viewBox':'0 0 1920 3240','width':'3840','height':'6480'})
    full.append(shadow_defs())
    for i,r in enumerate(roots):
        g=ET.SubElement(full,tag('g'),{'transform':f'translate(0 {1080*i})'})
        for child in r:
            if child.tag != tag('defs'): g.append(deepcopy(child))
    save_svg(full,dest/'小角-VI完整展板.svg')
    total=Image.new('RGB',(3840,6480),'#FFFFFF')
    for i,im in enumerate(images):total.paste(im.convert('RGB'),(0,i*2160))
    total.save(dest/'小角-VI完整展板.png')
    total.resize((1440,2430),Image.Resampling.LANCZOS).save(dest/'小角-VI完整展板-预览.jpg',quality=92)


def documents():
    prompt=(SOURCE/'prompt.md').read_text(encoding='utf-8')
    prompt=prompt.replace('无描边、渐变、阴影、纹理或三维效果','无描边、渐变、纹理或三维厚度；仅在身体轮廓后添加低透明度的柔和投影')
    prompt=prompt.replace('深墨 #222222 圆角正方形背景','浅灰 #C8CAC7 圆角正方形背景').replace('深墨 #222222 方形底','浅灰 #C8CAC7 方形底')
    prompt += '\n正式：主背景为浅灰 #C8CAC7，浅米 #EDE4D3 仅作辅助。阴影颜色 #252825，按身体600设计宽度：向下8、模糊标准差12、不透明度14%；接触阴影向下2、模糊2.5、不透明度4.5%。无外轮廓描边。微型favicon和单色版使用平面形态。\n\n眨眼：左眼保持标准睁眼，右眼为向左收拢的＜形折线，设计坐标 M338 151 L281 190 L338 229，深墨色17宽圆端圆角；身体、眼睛中心和砖红切角不变。\n'
    (HERE/'prompt.md').write_text(prompt,encoding='utf-8')
    (HERE/'README.md').write_text('''# 小角IP规范与源文件

主背景 #C8CAC7；身体 #F3EBDF、双眼 #222222、切角 #D44A36 保持不变。取消外轮廓描边，使用轻微向下投影；浅米 #EDE4D3 为辅助背景。身体600×380、R95，眼睛90×130、R45，APP与头像内身体占宽74%。

VI展板页面及卡片底色均为白色 #FFFFFF，图标和头像自身保留品牌灰底，色卡保留标准色。

眨眼改为左眼睁开、右眼＜形，已同步静态表情、动态GIF及表情VI展板。

00-基板提供透明SVG和PNG；01-主标识提供透明、灰底、白底、辅助米底、深色底及单色版；02-应用图标、03-社交头像使用灰底；04-表情包包含12种透明静态表情及8种动态GIF；05-VI展板提供三张3840×2160分板和3840×6480完整展板；06-网站favicon提供16/32/48px PNG、SVG及ICO。

SVG和PNG保留透明背景及半透明投影。GIF采用主背景灰色，避免GIF不支持半透明造成阴影杂点。微型favicon和单色版使用平面形态，保证清晰度。阴影随本体同比缩放，身体保持纯色，无渐变、立体厚度或额外描边。

geometry.json与prompt.md为本版参数和形象描述；生成VI.py可从正式素材目录重建当前资产。正式素材目录 00–06 即为当前源文件与交付文件。
''',encoding='utf-8')


if __name__ == '__main__':
    convert_assets()
    print('Assets rendered.',flush=True)
    convert_gifs()
    boards()
    documents()
    print('Complete:',HERE,flush=True)
