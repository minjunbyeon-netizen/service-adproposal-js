"""모든 슬라이드 검사: overflow, 텍스트 잘림, console 에러."""
import asyncio, sqlite3
from playwright.async_api import async_playwright


async def main():
    conn = sqlite3.connect("data/adproposal.db")
    pid = conn.execute("SELECT id FROM proposals WHERE version='V26' ORDER BY id DESC LIMIT 1").fetchone()[0]
    conn.close()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        console_messages = []
        page.on("console", lambda msg: console_messages.append((msg.type, msg.text)))
        page.on("pageerror", lambda err: console_messages.append(("error", str(err))))

        await page.goto(f"http://localhost:5000/api/proposals/{pid}/export-html")
        await page.wait_for_timeout(800)

        print("=" * 80)
        print("SLIDE INSPECTION REPORT")
        print("=" * 80)

        for i in range(28):
            current = i + 1
            # overflow / height / scrollable check
            info = await page.evaluate("""() => {
                const slide = document.querySelector('.slide.active');
                if (!slide) return null;
                const body = slide.querySelector('.content-body');
                const header = slide.querySelector('.content-header');
                const sp = slide.querySelector('.section-parent');
                const h3 = slide.querySelector('h3');
                const tag = slide.querySelector('.slide-tag');
                const sidebar = slide.querySelector('.script-side');
                return {
                    cls: slide.className,
                    parent: sp?.textContent?.trim() || '',
                    title: h3?.textContent?.trim() || '',
                    tag: tag?.textContent?.trim() || '',
                    bodyScrollHeight: body?.scrollHeight || 0,
                    bodyClientHeight: body?.clientHeight || 0,
                    overflow: body ? (body.scrollHeight > body.clientHeight + 5) : false,
                    hasScript: !!sidebar,
                    scriptScrollable: sidebar ? (sidebar.scrollHeight > sidebar.clientHeight + 5) : false,
                    headerBottom: header?.getBoundingClientRect().bottom || 0,
                };
            }""")
            if info:
                flags = []
                if info["overflow"]:
                    flags.append(f"OVERFLOW(body {info['bodyScrollHeight']}>{info['bodyClientHeight']})")
                if info["scriptScrollable"]:
                    flags.append("SCRIPT_SCROLL")
                flag_str = " ".join(flags) if flags else "OK"
                title = info["title"][:30] if info["title"] else "(divider)"
                print(f"#{current:2} [{flag_str:30}] {title}")
            await page.keyboard.press("ArrowRight")
            await page.wait_for_timeout(120)

        print()
        print("=" * 80)
        print("CONSOLE MESSAGES")
        print("=" * 80)
        for msg_type, text in console_messages:
            if msg_type in ("error", "warning"):
                print(f"[{msg_type}] {text}")

        await browser.close()


asyncio.run(main())
