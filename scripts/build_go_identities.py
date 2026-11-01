"""Second-round Go identities. Original DraftGo and first-round studies stay intact.

Run from the repository root: python scripts/build_go_identities.py
Requires the project's resvg-py and Pillow export dependencies.
"""
from pathlib import Path
import hashlib
import json
import zipfile
from xml.etree import ElementTree as ET

import resvg_py
from PIL import Image, ImageDraw, ImageFont
from go_identity_geometry import BENCHGO_DEFAULT_ID, BENCHGO_PALETTES, BRANDS, svg_for


ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / 'frontend/public/logos/go'
OUT = LEGACY / 'v2'
OUT.mkdir(parents=True, exist_ok=True)
SVG_NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG_NS)


def add_soft_shadow(svg):
    """A single soft shadow beneath the existing artwork, above the app tile."""
    doc = ET.fromstring(svg)
    defs = ET.SubElement(doc, f'{{{SVG_NS}}}defs')
    effect = ET.SubElement(defs, f'{{{SVG_NS}}}filter', {
        'id': 'go-soft-shadow', 'x': '-15%', 'y': '-20%',
        'width': '130%', 'height': '145%', 'color-interpolation-filters': 'sRGB',
    })
    ET.SubElement(effect, f'{{{SVG_NS}}}feDropShadow', {
        'dx': '0', 'dy': '8', 'stdDeviation': '10',
        'flood-color': '#1F2925', 'flood-opacity': '0.10',
    })
    for child in list(doc):
        if child.tag == f'{{{SVG_NS}}}g':
            index = list(doc).index(child)
            doc.remove(child)
            group = ET.Element(f'{{{SVG_NS}}}g', {'filter': 'url(#go-soft-shadow)', 'data-effect': 'soft-shadow'})
            group.append(child)
            doc.insert(index, group)
    return ET.tostring(doc, encoding='unicode')


def resized_svg(svg, size):
    doc = ET.fromstring(svg)
    doc.set('width', str(size))
    doc.set('height', str(size))
    return ET.tostring(doc, encoding='unicode')


def save_svg_png(stem, svg):
    if stem.endswith(('-mark', '-app')):
        svg = add_soft_shadow(svg)
    ET.fromstring(svg)
    (OUT / f'{stem}.svg').write_text(svg, encoding='utf-8')
    (OUT / f'{stem}.png').write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=svg)))


def font(size, bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/' + ('segoeuib.ttf' if bold else 'segoeui.ttf'), size)


def build_benchgo_palettes():
    manifest = []
    for palette in BENCHGO_PALETTES:
        stem = f'benchgo-{palette["id"]}'
        manifest.append({**palette, 'stem': stem, 'default': palette['id'] == BENCHGO_DEFAULT_ID})
        for variant in ('mark', 'app', 'favicon'):
            save_svg_png(f'{stem}-{variant}', svg_for('benchgo', variant, palette=palette))
        for size in (16, 32, 48, 64, 180, 192, 512):
            variant = 'favicon' if size <= 64 else 'app'
            svg = svg_for('benchgo', variant, size, palette=palette)
            if size > 64:
                svg = add_soft_shadow(svg)
            (OUT / f'{stem}-icon-{size}.png').write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=svg)))
        Image.open(OUT / f'{stem}-favicon.png').save(OUT / f'{stem}-favicon.ico', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    data = json.dumps(manifest, ensure_ascii=False, indent=2)
    (OUT / 'benchgo-palettes.json').write_text(data, encoding='utf-8')
    (ROOT / 'frontend/src/data/benchgo-palettes.json').write_text(data, encoding='utf-8')
    make_benchgo_palette_board(manifest)


def make_benchgo_palette_board(palettes):
    rows = (len(palettes) + 3) // 4
    height = 270 + rows*490 + (rows-1)*24 + 112
    board = Image.new('RGB', (2400, height), '#F7F8F5')
    d = ImageDraw.Draw(board)
    ink, secondary = '#252D40', '#6C7378'

    def cn(size, bold=False):
        return ImageFont.truetype('C:/Windows/Fonts/' + ('msyhbd.ttc' if bold else 'msyh.ttc'), size)

    def paste_asset(path, box):
        art = Image.open(path).convert('RGBA')
        art.thumbnail((box[2], box[3]), Image.Resampling.LANCZOS)
        board.paste(art, (box[0]+(box[2]-art.width)//2, box[1]+(box[3]-art.height)//2), art)

    d.text((72, 46), 'BENCHGO / COLOUR COLLECTION', font=font(23), fill=secondary)
    d.text((68, 91), 'The original XiaoJiao colours.', font=font(72, True), fill=ink)
    d.text((72, 198), f'当前方案：小角原配色 · 保留此前 {len(palettes)-1} 款配色研究。', font=cn(27), fill=secondary)
    for index, palette in enumerate(palettes):
        x, y = 72+(index%4)*570, 270+(index//4)*514
        d.rounded_rectangle((x, y, x+546, y+490), radius=18, fill='#F0F1EC')
        d.text((x+26, y+25), f'{index+1:02d} / {palette["name"]}', font=cn(26, True), fill=palette['wordmark'])
        if palette['default']:
            d.rounded_rectangle((x+439, y+24, x+514, y+64), radius=20, fill=palette['wordmark'])
            d.text((x+459, y+31), '当前', font=cn(17), fill='#FFFFFF')
        paste_asset(OUT / f'{palette["stem"]}-mark.png', (x+17, y+76, 512, 270))
        d.text((x+26, y+350), palette['note'], font=cn(18), fill=secondary)
        paste_asset(OUT / f'{palette["stem"]}-app.png', (x+26, y+398, 66, 66))
        for n, key in enumerate(('color', 'accent', 'syntax')):
            px = x+140+n*124
            d.rounded_rectangle((px, y+402, px+99, y+433), radius=6, fill=palette[key])
            d.text((px, y+446), palette[key], font=font(15), fill=secondary)
    d.line((72, height-78, 2328, height-78), fill='#D9DFE0', width=2)
    d.text((72, height-52), 'XIAOJIAO / 标准身体、双眼与切角 / 编辑器形态', font=cn(21), fill=ink)
    d.text((2110, height-52), 'benchgo.cn', font=font(26), fill=secondary)
    board.save(OUT / 'benchgo-palette-board.png')


def make_benchgo_comparison():
    previous = LEGACY / 'history/benchgo-editor-mint'
    board = Image.new('RGB', (1800, 1336), '#F7F8F3')
    d = ImageDraw.Draw(board)
    ink, secondary = '#26363B', '#68766E'

    def cn(size, bold=False):
        return ImageFont.truetype('C:/Windows/Fonts/' + ('msyhbd.ttc' if bold else 'msyh.ttc'), size)

    def paste_asset(path, box):
        art = Image.open(path).convert('RGBA')
        art.thumbnail((box[2], box[3]), Image.Resampling.LANCZOS)
        board.paste(art, (box[0]+(box[2]-art.width)//2, box[1]+(box[3]-art.height)//2), art)

    d.text((80, 52), 'BENCHGO / IDENTITY UPDATE', font=font(22), fill=secondary)
    d.text((76, 94), 'A companion for your code.', font=font(68, True), fill=ink)
    d.text((80, 198), '收起两侧括号，保留熟悉的编辑器细节。', font=cn(27), fill=secondary)

    for x, directory, bg, label, caption in (
        (80, previous, '#E5ECE7', '01 / 此前方案', '石墨薄荷 · 外侧括号'),
        (920, OUT, BRANDS['benchgo']['background'], '02 / 小角原配色 · 编辑器', '暖米白身体 · 砖红切角 · 深墨双眼'),
    ):
        d.rounded_rectangle((x, 278, x+800, 936), radius=20, fill=bg)
        d.text((x+32, 308), label, font=cn(22, True), fill=ink)
        paste_asset(directory / 'benchgo-mark.png', (x+24, 350, 752, 478))
        d.text((x+32, 848), 'BenchGo', font=font(36, True), fill=ink)
        d.text((x+32, 898), caption, font=cn(17), fill=secondary)

    d.text((80, 970), '应用图标', font=cn(19), fill=secondary)
    paste_asset(OUT / 'benchgo-app.png', (80, 1014, 158, 158))
    d.text((314, 970), '单色 / 反白', font=cn(19), fill=secondary)
    d.rounded_rectangle((314, 1014, 474, 1172), radius=15, fill='#E8ECE5')
    d.rounded_rectangle((484, 1014, 644, 1172), radius=15, fill=ink)
    paste_asset(OUT / 'benchgo-mono.png', (314, 1020, 160, 146))
    paste_asset(OUT / 'benchgo-reverse.png', (484, 1020, 160, 146))

    d.text((720, 970), '小尺寸', font=cn(19), fill=secondary)
    for x, size in ((720, 16), (792, 32), (880, 48), (984, 64)):
        paste_asset(OUT / f'benchgo-icon-{size}.png', (x, 1058+(64-size)//2, size, size))
        d.text((x, 1146), str(size), font=font(16), fill=secondary)

    d.text((1160, 970), '编辑器配色', font=cn(19), fill=secondary)
    for i, (key, label) in enumerate((('color', '暖米白'), ('accent', '砖红'), ('paper', '深墨眼睛'))):
        x = 1160+i*192
        color = BRANDS['benchgo'][key]
        d.rounded_rectangle((x, 1028, x+158, 1082), radius=8, fill=color)
        d.text((x, 1098), label, font=cn(18), fill=ink)
        d.text((x, 1134), color, font=font(17), fill=secondary)

    d.line((80, 1210, 1720, 1210), fill='#D9E1D9', width=2)
    d.text((80, 1244), '同一基准：600 × 380 身体 / 标准双眼 / 45° 切角', font=cn(22), fill=ink)
    d.text((1450, 1248), 'benchgo.cn', font=font(26), fill=secondary)
    board.save(OUT / 'benchgo-comparison.png')


def make_board():
    board = Image.new('RGB', (2400, 1490), '#F7F5EF')
    d = ImageDraw.Draw(board)
    d.text((104, 66), 'GO / A FAMILY OF INDIVIDUALS', font=font(24), fill='#74766E')
    d.text((100, 122), 'One family. Four characters.', font=font(76, True), fill='#242D27')
    names = ['draftgo', *BRANDS]
    tags = ['BUILD / THE FOUNDATION', 'CONNECT / THE GATEWAY', 'THINK / THE OPEN CANVAS', 'CODE / THE COMPANION']
    for i, name in enumerate(names):
        x = 100 + i * 562
        b = BRANDS.get(name, dict(name='DraftGo', background='#E8ECF7', color='#244DE0', domain='draftgo.cn'))
        wordmark = b.get('wordmark', b['color'])
        d.rounded_rectangle((x, 282, x+532, 1110), radius=18, fill=b['background'])
        d.text((x+30, 310), f'0{i+1}   {tags[i]}', font=font(16), fill=wordmark)
        path = OUT / f'{name}-mark.png'
        art = Image.open(path).convert('RGBA')
        art.thumbnail((508, 476), Image.Resampling.LANCZOS)
        board.paste(art, (x + (532-art.width)//2, 386+(460-art.height)//2), art)
        d.text((x+30, 882), b['name'], font=font(50, True), fill=wordmark)
        d.text((x+32, 955), b['domain'], font=font(23), fill=wordmark)
        mono = Image.open(OUT / f'{name}-mono.png').convert('RGBA')
        mono.thumbnail((94, 82), Image.Resampling.LANCZOS)
        board.paste(mono, (x+30, 1010), mono)
        for n, sz in enumerate((88, 48, 32)):
            variant = 'app' if sz > 64 else 'favicon'
            app = Image.open(OUT / f'{name}-{variant}.png').convert('RGBA')
            icon = app.resize((sz, sz), Image.Resampling.LANCZOS)
            board.paste(icon, (x+277+n*76, 1014+(88-sz)//2), icon)
        d.text((x+30, 1160), ['SPACE', 'CONNECTION', 'THOUGHTS', 'CODE'][i], font=font(24, True), fill='#3C463E')
        for n, c in enumerate([b['color'], b.get('accent', '#EE9853'), b.get('syntax', b.get('paper', '#F1F5FF'))]):
            d.rounded_rectangle((x+30+n*82, 1215, x+98+n*82, 1243), radius=5, fill=c)
            d.text((x+30+n*82, 1254), c.upper(), font=font(13), fill='#6C746C')
    d.line((100, 1330, 2300, 1330), fill='#D8DCD3', width=2)
    d.text((100, 1365), 'XIAOJIAO / PRODUCT IDENTITIES', font=font(21), fill='#74766E')
    d.text((1730, 1365), 'VECTOR STUDIES / ROUND 02', font=font(21), fill='#74766E')
    board.save(OUT / 'go-family-board.png')


def build_benchgo_final_package():
    with zipfile.ZipFile(OUT / 'benchgo-final.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(OUT / 'benchgo-final-README.md', 'BenchGo/README.md')
        palette = next(p for p in BENCHGO_PALETTES if p['id'] == BENCHGO_DEFAULT_ID)
        z.writestr('BenchGo/palette.json', json.dumps(palette, ensure_ascii=False, indent=2))
        for variant in ('mark', 'app', 'mono', 'reverse', 'favicon'):
            for ext in ('svg', 'png'):
                filename = f'benchgo-{variant}.{ext}'
                z.write(OUT / filename, f'BenchGo/{filename}')
        for size in (16, 32, 48, 64, 180, 192, 512):
            filename = f'benchgo-icon-{size}.png'
            z.write(OUT / filename, f'BenchGo/{filename}')
        z.write(OUT / 'benchgo-favicon.ico', 'BenchGo/benchgo-favicon.ico')


def build():
    original = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in LEGACY.glob('draftgo-*')}
    # Keep legacy originals intact and publish shadowed colour editions in v2.
    for variant in ('mark', 'app', 'mono'):
        source = (LEGACY / f'draftgo-{variant}.svg').read_text(encoding='utf-8')
        if variant == 'mono':
            for ext in ('svg', 'png'):
                filename = f'draftgo-mono.{ext}'
                (OUT / filename).write_bytes((LEGACY / filename).read_bytes())
        else:
            save_svg_png(f'draftgo-{variant}', source)
    flat_draft_app = (LEGACY / 'draftgo-app.svg').read_text(encoding='utf-8')
    save_svg_png('draftgo-favicon', flat_draft_app)
    for size in (16, 32, 48, 64, 180, 192, 512):
        source = flat_draft_app if size <= 64 else (OUT / 'draftgo-app.svg').read_text(encoding='utf-8')
        (OUT / f'draftgo-icon-{size}.png').write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=resized_svg(source, size))))
    Image.open(OUT / 'draftgo-favicon.png').save(OUT / 'draftgo-favicon.ico', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    for name in BRANDS:
        for variant in ('mark', 'app', 'mono', 'reverse', 'favicon'):
            svg = (LEGACY / f'{name}-{variant}.svg').read_text(encoding='utf-8') if name == 'routergo' and variant in ('mark', 'app') else svg_for(name, variant)
            save_svg_png(f'{name}-{variant}', svg)
        for size in (16, 32, 48, 64, 180, 192, 512):
            variant = 'favicon' if size <= 64 else 'app'
            svg = svg_for(name, variant, size) if size <= 64 else resized_svg((OUT / f'{name}-app.svg').read_text(encoding='utf-8'), size)
            (OUT / f'{name}-icon-{size}.png').write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=svg)))
        icon = Image.open(OUT / f'{name}-favicon.png')
        icon.save(OUT / f'{name}-favicon.ico', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
        if name == 'benchgo':
            build_benchgo_palettes()
            make_benchgo_comparison()
            build_benchgo_final_package()
        with zipfile.ZipFile(OUT / f'{name}-identity.zip', 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(OUT / 'README.md', 'README.md')
            for p in sorted(OUT.glob(f'{name}-*')):
                if p.suffix != '.zip':
                    z.write(p, f'{BRANDS[name]["name"]}/{p.name}')
    (OUT / 'palette.json').write_text(json.dumps(BRANDS, ensure_ascii=False, indent=2), encoding='utf-8')
    make_board()
    with zipfile.ZipFile(OUT / 'go-family-v2.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.iterdir()):
            if p.suffix != '.zip':
                z.write(p, p.name)
        for p in sorted(LEGACY.glob('draftgo-*')):
            z.write(p, 'DraftGo-original/' + p.name)
    assert original == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in LEGACY.glob('draftgo-*')}
    print(f'Created 3 identities with true monochrome / reverse, multi-size icons and ZIPs in {OUT}')


if __name__ == '__main__':
    build()
