"""V26 슬라이드 17 스크린샷."""
import asyncio, sqlite3
from playwright.async_api import async_playwright


async def main():
    conn = sqlite3.connect("data/adproposal.db")
    pid = conn.execute("SELECT id FROM proposals WHERE version='V26' ORDER BY id DESC LIMIT 1").fetchone()[0]
    conn.close()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto(f"http://localhost:5000/api/proposals/{pid}/export-html")
        await page.wait_for_timeout(600)
        for _ in range(16):
            await page.keyboard.press("ArrowRight")
            await page.wait_for_timeout(150)
        await page.screenshot(path="scripts/v26_slide_17.png")
        print("saved")
        await browser.close()


asyncio.run(main())
