"""매핑 확인."""
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
        for i in range(28):
            current = i + 1
            info = await page.evaluate("""() => {
                const a = document.querySelector('.slide.active');
                const sp = a?.querySelector('.section-parent');
                const h3 = a?.querySelector('h3');
                const tag = a?.querySelector('.slide-tag');
                return {
                    parent: sp?.textContent?.trim() || '',
                    title: h3?.textContent?.trim() || '',
                    tag: tag?.textContent?.trim() || ''
                };
            }""")
            print(f"#{current:2}: [{info['parent']}] {info['title']}{' · ' + info['tag'] if info['tag'] else ''}")
            if current in (2, 3, 5, 11, 17, 24):
                await page.screenshot(path=f"scripts/v26_map_{current}.png")
            await page.keyboard.press("ArrowRight")
            await page.wait_for_timeout(120)
        await browser.close()


asyncio.run(main())
