# -*- coding: utf-8 -*-
"""Playwright로 리팩토링 후 V101 재캡처."""
from playwright.sync_api import sync_playwright
from pathlib import Path

URL = "http://localhost:8881/api/proposals/179/export-html"
OUT = Path(__file__).resolve().parent / "v101_shots_v2"
OUT.mkdir(exist_ok=True)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1600, "height": 900})
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(1000)
        n = page.locator(".slide").count()
        print(f"슬라이드 {n}장 재캡처")
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
            page.wait_for_timeout(350)
            page.screenshot(path=str(OUT / f"slide_{i:02d}.png"), full_page=False)
        browser.close()
    print(f"완료 -> {OUT}")


if __name__ == "__main__":
    main()
