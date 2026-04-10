"""V26 PT 실제 렌더링 확인."""
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        # 호스트 포트 자동 탐지
        for port in [5000, 8881, 8080]:
            try:
                await page.goto(f"http://localhost:{port}/health", timeout=2000)
                host_port = port
                break
            except Exception:
                continue
        else:
            print("서버 못 찾음")
            return

        print(f"port={host_port}")
        url = f"http://localhost:{host_port}/api/proposals/81/export-html"
        await page.goto(url)
        await page.wait_for_timeout(800)

        # 첫 5장 스크린샷
        for i in range(5):
            path = f"scripts/v26_slide_{i+1}.png"
            await page.screenshot(path=path, full_page=False)
            print(f"saved {path}")
            await page.keyboard.press("ArrowRight")
            await page.wait_for_timeout(400)

        # 현재 화면 DOM 상태 체크
        active = await page.query_selector(".slide.active")
        if active:
            box = await active.bounding_box()
            print(f"active slide box: {box}")
            body = await active.query_selector(".content-body")
            if body:
                bb = await body.bounding_box()
                visible = await body.evaluate("el => getComputedStyle(el).display + '/' + getComputedStyle(el).visibility + '/' + getComputedStyle(el).opacity")
                inner = await body.inner_text()
                print(f"content-body box: {bb}")
                print(f"content-body style: {visible}")
                print(f"content-body text (first 200): {inner[:200]}")

        await browser.close()


asyncio.run(main())
