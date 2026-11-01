"""Non-visual production checks. Start Vite preview on port 4173 first."""
from pathlib import Path
import hashlib
import json
import os
from urllib.parse import urljoin, urlsplit, unquote
import zipfile
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'frontend/public'
BASE_URL = os.environ.get('GALLERY_URL', 'http://127.0.0.1:4173/').rstrip('/') + '/'
PREFIX = urlsplit(BASE_URL).path.rstrip('/')


def deployed(path):
    return PREFIX + path


def check_files():
    items = json.loads((PUBLIC / 'assets/catalog.json').read_text(encoding='utf-8'))
    assert len(items) == 102
    assert len([item for item in items if item['id'].startswith('vi-')]) == 4
    for item in items:
        for key in ['svg', 'png', 'preview', 'pdf', 'bundle', 'guide', 'boardBundle']:
            if item.get(key):
                assert (PUBLIC / item[key].lstrip('/')).is_file(), item
    with zipfile.ZipFile(PUBLIC / 'assets/xiaojiao-assets.zip') as archive:
        assert len(archive.namelist()) == len(set(archive.namelist()))
        assert not any('.sqlite' in name for name in archive.namelist())
        assert archive.testzip() is None
    snapshot = ROOT / 'out/asset-preservation.json'
    if snapshot.exists():
        before = json.loads(snapshot.read_text(encoding='utf-8'))
        for path, sha in before.items():
            assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha, path
        print(f'Preserved {len(before)} original files byte for byte.')


def check_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 1000})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(BASE_URL, wait_until='networkidle')
        expect(page).to_have_title('小角 · 图标展厅')
        assert page.get_by_text('我的项目', exact=True).count() == 0
        expect(page.locator('.hero-object')).to_have_count(4)
        page.get_by_role('button', name='查看 BenchGo', exact=True).click()
        page.locator('.palette-label select').select_option('sky')
        expect(page.locator('.product-art img')).to_have_attribute('src', deployed('/logos/go/v2/benchgo-sky-mark.png'))
        page.locator('.product-controls').get_by_role('button', name='单色', exact=True).click()
        expect(page.locator('.palette-label select')).to_be_disabled()
        expect(page.locator('.product-art img')).to_have_attribute('src', deployed('/logos/go/v2/benchgo-mono.png'))
        for name in ['DraftGo', 'RouterGo', 'SelfGo', 'BenchGo']:
            page.locator('.product-tabs').get_by_role('button', name=name).click()
            for label in ['品牌标志', '应用图标', '单色']:
                page.locator('.product-controls').get_by_role('button', name=label, exact=True).click()
                src = page.locator('.product-art img').get_attribute('src')
                assert page.request.get(urljoin(BASE_URL, src)).ok
        page.locator('.case').first.click()
        expect(page.locator('dialog')).to_be_visible()
        page.get_by_role('button', name='小角基准', exact=True).click()
        expect(page.locator('.detail-art img')).to_have_attribute('src', deployed('/logos/studies/orbital-base-mark.png'))
        page.locator('dialog').get_by_role('button', name='应用图标', exact=True).click()
        with page.expect_download() as download:
            page.locator('dialog').get_by_role('link', name='下载 SVG').click()
        assert download.value.suggested_filename == 'orbital-base-app.svg'
        page.keyboard.press('Escape')
        expect(page.locator('dialog')).not_to_be_visible()
        expect(page.locator('.case').first).to_be_focused()
        page.locator('.library-tabs').get_by_role('button', name='表情', exact=True).click()
        expect(page.locator('.asset-grid button')).to_have_count(21)
        page.get_by_role('searchbox').fill('思考')
        expect(page.locator('.asset-grid button')).to_have_count(1)
        page.locator('.asset-grid button').click()
        expect(page.locator('#detail-title')).to_have_text('思考')
        page.get_by_role('button', name='关闭详情').click()
        page.get_by_role('searchbox').fill('不存在的资产')
        expect(page.get_by_role('status')).to_contain_text('没有找到')
        for group in ['基准', '装饰', '配色', '历史', '展板']:
            page.locator('.library-tabs').get_by_role('button', name=group, exact=True).click()
            assert page.locator('.asset-grid button').count() > 0
        page.locator('.asset-grid').get_by_role('button', name='DraftGo · VI 资产包').click()
        expect(page.locator('#detail-title')).to_have_text('DraftGo · VI 资产包')
        with page.expect_download() as vi_download:
            page.locator('dialog').get_by_role('link', name='下载展板 PDF').click()
        assert vi_download.value.suggested_filename == 'draftgo-vi.pdf'
        with page.expect_download() as package_download:
            page.locator('dialog').get_by_role('link', name='下载完整 VI 资产包').click()
        assert package_download.value.suggested_filename == 'draftgo-vi-assets.zip'
        expect(page.locator('dialog').get_by_role('link', name='下载品牌规范手册')).to_have_attribute('href', deployed('/logos/vi/draftgo-vi-guidelines.pdf'))
        expect(page.locator('dialog').get_by_role('link', name='仅下载展板文件包')).to_have_attribute('href', deployed('/logos/vi/draftgo-vi.zip'))
        expect(page.get_by_role('link', name='四产品完整 VI 资产包')).to_have_attribute('href', deployed('/logos/vi/go-family-vi-assets.zip'))
        page.keyboard.press('Escape')
        page.get_by_role('button', name='暂停动态').click()
        expect(page.locator('.gallery')).to_have_class('gallery paused')
        for width in [1440, 768, 390]:
            page.set_viewport_size({'width': width, 'height': 900})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), width
        page.emulate_media(reduced_motion='reduce')
        assert page.locator('.hero-object img').first.evaluate("e => getComputedStyle(e).animationName") == 'none'
        # Every downloadable target and image source on the page must resolve to a file,
        # rather than Vite's SPA fallback HTML.
        for url in page.locator('a[download], img').evaluate_all("els => [...new Set(els.map(e => e.getAttribute('href') || e.getAttribute('src')))]"):
            if url:
                assert url.startswith(PREFIX + '/'), url
                assert (PUBLIC / unquote(url[len(PREFIX):]).lstrip('/')).is_file(), url
        assert not errors, errors
        browser.close()
    print('Production interactions, downloads, reduced motion and responsive boundaries passed.')


if __name__ == '__main__':
    check_files()
    check_browser()
