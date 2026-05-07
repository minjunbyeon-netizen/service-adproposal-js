"""V101.pdf 에 영상 4개를 각 슬라이드 위치에 임베드 (v4: 단순·명확).

원본 PT의 SHORT 라벨 검정 박스가 이미 영상 위치 안내 역할.
추가 시각 요소는 외곽선 강조만 — 텍스트 렌더링 의존 X.

- Square annotation (주황 외곽선 8pt) — 영상 영역 강조
- FileAttachment annotation (페이퍼클립) — 우상단, 클릭 시 영상 재생
"""
import fitz, sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r'C:/dev/services/adproposal-js')
SRC_PDF = Path(r'C:/Users/USER/Desktop/V101.pdf')
OUT_PDF = Path(r'C:/Users/USER/Desktop/V101_영상포함.pdf')
VIDEO_DIR = ROOT / 'assets' / 'video'

SCALE = 1440.0 / 1920.0
ORANGE = (0.91, 0.306, 0.063)

PLAN = [
    (34, 0,    0,   1920, 1080, 'story01.mp4', 'STORY 01 — 본 영상'),
    (40, 222,  386, 460,  520,  'short03.mp4', 'SHORT 03 — 학과 현장'),
    (40, 730,  386, 460,  520,  'short02.mp4', 'SHORT 02 — 홍보단 캠퍼스'),
    (40, 1238, 386, 460,  520,  'short01.mp4', 'SHORT 01 — 재학생 브이로그'),
]

doc = fitz.open(str(SRC_PDF))
print(f'opened {SRC_PDF.name}: {doc.page_count} pages')

for pidx, x, y, w, h, fname, label in PLAN:
    page = doc[pidx]
    data = (VIDEO_DIR / fname).read_bytes()
    rect = fitz.Rect(x * SCALE, y * SCALE, (x + w) * SCALE, (y + h) * SCALE)

    # 1) 영역 외곽선 — 주황 8pt
    sq = page.add_rect_annot(rect)
    sq.set_colors(stroke=ORANGE)
    sq.set_border(width=8)
    sq.set_opacity(1.0)
    sq.set_info(title='영상 재생', content=f'{label} (페이퍼클립 클릭)')
    sq.update()

    # 2) 영상 첨부 — 페이퍼클립 우상단
    pin_pt = fitz.Point(rect.x1 - 24, rect.y0 + 24)
    fa = page.add_file_annot(
        pin_pt, data, filename=fname,
        ufilename=fname, desc=label, icon='Paperclip',
    )
    print(f'  page{pidx+1}: {fname} ({len(data)/1024:.0f} KB) at {rect}')

doc.save(str(OUT_PDF), garbage=0, deflate=True, clean=False)
doc.close()

size_mb = OUT_PDF.stat().st_size / (1024 * 1024)
print(f'\nOK: {OUT_PDF} ({size_mb:.2f} MB)')
