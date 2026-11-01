"""Structural XiaoJiao studies, kept separate from the canonical character assets."""
from pathlib import Path
import resvg_py

ROOT = Path(__file__).resolve().parents[1] / 'frontend/public/logos/lab'
ROOT.mkdir(parents=True, exist_ok=True)
body = 'M95 0H505A95 95 0 0 1 600 95V285A95 95 0 0 1 505 380H95A95 95 0 0 1 0 285V95A95 95 0 0 1 95 0Z'
eyes = '<rect x="123" y="125" width="90" height="130" rx="45"/><rect x="261" y="125" width="90" height="130" rx="45"/>'
fold = 'M410 380H505A95 95 0 0 0 600 285V190Z'
def character(color, ink, corner):
    return f'<path d="{body}" fill="{color}"/><path d="{fold}" fill="{corner}"/><g fill="{ink}">{eyes}</g>'

studies = {
 'folio': f'''<g transform="translate(120 145) rotate(-8 300 190)">
 <path d="{body}" transform="translate(-24 36)" fill="#93B5A3"/><path d="{body}" transform="translate(-12 18)" fill="#C5D9C7"/>
 <path d="M95 0H505A95 95 0 0 1 600 95V190L410 380H95A95 95 0 0 1 0 285V95A95 95 0 0 1 95 0Z" fill="#F5F8EC"/>
 <path d="M410 380V252Q410 190 472 190H600Z" fill="#3F8061"/><path d="M410 380L600 190L459 247Z" fill="#75AC86"/>
 <g fill="#214A38">{eyes}</g><path d="M77 68H196" stroke="#C2D5BE" stroke-width="9" stroke-linecap="round"/>
 </g>''',
 'pulse': f'''<g transform="translate(120 160)"><path d="{body}" fill="#252E38"/><path d="{fold}" fill="#FF7156"/>
 <g fill="#F4F3EB"><rect x="124" y="130" width="42" height="120" rx="21"/><rect x="183" y="100" width="42" height="180" rx="21"/><rect x="242" y="142" width="42" height="96" rx="21"/><rect x="301" y="120" width="42" height="140" rx="21"/></g>
 <path d="M420 105Q458 140 420 175M449 83Q510 140 449 197" fill="none" stroke="#FF7156" stroke-width="12" stroke-linecap="round"/>
 </g>''',
 'orbit': f'''<g transform="translate(120 160)"><ellipse cx="300" cy="190" rx="370" ry="118" transform="rotate(-28 300 190)" fill="none" stroke="#77A8C3" stroke-width="17"/>
 {character('#F1F8FA','#22506B','#4A90B6')}
 <path d="M-20 362C94 427 450 307 621 101" fill="none" stroke="#22506B" stroke-width="17" stroke-linecap="round"/>
 <circle cx="545" cy="192" r="24" fill="#EF8D4E"/><path d="M628 23V61M609 42H647" stroke="#EF8D4E" stroke-width="10" stroke-linecap="round"/>
 </g>''',
 'stride': f'''<g transform="translate(120 120) rotate(-9 300 190)">
 <path d="M154 353L125 451L55 451M399 355L465 422L526 393" fill="none" stroke="#323D31" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
 <path d="M15 213L-37 260M580 152L648 88" fill="none" stroke="#323D31" stroke-width="27" stroke-linecap="round"/>
 {character('#E9F08F','#323D31','#6D9561')}
 <path d="M-35 105H-73M-25 151H-92" stroke="#A9B87C" stroke-width="13" stroke-linecap="round"/>
 </g>''',
 'ribbon': f'''<g transform="translate(120 160)"><path d="{body}" fill="#763450"/>
 <path d="M410 380H505Q600 380 600 285V190L410 380L329 461L320 385L246 381L410 217Z" fill="#E9A6BB"/>
 <path d="M410 217L491 299L410 380L329 299Z" fill="#F9DDE6"/>
 <g fill="#FFF2EC">{eyes}</g><path d="M444 346L491 299" stroke="#AC5274" stroke-width="5"/>
 </g>''',
 'portal': f'''<defs><mask id="cut"><rect width="840" height="700" fill="white"/><g transform="translate(120 160)" fill="black">{eyes}<path d="M410 380L600 190V380Z"/></g></mask></defs>
 <g mask="url(#cut)"><g transform="translate(120 160)"><path d="{body}" fill="#303A36"/></g></g>
 <path d="M552 541L720 373V450Q720 540 630 540Z" fill="#D37B51"/>
 <path d="M698 177L723 152M729 214H764" stroke="#D37B51" stroke-width="12" stroke-linecap="round"/>''',
}
for name, drawing in studies.items():
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="840" height="700" viewBox="0 0 840 700"><title>XiaoJiao {name}</title>{drawing}</svg>'
    (ROOT/f'{name}.svg').write_text(svg,encoding='utf-8')
    (ROOT/f'{name}.png').write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=svg)))
print('Built six structural logo studies')
