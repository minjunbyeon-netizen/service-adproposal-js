from playwright.sync_api import sync_playwright
from pathlib import Path

OUT = Path(r"C:/Users/USER/Desktop/p53_shot.png")
URL = "http://localhost:5000/api/proposals/179/export-html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(800)

    # Directly activate the bookend slide (the one with TAG:Bookend).
    info = page.evaluate("""() => {
      const slides = document.querySelectorAll('.slide');
      let target = -1;
      slides.forEach((s, i) => {
        if (s.innerHTML.includes('Bookend') || s.innerHTML.includes('수미상관') || s.innerHTML.includes('무엇을 기억시킬')) {
          target = i;
        }
      });
      if (target < 0) return { count: slides.length, target: -1 };
      slides.forEach((s, i) => {
        s.style.visibility = (i === target) ? 'visible' : 'hidden';
        s.style.opacity = (i === target) ? '1' : '0';
        s.classList.toggle('active', i === target);
      });
      // Expand bookend morph phases
      const mw = slides[target].querySelector('.morph-wrap');
      if (mw) { mw.classList.add('expanded'); mw.classList.add('expanded2'); }
      return { count: slides.length, target };
    }""")
    print("info:", info)
    page.wait_for_timeout(1500)
    page.screenshot(path=str(OUT), full_page=False)
    print("shot ->", OUT)
    browser.close()
