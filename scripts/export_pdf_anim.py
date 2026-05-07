"""V101 PT를 PDF로 export — 애니메이션 9개 슬라이드 모두 final state로 캡처.

전략:
- 페이지 로드 후 모든 `.morphWrap`에 `.expanded` + `.expanded2` 클래스 추가
- 모든 animation duration 강제 0.001s → 즉시 final frame (forwards로 유지)
- 페이지 unlock으로 49 슬라이드 vertical stack 풀어 한 페이지당 1슬라이드
- 1920x1080 페이지 49장
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pathlib import Path
from playwright.sync_api import sync_playwright

URL = 'http://localhost:8881/pt'
OUT = Path(r'C:/Users/USER/Desktop/V101_애니메이션완료.pdf')

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

/* 모든 애니메이션·전환을 즉시 final frame 으로 점프 (forwards 유지) */
*, *::before, *::after {
  animation-delay: 0s !important;
  animation-duration: 0.001s !important;
  animation-iteration-count: 1 !important;
  animation-play-state: running !important;
  transition-delay: 0s !important;
  transition-duration: 0s !important;
}
"""

EXPAND_JS = """() => {
  // morphWrap (id, class hyphen 두 형태) + 비슷한 토글 컨테이너 모두 expanded
  const sel = '#morphWrap, .morph-wrap, .morphWrap, [id*="morphWrap"], [class*="morph-wrap"], [class*="morphWrap"]';
  let cnt = 0;
  document.querySelectorAll(sel).forEach(el => {
    el.classList.add('expanded');
    el.classList.add('expanded2');
    cnt++;
  });
  // 일부 슬라이드의 step / phase / on 활성
  document.querySelectorAll('[class*="step-"], [class*="phase"], [data-step]').forEach(el => {
    el.classList.add('active');
    el.classList.add('on');
    if (el.dataset && 'step' in el.dataset) el.dataset.step = '99';
  });
  // 슬라이드 자체에도 expanded 추가 (CSS rule 호환용)
  document.querySelectorAll('.slide').forEach(el => {
    el.classList.add('expanded');
    el.classList.add('expanded2');
  });
  return cnt;
}"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={'width': 1920, 'height': 1080}, device_scale_factor=1)
    page = ctx.new_page()
    print(f'-> {URL}')
    page.goto(URL, wait_until='networkidle', timeout=60_000)
    page.add_style_tag(content=UNLOCK_CSS)
    morph_count = page.evaluate(EXPAND_JS)
    # animation forwards 적용 + 폰트/이미지 안정화 대기
    time.sleep(3)
    # 다시 한번 expand (re-render 후 추가된 요소 대비)
    page.evaluate(EXPAND_JS)
    time.sleep(1)
    n = page.evaluate('document.querySelectorAll(".slide").length')
    nx = page.evaluate('document.querySelectorAll("#morphWrap.expanded, .morph-wrap.expanded, .morphWrap.expanded").length')
    print(f'slides={n}  morphWrap expanded={nx} (initial morph found={morph_count})')
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
