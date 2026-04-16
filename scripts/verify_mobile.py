"""모바일/데스크탑 뷰 검증 -- 여러 viewport 크기에서 스크린샷."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

URL = "http://localhost:8881/pt"
OUT_DIR = Path(__file__).parent / "mobile_shots"
OUT_DIR.mkdir(exist_ok=True)

VIEWPORTS = [
    ("desktop", 1920, 1080),
    ("laptop", 1366, 768),
    ("tablet", 1024, 768),
    ("mobile_land", 844, 390),   # iPhone 13 landscape
    ("mobile_port", 390, 844),    # iPhone 13 portrait
    ("mobile_narrow", 360, 640),  # Android small
]

FOCUS = [1, 2, 12, 13, 25, 44]


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for name, w, h in VIEWPORTS:
            ctx = await browser.new_context(viewport={"width": w, "height": h})
            page = await ctx.new_page()
            await page.goto(URL, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_selector(".slide", timeout=30000)
            await page.wait_for_timeout(400)

            for idx in FOCUS:
                await page.evaluate(f"""
                    document.querySelectorAll('.slide').forEach((s, i) => {{
                        s.style.visibility = i === {idx - 1} ? 'visible' : 'hidden';
                        s.style.opacity = i === {idx - 1} ? '1' : '0';
                        s.classList.toggle('active', i === {idx - 1});
                    }});
                """)
                try:
                    await page.wait_for_function(
                        """() => {
                            const a = document.querySelector('.slide.active');
                            if (!a) return false;
                            const imgs = a.querySelectorAll('img');
                            for (const img of imgs) {
                                if (!img.complete || img.naturalWidth === 0) return false;
                            }
                            return true;
                        }""",
                        timeout=8000,
                    )
                except Exception:
                    pass
                await page.wait_for_timeout(300)
                out = OUT_DIR / f"{name}_{idx:02d}.png"
                await page.screenshot(path=str(out))
                print(f"{name} {w}x{h} slide {idx}")
            await ctx.close()
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
