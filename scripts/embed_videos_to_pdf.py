"""V101.pdf 에 영상 4개를 각 슬라이드 위치에 임베드 (v6: 검정 fill).

v5의 insert_image 좌표 문제 (chromium PDF cm matrix 충돌) 우회 → annotation 만 사용.
- Square annotation: stroke=주황 외곽선 + fill=#0a0a0a 검정 (영상 빈공간 채움)
- FileAttachment: 페이퍼클립 우상단 (클릭 시 외부 player 영상 재생)
- 원본 PT의 SHORT 라벨 박스가 검정 fill 위에 그대로 떠있어 디자인 자연스러움
"""
import fitz, sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r'C:/dev/services/adproposal-js')
SRC_PDF = Path(r'C:/Users/USER/Desktop/V101.pdf')
OUT_PDF = Path(r'C:/Users/USER/Desktop/V101_영상포함_TMP.pdf')
VIDEO_DIR = ROOT / 'assets' / 'video'

SCALE = 1440.0 / 1920.0
ORANGE = (0.91, 0.306, 0.063)
BLACK10 = (0.039, 0.039, 0.039)  # #0a0a0a — 원본 PT 영상 wrapper 색

PLAN = [
    (34, 0,    0,   1920, 1080, 'story01.mp4', 'STORY 01'),
    (40, 222,  386, 460,  520,  'short03.mp4', 'SHORT 01'),
    (40, 730,  386, 460,  520,  'short02.mp4', 'SHORT 02'),
    (40, 1238, 386, 460,  520,  'short01.mp4', 'SHORT 03'),
]

doc = fitz.open(str(SRC_PDF))
print(f'opened {SRC_PDF.name}: {doc.page_count} pages')

for pidx, x, y, w, h, fname, label in PLAN:
    page = doc[pidx]
    data = (VIDEO_DIR / fname).read_bytes()
    rect = fitz.Rect(x * SCALE, y * SCALE, (x + w) * SCALE, (y + h) * SCALE)

    # 1) 영역 검정 fill + 주황 외곽선 — Square annotation
    sq = page.add_rect_annot(rect)
    sq.set_colors(stroke=ORANGE, fill=BLACK10)
    sq.set_border(width=8)
    sq.set_opacity(1.0)
    sq.set_info(title='영상 재생', content=f'{label} — 페이퍼클립 클릭')
    sq.update(fill_color=BLACK10)

    # 2) 페이퍼클립 (우상단)
    pin_pt = fitz.Point(rect.x1 - 24, rect.y0 + 24)
    page.add_file_annot(
        pin_pt, data, filename=fname, ufilename=fname,
        desc=label, icon='Paperclip',
    )
    print(f'  page{pidx+1}: {fname} ({len(data)/1024:.0f} KB) at {rect}')

doc.save(str(OUT_PDF), garbage=0, deflate=True, clean=False)
doc.close()

size_mb = OUT_PDF.stat().st_size / (1024 * 1024)
print(f'\nOK: {OUT_PDF} ({size_mb:.2f} MB)')
