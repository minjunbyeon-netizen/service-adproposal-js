"""11(method), 12(bridge-new), 13(사례 1-1), 44(ending) 검증."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

URL = "http://localhost:8881/pt"
OUT_DIR = Path(__file__).parent / "local_shots"
OUT_DIR.mkdir(exist_ok=True)

FOCUS = [11, 12, 13, 44]


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await ctx.new_page()
        await page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_selector(".slide", timeout=30000)

        total = await page.evaluate("document.querySelectorAll('.slide').length")
        print(f"total = {total}")

        for idx in FOCUS:
            if idx > total:
                print(f"skip {idx} (total={total})")
                continue
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
                    timeout=10000,
                )
            except Exception:
                pass
            await page.wait_for_timeout(500)
            out_path = OUT_DIR / f"v_{idx:02d}.png"
            await page.screenshot(path=str(out_path), full_page=False)
            print(f"saved {idx}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
