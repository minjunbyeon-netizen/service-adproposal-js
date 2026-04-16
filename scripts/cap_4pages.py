# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
from pathlib import Path

URL = "http://localhost:8881/api/proposals/179/export-html"
OUT = Path(__file__).resolve().parent / "p37_p39_shots"


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
            ("p02_swap", "기억시킬 것이냐"),
            ("p39_table_center", "3채널 통합 운영"),
            ("p44_3tier", "3계층"),
            ("p47_bookend", "2026년 기억"),
            ("p48_thanks", "감사합니다"),
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
                page.wait_for_timeout(220)
                text = page.locator(".slide.active").inner_text()
                if keyword in text:
                    page.screenshot(path=str(OUT / f"{fname}.png"), full_page=False)
                    print(f"  [{fname}] dom={i} saved")
                    break
        browser.close()


if __name__ == "__main__":
    main()
