from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Literal

import resvg_py
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response
from backend.models import Palette, State
from scripts.extract_expressions import SRC_DIR, extract
from backend.renderer import compose as render_svg
from backend.scene_assets import scene_decorations

ROOT = Path(__file__).resolve().parent.parent
CATALOG = json.loads((ROOT / 'backend/data/catalog.json').read_text(encoding='utf-8'))
CATALOG['geometry'] = json.loads((ROOT / '小角IP/geometry.json').read_text(encoding='utf-8'))
CATALOG['decorations'].extend(scene_decorations())
base = [extract(path) for path in sorted(SRC_DIR.glob('sticker-*.svg'))]
assert len(base) == 12, 'Expected 12 original expressions'
base_ids = {e['id'] for e in base}
CATALOG['expressions'] = base + [e for e in CATALOG['expressions'] if e['id'] not in base_ids]
EXPRS = {e['id']: e for e in CATALOG['expressions']}
DECOS = {d['id']: d for d in CATALOG['decorations']}
CATALOG['default_state'] = {'expression': 'expr-01-standard', 'decorations': [], 'palette': CATALOG['palettes'][0]}

def boxes(d):
    return d.get('bboxes', [d['bbox']])

def hit(a, b):
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]

def corner_hit(b):
    x1, y1, x2, y2 = b
    inside = lambda x,y: 410 <= x <= 600 and 190 <= y <= 380 and x+y >= 790
    if any(inside(x,y) for x,y in [(x1,y1),(x1,y2),(x2,y1),(x2,y2)]):
        return True
    if any(x1 <= x <= x2 and y1 <= y <= y2 for x,y in [(410,380),(600,380),(600,190)]):
        return True
    lo, hi = max(410,x1), min(600,x2)
    return lo <= hi and 790-hi <= y2 and 790-lo >= y1

def contrast(a, b):
    def lum(c):
        values = [int(c[i:i+2],16)/255 for i in (1,3,5)]
        values = [v/12.92 if v <= .03928 else ((v+.055)/1.055)**2.4 for v in values]
        return sum(v*w for v,w in zip(values,[.2126,.7152,.0722]))
    a,b = lum(a),lum(b)
    return (max(a,b)+.05)/(min(a,b)+.05)

def check(s: State):
    if s.expression not in EXPRS:
        raise HTTPException(422, 'Unknown expression')
    if len(set(s.decorations)) != len(s.decorations) or any(d not in DECOS for d in s.decorations):
        raise HTTPException(422, 'Unknown or duplicate decoration')
    selected = [DECOS[d] for d in s.decorations]
    if len({d['group'] for d in selected}) != len(selected):
        raise HTTPException(422, 'Only one decoration per attachment point')
    warnings = []
    for i,d in enumerate(selected):
        for b in boxes(d):
            if corner_hit(b): warnings.append(d['name']+'进入切角保护区')
            if not d['covers_eyes'] and any(hit(b,e) for e in [[123,125,213,255],[261,125,351,255]]):
                warnings.append(d['name']+'遮挡眼部')
            if b[0] < -78 or b[1] < -78 or b[2] > 678 or b[3] > 458:
                warnings.append(d['name']+'超出安全区')
        for other in selected[i+1:]:
            if any(hit(a,b) for a in boxes(d) for b in boxes(other)):
                warnings.append(d['name']+'与'+other['name']+'重叠')
    p=s.palette
    for key,label,threshold in [('ink','眼睛',2),('corner','切角',1.25),('accent','点缀',1.25),('blush','腮红',1.25),('fluid','汗泪',1.25),('scene','背景',1.25)]:
        color=getattr(p,key)
        if color and contrast(p.body,color) < threshold:
            warnings.append(label+'与身体对比不足')
    return list(dict.fromkeys(warnings))

def svg(s: State):
    check(s)
    return render_svg(CATALOG['expressions'], CATALOG['geometry'], CATALOG['decorations'], s.palette.model_dump(), s.expression, s.decorations)

app=FastAPI(title='XiaoJiao Generator API',version='1.0.0')

@app.get('/api/health')
def health():
    return {'status':'ok','service':'xiao-jiao-generator'}

@app.get('/api/catalog')
def catalog():
    return CATALOG

@app.post('/api/compose',response_class=Response)
def compose(s:State):
    return Response(svg(s),media_type='image/svg+xml')

@app.post('/api/validate')
def validate(s:State):
    return {'warnings':check(s)}

@app.post('/api/random',response_model=State)
def random_state():
    s=State(expression=random.choice(list(EXPRS)),palette=CATALOG['palettes'][0])
    candidates=[Palette(**p) for p in CATALOG['palettes']]
    random.shuffle(candidates)
    for palette in candidates:
        s.palette=palette
        if not check(s): break
    for d in random.sample(list(DECOS.values()),len(DECOS)):
        if random.random()<.45 and not any(DECOS[x]['group']==d['group'] for x in s.decorations):
            s.decorations.append(d['id'])
            if check(s): s.decorations.pop()
    return s

@app.post('/api/export',response_class=Response)
def export(s:State,format:Literal['svg','png']=Query('svg'),size:int=Query(512)):
    if size not in (240,512,1024): raise HTTPException(422,'Unsupported size')
    content=svg(s)
    if format=='png':
        height=round(size*560/780)
        content=content.replace('width="780" height="560"',f'width="{size}" height="{height}"',1)
        content=bytes(resvg_py.svg_to_bytes(svg_string=content))
    return Response(content,media_type='image/svg+xml' if format=='svg' else 'image/png',headers={'Content-Disposition':f'attachment; filename=xiaojiao-{s.expression}.{format}'})


