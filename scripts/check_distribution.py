"""Dependency-free CI checks for the committed static asset distribution."""
from pathlib import Path
from html.parser import HTMLParser
import argparse
import hashlib
import json
import re
import zipfile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'frontend/public'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def record_check(record, base):
    relative = Path(record['path'])
    assert not relative.is_absolute() and '..' not in relative.parts
    path = base / relative
    assert path.is_file(), path
    data = path.read_bytes()
    assert len(data) == record['bytes'] and sha(data) == record['sha256'], path


def check():
    manifest = json.loads((PUBLIC / 'vi-manifest.json').read_text(encoding='utf-8'))
    assert manifest['schemaVersion'] == 1
    assert set(manifest['products']) == {'draftgo','routergo','selfgo','benchgo'}
    count = 0
    for product in manifest['products'].values():
        for record in product['files'].values():
            record_check(record, PUBLIC)
            count += 1
            if record['path'].endswith('.svg'):
                doc = ET.parse(PUBLIC / record['path'])
                ids = [n.get('id') for n in doc.iter() if n.get('id')]
                assert len(ids) == len(set(ids))
                for node in doc.iter():
                    for name, value in node.attrib.items():
                        assert all(ref in ids for ref in re.findall(r'url\(#([^)]*)\)', value))
                        if name.endswith('href'):
                            assert value.startswith(('#','data:image/'))
        package = PUBLIC / product['files']['package']['path']
        with zipfile.ZipFile(package) as archive:
            names = archive.namelist()
            assert len(names) == len(set(names))
            assert archive.testzip() is None
            assert not any('..' in Path(name).parts or name.startswith('/') for name in names)
            assert not any(name.endswith(('.sqlite3','.env','.ttf','.ttc','.woff','.woff2')) for name in names)
            prefix = product['name'] + '-VI/'
            index = json.loads(archive.read(prefix + '00-使用说明/manifest.json'))
            for entry in index['files']:
                data = archive.read(prefix + entry['path'])
                assert sha(data) == entry['sha256'] and len(data) == entry['bytes']
            assert len(index['files']) + 2 == len(names)
    record_check(manifest['familyPackage'], PUBLIC)
    assets = json.loads((PUBLIC / 'assets/catalog.json').read_text(encoding='utf-8'))
    for item in assets:
        for key in ['svg','png','preview','pdf','guide','bundle','boardBundle']:
            if item.get(key):
                assert (PUBLIC / item[key].lstrip('/')).is_file(), item[key]
    forbidden = [p for p in PUBLIC.rglob('*') if p.is_file() and (p.name.startswith('.env') or '.sqlite' in p.name or p.suffix in {'.log','.pyc'})]
    assert not forbidden, forbidden
    print(f'Static distribution passed: {len(assets)} library entries, {count} verified file references, four complete VI packages.')


class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag in {'script','link'}:
            attrs = dict(attrs)
            path = attrs.get('src') or attrs.get('href')
            if path:
                self.urls.append(path)


def check_dist(folder, base):
    parser = Assets()
    parser.feed((folder / 'index.html').read_text(encoding='utf-8'))
    for url in parser.urls:
        assert url.startswith(base), (url, base)
        assert (folder / url[len(base):]).is_file(), url
    distribution = json.loads((folder / 'vi-manifest.json').read_text(encoding='utf-8'))
    for product in distribution['products'].values():
        for record in product['files'].values():
            record_check(record, folder)
    assert not (folder / 'backend').exists()
    assert not (folder / 'archive').exists()
    assert not (folder / 'node_modules').exists()
    print(f'Production artifact passed: base {base}, static distribution and no private runtime directories.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dist', type=Path)
    parser.add_argument('--base', default='/')
    args = parser.parse_args()
    check()
    if args.dist:
        assert args.base.startswith('/') and args.base.endswith('/')
        check_dist(args.dist, args.base)
