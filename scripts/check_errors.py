"""브라우저 콘솔 에러 / 네트워크 실패 체크."""
import asyncio
from playwright.async_api import async_playwright

URL = "http://localhost:8881/pt"


async def main():
    errors = []
    warnings = []
    failed = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await ctx.new_page()

        def on_console(msg):
            t = msg.type
            if t == "error":
                errors.append(f"[{t}] {msg.text}")
            elif t == "warning":
                warnings.append(f"[{t}] {msg.text}")

        def on_page_error(exc):
            errors.append(f"[pageerror] {exc}")

        def on_request_failed(req):
            failed.append(f"{req.method} {req.url} - {req.failure}")

        def on_response(resp):
            if resp.status >= 400:
                failed.append(f"{resp.status} {resp.url}")

        page.on("console", on_console)
        page.on("pageerror", on_page_error)
        page.on("requestfailed", on_request_failed)
        page.on("response", on_response)

        await page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_selector(".slide", timeout=30000)
        await page.wait_for_timeout(2000)

        # 화살표 키로 10페이지 연속 이동 (트랜지션/slide 전환 오류 체크)
        for _ in range(10):
            await page.keyboard.press("ArrowRight")
            await page.wait_for_timeout(300)

        # 중간 페이지에서 이미지 로딩 확인
        await page.wait_for_timeout(1000)

        # 맨 뒤로
        for _ in range(50):
            await page.keyboard.press("ArrowRight")
            await page.wait_for_timeout(100)

        await page.wait_for_timeout(2000)

        # total slides
        total = await page.evaluate("document.querySelectorAll('.slide').length")
        active = await page.evaluate("""() => {
            const a = document.querySelector('.slide.active');
            return a ? Array.from(document.querySelectorAll('.slide')).indexOf(a) + 1 : -1;
        }""")

        # stage scale check
        stage_transform = await page.evaluate(
            "getComputedStyle(document.getElementById('stage')).transform"
        )

        await browser.close()

    print(f"total slides: {total}")
    print(f"active slide: {active}")
    print(f"stage transform: {stage_transform}")
    print()
    print(f"errors: {len(errors)}")
    for e in errors[:20]:
        print(f"  {e}")
    print(f"warnings: {len(warnings)}")
    for w in warnings[:10]:
        print(f"  {w}")
    print(f"failed requests: {len(failed)}")
    for f in failed[:20]:
        print(f"  {f}")


if __name__ == "__main__":
    asyncio.run(main())
