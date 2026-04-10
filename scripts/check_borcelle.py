"""Borcelle 스타일 적용 확인."""
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
        await page.wait_for_timeout(500)
        # 1: cover, 2: 제안배경, 4: 간지, 5: 965,525, 11: 3.6%
        targets = {1, 2, 4, 5, 11}
        for i in range(28):
            current = i + 1
            if current in targets:
                await page.screenshot(path=f"scripts/v26_borcelle_{current}.png")
                print(f"saved {current}")
            await page.keyboard.press("ArrowRight")
            await page.wait_for_timeout(150)
        await browser.close()


asyncio.run(main())
