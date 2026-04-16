# -*- coding: utf-8 -*-
"""V101 - P12 뒤에 영산대 광고 시안 슬라이드 복원 (타대학 오버레이 없이 YSU만)."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


YSU_POSTER = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:광고 시안--><div style="height:100%;display:flex;justify-content:center;align-items:center;padding:0;background:#FFFFFF"><div style="height:88%;max-height:860px"><img src="/assets/image/ysu_ad_poster.png" alt="YSU 광고 시안" style="height:100%;width:auto;display:block;box-shadow:0 8px 32px rgba(0,0,0,0.15)"></div></div>"""


def main():
    conn = sqlite3.connect(str(DB))

    # idx >= 12 전부 +1 시프트
    rows = conn.execute(
        "SELECT id, order_idx FROM sections WHERE proposal_id=? AND order_idx >= 12 ORDER BY order_idx DESC",
        (PID,),
    ).fetchall()
    for rid, idx in rows:
        conn.execute("UPDATE sections SET order_idx=? WHERE id=?", (idx + 1, rid))
    print(f"idx >= 12 인 {len(rows)}개 row +1 시프트")

    # idx=12에 삽입
    conn.execute(
        """INSERT INTO sections (proposal_id, order_idx, level, title, content)
           VALUES (?, 12, 2, '영산대 광고 시안', ?)""",
        (PID, YSU_POSTER),
    )
    print("idx=12 영산대 광고 시안 삽입")

    conn.commit()

    rows = conn.execute(
        "SELECT order_idx, title FROM sections WHERE proposal_id=? AND order_idx BETWEEN 10 AND 15 ORDER BY order_idx",
        (PID,),
    ).fetchall()
    for r in rows:
        print(f"  idx={r[0]}: {r[1]}")

    conn.close()
    print("\n완료")


if __name__ == "__main__":
    main()
