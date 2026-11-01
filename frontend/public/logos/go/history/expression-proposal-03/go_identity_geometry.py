"""Product identities around XiaoJiao's canonical body and corner.

RouterGo and SelfGo also have user-approved eye expressions, derived inside
the original eye boxes. Neutral versions retain the literal canonical eyes.
"""

INK = '#242725'
BODY = 'M95 0H505A95 95 0 0 1 600 95V285A95 95 0 0 1 505 380H95A95 95 0 0 1 0 285V95A95 95 0 0 1 95 0Z'
CORNER = 'M410 380H505A95 95 0 0 0 600 285V190Z'
EYES = '<rect x="123" y="125" width="90" height="130" rx="45"/><rect x="261" y="125" width="90" height="130" rx="45"/>'
# Core colours match 小角IP/geometry.json; warm grey supports the editor strip.
BENCHGO_ORIGINAL = dict(id='original', group='original', name='小角原配色', note='暖米白 · 砖红切角', detail='暖米白的身体、深墨双眼与砖红切角，沿用小角熟悉的原配色。顶部保留编辑器标签、分隔线与光标，让温暖的陪伴感和随时开工的状态放在一起。', color='#F3EBDF', accent='#D44A36', paper='#222222', background='#C8CAC7', dark='#222222', app_background='#C8CAC7', syntax='#D44A36', muted='#B6B1A7', wordmark='#222222')
BENCHGO_PREVIOUS_PALETTES = [
    dict(id='ice', name='深海蓝', note='深蓝主色 · 冰青切角', detail='深海蓝作为身体主色，搭配冰青切角与墨蓝双眼。顶部的活动标签和暖金光标，保留熟悉的编辑器气质。', color='#30496B', accent='#8ACEDA', paper='#101F30', background='#E8EEF4', dark='#20364F', app_background='#DDE7F1', syntax='#EAC793', muted='#657C95', wordmark='#30496B'),
    dict(id='mist', name='雾蓝灰', note='中明度主色 · 轻盈、安静', detail='身体换成明度更高的雾蓝灰，搭配浅冰蓝切角与深灰蓝双眼。整体轻盈、安静，适合日常常驻的工作伙伴。', color='#829AA8', accent='#C5DDE0', paper='#304955', background='#EBF0F2', dark='#435D6C', app_background='#E0E8EC', syntax='#F4D49F', muted='#B3C5CE', wordmark='#435D6C'),
    dict(id='sand', name='暖砂白', note='浅色主色 · 温暖、亲近', detail='暖砂白的身体配上深灰蓝双眼，蓝灰切角和铜色光标呼应纸张与桌面。温暖的浅色主调，让办公与开发都更亲近。', color='#E5DACA', accent='#8B9EAD', paper='#424B55', background='#F3F0E9', dark='#424B55', app_background='#D0D5D5', syntax='#B98455', muted='#B9B1A6', wordmark='#424B55'),
    dict(id='mint', name='石墨黑', note='原灰黑主色 · 薄荷绿切角', detail='保留上一版灰黑身体与薄荷绿切角，顶部保留活动标签和琥珀色光标。作为原配色参照，可以直接比较主色深浅的差异。', color='#26363B', accent='#78CBA8', paper='#0C171B', background='#E5ECE7', dark='#182A30', app_background='#DBE8DF', syntax='#E3B96F', muted='#526863', wordmark='#26363B'),
]
BENCHGO_SOFT_PALETTES = [
    dict(id='sky', group='soft', name='晴空蓝', note='晴空蓝 · 奶油黄', detail='晴空蓝的身体，配奶油黄切角与深蓝双眼。清爽里带一点暖意，让小角像一个轻松、可靠的工作伙伴。', color='#89B9D8', accent='#F3D89B', paper='#29465C', background='#EDF3F6', dark='#29465C', app_background='#F6F0E4', syntax='#FFF6E4', muted='#6094B5', wordmark='#29465C'),
    dict(id='apricot', group='soft', name='奶油杏', note='温暖亲近 · 鼠尾草绿切角', detail='奶油杏的身体搭配柔和绿切角，深暖灰双眼让表情更亲近。像日光照进工作桌，轻快、温暖，也留得住专注。', color='#F2C8A9', accent='#99B9B0', paper='#4B4A43', background='#F7F1E9', dark='#4B4A43', app_background='#F1E8DC', syntax='#77998D', muted='#D5A788', wordmark='#665446'),
    dict(id='sage', group='soft', name='鼠尾草绿', note='清新自然 · 燕麦黄切角', detail='清浅的鼠尾草绿配上燕麦黄，像给桌面添了一点自然光。整体松弛、平和，深绿双眼保留小角清楚的神态。', color='#ABC5B1', accent='#EDDCAD', paper='#344D47', background='#EFF3EB', dark='#344D47', app_background='#F2EDDF', syntax='#E0BA8D', muted='#86A591', wordmark='#344D47'),
    dict(id='lilac', group='soft', name='柔雾紫', note='柔和灵动 · 杏桃色切角', detail='柔雾紫搭配杏桃色，给编辑器一点轻盈的想象力。深紫灰双眼收住甜度，让年轻感和日常工作的分寸并存。', color='#B8AFD8', accent='#F0CCA9', paper='#47405C', background='#F2EFF7', dark='#47405C', app_background='#ECE7F4', syntax='#F8E8CA', muted='#9488B8', wordmark='#47405C'),
]
BENCHGO_RICH_PALETTES = [
    dict(id='denim', name='牛仔蓝', note='牛仔蓝 · 麦芽黄', detail='有明度也有分量的牛仔蓝，搭配麦芽黄切角。日常、清爽，让编辑器保持亲近感。', color='#426F9C', accent='#F0C884', paper='#172C40', background='#E9EFF4', dark='#304E6E', app_background='#E5ECF2', syntax='#A8D4D8', muted='#7192AF', wordmark='#304E6E'),
    dict(id='cobalt', name='钴蓝', note='钴蓝 · 浅冰蓝', detail='更明确的钴蓝主色，配浅冰蓝切角和暖金光标。颜色集中，带一点年轻的锐气。', color='#3856A6', accent='#A0BFE8', paper='#152343', background='#E8EDF8', dark='#293F79', app_background='#E2E9F6', syntax='#F1C880', muted='#647AB6', wordmark='#3856A6'),
    dict(id='iris', name='鸢尾蓝', note='蓝紫 · 浅苔绿', detail='介于蓝与紫之间的鸢尾色，搭配浅苔绿切角。柔和中保留清晰的色彩性格。', color='#716BAD', accent='#C4DCC8', paper='#322D54', background='#EEEDF5', dark='#544E87', app_background='#E6E3F1', syntax='#ECCAAC', muted='#9690C5', wordmark='#544E87'),
    dict(id='teal', name='孔雀青', note='孔雀青 · 嫩叶绿', detail='有深度的青色，配嫩叶绿切角。清新而有分量，适合安静又充满活力的工作台。', color='#347D83', accent='#BCDCA9', paper='#153536', background='#E7EFEC', dark='#285F64', app_background='#E1ECE5', syntax='#E9C786', muted='#67A1A2', wordmark='#285F64'),
    dict(id='jade', name='松石绿', note='松石绿 · 蜂蜜黄', detail='松石绿的身体配蜂蜜黄切角，墨绿双眼让表情更亲近。自然、温暖，保留充实的颜色。', color='#478774', accent='#E5D08B', paper='#173B32', background='#E9F0E7', dark='#316455', app_background='#E1EBDC', syntax='#BDE1C1', muted='#78A592', wordmark='#316455'),
    dict(id='olive', name='橄榄绿', note='橄榄绿 · 谷物黄', detail='温润的橄榄绿配谷物黄，适合偏自然、安定的气质。顶部编辑器细节依然清楚。', color='#727E4E', accent='#E7CB7F', paper='#303820', background='#F0F0E3', dark='#535E36', app_background='#E8E9D8', syntax='#BBCFA5', muted='#9AA474', wordmark='#535E36'),
    dict(id='terracotta', name='陶土橙', note='陶土橙 · 浅杏色', detail='带一点土色的暖橙，搭配浅杏切角。温暖、明快，也有适合长期使用的沉静感。', color='#BC7958', accent='#E8CAA0', paper='#54352A', background='#F6ECE2', dark='#85523F', app_background='#EFE3D3', syntax='#A7C4BC', muted='#D49A78', wordmark='#85523F'),
    dict(id='berry', name='莓果紫', note='莓果紫 · 杏桃色', detail='有浓度的莓果紫，搭配杏桃色切角。亲近、灵动，让小角更有自己的性格。', color='#825879', accent='#E9B496', paper='#392635', background='#F0E8EF', dark='#67405F', app_background='#EBDEE8', syntax='#CFBBDD', muted='#A17C9C', wordmark='#67405F'),
]
_BENCHGO_BY_ID = {p['id']: p for p in BENCHGO_PREVIOUS_PALETTES + BENCHGO_SOFT_PALETTES + BENCHGO_RICH_PALETTES}
BENCHGO_PALETTES = [BENCHGO_ORIGINAL] + [
    dict(_BENCHGO_BY_ID[id], group=group)
    for group, ids in (
        ('blue', ('ice', 'denim', 'cobalt', 'iris')),
        ('green', ('teal', 'jade', 'olive', 'mint')),
        ('warm', ('terracotta', 'berry', 'apricot', 'lilac')),
        ('light', ('sky', 'sage', 'mist', 'sand')),
    ) for id in ids
]
BENCHGO_DEFAULT_ID = 'original'
BENCHGO_DEFAULT = next(p for p in BENCHGO_PALETTES if p['id'] == BENCHGO_DEFAULT_ID)
BRANDS = {
    'routergo': dict(name='RouterGo', concept='专注连接', color='#B94332', accent='#F08D70', paper='#FFF6EE', eye='#351F1B', background='#F6EAE3', app_background='#F6EAE3', dark='#351F1B', expression='专注', domain='routergo.cn'),
    'selfgo': dict(name='SelfGo', concept='轻松整理', color='#265B4C', accent='#80A68C', paper='#F1F3E7', rear='#A8BEA3', background='#EDF1E8', app_background='#DBE6D6', dark='#193E33', expression='轻笑', domain='selfgo.cn'),
    'benchgo': dict(**{k: v for k, v in BENCHGO_DEFAULT.items() if k not in ('id', 'name', 'note', 'detail')}, name='BenchGo', concept='代码伙伴', domain='benchgo.cn'),
}


def expression_eyes(name, micro=False):
    if name == 'routergo':
        return ''.join(f'<path d="M{x+20} 138H{x+70}Q{x+90} 138 {x+90} 158V197A45 45 0 0 1 {x} 197V158Q{x} 138 {x+20} 138Z"/>' for x in (123, 261))
    if name == 'selfgo':
        # Rounded smile arches stay inside the two canonical eye boxes.
        width = 34 if micro else 26
        half = 45-width//2
        return ''.join(f'<path d="M{x-half} 204Q{x} 148 {x+half} 204" fill="none" stroke="currentColor" stroke-width="{width}" stroke-linecap="round"/>' for x in (168, 306))
    return EYES


def face(body, ink, corner, eyes=EYES):
    expression_color = f' color="{ink}"' if eyes != EYES else ''
    return f'<path data-part="body" d="{BODY}" fill="{body}"/><path data-part="corner" d="{CORNER}" fill="{corner}"/><g data-part="eyes" fill="{ink}"{expression_color}>{eyes}</g>'


def monochrome(name, solid, rear='', front='', additional_cut='', eyes=EYES):
    # Remove the main body's full footprint from rear objects, so its eye
    # knockouts always remain transparent rather than showing another layer.
    expression_color = ' color="black"' if eyes != EYES else ''
    return f'''<defs>
      <mask id="{name}-rear" maskUnits="userSpaceOnUse" x="-100" y="-100" width="900" height="650"><rect x="-100" y="-100" width="900" height="650" fill="white"/><path d="{BODY}" fill="black" stroke="black" stroke-width="22"/></mask>
      <mask id="{name}-face" maskUnits="userSpaceOnUse" x="0" y="0" width="600" height="380"><rect width="600" height="380" fill="white"/><g fill="black"{expression_color}>{eyes}</g><path d="M410 380L600 190" fill="none" stroke="black" stroke-width="14"/>{additional_cut}</mask>
    </defs><g mask="url(#{name}-rear)">{rear}</g><path data-part="body" d="{BODY}" fill="{solid}" mask="url(#{name}-face)"/>{front}'''


def drawing(name, mono=False, reverse=False, micro=False, app=False, palette=None, expression=True):
    b = {**BRANDS[name], **(palette or {})}
    solid = '#FFFFFF' if reverse else INK
    eyes = expression_eyes(name, micro) if expression else EYES
    if name == 'routergo':
        # Keep both outputs above the corner, with a single rounded junction.
        route = 'M425 170H474Q494 170 494 150V104Q494 80 518 80H628M474 170H622'
        width = 26 if micro else 20
        endpoint = solid if mono else b['color']
        terminal = (f'<circle cx="628" cy="80" r="16" fill="{endpoint}"/>' if micro else f'<path d="M611 63L628 80L611 97" fill="none" stroke="{endpoint}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>')
        terminal += f'<circle cx="622" cy="170" r="{16 if micro else 14}" fill="{endpoint}"/>'
        outside = f'<path d="M598 80H624M600 170H622" fill="none" stroke="{endpoint}" stroke-width="{width}"/>' + terminal
        if mono:
            cut = f'<path d="{route}" fill="none" stroke="black" stroke-width="{width}" stroke-linecap="round"/>'
            art = monochrome(name, solid, front=outside, additional_cut=cut, eyes=eyes)
        else:
            art = face(b['color'], b['eye'], b['accent'], eyes)
            art += f'<g data-part="routing"><path d="{route}" fill="none" stroke="{b["paper"]}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>{outside}</g>'
        return f'<g transform="translate(105 190)">{art}</g>'
    if name == 'selfgo':
        rear = f'<path data-part="canvas" d="{BODY}" transform="translate(40 -42)" fill="{solid if mono else b["rear"]}"/>'
        art = monochrome(name, solid, rear=rear, eyes=eyes) if mono else rear + face(b['paper'], b['color'], b['accent'], eyes)
        return f'<g transform="translate(100 211)">{art}</g>'
    # The editing strip uses only the clear top area; the canonical body,
    # eyes and corner remain unchanged, with no objects on either side.
    tabs = '<rect x="78" y="45" width="128" height="14" rx="7"/><rect x="230" y="45" width="52" height="14" rx="7"/><rect x="516" y="40" width="10" height="25" rx="3"/>'
    separator = '<path d="M49 82H551" fill="none" stroke="black" stroke-width="5"/>'
    if mono:
        cut = '' if micro else f'<g fill="black">{tabs}</g>{separator}'
        art = monochrome(name, solid, additional_cut=cut)
    else:
        toolbar = '' if micro else f'''<g data-part="editor-strip">
          <rect x="78" y="45" width="128" height="14" rx="7" fill="{b['accent']}"/>
          <rect x="230" y="45" width="52" height="14" rx="7" fill="{b['muted']}"/>
          <rect x="516" y="40" width="10" height="25" rx="3" fill="{b['syntax']}"/>
          <path d="M49 82H551" fill="none" stroke="{b['muted']}" stroke-width="5"/>
        </g>'''
        art = face(b['color'], b['paper'], b['accent']) + toolbar
    return f'<g data-part="placement" transform="translate(120 190)">{art}</g>'


def svg_for(name, variant, size=None, palette=None, expression=True):
    app = variant in ('app', 'favicon')
    b = {**BRANDS[name], **(palette or {})}
    art = drawing(name, mono=variant in ('mono', 'reverse'), reverse=variant == 'reverse', micro=variant == 'favicon', app=app, palette=palette, expression=expression)
    if app:
        bg = b.get('app_background', b['dark'])
        art = f'<rect width="840" height="840" rx="184" fill="{bg}"/><g transform="translate(0 40)">{art}</g>'
    height = 840 if app else 760
    pixels = size or (1024 if app else 840)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{pixels}" height="{pixels if app else round(pixels*height/840)}" viewBox="0 0 840 {height}"><title>{BRANDS[name]["name"]} · 小角 · {variant}</title>{art}</svg>'
