# -*- coding: utf-8 -*-
"""V101 P19 (idx=18) - 4계층 레이어 광고 브리프."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


P19 = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:4-Layer Brief--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;padding:var(--s-5) var(--s-6);max-width:1500px;margin:0 auto">

<div style="font-size:14px;color:#E84E10;font-weight:700;letter-spacing:4px;margin-bottom:var(--s-2)">AD BRIEF · 4 LAYERS</div>

<div style="font-size:48px;font-weight:700;color:#1A1A1A;line-height:1.2;margin-bottom:var(--s-5);letter-spacing:-1px">4계층 레이어 광고 브리프</div>

<div style="display:flex;flex-direction:column;gap:0;border-top:1px solid #1A1A1A">

<div style="display:grid;grid-template-columns:140px 280px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-4) var(--s-2);border-bottom:1px solid #E8E8E8">
<div style="font-size:20px;color:#6E6E73;letter-spacing:4px;font-weight:700">LAYER</div>
<div style="font-size:14px;color:#6E6E73;letter-spacing:3px;font-weight:700">CATEGORY</div>
<div style="font-size:14px;color:#6E6E73;letter-spacing:3px;font-weight:700">DESCRIPTION</div>
</div>

<div style="display:grid;grid-template-columns:140px 280px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-4) var(--s-2);border-bottom:1px solid #E8E8E8">
<div style="font-size:36px;color:#1A1A1A;font-weight:700;letter-spacing:2px">WHY</div>
<div style="font-size:22px;color:#E84E10;font-weight:700">Reframing</div>
<div style="font-size:22px;color:#1A1A1A;line-height:1.4">영산대를 다르게 보게 만든다</div>
</div>

<div style="display:grid;grid-template-columns:140px 280px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-4) var(--s-2);border-bottom:1px solid #E8E8E8">
<div style="font-size:36px;color:#1A1A1A;font-weight:700;letter-spacing:2px">HOW</div>
<div style="font-size:22px;color:#E84E10;font-weight:700">Insight Translation</div>
<div style="font-size:22px;color:#1A1A1A;line-height:1.4">숫자를 감각적 언어로 번역한다</div>
</div>

<div style="display:grid;grid-template-columns:140px 280px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-4) var(--s-2);border-bottom:1px solid #E8E8E8">
<div style="font-size:36px;color:#1A1A1A;font-weight:700;letter-spacing:2px">WHAT</div>
<div style="font-size:22px;color:#E84E10;font-weight:700">Social Proof</div>
<div style="font-size:22px;color:#1A1A1A;line-height:1.4">산업계가 숫자로 증명한다</div>
</div>

<div style="display:grid;grid-template-columns:140px 280px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-4) var(--s-2);border-bottom:2px solid #1A1A1A;background:#FFF8F3">
<div style="font-size:36px;color:#E84E10;font-weight:700;letter-spacing:2px">GOAL</div>
<div style="font-size:22px;color:#E84E10;font-weight:700">Imprinting</div>
<div style="font-size:22px;color:#1A1A1A;font-weight:700;line-height:1.4">영산대 = 호텔·관광 특성화 대학</div>
</div>

</div>
</div>"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.execute(
        "UPDATE sections SET content=?, title=? WHERE proposal_id=? AND order_idx=18",
        (P19, "4계층 레이어 광고 브리프", PID),
    )
    conn.commit()
    conn.close()
    print("[P19] 4계층 레이어 광고 브리프 적용")


if __name__ == "__main__":
    main()
