"""V26 전체 슬라이드 스크린샷 + section_parent 확인."""
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

        # 주요 슬라이드만 캡처: 2, 3, 5, 11, 15, 18, 19, 23, 24, 25, 26, 27
        targets = {2, 3, 5, 11, 15, 18, 19, 23, 24, 25, 26, 27}
        for i in range(28):
            current = i + 1
            if current in targets:
                # section-parent 텍스트 확인
                parent_text = await page.evaluate("""() => {
                    const active = document.querySelector('.slide.active');
                    const sp = active?.querySelector('.section-parent');
                    return sp?.textContent?.trim() || '(none)';
                }""")
                title = await page.evaluate("""() => {
                    const active = document.querySelector('.slide.active');
                    const h3 = active?.querySelector('h3');
                    return h3?.textContent?.trim() || '(none)';
                }""")
                print(f"#{current}: parent='{parent_text}' | title='{title}'")
                if current in (5, 11, 15, 18, 23, 25, 27):
                    await page.screenshot(path=f"scripts/v26_final_{current}.png")
            await page.keyboard.press("ArrowRight")
            await page.wait_for_timeout(150)

        await browser.close()


asyncio.run(main())
