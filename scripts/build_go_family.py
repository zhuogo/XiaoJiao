from pathlib import Path
import zipfile
import resvg_py

ROOT=Path(__file__).resolve().parents[1]/'frontend/public/logos/go'
ROOT.mkdir(parents=True,exist_ok=True)
BODY='M95 0H505A95 95 0 0 1 600 95V285A95 95 0 0 1 505 380H95A95 95 0 0 1 0 285V95A95 95 0 0 1 95 0Z'
EYES='<rect x="123" y="125" width="90" height="130" rx="45"/><rect x="261" y="125" width="90" height="130" rx="45"/>'
# Spatial relationship study, following the "Gravity Partner" construction:
# the XiaoJiao body is still the anchor, while one continuous system route
# disappears behind it and returns in front. The ring is a true ellipse, so
# the spatial relationship stays circular rather than becoming a loose ribbon.
# The monochrome artwork remains flat, as required by the identity system.
def draftgo_drawing(mono=False):
    cut_path = 'M410 380H505A95 95 0 0 0 600 285V190Z'
    ring = '<ellipse cx="300" cy="190" rx="370" ry="150" transform="rotate(-28 300 190)" fill="none" stroke="{color}" stroke-width="17"/>'
    # The lower half is the exact same ellipse, brought to the foreground after
    # the body. Start/end points are the ellipse's left/right extremes.
    front_path = 'M-70 190A370 150 0 0 0 670 190'
    ring_transform = 'rotate(-28 300 190)'
    front_ring = f'<path d="{front_path}" transform="{ring_transform}" fill="none" stroke="{{color}}" stroke-width="17" stroke-linecap="round"/>'
    module = '<rect x="598" y="77" width="46" height="46" rx="11" transform="rotate(-28 621 100)" fill="{color}"/>'
    if mono:
        return f'''<defs><mask id="draftgo-knockouts" maskUnits="userSpaceOnUse" x="-90" y="-70" width="790" height="540"><rect x="-90" y="-70" width="790" height="540" fill="white"/><g fill="black">{EYES}</g><path d="M410 380L600 190" fill="none" stroke="black" stroke-width="14"/><path d="{front_path}" transform="{ring_transform}" fill="none" stroke="black" stroke-width="35" stroke-linecap="round"/></mask></defs>
<g transform="translate(120 160)" fill="#222822">
  <g mask="url(#draftgo-knockouts)">{ring.format(color='#222822')}<path d="{BODY}"/></g>
  {front_ring.format(color='#222822')}
  {module.format(color='#222822')}
</g>'''
    # Shared user-space coordinates keep the two strokes identical at joins.
    # Only the ring receives a gradient; the character stays flat and unchanged.
    return f'''<defs><linearGradient id="draftgo-ring-gradient" gradientUnits="userSpaceOnUse" x1="300" y1="40" x2="300" y2="340"><stop offset="0" stop-color="#B8CEF5"/><stop offset="0.5" stop-color="#6187EF"/><stop offset="1" stop-color="#244DE0"/></linearGradient></defs>
<g transform="translate(120 160)">
  {ring.format(color='url(#draftgo-ring-gradient)')}
  <path d="{BODY}" fill="#F1F5FF"/>
  <path d="{cut_path}" fill="#5075E4"/>
  <g fill="#2346AA">{EYES}</g>
  {front_ring.format(color='url(#draftgo-ring-gradient)')}
  {module.format(color='#EE9853')}
</g>'''


DRAWINGS={
'draftgo':draftgo_drawing(),
'routergo':f'''<g transform="translate(105 160)"><path d="{BODY}" fill="#B94332"/><path d="M410 380H505Q600 380 600 285V190Z" fill="#F08D70"/><g fill="#FFF6EE">{EYES}</g><path d="M425 190H476Q504 190 504 162V92Q504 64 532 64H659M504 162V272Q504 300 532 300H640" fill="none" stroke="#FFF6EE" stroke-width="23" stroke-linecap="round" stroke-linejoin="round"/><path d="M632 37L660 64L632 91" fill="none" stroke="#B94332" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/><circle cx="641" cy="300" r="21" fill="#B94332"/></g>''',
'selfgo':f'''<g transform="translate(120 160)"><path d="{BODY}" transform="translate(-25 26) rotate(-7 300 190)" fill="#A4BAAE"/><path d="{BODY}" fill="#265B4C"/><path d="M410 380V252Q410 190 472 190H600Z" fill="#C5DCC6"/><path d="M410 380L600 190L463 247Z" fill="#75A68B"/><g fill="#F3F4E7">{EYES}</g><circle cx="478" cy="73" r="16" fill="#C5DCC6"/><path d="M478 89V112Q478 131 459 131H429" fill="none" stroke="#C5DCC6" stroke-width="10" stroke-linecap="round"/></g>'''
}
for name,drawing in DRAWINGS.items():
    for variant in ('mark','app','mono'):
        content=drawing
        if variant=='mono':
            if name == 'draftgo':
                content = draftgo_drawing(mono=True)
            else:
                import re
                content=re.sub(r'#[0-9A-Fa-f]{6}',lambda m:'#FFFFFF' if m[0] in ('#FFFFFF','#FFF6EE','#F3F4E7','#F2B15A') else '#222822',content)
        bg=''
        if variant=='app':
            bg='<rect width="840" height="840" rx="184" fill="'+{'draftgo':'#E7EDFF','routergo':'#FAEAE2','selfgo':'#E7EEE4'}[name]+'"/>'
            content='<g transform="translate(42 95) scale(.9)">'+content+'</g>'
        height=840 if variant=='app' else 700
        title = 'DraftGo — 小角 · 系统环绕' if name == 'draftgo' else f'{name} — XiaoJiao family concept'
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{1024 if variant=="app" else 840}" height="{1024 if variant=="app" else 700}" viewBox="0 0 840 {height}"><title>{title}</title>{bg}{content}</svg>'
        (ROOT/f'{name}-{variant}.svg').write_text(svg,encoding='utf-8')
        (ROOT/f'{name}-{variant}.png').write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=svg)))
with zipfile.ZipFile(ROOT/'go-family.zip','w',zipfile.ZIP_DEFLATED) as archive:
    for file in ROOT.glob('*'):
        if file.suffix in ('.svg','.png'): archive.write(file,file.name)
print('Created 3 family identities, 18 assets and ZIP')
