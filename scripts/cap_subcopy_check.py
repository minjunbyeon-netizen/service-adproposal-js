# -*- coding: utf-8 -*-
"""P22, P23, P25, P26, P27 서브카피 가독성 진단용 캡처."""
from playwright.sync_api import sync_playwright
from pathlib import Path

URL = "http://localhost:8881/api/proposals/179/export-html"
OUT = Path(__file__).resolve().parent / "subcopy_check"
OUT.mkdir(exist_ok=True)

PAGES = [22, 23, 25, 26, 27]


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1600, "height": 900})
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(1200)
        for pt_num in PAGES:
            slide_idx = pt_num - 1
            page.evaluate(
                """(i) => {
                document.querySelectorAll('.slide').forEach((s, idx) => {
                    if (idx === i) s.classList.add('active');
                    else s.classList.remove('active');
                });
                window.scrollTo(0, 0);
            }""",
                slide_idx,
            )
            page.wait_for_timeout(400)
            path = OUT / f"p{pt_num:02d}.png"
            page.screenshot(path=str(path), full_page=False)
            print(f"P{pt_num} -> {path.name}")
        browser.close()


if __name__ == "__main__":
    main()
