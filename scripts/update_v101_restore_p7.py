# -*- coding: utf-8 -*-
"""V101 P6 다음에 '각인 선언' 슬라이드 복원.

P6  morph → "영산대는 이렇게 움직이고 있습니다"
P7  (신규) 각인 선언 — "이 움직임을 각인시키는 것, 그것이 전부"
P8~ 제안업체 + divider + 이하 (+1 시프트)
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

P7_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-title" style="line-height:1.4;margin-bottom:var(--s-5);max-width:1100px">이 움직임을,<br>수험생과 학부모에게 <span class="is-accent">각인시키는 것</span></div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div class="t-subtitle w-regular is-muted">그것이, 이번 제안의 <span class="is-accent w-bold">전부</span>입니다</div></div><!--SCRIPT_START-->"이 움직임을 — 수험생과 학부모에게 <strong>각인시키는 것.</strong><br><br>그것이, 이번 제안의 <strong>전부</strong>입니다."<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    try:
        # 1. 기존 idx 6~ 전체를 +1 시프트 (역순 처리: 음수 경유)
        conn.execute(
            "UPDATE sections SET order_idx = -(order_idx + 1) "
            "WHERE proposal_id=? AND order_idx >= 6",
            (PID,),
        )
        conn.execute(
            "UPDATE sections SET order_idx = -order_idx "
            "WHERE proposal_id=? AND order_idx < 0",
            (PID,),
        )
        print("기존 idx 6~ +1 시프트")

        # 2. 레퍼런스 (level, status)
        sample = conn.execute(
            "SELECT level, status FROM sections WHERE proposal_id=? AND order_idx=7",
            (PID,),
        ).fetchone()
        lvl = sample["level"]
        st = sample["status"]

        # 3. 신규 idx 6에 각인 선언 (잠깐, P7이 새 각인이고 기존 P6 morph는 idx=5 그대로)
        # 기존 idx 5가 morph, 시프트된 후 idx 7은 구 idx 6 (제안업체)
        # 즉 이미 idx 6이 비어있음 — INSERT하면 됨
        conn.execute(
            """INSERT INTO sections (proposal_id, level, title, order_idx, content, status)
               VALUES (?,?,?,?,?,?)""",
            (PID, lvl, "각인 선언", 6, P7_CONTENT, st),
        )
        print("신규 idx 6 '각인 선언' 삽입")

        conn.commit()

        # 4. 결과 확인
        rows = conn.execute(
            "SELECT order_idx, title FROM sections WHERE proposal_id=? ORDER BY order_idx LIMIT 14",
            (PID,),
        ).fetchall()
        print(f"\n=== V101 각인 선언 복원 후 ===")
        for r in rows:
            print(f"  idx={r['order_idx']:2d} | {r['title']}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
