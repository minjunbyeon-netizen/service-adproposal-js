"""모바일 viewport에서 에러 + 스케일 동작 확인."""
import asyncio
from playwright.async_api import async_playwright

URL = "http://localhost:8881/pt"


async def check(viewport_name, w, h):
    errors = []
    warnings = []
    failed = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": w, "height": h})
        page = await ctx.new_page()

        page.on("console", lambda m: errors.append(f"[{m.type}] {m.text}") if m.type == "error" else warnings.append(m.text) if m.type == "warning" else None)
        page.on("pageerror", lambda e: errors.append(f"[pageerror] {e}"))
        page.on("response", lambda r: failed.append(f"{r.status} {r.url}") if r.status >= 400 else None)

        await page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_selector(".slide", timeout=15000)
        await page.wait_for_timeout(1000)

        scale = await page.evaluate("""() => {
            const s = document.getElementById('stage');
            const t = getComputedStyle(s).transform;
            if (t === 'none') return 1;
            const m = t.match(/matrix\\(([^,]+)/);
            return m ? parseFloat(m[1]) : null;
        }""")

        stage_rect = await page.evaluate("""() => {
            const r = document.getElementById('stage').getBoundingClientRect();
            return {x:r.x, y:r.y, w:r.width, h:r.height};
        }""")

        # trigger resize
        await page.set_viewport_size({"width": w // 2, "height": h // 2})
        await page.wait_for_timeout(500)

        scale_after = await page.evaluate("""() => {
            const s = document.getElementById('stage');
            const t = getComputedStyle(s).transform;
            if (t === 'none') return 1;
            const m = t.match(/matrix\\(([^,]+)/);
            return m ? parseFloat(m[1]) : null;
        }""")

        await browser.close()

    expected_scale = min(w / 1920, h / 1080)
    print(f"{viewport_name} {w}x{h}")
    print(f"  expected scale: {expected_scale:.4f}")
    print(f"  actual scale:   {scale:.4f}")
    print(f"  stage rect: x={stage_rect['x']:.0f} y={stage_rect['y']:.0f} w={stage_rect['w']:.0f} h={stage_rect['h']:.0f}")
    print(f"  after resize to {w//2}x{h//2}: scale={scale_after:.4f}")
    print(f"  errors: {len(errors)}, warnings: {len(warnings)}, failed: {len(failed)}")
    for e in errors[:5]:
        print(f"    ERR: {e}")
    for f in failed[:5]:
        print(f"    HTTP: {f}")
    print()


async def main():
    tests = [
        ("desktop", 1920, 1080),
        ("laptop", 1366, 768),
        ("mobile_port", 390, 844),
        ("mobile_narrow", 360, 640),
    ]
    for name, w, h in tests:
        await check(name, w, h)


if __name__ == "__main__":
    asyncio.run(main())
