# -*- coding: utf-8 -*-
"""P45 '우리' -> '하이브미디어' + P50 삭제."""
import sqlite3
import re
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 138


def main():
    conn = sqlite3.connect(str(DB))
    # P45: '우리' label 교체 + label column width 확장 (64 -> 96px)
    r = conn.execute(
        "SELECT id, content FROM sections WHERE proposal_id=? AND order_idx=44",
        (PID,),
    ).fetchone()
    body = r[1]
    # label 너비 64px -> 96px
    body = body.replace(
        "width:64px;font-size:11px;color:#E84E10",
        "width:96px;font-size:11px;color:#E84E10",
    )
    body = body.replace(
        "width:64px;font-size:11px;color:#6E6E73",
        "width:96px;font-size:11px;color:#6E6E73",
    )
    # '우리' -> '하이브미디어' (label 전용)
    body = body.replace(
        ">우리</div>",
        ">하이브미디어</div>",
    )
    conn.execute("UPDATE sections SET content=? WHERE id=?", (body, r[0]))
    print("P45 label: 우리 -> 하이브미디어, width 64->96px")

    # P50 삭제
    cur = conn.execute(
        "DELETE FROM sections WHERE proposal_id=? AND order_idx=49", (PID,)
    )
    print(f"P50 (order=49) 삭제: {cur.rowcount}행")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
