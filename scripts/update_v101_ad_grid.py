# -*- coding: utf-8 -*-
"""V101 광고 시안 3장을 비율별 그리드로 재구성.

P4 (idx=3)  가로형 2장 (2열 그리드)
P5 (idx=4)  정방형 2장 (2열 그리드)
P6 (idx=5)  세로형 3장 (3열 그리드)
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


def ad_grid(imgs: list[str], cols: int, max_width: int) -> str:
    """비율별 그리드 광고 슬라이드 content."""
    grid_cols = " ".join(["1fr"] * cols)
    imgs_html = "".join(
        f'<img src="/assets/image/ads/{img}" alt="광고 시안" '
        f'style="width:100%;height:auto;display:block;border:1px solid #E8E8E8">'
        for img in imgs
    )
    return (
        '<!--PARENT:I 제안개요--><!--TAG:다른 대학 광고-->'
        '<div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0">'
        '<div class="t-caption is-muted" style="letter-spacing:3px;margin-bottom:var(--s-4)">다른 대학 광고 예시</div>'
        f'<div style="display:grid;grid-template-columns:{grid_cols};gap:var(--s-3);max-width:{max_width}px;width:92%;margin:0 auto">'
        f'{imgs_html}'
        '</div>'
        '</div>'
        '<!--SCRIPT_START-->"(다른 대학 광고를 가리키며) 이런 광고들이, 지금도 쏟아지고 있습니다."<!--SCRIPT_END-->'
    )


def main():
    conn = sqlite3.connect(str(DB))
    try:
        updates = [
            (3, "광고 시안 — 가로형", ad_grid(["wide01.png", "wide02.png"], cols=2, max_width=1100)),
            (4, "광고 시안 — 정방형", ad_grid(["square01.png", "square02.png"], cols=2, max_width=900)),
            (5, "광고 시안 — 세로형", ad_grid(["portrait01.png", "portrait02.png", "portrait03.png"], cols=3, max_width=1000)),
        ]
        for idx, title, content in updates:
            conn.execute(
                "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=?",
                (title, content, PID, idx),
            )
            print(f"idx={idx}: {title}")

        conn.commit()
        print("\n광고 슬라이드 3장 그리드 재구성 완료 (총 이미지 7장)")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
