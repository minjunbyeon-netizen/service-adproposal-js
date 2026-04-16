"""V28 트랜지션 검증 -- 실제 키 입력으로 전환하며 중간 프레임 캡처."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

URL = "http://localhost:8881/pt"
OUT_DIR = Path(__file__).parent / "v28_shots"
OUT_DIR.mkdir(exist_ok=True)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await ctx.new_page()
        await page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_selector(".slide", timeout=30000)

        total = await page.evaluate("document.querySelectorAll('.slide').length")
        print(f"total = {total}")

        # 1. 정적: 전환 후 최종 상태 스크린샷 (전환 룰 적용된 핵심 페이지)
        focus = [1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 19, 24, 25, 42, 43, 44]
        for idx in focus:
            if idx > total:
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
                    timeout=8000,
                )
            except Exception:
                pass
            await page.wait_for_timeout(400)
            out = OUT_DIR / f"static_{idx:02d}.png"
            await page.screenshot(path=str(out), full_page=False)
            print(f"  static {idx}")

        # 2. 트랜지션 테스트: 8 -> 9 (invert), 9 -> 10 (letter-morph)
        # 먼저 8페이지로 이동
        await page.evaluate("""
            document.querySelectorAll('.slide').forEach((s, i) => {
                s.style.visibility = i === 7 ? 'visible' : 'hidden';
                s.style.opacity = i === 7 ? '1' : '0';
                s.classList.toggle('active', i === 7);
            });
        """)
        await page.wait_for_timeout(400)

        # 화살표 키로 전환 (JS transition 실행)
        await page.keyboard.press("ArrowRight")
        await page.wait_for_timeout(100)
        await page.screenshot(path=str(OUT_DIR / "trans_8to9_100ms.png"))
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(OUT_DIR / "trans_8to9_400ms.png"))
        await page.wait_for_timeout(600)
        await page.screenshot(path=str(OUT_DIR / "trans_8to9_done.png"))
        print("  captured 8->9 transition frames")

        # 9 -> 10 (letter morph)
        await page.keyboard.press("ArrowRight")
        await page.wait_for_timeout(200)
        await page.screenshot(path=str(OUT_DIR / "trans_9to10_200ms.png"))
        await page.wait_for_timeout(400)
        await page.screenshot(path=str(OUT_DIR / "trans_9to10_600ms.png"))
        await page.wait_for_timeout(500)
        await page.screenshot(path=str(OUT_DIR / "trans_9to10_done.png"))
        print("  captured 9->10 transition frames")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
