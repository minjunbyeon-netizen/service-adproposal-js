# -*- coding: utf-8 -*-
"""V101 P11 (idx=10) - 각인시켜야 할 것 - ROW 깔끔 정리."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


# ROW 5행 - 4개 팩트 + 취업률 1위(강조)
# P6(0825503)와 대구를 이루도록 숫자 prefix 사용
P11 = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;padding:var(--s-5) var(--s-5)">

<div style="text-align:center;margin-bottom:var(--s-5)">
<div style="font-size:20px;color:#6E6E73;letter-spacing:3px;font-weight:400;margin-bottom:var(--s-2)">Ⅲ. 세부 과업 수행 계획</div>
<div style="font-size:64px;font-weight:700;color:#1A1A1A;line-height:1.2;letter-spacing:-1px">각인시켜야 할 것</div>
</div>

<div style="display:flex;flex-direction:column;gap:0;max-width:960px;width:100%;margin:0 auto">

<div style="display:grid;grid-template-columns:80px 1fr auto;gap:var(--s-3);align-items:center;padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8">
<div style="font-size:36px;font-weight:700;color:#E84E10;line-height:1">08</div>
<div style="font-size:24px;color:#1A1A1A">연구력 세계 8위</div>
<div style="font-size:14px;color:#6E6E73;letter-spacing:2px">NATIONAL NO.1</div>
</div>

<div style="display:grid;grid-template-columns:80px 1fr auto;gap:var(--s-3);align-items:center;padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8">
<div style="font-size:36px;font-weight:700;color:#E84E10;line-height:1">55</div>
<div style="font-size:24px;color:#1A1A1A">QS 호스피탈리티 세계 55위</div>
<div style="font-size:14px;color:#6E6E73;letter-spacing:2px">NON CAPITAL NO.1</div>
</div>

<div style="display:grid;grid-template-columns:80px 1fr auto;gap:var(--s-3);align-items:center;padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8">
<div style="font-size:36px;font-weight:700;color:#E84E10;line-height:1">25</div>
<div style="font-size:24px;color:#1A1A1A">호텔 총지배인 25명 배출</div>
<div style="font-size:14px;color:#6E6E73;letter-spacing:2px">KOREA LEADER</div>
</div>

<div style="display:grid;grid-template-columns:80px 1fr auto;gap:var(--s-3);align-items:center;padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8">
<div style="font-size:36px;font-weight:700;color:#E84E10;line-height:1">03</div>
<div style="font-size:24px;color:#1A1A1A">한국 호텔관광 TOP 3</div>
<div style="font-size:14px;color:#6E6E73;letter-spacing:2px">KOREA TOP 3</div>
</div>

<div style="display:grid;grid-template-columns:80px 1fr auto;gap:var(--s-3);align-items:center;padding:var(--s-4) 0;background:#FFF8F3;border-top:2px solid #E84E10;border-bottom:2px solid #E84E10;margin-top:var(--s-2);padding-left:var(--s-3);padding-right:var(--s-3)">
<div style="font-size:36px;font-weight:700;color:#E84E10;line-height:1">+</div>
<div style="font-size:28px;color:#1A1A1A;font-weight:700">취업률 1위</div>
<div style="font-size:14px;color:#E84E10;letter-spacing:3px;font-weight:700">THE PROOF</div>
</div>

</div>

</div>"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=10",
        (P11, PID),
    )
    conn.commit()
    conn.close()
    print("[P11] 각인시켜야 할 것 - ROW 5행 깔끔 레이아웃 완료")


if __name__ == "__main__":
    main()
