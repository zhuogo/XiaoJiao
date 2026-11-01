"""Build twelve homepage studies around the immutable XiaoJiao geometry.

All new objects are behind the canonical character. Their pixels cannot cover
its eyes or its signature corner. Run: python scripts/build_form_studies.py
"""
from pathlib import Path
from html import escape
import json
import math
import zipfile

import resvg_py
from PIL import Image, ImageDraw, ImageFont
from go_identity_geometry import BODY, face, monochrome

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'frontend/public/logos/studies'
DATA = ROOT / 'frontend/src/data/form-studies.json'


def study(id, name, english, group, usage, description, body, ink, corner, accent, background, icon):
    # Light eyes on a dark character need a separate readable caption color.
    label = body if sum(int(ink[i:i+2], 16) for i in (1, 3, 5)) > 600 else ink
    return dict(id=id, name=name, english=english, group=group, usage=usage,
                description=description, body=body, ink=ink, corner=corner,
                accent=accent, background=background, icon=icon, label=label)


STUDIES = [
    study('orbital', '环绕之间', 'ORBITAL', '连接', '云服务 · 系统平台', '一条完整的椭圆从身后绕过，外侧的暖色模块成为连接的落点。小角稳稳留在中心。', '#F0F3FF', '#344C9C', '#748ACB', '#E7A260', '#E8ECF5', '#253A6D'),
    study('companion', '双星相伴', 'COMPANION', '连接', '协作 · AI 伙伴', '两个大小不同的节点沿同一条曲线相遇，表达彼此响应的伙伴关系。连接线藏在身体后方。', '#E8F1EF', '#2C6867', '#79AEAB', '#E8B06D', '#E1EDEA', '#24524F'),
    study('bridge', '连接有度', 'BRIDGE', '连接', '插件 · API 服务', '两端的连接模块以折线路径接入，圆角与小角相互呼应。完整的面部留出清楚、安静的中心。', '#F9ECE4', '#964C39', '#C87558', '#DCA98B', '#F0E5DD', '#713E31'),
    study('echo', '听见回响', 'ECHO', '连接', '声音 · 即时交流', '两道舒展的声弧停在身体外侧，既有声音的节奏，也有倾听的余地。双眼保留最初的神情。', '#313B43', '#F6EEE2', '#D58367', '#9CA9AB', '#E5E8E5', '#DCE4E0'),
    study('folio', '思绪叠层', 'FOLIO', '收纳', '笔记 · 灵感画布', '向两个方向轻轻错开的画布形成层次。最前方始终是完整的小角，像把散落的思绪慢慢收好。', '#F1F3E7', '#315C48', '#8BA487', '#B4C5A7', '#E7EBDD', '#264A3D'),
    study('bookmark', '留在这一页', 'BOOKMARK', '收纳', '阅读 · 收藏', '一条书签从小角身后穿过，只在上下露出。把重要的一页留住，也给简洁的轮廓添一处记忆点。', '#F7EAEC', '#743F59', '#BD8195', '#8F536B', '#EFE3E6', '#5E374D'),
    study('index', '各有位置', 'INDEX', '收纳', '知识库 · 资料整理', '三枚圆角索引从上缘依次露出，以深浅区分层级。整齐的节奏承接分类与整理的秩序感。', '#EDF1E8', '#3E6055', '#7D9C8A', '#B9C8AF', '#E2E9DF', '#304C42'),
    study('frame', '留一点白', 'FRAME', '探索', '设计 · 内容创作', '四个取景角在身体之外留出距离，其中一角点亮。用留白提示专注，让小角成为画面里的主角。', '#F5EFE5', '#3C4844', '#C78A5C', '#929E92', '#E9E8DF', '#394741'),
    study('shelter', '安心所在', 'SHELTER', '陪伴', '个人空间 · 健康', '柔和的拱线从身后撑起一小片空间，温暖的小方块停在拱顶。亲近的保护感来自周围的留白。', '#F8F0DE', '#7A5B36', '#C6A16B', '#D5B781', '#F0E9D9', '#695039'),
    study('dock', '轻轻靠岸', 'DOCK', '陪伴', '桌面助手 · 工作台', '一条开放的底部曲线承接小角，外侧亮点保持清醒。它安静地在场，随时可以一起开始工作。', '#F0EBF7', '#4F3E65', '#AB93C5', '#E6AB60', '#EAE5EF', '#382D48'),
    study('horizon', '向着微光', 'HORIZON', '探索', '旅行 · 日常记录', '一轮小小的日光从身后升起，下方的弧线向远处舒展。身体保持平正，轻快感交给周围的景象。', '#EAF1F1', '#315963', '#78A0A7', '#E2AD68', '#E2EAEB', '#2D515A'),
    study('ribbon', '值得珍藏', 'RIBBON', '陪伴', '会员 · 成就纪念', '独立的圆章与短缎带露在右侧，像一次被认真记录的小成就。奖章和切角各自完整、互不借形。', '#F7EBE8', '#78495A', '#BC8293', '#D2A15B', '#EEE2E2', '#603B4D'),
]


def peripheral(s, mono=False):
    c = '#242725' if mono else s['corner']
    a = '#242725' if mono else s['accent']
    k = '#242725' if mono else s['ink']
    id = s['id']
    if id == 'orbital':
        # The ring is behind the body; the main character is never rotated.
        theta, tilt = math.radians(-16), math.radians(-18)
        x, y = 368 * math.cos(theta), 223 * math.sin(theta)
        px, py = 300 + x*math.cos(tilt)-y*math.sin(tilt), 190+x*math.sin(tilt)+y*math.cos(tilt)
        return f'<ellipse cx="300" cy="190" rx="368" ry="223" transform="rotate(-18 300 190)" fill="none" stroke="{c}" stroke-width="17"/><rect x="{px-22:.3f}" y="{py-22:.3f}" width="44" height="44" rx="12" transform="rotate(-18 {px:.3f} {py:.3f})" fill="{a}"/>'
    if id == 'companion':
        return f'<path d="M-33 304C-84 219 55 42 266 -12S588 -16 638 56" fill="none" stroke="{c}" stroke-width="17" stroke-linecap="round"/><circle cx="-32" cy="302" r="29" fill="{a}"/><rect x="603" y="14" width="76" height="76" rx="26" fill="{k}"/>'
    if id == 'bridge':
        return f'<path d="M-31 276H82Q122 276 122 236V122Q122 82 162 82H508Q548 82 548 42V-24Q548 -52 576 -52H629V53" fill="none" stroke="{c}" stroke-width="21" stroke-linecap="round" stroke-linejoin="round"/><rect x="-72" y="244" width="76" height="64" rx="22" fill="{k}"/><rect x="602" y="25" width="68" height="68" rx="21" fill="{a}"/>'
    if id == 'echo':
        return f'<path d="M-29 82Q-100 190 -29 298M629 82Q700 190 629 298" fill="none" stroke="{c}" stroke-width="20" stroke-linecap="round"/><path d="M-56 144Q-79 190 -56 236M656 144Q679 190 656 236" fill="none" stroke="{a}" stroke-width="11" stroke-linecap="round"/>'
    if id == 'folio':
        return f'<path d="{BODY}" transform="translate(-25 32)" fill="{k}"/><path d="{BODY}" transform="translate(30 -36)" fill="{a}"/>'
    if id == 'bookmark':
        return f'<path d="M113 -62H157Q172 -62 172 -47V455L135 433L98 455V-47Q98 -62 113 -62Z" fill="{a}"/>'
    if id == 'index':
        return ''.join(f'<rect x="{x}" y="{y}" width="68" height="115" rx="20" fill="{color}"/>' for x,y,color in [(325,-47,k),(407,-61,c),(489,-75,a)])
    if id == 'frame':
        return f'<path d="M-29 62V-29H62M538 -29H629V62M629 318V409H538M62 409H-29V318" fill="none" stroke="{a}" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/><path d="M538 -29H629V62" fill="none" stroke="{c}" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/>'
    if id == 'shelter':
        return f'<path d="M-25 227V111Q-25 -67 147 -67H453Q625 -67 625 111V227" fill="none" stroke="{c}" stroke-width="19" stroke-linecap="round"/><rect x="444" y="-86" width="40" height="40" rx="12" fill="{a}"/>'
    if id == 'dock':
        return f'<path d="M-30 255V348Q-30 425 48 425H543Q638 425 638 330V190" fill="none" stroke="{c}" stroke-width="18" stroke-linecap="round"/><circle cx="638" cy="138" r="20" fill="{a}"/>'
    if id == 'horizon':
        return f'<circle cx="523" cy="-25" r="61" fill="{a}"/><path d="M18 422C176 476 364 371 579 427" fill="none" stroke="{c}" stroke-width="17" stroke-linecap="round"/><path d="M75 465C140 476 213 466 273 454" fill="none" stroke="{a}" stroke-width="11" stroke-linecap="round"/>'
    if id == 'ribbon':
        return f'<path d="M604 111L591 200L620 183L646 207L660 116Z" fill="{c}"/><circle cx="630" cy="75" r="46" fill="{a}"/><circle cx="630" cy="75" r="19" fill="{k}"/>'
    raise ValueError(id)


def svg_for(s, mode='mark', base=False, size=None):
    mono = mode == 'mono'
    rear = '' if base else peripheral(s, mono=mono)
    if mono:
        art = monochrome('study-'+s['id'], '#242725', rear=rear)
    else:
        art = f'<g data-part="peripheral">{rear}</g><g data-part="character">{face(s["body"],s["ink"],s["corner"])}</g>'
    height = 840 if mode == 'app' else 760
    pixels = size or (1024 if mode == 'app' else 840)
    bg = f'<rect width="840" height="840" rx="184" fill="{s["icon"]}"/>' if mode == 'app' else ''
    y = 230 if mode == 'app' else 190
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{pixels}" height="{pixels if mode == "app" else round(pixels*height/840)}" viewBox="0 0 840 {height}"><title>小角 · {escape(s["name"])} · {"基准" if base else "完整形态"} · {mode}</title>{bg}<g data-part="placement" transform="translate(120 {y})">{art}</g></svg>'


def board():
    result = Image.new('RGB', (2080, 1900), '#F7F6F1')
    d = ImageDraw.Draw(result)
    font = lambda size: ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', size)
    bold = lambda size: ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', size)
    d.text((65, 38), 'XIAOJIAO / TWELVE WAYS TO BELONG', font=bold(43), fill='#34483C')
    d.text((68, 107), 'One constant character. New relationships around it.', font=font(24), fill='#7A857A')
    for i, s in enumerate(STUDIES):
        x, y = 64 + (i % 4)*490, 185 + (i // 4)*548
        d.rounded_rectangle((x, y, x+466, y+520), radius=16, fill=s['background'])
        d.text((x+24, y+22), f'{i+1:02} / {s["english"]}', font=font(21), fill=s['label'])
        art = Image.open(OUT / f'{s["id"]}-mark.png').convert('RGBA')
        art.thumbnail((458, 410), Image.Resampling.LANCZOS)
        result.paste(art, (x+(466-art.width)//2, y+55+(385-art.height)//2), art)
        for n, size in enumerate((56, 32, 16)):
            icon = Image.open(OUT / f'{s["id"]}-app.png').convert('RGBA').resize((size, size), Image.Resampling.LANCZOS)
            result.paste(icon, (x+25+n*68, y+442+(56-size)//2), icon)
        for n, color in enumerate((s['ink'], s['corner'], s['accent'])):
            d.ellipse((x+355+n*28, y+463, x+372+n*28, y+480), fill=color)
    result.save(OUT / 'form-studies-board.png')


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    DATA.parent.mkdir(parents=True, exist_ok=True)
    catalog = json.dumps(STUDIES, ensure_ascii=False, indent=2)
    DATA.write_text(catalog+'\n', encoding='utf-8')
    (OUT / 'catalog.json').write_text(catalog+'\n', encoding='utf-8')
    for s in STUDIES:
        for mode in ('mark', 'app', 'mono'):
            for base in (False, True):
                stem = s['id'] + ('-base' if base else '') + '-' + mode
                svg = svg_for(s, mode, base)
                (OUT / f'{stem}.svg').write_text(svg, encoding='utf-8')
                (OUT / f'{stem}.png').write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=svg)))
        for size in (16, 32, 64, 192):
            (OUT / f'{s["id"]}-icon-{size}.png').write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=svg_for(s, 'app', size=size))))
        with zipfile.ZipFile(OUT / f'{s["id"]}.zip', 'w', zipfile.ZIP_DEFLATED) as z:
            for p in sorted(OUT.glob(s['id']+'-*')):
                if p.suffix in ('.svg', '.png'):
                    z.write(p, p.name)
    board()
    notes = '''# 小角 · 12 款形态案例

小角身体为 600 × 380、圆角 R95。双眼各 90 × 130，中心分别为 (168,190)、(306,190)。切角保持原始 45° 几何。

全部新增结构在小角后方绘制；不旋转、拉伸本体，不改变眼距，不折叠或覆盖彩色切角。

- `-mark`：透明彩色标志，SVG / PNG。
- `-app`：应用图标，SVG / 1024px PNG。
- `-mono`：单色标志，双眼与切角分界使用透明负形。
- `-base-*`：去掉外围结构后的同色基准，可与完整形态叠加对照。
- `-icon-16/32/64/192.png`：小尺寸应用图标。
- `catalog.json`：案例说明与配色；`form-studies-board.png`：完整对比图。

标志请等比缩放。小尺寸优先保留小角本体，外围细节在 32px 以上更清晰。
源文件：scripts/build_form_studies.py；基准：scripts/go_identity_geometry.py。
'''
    (OUT / 'README.md').write_text(notes, encoding='utf-8')
    with zipfile.ZipFile(OUT / 'xiaojiao-form-studies.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.iterdir()):
            if p.suffix != '.zip':
                z.write(p, p.name)
    print(f'Built {len(STUDIES)} canonical form studies, baseline comparisons, icons and download packages.')


if __name__ == '__main__':
    build()
