# -*- coding: utf-8 -*-
"""V101 P17 - THE PROPOSAL / CONCEPT: / ONE MESSAGE: 라벨 제거."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


P17 = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;padding:var(--s-5) var(--s-7);max-width:1600px;margin:0 auto;text-align:left">

<div style="font-size:140px;font-weight:700;color:#1A1A1A;line-height:0.95;margin-bottom:var(--s-1)">증명</div>

<div style="font-size:140px;font-weight:700;color:#E84E10;line-height:0.95;margin-bottom:var(--s-6)">리프레이밍</div>

<div style="width:100%;height:1px;background:#1A1A1A;margin-bottom:var(--s-5)"></div>

<div style="display:grid;grid-template-columns:80px 1fr;gap:var(--s-4);align-items:baseline;padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8">
<div style="font-size:18px;color:#6E6E73;font-weight:700">01</div>
<div style="font-size:36px;font-weight:700;color:#1A1A1A;line-height:1.2">산업이 선택한 대학</div>
</div>

<div style="display:grid;grid-template-columns:80px 1fr;gap:var(--s-4);align-items:baseline;padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8">
<div style="font-size:18px;color:#6E6E73;font-weight:700">02</div>
<div style="font-size:36px;font-weight:700;color:#1A1A1A;line-height:1.2">글로벌 1위가 될 때까지</div>
</div>

<div style="display:grid;grid-template-columns:80px 1fr;gap:var(--s-4);align-items:baseline;padding:var(--s-3) 0">
<div style="font-size:18px;color:#6E6E73;font-weight:700">03</div>
<div style="font-size:36px;font-weight:700;color:#1A1A1A;line-height:1.2">26번째가 당신</div>
</div>

</div>"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=16",
        (P17, PID),
    )
    conn.commit()
    conn.close()
    print("[P17] THE PROPOSAL / CONCEPT / ONE MESSAGE 라벨 제거")


if __name__ == "__main__":
    main()
