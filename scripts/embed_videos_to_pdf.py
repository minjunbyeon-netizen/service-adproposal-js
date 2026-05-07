"""V101.pdf 에 영상 4개를 각 슬라이드 위치에 임베드.

- PDF page 35 (idx 34): story01.mp4 풀스크린
- PDF page 41 (idx 40): short03 / short02 / short01 (좌→우)

전략: PyMuPDF add_file_annot 으로 페이지 내 클릭 가능 영역 + 시각 표시 박스.
Adobe Reader 등에서 클릭 시 OS default player 로 영상 재생.
"""
import fitz, sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r'C:/dev/services/adproposal-js')
SRC_PDF = Path(r'C:/Users/USER/Desktop/V101.pdf')
OUT_PDF = Path(r'C:/Users/USER/Desktop/V101_영상포함.pdf')
VIDEO_DIR = ROOT / 'assets' / 'video'

SCALE = 1440.0 / 1920.0  # px(1920) -> pt(1440)

# (PDF page idx0, x_px, y_px, w_px, h_px, video filename, label)
PLAN = [
    (34, 0,    0,   1920, 1080, 'story01.mp4', '본 영상 — STORY 01'),
    (40, 222,  386, 460,  520,  'short03.mp4', 'SHORT 03 — 학과 소개'),
    (40, 730,  386, 460,  520,  'short02.mp4', 'SHORT 02 — 홍보단 캠퍼스'),
    (40, 1238, 386, 460,  520,  'short01.mp4', 'SHORT 01 — 일상'),
]

doc = fitz.open(str(SRC_PDF))
print(f'opened {SRC_PDF.name}: {doc.page_count} pages')

for pidx, x, y, w, h, fname, label in PLAN:
    page = doc[pidx]
    vpath = VIDEO_DIR / fname
    data = vpath.read_bytes()
    rect = fitz.Rect(x * SCALE, y * SCALE, (x + w) * SCALE, (y + h) * SCALE)

    # 1) 시각 박스 — 반투명 오버레이 + 보더
    border = fitz.Rect(rect.x0 + 4, rect.y0 + 4, rect.x1 - 4, rect.y1 - 4)
    page.draw_rect(border, color=(0.91, 0.306, 0.063), width=4, overlay=True)

    # 2) 중앙 재생 표지 — ▶ + 라벨
    cx, cy = (rect.x0 + rect.x1) / 2, (rect.y0 + rect.y1) / 2
    badge_w, badge_h = 360, 80
    badge = fitz.Rect(cx - badge_w / 2, cy - badge_h / 2, cx + badge_w / 2, cy + badge_h / 2)
    page.draw_rect(badge, color=(0.91, 0.306, 0.063), fill=(0.91, 0.306, 0.063),
                   width=0, overlay=True, fill_opacity=0.92)
    page.insert_textbox(
        badge, f'▶ {label}',
        fontsize=20, color=(1, 1, 1),
        align=fitz.TEXT_ALIGN_CENTER, fontname='helv',
    )

    # 3) 클릭 가능 영역 — file annotation (rect 영역 전체 클릭)
    annot = page.add_file_annot(
        rect.tl,           # point — 좌상단 아이콘 표시 위치
        data,
        filename=fname,
        ufilename=fname,
        desc=label,
        icon='Paperclip',
    )
    # 아이콘이 작아 영역 전체 클릭 안 되므로 — 위에 큰 클릭 영역 추가
    # PyMuPDF 의 add_file_annot 은 point 기반이라 rect 전체를 cover 못함.
    # 대안: 추가로 link annotation + JavaScript action 으로 첨부 영상을 export+open.
    # 가장 호환 좋은 방법은 별도 큰 사각형 file_annot 또는 popup.
    # 여기서는 rect 좌상단 + 중앙 + 우하단 3 포인트에 file_annot 분산해서
    # 영역 어디 눌러도 잡히게 한다.
    for px, py in [(cx, cy), (rect.x1 - 30, rect.y1 - 30)]:
        page.add_file_annot(
            fitz.Point(px, py), data, filename=fname,
            ufilename=fname, desc=label, icon='Paperclip',
        )
    print(f'  page{pidx+1}: {fname} ({len(data)/1024:.0f} KB) at {rect}')

doc.save(str(OUT_PDF), garbage=4, deflate=True, clean=True)
doc.close()

size_mb = OUT_PDF.stat().st_size / (1024 * 1024)
print(f'\nOK: {OUT_PDF} ({size_mb:.2f} MB)')
