"""Expose a small, stable static interface from the verified VI delivery ZIPs."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'frontend/public'
DELIVERIES = PUBLIC / 'logos/vi/delivery-catalog.json'
EXPORTS = {
    'logo.svg': '02-品牌标识/symbol-color.svg',
    'logo.png': '02-品牌标识/symbol-color.png',
    'logo-mono.svg': '02-品牌标识/symbol-mono.svg',
    'logo-reverse.svg': '02-品牌标识/symbol-reverse.svg',
    'horizontal.svg': '02-品牌标识/horizontal-color.svg',
    'horizontal-mono.svg': '02-品牌标识/horizontal-mono.svg',
    'horizontal-reverse.svg': '02-品牌标识/horizontal-reverse.svg',
    'app.svg': '03-应用图标/app.svg',
    'icon-192.png': '03-应用图标/icon-192.png',
    'icon-512.png': '03-应用图标/icon-512.png',
    'maskable-512.png': '03-应用图标/maskable-512.png',
    'apple-touch-icon.png': '03-应用图标/apple-touch-icon.png',
    'favicon.svg': '03-应用图标/favicon.svg',
    'favicon.ico': '03-应用图标/favicon.ico',
    'tokens.json': '04-色彩与字体/design-tokens.json',
    'variables.css': '04-色彩与字体/variables.css',
}
ROLES = dict(draftgo='开发底座', routergo='模型连接', selfgo='思考画布', benchgo='全天候助手')


def file_record(path):
    data = path.read_bytes()
    return dict(path=path.relative_to(PUBLIC).as_posix(), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def build():
    manifest = dict(schemaVersion=1, assetVersion='1.0.0', signature='卓越构建', pathBase='Resolve file paths relative to this manifest URL', usage='Public access does not grant a trademark or asset license. See BRAND-USAGE.md.', products={})
    for delivery in json.loads(DELIVERIES.read_text(encoding='utf-8')):
        target = PUBLIC / 'vi' / delivery['id']
        target.mkdir(parents=True, exist_ok=True)
        package = PUBLIC / delivery['bundle'].lstrip('/')
        assert file_record(package)['sha256'] == delivery['sha256'], package
        files = {}
        with zipfile.ZipFile(package) as archive:
            prefix = delivery['name'] + '-VI/'
            records = {item['path']: item for item in json.loads(archive.read(prefix + '00-使用说明/manifest.json'))['files']}
            for name, source in EXPORTS.items():
                data = archive.read(prefix + source)
                assert hashlib.sha256(data).hexdigest() == records[source]['sha256']
                path = target / name
                path.write_bytes(data)
                files[name] = file_record(path)
        files['package'] = file_record(package)
        files['guidelines'] = file_record(PUBLIC / delivery['guide'].lstrip('/'))
        manifest['products'][delivery['id']] = dict(name=delivery['name'], role=ROLES[delivery['id']], files=files)
    manifest['familyPackage'] = file_record(PUBLIC / 'logos/vi/go-family-vi-assets.zip')
    (PUBLIC / 'vi-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    # This notice is served alongside the public assets; it does not invent an open license.
    usage_source = ROOT / 'BRAND-USAGE.md'
    if usage_source.exists():
        (PUBLIC / 'BRAND-USAGE.md').write_bytes(usage_source.read_bytes())
    print('Published stable static paths for four products; all exported bytes match verified packages.')


if __name__ == '__main__':
    build()
