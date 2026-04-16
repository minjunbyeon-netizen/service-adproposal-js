# -*- coding: utf-8 -*-
"""V101 - P19 앞에 '각인' 컨셉 선언 슬라이드 삽입 + P19 4계층 인트로 추가."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


GAKGIN = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:Ad Concept--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0">

<div style="font-size:24px;color:#6E6E73;margin-bottom:var(--s-3)">그래서 이 숫자를 기억시키는 행위, 즉</div>

<div style="font-size:160px;font-weight:700;color:#E84E10;line-height:1;letter-spacing:-4px;margin-bottom:var(--s-4)">각인</div>

<div style="font-size:24px;color:#1A1A1A;line-height:1.5">이것이 우리가 제안하는<br>영산대학교의 광고 컨셉입니다</div>

</div>"""


P19_WITH_INTRO = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:4-Layer Brief--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;padding:var(--s-5) var(--s-6);max-width:1500px;margin:0 auto">

<div style="font-size:14px;color:#E84E10;font-weight:700;letter-spacing:4px;margin-bottom:var(--s-2)">AD BRIEF · 4 LAYERS</div>

<div style="font-size:44px;font-weight:700;color:#1A1A1A;line-height:1.3;margin-bottom:var(--s-5);letter-spacing:-1px"><span style="color:#E84E10">각인</span>을 위해, 우리는<br><span style="color:#1A1A1A">4계층 레이어</span>를 제안합니다</div>

<div style="display:flex;flex-direction:column;gap:0;border-top:1px solid #1A1A1A">

<div style="display:grid;grid-template-columns:140px 280px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-3) var(--s-2);border-bottom:1px solid #E8E8E8">
<div style="font-size:14px;color:#6E6E73;letter-spacing:4px;font-weight:700">LAYER</div>
<div style="font-size:14px;color:#6E6E73;letter-spacing:3px;font-weight:700">CATEGORY</div>
<div style="font-size:14px;color:#6E6E73;letter-spacing:3px;font-weight:700">DESCRIPTION</div>
</div>

<div style="display:grid;grid-template-columns:140px 280px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-3) var(--s-2);border-bottom:1px solid #E8E8E8">
<div style="font-size:32px;color:#1A1A1A;font-weight:700;letter-spacing:2px">WHY</div>
<div style="font-size:20px;color:#E84E10;font-weight:700">Reframing</div>
<div style="font-size:20px;color:#1A1A1A;line-height:1.4">영산대를 다르게 보게 만든다</div>
</div>

<div style="display:grid;grid-template-columns:140px 280px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-3) var(--s-2);border-bottom:1px solid #E8E8E8">
<div style="font-size:32px;color:#1A1A1A;font-weight:700;letter-spacing:2px">HOW</div>
<div style="font-size:20px;color:#E84E10;font-weight:700">Insight Translation</div>
<div style="font-size:20px;color:#1A1A1A;line-height:1.4">숫자를 감각적 언어로 번역한다</div>
</div>

<div style="display:grid;grid-template-columns:140px 280px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-3) var(--s-2);border-bottom:1px solid #E8E8E8">
<div style="font-size:32px;color:#1A1A1A;font-weight:700;letter-spacing:2px">WHAT</div>
<div style="font-size:20px;color:#E84E10;font-weight:700">Social Proof</div>
<div style="font-size:20px;color:#1A1A1A;line-height:1.4">산업계가 숫자로 증명한다</div>
</div>

<div style="display:grid;grid-template-columns:140px 280px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-3) var(--s-2);border-bottom:2px solid #1A1A1A;background:#FFF8F3">
<div style="font-size:32px;color:#E84E10;font-weight:700;letter-spacing:2px">GOAL</div>
<div style="font-size:20px;color:#E84E10;font-weight:700">Imprinting</div>
<div style="font-size:20px;color:#1A1A1A;font-weight:700;line-height:1.4">영산대 = 호텔·관광 특성화 대학</div>
</div>

</div>
</div>"""


def main():
    conn = sqlite3.connect(str(DB))

    # idx >= 18 전부 +1 시프트
    rows = conn.execute(
        "SELECT id, order_idx FROM sections WHERE proposal_id=? AND order_idx >= 18 ORDER BY order_idx DESC",
        (PID,),
    ).fetchall()
    for rid, idx in rows:
        conn.execute("UPDATE sections SET order_idx=? WHERE id=?", (idx + 1, rid))
    print(f"[1] idx >= 18 인 {len(rows)}개 +1 시프트")

    # idx=18에 각인 컨셉 슬라이드 삽입
    conn.execute(
        """INSERT INTO sections (proposal_id, order_idx, level, title, content)
           VALUES (?, 18, 2, '각인 — 광고 컨셉', ?)""",
        (PID, GAKGIN),
    )
    print("[2] idx=18 각인 컨셉 슬라이드 삽입")

    # 원래 4계층 (현재 idx=19로 시프트됨)에 인트로 추가
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=19",
        (P19_WITH_INTRO, PID),
    )
    print("[3] idx=19 4계층 슬라이드 인트로 추가 (각인을 위해, 4계층 레이어)")

    conn.commit()
    rows = conn.execute(
        "SELECT order_idx, title FROM sections WHERE proposal_id=? AND order_idx BETWEEN 16 AND 21 ORDER BY order_idx",
        (PID,),
    ).fetchall()
    print("\n== 앞뒤 순서 ==")
    for r in rows:
        print(f"  idx={r[0]}: {r[1]}")
    conn.close()


if __name__ == "__main__":
    main()
