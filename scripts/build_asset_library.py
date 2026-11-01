"""Build the public asset index from preserved originals; never rewrite source artwork."""
from pathlib import Path
import json
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.app import CATALOG, svg
from backend.models import State
import resvg_py

PUBLIC = ROOT / 'frontend/public'
DEST = PUBLIC / 'assets'
DEST.mkdir(exist_ok=True)
items = []


def add(name, group, source, png=None):
    source = Path(source)
    if source.is_relative_to(PUBLIC):
        path = '/' + source.relative_to(PUBLIC).as_posix()
    else:
        target = DEST / 'originals' / source.relative_to(ROOT / '小角IP')
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        path = '/' + target.relative_to(PUBLIC).as_posix()
    items.append(dict(id=str(len(items)), name=name, group=group, svg=path,
                      png='/' + png.relative_to(PUBLIC).as_posix() if png else None))


def render(name, group, key, expression='expr-01-standard', decorations=None, palette=None):
    state = State(expression=expression, decorations=decorations or [], palette=palette or CATALOG['palettes'][0])
    text = svg(state)
    target = DEST / (key + '.svg')
    target.write_text(text, encoding='utf-8')
    png = target.with_suffix('.png')
    png.write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=text.replace('width="780" height="560"', 'width="390" height="280"', 1))))
    add(name, group, target, png)


for folder in ['00-基板', '01-主标识', '02-应用图标', '03-社交头像', '06-网站favicon']:
    for source in sorted((ROOT / '小角IP' / folder).rglob('*.svg')):
        add(source.stem.replace('小角-', ''), '基准', source)
extra_names = {13:'闪闪', 14:'斜眼', 15:'无语', 16:'害羞', 18:'惊恐', 19:'可怜', 20:'盯', 21:'思考', 22:'窃喜'}
for expr in CATALOG['expressions']:
    render(extra_names.get(expr['no'], expr['name']), '表情', expr['id'], expression=expr['id'])
deco_names = ['毛线帽','棒球帽','贝雷帽','蝴蝶结','发夹','圣诞帽','圆框眼镜','墨镜','围巾','爱心','睡眠 ZZZ','书本','账本','完成','查找','提醒','进度']
for deco, name in zip(CATALOG['decorations'], deco_names, strict=True):
    render(name, '装饰', deco['id'], decorations=[deco['id']])
for palette, name in zip(CATALOG['palettes'], ['原味','墨玉','蜜桃','抹茶','海盐','樱花','落日','夜航'], strict=True):
    render(name, '配色', 'palette-' + palette['id'], palette=palette)
for item in json.loads((PUBLIC / 'logos/collection.json').read_text(encoding='utf-8')):
    add(item['name'], '配色', PUBLIC / 'logos' / (item['id'] + '-mark.svg'), PUBLIC / 'logos' / (item['id'] + '-mark.png'))
for item in json.loads((ROOT / 'frontend/src/data/benchgo-palettes.json').read_text(encoding='utf-8')):
    stem = PUBLIC / 'logos/go/v2' / (item['stem'] + '-mark')
    add('BenchGo · ' + item['name'], '配色', stem.with_suffix('.svg'), stem.with_suffix('.png'))
for name in ['draftgo', 'routergo', 'selfgo']:
    add(name + ' · 初版', '历史', PUBLIC / 'logos/go' / (name + '-mark.svg'), PUBLIC / 'logos/go' / (name + '-mark.png'))
for source in sorted((PUBLIC / 'logos/lab').glob('*.svg')):
    add(source.stem + ' · 形态实验', '历史', source, source.with_suffix('.png'))
for source in sorted((ROOT / '小角IP/05-VI展板').glob('*.svg')):
    add(source.stem, '展板', source)
for name, filename in [('产品家族','logos/go/v2/go-family-board.png'),('形态案例','logos/studies/form-studies-board.png'),('BenchGo 配色','logos/go/v2/benchgo-palette-board.png'),('BenchGo 形态对比','logos/go/v2/benchgo-comparison.png')]:
    add(name, '展板', PUBLIC / filename)
vi_catalog = PUBLIC / 'logos/vi/catalog.json'
if vi_catalog.exists():
    delivery_file = PUBLIC / 'logos/vi/delivery-catalog.json'
    deliveries = {entry['id']: entry for entry in json.loads(delivery_file.read_text(encoding='utf-8'))} if delivery_file.exists() else {}
    for board in json.loads(vi_catalog.read_text(encoding='utf-8')):
        stem = '/logos/vi/' + board['stem']
        delivery = deliveries.get(board['id'])
        item = dict(id='vi-' + board['id'], name=board['name'], group='展板',
                    svg=stem + '.svg', png=stem + '.png', preview=stem + '-preview.jpg',
                    pdf=stem + '.pdf', bundle=stem + '.zip')
        if delivery:
            item.update(name=delivery['name'] + ' · VI 资产包', bundle=delivery['bundle'],
                        guide=delivery['guide'], boardBundle=stem + '.zip', fileCount=delivery['files'])
        items.append(item)
(DEST / 'catalog.json').write_text(json.dumps(items, ensure_ascii=False), encoding='utf-8')
# Include source artwork and the four complete delivery packages, but no redundant
# family ZIPs, other nested archives or private project data.
with zipfile.ZipFile(DEST / 'xiaojiao-assets.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for folder in [ROOT / '小角IP', PUBLIC / 'logos']:
        for path in sorted(folder.rglob('*')):
            if path.is_file() and path.suffix.lower() not in {'.zip', '.pyc'}:
                archive.write(path, path.relative_to(ROOT if folder.name == '小角IP' else PUBLIC))
    for package in sorted((PUBLIC / 'logos/vi').glob('*-vi-assets.zip')):
        if not package.name.startswith('go-family-'):
            archive.write(package, package.relative_to(PUBLIC))
    archive.write(ROOT / 'backend/data/catalog.json', 'modules/source-catalog.json')
    for path in sorted(DEST.glob('*')):
        if path.suffix in {'.svg', '.png', '.json'}:
            archive.write(path, 'modules/' + path.name)
print(f'Built {len(items)} indexed assets and complete archive.')
