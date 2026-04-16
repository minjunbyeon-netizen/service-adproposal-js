# -*- coding: utf-8 -*-
"""V101 P17 — '저희가 제안하는 한 장' 요약 슬라이드 신규 삽입."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

P17_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:제안 요약--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-5)">저희가 제안하는, <span class="is-accent">한 장</span></div><div style="display:flex;flex-direction:column;gap:0;max-width:1120px;width:96%;margin:0 auto;border:2px solid #1A1A1A"><div style="display:grid;grid-template-columns:180px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-4) var(--s-5);border-bottom:1px solid #E8E8E8"><div style="font-size:14px;font-weight:700;color:#E84E10;letter-spacing:4px;text-align:left">컨셉</div><div style="text-align:left"><div style="font-size:40px;font-weight:700;color:#1A1A1A;line-height:1;letter-spacing:-1px;margin-bottom:6px">증명</div><div style="font-size:14px;color:#6E6E73;line-height:1.5">주장이 아닌, 숫자가 기억에 박히는 일</div></div></div><div style="display:grid;grid-template-columns:180px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-4) var(--s-5);border-bottom:1px solid #E8E8E8"><div style="font-size:14px;font-weight:700;color:#E84E10;letter-spacing:4px;text-align:left">기법</div><div style="text-align:left"><div style="font-size:40px;font-weight:700;color:#1A1A1A;line-height:1;letter-spacing:-1px;margin-bottom:6px">리프레이밍</div><div style="font-size:14px;color:#6E6E73;line-height:1.5">같은 숫자를, 다른 프레임으로</div></div></div><div style="display:grid;grid-template-columns:180px 1fr;gap:var(--s-4);align-items:flex-start;padding:var(--s-4) var(--s-5)"><div style="font-size:14px;font-weight:700;color:#E84E10;letter-spacing:4px;text-align:left;padding-top:8px">슬로건 3가지</div><div style="text-align:left;display:flex;flex-direction:column;gap:var(--s-2)"><div style="font-size:20px;font-weight:700;color:#1A1A1A;line-height:1.45;letter-spacing:-0.3px">"대학이 아니라, <span class="is-accent">산업이 선택한 대학</span>"</div><div style="font-size:20px;font-weight:700;color:#1A1A1A;line-height:1.45;letter-spacing:-0.3px">"국내 3위지만, <span class="is-accent">글로벌 1위가 될 때까지</span>"</div><div style="font-size:20px;font-weight:700;color:#1A1A1A;line-height:1.45;letter-spacing:-0.3px">"25명이 끝이 아닙니다. <span class="is-accent">26번째가, 당신이 될 때까지</span>"</div></div></div></div></div><!--SCRIPT_START-->"저희가 제안하는 — <strong>한 장</strong>입니다.<br><br><strong>컨셉</strong>은 <strong>증명</strong>. 주장이 아닌, 숫자가 기억에 박히는 일.<br><strong>기법</strong>은 <strong>리프레이밍</strong>. 같은 숫자를, 다른 프레임으로.<br><strong>슬로건 3가지</strong>는 —<br><br>'대학이 아니라, 산업이 선택한 대학.'<br>'국내 3위지만, 글로벌 1위가 될 때까지.'<br>'25명이 끝이 아닙니다. 26번째가, 당신이 될 때까지.'"<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row

    # idx 16+ +1 시프트
    conn.execute(
        "UPDATE sections SET order_idx = -(order_idx + 1) WHERE proposal_id=? AND order_idx >= 16",
        (PID,),
    )
    conn.execute(
        "UPDATE sections SET order_idx = -order_idx WHERE proposal_id=? AND order_idx < 0",
        (PID,),
    )
    print("idx 16+ +1 시프트")

    # 신규 idx=16 INSERT
    sample = conn.execute(
        "SELECT level, status FROM sections WHERE proposal_id=? AND order_idx=15",
        (PID,),
    ).fetchone()
    conn.execute(
        """INSERT INTO sections (proposal_id, level, title, order_idx, content, status)
           VALUES (?,?,?,?,?,?)""",
        (PID, sample["level"], "저희가 제안하는, 한 장", 16, P17_CONTENT, sample["status"]),
    )
    print("idx=16 P17 요약 슬라이드 INSERT")

    conn.commit()

    # 확인
    rows = conn.execute(
        "SELECT order_idx, title FROM sections WHERE proposal_id=? AND order_idx BETWEEN 12 AND 20 ORDER BY order_idx",
        (PID,),
    ).fetchall()
    print("\n=== V101 P13~P21 ===")
    for r in rows:
        print(f"  P{r['order_idx']+1:2d} (idx={r['order_idx']:2d}) | {r['title']}")
    conn.close()


if __name__ == "__main__":
    main()
