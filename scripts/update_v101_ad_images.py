# -*- coding: utf-8 -*-
"""V101 광고 시안 슬라이드 P4~P6에 실제 이미지 삽입.

P4 (idx=3) ← ad01.png
P5 (idx=4) ← ad02.png
P6 (idx=5) ← ad03.png
P7 (idx=6) ← 플레이스홀더 유지 (이미지 없음)
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


def ad_slide_img(img_path: str) -> str:
    """실제 이미지를 담은 광고 슬라이드 content."""
    return (
        '<!--PARENT:I 제안개요--><!--TAG:다른 대학 광고-->'
        '<div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0">'
        '<div class="t-caption is-muted" style="letter-spacing:3px;margin-bottom:var(--s-3)">다른 대학 광고 예시</div>'
        f'<div style="width:88%;max-width:880px;margin:0 auto;border:1px solid #E8E8E8;background:#FFFFFF">'
        f'<img src="/assets/image/ads/{img_path}" alt="광고 시안" style="width:100%;height:auto;display:block">'
        '</div>'
        '</div>'
        '<!--SCRIPT_START-->(다른 대학 광고를 가리키며) "이건, 다른 대학의 광고입니다."<!--SCRIPT_END-->'
    )


def main():
    conn = sqlite3.connect(str(DB))
    try:
        updates = [
            (3, "광고 시안 1", ad_slide_img("ad01.png")),
            (4, "광고 시안 2", ad_slide_img("ad02.png")),
            (5, "광고 시안 3", ad_slide_img("ad03.png")),
        ]
        for idx, title, content in updates:
            conn.execute(
                "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=?",
                (title, content, PID, idx),
            )
            print(f"idx={idx}: {title} (이미지 삽입)")

        conn.commit()
        print("\n광고 이미지 3장 삽입 완료")
        print("P7 (idx=6) 4번째 광고는 플레이스홀더 유지")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
