# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

URL = "http://localhost:8881/api/proposals/179/export-html"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1600, "height": 900})
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(1000)
        n = page.locator(".slide").count()
        for i in range(n):
            page.evaluate(
                """(i) => {
                document.querySelectorAll('.slide').forEach((s, idx) => {
                    if (idx === i) s.classList.add('active');
                    else s.classList.remove('active');
                });
            }""",
                i,
            )
            page.wait_for_timeout(80)
            active = page.locator(".slide.active")
            pagenum = active.locator(".slide-pagenum").count()
            pn_text = ""
            if pagenum > 0:
                pn_text = active.locator(".slide-pagenum").inner_text()
            body = active.inner_text()[:80].replace("\n", " | ")
            print(f"dom={i:02d} pn={pn_text:>3s} :: {body}")
        browser.close()


if __name__ == "__main__":
    main()
