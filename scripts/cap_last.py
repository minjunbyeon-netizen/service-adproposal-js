# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
from pathlib import Path

URL = "http://localhost:8881/api/proposals/179/export-html"
OUT = Path(__file__).resolve().parent / "p37_p39_shots"
OUT.mkdir(exist_ok=True)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1600, "height": 900})
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(1000)
        n = page.locator(".slide").count()
        last_i = n - 1
        page.evaluate(
            """(i) => {
            document.querySelectorAll('.slide').forEach((s, idx) => {
                if (idx === i) s.classList.add('active');
                else s.classList.remove('active');
            });
            window.scrollTo(0, 0);
        }""",
            last_i,
        )
        page.wait_for_timeout(400)
        page.screenshot(path=str(OUT / "last_slide.png"), full_page=False)
        print(f"마지막장 저장 (idx={last_i})")
        browser.close()


if __name__ == "__main__":
    main()
