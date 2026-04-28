# -*- coding: utf-8 -*-
"""영산대 광고제안서 PDF 빌더 — 모든 슬라이드를 1920x1080 PNG로 캡처 후 PDF 결합."""
from playwright.sync_api import sync_playwright
from pathlib import Path
from PIL import Image
import shutil

URL = "http://localhost:5000/api/proposals/179/export-html"
TMP = Path(__file__).resolve().parent / "pdf_build_tmp"
OUT_PDF = Path(r"C:/Users/USER/Desktop/영산대_광고제안서_V101_최신.pdf")


def capture():
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(1200)

        n = page.locator(".slide").count()
        print(f"슬라이드 개수: {n}")

        for i in range(n):
            page.evaluate(
                """(i) => {
                document.querySelectorAll('.slide').forEach((s, idx) => {
                    s.style.visibility = (idx === i) ? 'visible' : 'hidden';
                    s.style.opacity = (idx === i) ? '1' : '0';
                    s.classList.toggle('active', idx === i);
                });
                // Expand all morph phases so every reveal shows
                const target = document.querySelectorAll('.slide')[i];
                if (target) {
                    target.querySelectorAll('.morph-wrap').forEach(w => {
                        w.classList.add('expanded');
                        w.classList.add('expanded2');
                    });
                }
                window.scrollTo(0, 0);
            }""",
                i,
            )
            page.wait_for_timeout(900)  # let animations settle
            out_path = TMP / f"slide_{i:03d}.png"
            page.screenshot(path=str(out_path), full_page=False)
            print(f"  {i+1}/{n}")

        browser.close()
    return n


def build_pdf(n):
    imgs = []
    for i in range(n):
        p = TMP / f"slide_{i:03d}.png"
        im = Image.open(p).convert("RGB")
        imgs.append(im)
    OUT_PDF.parent.mkdir(exist_ok=True, parents=True)
    imgs[0].save(
        str(OUT_PDF),
        save_all=True,
        append_images=imgs[1:],
        resolution=150.0,
    )
    print(f"\nPDF 생성 완료: {OUT_PDF}")
    print(f"크기: {OUT_PDF.stat().st_size / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    n = capture()
    build_pdf(n)
