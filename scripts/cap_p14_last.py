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
        print(f"슬라이드 {n}장")

        targets = [
            ("p14_4imgs", "모두가"),
            ("last_final", "많이 팔겠"),
        ]
        for fname, keyword in targets:
            for i in range(n):
                page.evaluate(
                    """(i) => {
                    document.querySelectorAll('.slide').forEach((s, idx) => {
                        if (idx === i) s.classList.add('active');
                        else s.classList.remove('active');
                    });
                    window.scrollTo(0, 0);
                }""",
                    i,
                )
                page.wait_for_timeout(300)
                text = page.locator(".slide.active").inner_text()
                if keyword in text:
                    page.screenshot(path=str(OUT / f"{fname}_dom{i:02d}.png"), full_page=False)
                    print(f"  [{fname}] dom idx={i} -> saved")
                    break
        browser.close()


if __name__ == "__main__":
    main()
