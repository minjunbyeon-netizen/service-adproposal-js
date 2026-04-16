# -*- coding: utf-8 -*-
"""Playwright로 V101 각 슬라이드 스크린샷 캡처."""
from playwright.sync_api import sync_playwright
from pathlib import Path

URL = "http://localhost:8881/api/proposals/179/export-html"
OUT = Path(__file__).resolve().parent / "v101_shots"
OUT.mkdir(exist_ok=True)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1600, "height": 900})
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(1000)

        # 슬라이드 개수
        n = page.locator(".slide").count()
        print(f"슬라이드 개수: {n}")

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
            page.wait_for_timeout(400)
            out_path = OUT / f"slide_{i:02d}.png"
            page.screenshot(path=str(out_path), full_page=False)
            print(f"  {i+1}/{n}: {out_path.name}")

        browser.close()
    print(f"\n완료: {OUT}")


if __name__ == "__main__":
    main()
