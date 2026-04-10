"""V26 시안 3장(11,12,13) 스크린샷."""
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        # 최신 V26 id 찾기
        import sqlite3
        conn = sqlite3.connect("data/adproposal.db")
        row = conn.execute("SELECT id FROM proposals WHERE version='V26' ORDER BY id DESC LIMIT 1").fetchone()
        pid = row[0]
        conn.close()
        print(f"V26 id={pid}")

        await page.goto(f"http://localhost:5000/api/proposals/{pid}/export-html")
        await page.wait_for_timeout(600)

        # 10번(컨셉/슬로건) 까지 넘기고 11,12,13 캡처
        for _ in range(10):
            await page.keyboard.press("ArrowRight")
            await page.wait_for_timeout(200)

        for n in [11, 12, 13]:
            await page.screenshot(path=f"scripts/v26_sian_{n}.png")
            print(f"saved sian_{n}.png")
            await page.keyboard.press("ArrowRight")
            await page.wait_for_timeout(300)

        await browser.close()


asyncio.run(main())
