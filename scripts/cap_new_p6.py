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
        print(f"총 {n}장")
        for i in range(n):
            page.evaluate("(i)=>{document.querySelectorAll('.slide').forEach((s,idx)=>{if(idx===i)s.classList.add('active');else s.classList.remove('active')});window.scrollTo(0,0)}",i)
            page.wait_for_timeout(180)
            text = page.locator(".slide.active").inner_text()
            if "호텔관광" in text and "영산대" in text and "경성대" in text:
                page.screenshot(path=str(OUT / "p6_new_insert.png"))
                print(f"신규 페이지 dom={i} saved")
                break
        browser.close()

if __name__ == "__main__":
    main()
