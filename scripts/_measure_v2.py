"""영상 wrapper(#0a0a0a 검정 박스) bbox 측정 + 라벨 위치 측정."""
import json, time, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright

URL = 'http://localhost:8881/pt'
UNLOCK = """
html, body { width: 1920px !important; height: auto !important; overflow: visible !important;
             display: block !important; }
.stage { width: 1920px !important; height: auto !important; transform: none !important;
         display: block !important; position: relative !important; }
.deck { position: static !important; inset: auto !important; width: 1920px !important;
        height: auto !important; overflow: visible !important; display: block !important; }
.slide { position: relative !important; top: auto !important; left: auto !important;
         visibility: visible !important; opacity: 1 !important; transform: none !important;
         width: 1920px !important; height: 1080px !important; display: flex !important;
         overflow: hidden !important; }
"""

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()
    page.goto(URL, wait_until='networkidle', timeout=60_000)
    page.add_style_tag(content=UNLOCK)
    time.sleep(2)
    out = page.evaluate(r"""() => {
        const slides = Array.from(document.querySelectorAll('.slide'));
        const result = [];
        slides.forEach((slide, idx) => {
            const sR = slide.getBoundingClientRect();
            slide.querySelectorAll('video').forEach(v => {
                // wrapper = video 의 가장 가까운 background:#0a0a0a div
                let wrap = v.parentElement;
                while (wrap && !(wrap.style && wrap.style.background && /0a0a0a/i.test(wrap.style.background))) {
                    wrap = wrap.parentElement;
                    if (!wrap || wrap === slide) break;
                }
                const wR = wrap ? wrap.getBoundingClientRect() : v.getBoundingClientRect();
                const vR = v.getBoundingClientRect();
                // 라벨: video 다음 sibling
                let label = v.nextElementSibling;
                const lR = label ? label.getBoundingClientRect() : null;
                result.push({
                    slide: idx + 1,
                    src: (v.querySelector('source')?.src || v.src || '').split('/').pop(),
                    wrap: {x: wR.left - sR.left, y: wR.top - sR.top, w: wR.width, h: wR.height},
                    video: {x: vR.left - sR.left, y: vR.top - sR.top, w: vR.width, h: vR.height},
                    label: lR ? {x: lR.left - sR.left, y: lR.top - sR.top, w: lR.width, h: lR.height,
                                 text: label.textContent.trim()} : null,
                });
            });
        });
        return result;
    }""")
    b.close()

print(json.dumps(out, ensure_ascii=False, indent=2))
