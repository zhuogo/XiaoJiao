"""Validate delivered VI files without visual inspection or extra build dependencies.

PDF page count additionally uses the project's available pypdf test dependency.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import hashlib
import io
import json
import re
import zipfile

from PIL import Image, ImageChops
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'frontend/public/logos/vi'
SOURCE=ROOT/'frontend/public/logos/go/v2'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check_svg(data):
    root=ET.fromstring(data)
    ids=[node.get('id') for node in root.iter() if node.get('id')]
    assert len(ids)==len(set(ids)), 'Duplicate SVG IDs'
    references=[]
    for node in root.iter():
        for name,value in node.attrib.items():
            references.extend(re.findall(r'url\(#([^)]*)\)',value))
            if name.endswith('href'):
                assert value.startswith(('#','data:image/')), 'External SVG asset'
                if value.startswith('#'):
                    references.append(value[1:])
    assert set(references).issubset(ids), 'Unresolved SVG references'


def check():
    catalog=json.loads((OUT/'delivery-catalog.json').read_text(encoding='utf-8'))
    assert len(catalog)==4
    package_files={}
    for entry in catalog:
        id,name=entry['id'],entry['name']
        archive=OUT/Path(entry['bundle']).name
        assert digest_file(archive)==entry['sha256']
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            names=z.namelist()
            assert len(names)==len(set(names))==entry['files']
            assert all(n.startswith(name+'-VI/') and '..' not in Path(n).parts for n in names)
            assert not any(n.endswith(('.zip','.sqlite3','.ttf','.ttc','.woff','.woff2')) for n in names)
            prefix=name+'-VI/'
            files={n.removeprefix(prefix):z.read(n) for n in names}
            assert len({n.split('/')[0] for n in files})==8
            manifest=json.loads(files['00-使用说明/manifest.json'])
            checksums=files['00-使用说明/checksums.sha256'].decode().splitlines()
            for line in checksums:
                checksum,path=line.split('  ',1)
                assert sha(files[path])==checksum, path
            assert len(checksums)==len(files)-1
            assert len(manifest['files'])==len(files)-2
            for record in manifest['files']:
                assert sha(files[record['path']])==record['sha256']
                assert len(files[record['path']])==record['bytes']
                if record['path'].endswith('.png'):
                    image=Image.open(io.BytesIO(files[record['path']]))
                    assert image.size==(record['width'],record['height'])
            for path,data in files.items():
                if path.endswith('.svg'):
                    check_svg(data)
            assert len(PdfReader(io.BytesIO(files['01-品牌规范/品牌规范手册.pdf'])).pages)==6
            assert len(PdfReader(OUT/f'{id}-vi-guidelines.pdf').pages)==6
            for form in ['symbol','horizontal','vertical','wordmark']:
                for variant in ['color','mono','reverse']:
                    for ext in ['svg','png']:
                        assert f'02-品牌标识/{form}-{variant}.{ext}' in files
                    image=Image.open(io.BytesIO(files[f'02-品牌标识/{form}-{variant}.png'])).convert('RGBA')
                    assert image.getchannel('A').getextrema()==(0,255)
                    if variant=='reverse':
                        pixels = image.get_flattened_data() if hasattr(image, 'get_flattened_data') else image.getdata()
                        for r,g,b,a in pixels:
                            if a>0:
                                assert (r,g,b)==(255,255,255), (form,r,g,b)
                    if form!='symbol':
                        box=image.getchannel('A').getbbox()
                        assert box[0]>0 and box[1]>0 and box[2]<image.width and box[3]<image.height, form
            token=json.loads(files['04-色彩与字体/design-tokens.json'])
            assert token['signature']=='卓越构建'
            assert token['contrast']['body']['normalTextAA']
            assert token['contrast']['button']['normalTextAA']
            for size in [16,32,48,64,180,192,512]:
                data=files[f'03-应用图标/icon-{size}.png']
                assert data==(SOURCE/f'{id}-icon-{size}.png').read_bytes()
                assert Image.open(io.BytesIO(data)).size==(size,size)
            manifest_web=json.loads(files['03-应用图标/site.webmanifest'])
            for icon in manifest_web['icons']:
                assert '03-应用图标/'+icon['src'] in files
            maskable=Image.open(io.BytesIO(files['03-应用图标/maskable-512.png'])).convert('RGBA')
            assert maskable.getchannel('A').getextrema()==(255,255)
            bg=Image.new('RGB',maskable.size,token['colors']['surface'])
            diff=ImageChops.difference(maskable.convert('RGB'),bg)
            box=diff.getbbox()
            assert box
            assert all((x-256)**2+(y-256)**2 <= (512*.4)**2 for x in [box[0],box[2]] for y in [box[1],box[3]]), box
            sizes={'avatar':(1024,1024),'social-share':(1200,630),'presentation-cover':(1920,1080),'welcome-screen':(1440,900),'business-card-front':(1050,600),'business-card-back':(1050,600)}
            for stem,size in sizes.items():
                assert Image.open(io.BytesIO(files[f'06-应用模板/{stem}.png'])).size==size
            provenance=json.loads(files['07-源文件/provenance.json'])
            for filename,checksum in provenance['sources'].items():
                assert digest_file(SOURCE/filename)==checksum
            for variant in ['mark','app','mono']:
                assert files[f'07-源文件/{id}-{variant}-original.svg']==(SOURCE/f'{id}-{variant}.svg').read_bytes()
            package_files.update({prefix+path:sha(data) for path,data in files.items()})
            print(f'{name}: {len(files)} files, six-page guide, source preservation, SVGs, PNGs, tokens, templates and checksums passed.')
    with zipfile.ZipFile(OUT/'go-family-vi-assets.zip') as z:
        assert z.testzip() is None
        assert set(z.namelist())==set(package_files)
        assert all(sha(z.read(path))==checksum for path,checksum in package_files.items())
    # Old board-only download remains board-only, not an accidental giant package.
    with zipfile.ZipFile(OUT/'go-family-vi.zip') as z:
        assert not any('assets' in name or 'guidelines' in name or 'delivery' in name for name in z.namelist())
    print('Family delivery ZIP contains the four complete directories; legacy board ZIP preserved.')


def digest_file(path):
    return sha(path.read_bytes())


if __name__=='__main__':
    check()
