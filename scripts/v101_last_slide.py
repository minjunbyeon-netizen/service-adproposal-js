# -*- coding: utf-8 -*-
"""V101 마지막장 복원 - 2026년 확실히 각인시키고 / 2027년 많이 팔겠습니다."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


# 참조 스타일: Swiss Hero - 중앙 정렬, 대형 타이틀, 여백 극대화
LAST = """<!--PARENT:Epilogue--><!--TAG:클로징--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0;background:#FFFFFF">

<div style="font-size:80px;font-weight:700;color:#1A1A1A;line-height:1.3;letter-spacing:-2px">
2026년 확실히 <span style="color:#E84E10">각인</span>시키고<br>
2027년 많이 팔겠습니다
</div>

</div>"""


def main():
    conn = sqlite3.connect(str(DB))

    # 현재 최대 idx 확인
    max_idx = conn.execute(
        "SELECT MAX(order_idx) FROM sections WHERE proposal_id=?", (PID,)
    ).fetchone()[0]
    print(f"현재 최대 idx: {max_idx}")

    # 이미 Epilogue 슬라이드가 있으면 UPDATE, 없으면 INSERT
    existing = conn.execute(
        "SELECT id, order_idx FROM sections WHERE proposal_id=? AND content LIKE '%Epilogue%'",
        (PID,),
    ).fetchone()

    if existing:
        conn.execute(
            "UPDATE sections SET content=? WHERE id=?",
            (LAST, existing[0]),
        )
        print(f"기존 Epilogue(idx={existing[1]}) 업데이트")
    else:
        new_idx = max_idx + 1
        conn.execute(
            """INSERT INTO sections (proposal_id, order_idx, level, title, content)
               VALUES (?, ?, 2, '2026 각인 · 2027 판매', ?)""",
            (PID, new_idx, LAST),
        )
        print(f"신규 마지막장 추가 idx={new_idx}")

    conn.commit()

    # 확인
    rows = conn.execute(
        "SELECT order_idx, title FROM sections WHERE proposal_id=? ORDER BY order_idx DESC LIMIT 3",
        (PID,),
    ).fetchall()
    print("\n== 마지막 3장 ==")
    for r in rows:
        print(f"  idx={r[0]}: {r[1]}")

    conn.close()
    print("\n완료")


if __name__ == "__main__":
    main()
