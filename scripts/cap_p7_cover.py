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
        # Cover first
        page.evaluate("()=>{document.querySelectorAll('.slide').forEach((s,idx)=>{if(idx===0)s.classList.add('active');else s.classList.remove('active')});window.scrollTo(0,0)}")
        page.wait_for_timeout(300)
        page.screenshot(path=str(OUT / "p1_cover_ref.png"))
        print("P1 cover saved")
        # Then find P7 (dom=6)
        page.evaluate("()=>{document.querySelectorAll('.slide').forEach((s,idx)=>{if(idx===6)s.classList.add('active');else s.classList.remove('active')});window.scrollTo(0,0)}")
        page.wait_for_timeout(300)
        page.screenshot(path=str(OUT / "p7_cover_style.png"))
        print("P7 dom=6 saved")
        browser.close()

if __name__ == "__main__":
    main()
