"""로컬 PT 2, 3페이지 스크린샷 -- 편집 버튼 제거 + 전제/간극 삭제 확인용."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

URL = "http://localhost:8881/pt"
OUT_DIR = Path(__file__).parent / "local_shots"
OUT_DIR.mkdir(exist_ok=True)

FOCUS = [1, 2, 3]


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await ctx.new_page()
        await page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_selector(".slide", timeout=30000)

        for idx in FOCUS:
            await page.evaluate(f"""
                document.querySelectorAll('.slide').forEach((s, i) => {{
                    s.style.visibility = i === {idx - 1} ? 'visible' : 'hidden';
                    s.style.opacity = i === {idx - 1} ? '1' : '0';
                    s.classList.toggle('active', i === {idx - 1});
                }});
            """)
            await page.wait_for_timeout(500)
            out_path = OUT_DIR / f"new_{idx:02d}.png"
            await page.screenshot(path=str(out_path), full_page=False)
            print(f"saved {idx}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
