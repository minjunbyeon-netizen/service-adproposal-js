"""V101 PT를 PDF로 export.

GSAP 가로 슬라이딩(.stage absolute) 구조를 강제 vertical stack 으로 풀어
페이지당 1슬라이드(1920x1080)로 출력.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pathlib import Path
from playwright.sync_api import sync_playwright

URL = 'http://localhost:8881/pt'
OUT = Path('exports/V101.pdf')
OUT.parent.mkdir(parents=True, exist_ok=True)

UNLOCK_CSS = """
html, body { width: 1920px !important; height: auto !important; overflow: visible !important;
             display: block !important; background: #fff !important; }
.stage { width: 1920px !important; height: auto !important; transform: none !important;
         display: block !important; position: relative !important; }
.deck { position: static !important; inset: auto !important; width: 1920px !important;
        height: auto !important; overflow: visible !important; display: block !important; }
.slide { position: relative !important; top: auto !important; left: auto !important;
         visibility: visible !important; opacity: 1 !important; transform: none !important;
         width: 1920px !important; height: 1080px !important; display: flex !important;
         page-break-after: always !important; break-after: page !important;
         overflow: hidden !important; }
.slide:last-child { page-break-after: auto !important; break-after: auto !important; }
.nav-bar, .slide-counter, .key-hint, .vertical-rail, .script-side { display: none !important; }
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 1920, 'height': 1080}, device_scale_factor=1)
    page = context.new_page()
    print(f'-> {URL}')
    page.goto(URL, wait_until='networkidle', timeout=60_000)
    page.add_style_tag(content=UNLOCK_CSS)
    # 폰트·이미지·GSAP 안정화
    time.sleep(3)
    # 슬라이드 개수 검증
    n = page.evaluate('document.querySelectorAll(".slide").length')
    print(f'slides detected: {n}')
    page.pdf(
        path=str(OUT),
        width='1920px',
        height='1080px',
        print_background=True,
        margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
        prefer_css_page_size=False,
    )
    browser.close()

size_mb = OUT.stat().st_size / (1024 * 1024)
print(f'OK: {OUT} ({size_mb:.2f} MB)')
