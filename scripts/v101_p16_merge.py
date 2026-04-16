# -*- coding: utf-8 -*-
"""V101 P16+P17 합치기: 3가지 숫자 → 리프레이밍 서브스텝."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


P16_MERGED = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:숫자를 기억으로-->
<style>
@keyframes rfFade{from{opacity:0;transform:translateX(-16px)}to{opacity:1;transform:translateX(0)}}
@keyframes titleSwap{from{opacity:0}to{opacity:1}}
.rf-after{opacity:0}
.rf-title-after{display:none}
.rf-title-before{display:inline}
.rf-wrap.expanded .rf-title-before{display:none}
.rf-wrap.expanded .rf-title-after{display:inline;animation:titleSwap .5s ease forwards}
.rf-wrap.expanded .rf-r1{animation:rfFade .5s ease .3s forwards}
.rf-wrap.expanded .rf-r2{animation:rfFade .5s ease .6s forwards}
.rf-wrap.expanded .rf-r3{animation:rfFade .5s ease .9s forwards}
</style>

<div id="morphPhase1" style="position:absolute;top:0;left:0;right:0;bottom:0;background:#fff;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0;z-index:5">

<div class="rf-wrap" id="morphWrap">

<div class="t-heading" style="margin-bottom:var(--s-4)">
<span class="rf-title-before"><span class="w-bold">3가지 숫자</span></span>
<span class="rf-title-after">숫자를 <span style="font-weight:700;color:#E84E10">기억</span>으로</span>
</div>

<div style="display:flex;flex-direction:column;gap:0;max-width:1100px;width:94%;margin:0 auto var(--s-4)">

<div style="display:grid;grid-template-columns:60px 1fr 280px;gap:var(--s-3);align-items:center;padding:var(--s-3) var(--s-2);border-top:1px solid #E8E8E8">
<div style="font-size:24px;font-weight:700;text-align:left">01</div>
<div style="font-size:20px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:left">총지배인 25명 · 승무원 동남권 최다 · 셰프 4명</div>
<div class="rf-after rf-r1" style="font-size:22px;font-weight:700;color:#E84E10;text-align:right">산업이 선택한 대학</div>
</div>

<div style="display:grid;grid-template-columns:60px 1fr 280px;gap:var(--s-3);align-items:center;padding:var(--s-3) var(--s-2);border-top:1px solid #E8E8E8">
<div style="font-size:24px;font-weight:700;text-align:left">02</div>
<div style="font-size:20px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:left">QS 호스피탈리티 세계 55위 · 국내 3위</div>
<div class="rf-after rf-r2" style="font-size:22px;font-weight:700;color:#E84E10;text-align:right">글로벌 1위가 될 때까지</div>
</div>

<div style="display:grid;grid-template-columns:60px 1fr 280px;gap:var(--s-3);align-items:center;padding:var(--s-3) var(--s-2);border-top:1px solid #E8E8E8;border-bottom:1px solid #E8E8E8">
<div style="font-size:24px;font-weight:700;text-align:left">03</div>
<div style="font-size:20px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:left">호텔 총지배인 25명 배출</div>
<div class="rf-after rf-r3" style="font-size:22px;font-weight:700;color:#E84E10;text-align:right">26번째가 당신</div>
</div>

</div>

</div>
</div>"""


def main():
    conn = sqlite3.connect(str(DB))

    # 1) P16 (idx=15) 통합 콘텐츠
    conn.execute(
        "UPDATE sections SET content=?, title=? WHERE proposal_id=? AND order_idx=15",
        (P16_MERGED, "3가지 숫자 → 기억 서브스텝", PID),
    )
    print("[1] P16 (idx=15) 서브스텝 통합")

    # 2) P17 (idx=16) 삭제
    conn.execute(
        "DELETE FROM sections WHERE proposal_id=? AND order_idx=16",
        (PID,),
    )
    print("[2] P17 (idx=16) 삭제")

    # 3) idx >= 17 전부 -1 시프트
    rows = conn.execute(
        "SELECT id, order_idx FROM sections WHERE proposal_id=? AND order_idx >= 17 ORDER BY order_idx ASC",
        (PID,),
    ).fetchall()
    for rid, idx in rows:
        conn.execute("UPDATE sections SET order_idx=? WHERE id=?", (idx - 1, rid))
    print(f"[3] idx >= 17 인 {len(rows)}개 row -1 시프트")

    conn.commit()

    rows = conn.execute(
        "SELECT order_idx, title FROM sections WHERE proposal_id=? AND order_idx BETWEEN 13 AND 18 ORDER BY order_idx",
        (PID,),
    ).fetchall()
    for r in rows:
        print(f"  idx={r[0]}: {r[1]}")

    total = conn.execute("SELECT COUNT(*) FROM sections WHERE proposal_id=?", (PID,)).fetchone()[0]
    print(f"\n총 {total}개 섹션")
    conn.close()


if __name__ == "__main__":
    main()
