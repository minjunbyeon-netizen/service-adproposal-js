# -*- coding: utf-8 -*-
"""P37/P39 캡처 - 참조 이미지와 비교용."""
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
        print(f"총 슬라이드 {n}장")

        targets = [
            ("p37_shortform", "졸업선배가"),
            ("p38_official", "TVC 15"),
            ("p39_sns", "팔로워 +500"),
            ("p47_last", "기준 미달"),
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
                page.wait_for_timeout(200)
                text = page.locator(".slide.active").inner_text()
                if keyword in text:
                    page.screenshot(path=str(OUT / f"{fname}_idx{i:02d}.png"), full_page=False)
                    print(f"  [{fname}] idx={i} matched -> saved")
                    break
        browser.close()
    print(f"저장 -> {OUT}")


if __name__ == "__main__":
    main()
