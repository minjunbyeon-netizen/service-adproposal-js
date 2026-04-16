"""Railway 배포 PT 검증 -- 전체 43장 스크린샷."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

URL = "https://adproposal-js-production.up.railway.app/pt"
OUT_DIR = Path(__file__).parent / "rw_shots"
OUT_DIR.mkdir(exist_ok=True)

# 중점 검증 페이지 (편집자가 시각 확인)
FOCUS = [1, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 27, 28, 43]


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await ctx.new_page()
        await page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_selector(".slide", timeout=30000)

        # 총 슬라이드 수
        total = await page.evaluate("document.querySelectorAll('.slide').length")
        print(f"total slides = {total}")

        for idx in FOCUS:
            if idx > total:
                continue
            # 해당 슬라이드로 이동
            await page.evaluate(f"""
                document.querySelectorAll('.slide').forEach((s, i) => {{
                    s.classList.toggle('active', i === {idx - 1});
                }});
                const counter = document.querySelector('.slide-counter');
                if (counter) counter.textContent = '{idx} / {total}';
            """)
            # 이미지 전부 로드 대기
            try:
                await page.wait_for_function(
                    """() => {
                        const active = document.querySelector('.slide.active');
                        if (!active) return false;
                        const imgs = active.querySelectorAll('img');
                        for (const img of imgs) {
                            if (!img.complete || img.naturalWidth === 0) return false;
                        }
                        return true;
                    }""",
                    timeout=15000,
                )
            except Exception as e:
                print(f"#{idx} img wait timeout: {e}")
            # 추가 대기 (트랜지션/폰트)
            await page.wait_for_timeout(500)
            out_path = OUT_DIR / f"rw_{idx:02d}.png"
            await page.screenshot(path=str(out_path), full_page=False)
            print(f"saved {idx}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
