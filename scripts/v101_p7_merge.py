# -*- coding: utf-8 -*-
"""V101 P7+P8 합치기: 같은 슬라이드에서 0825503 → 08/25/55/03 서브스텝 트랜지션."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


# P7: 두 상태를 가진 슬라이드
# state-1: 표지 복제 (0825503)
# state-2: 숫자 분리 + 펜글씨 화살표 (방향키 한번 더 누르면)
P7_MERGED = """<!--PARENT:Ⅰ. 제안개요--><!--TAG:0825503 해독-->
<style>
@keyframes brushDraw{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
@keyframes labelUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
.morph-brush{clip-path:inset(0 100% 0 0)}
.morph-desc{opacity:0}
.morph-phase2.active .mg1 .morph-brush{animation:brushDraw .5s ease .2s forwards}
.morph-phase2.active .mg2 .morph-brush{animation:brushDraw .5s ease .5s forwards}
.morph-phase2.active .mg3 .morph-brush{animation:brushDraw .5s ease .8s forwards}
.morph-phase2.active .mg4 .morph-brush{animation:brushDraw .5s ease 1.1s forwards}
.morph-phase2.active .mg1 .morph-desc{animation:labelUp .4s ease .5s forwards}
.morph-phase2.active .mg2 .morph-desc{animation:labelUp .4s ease .8s forwards}
.morph-phase2.active .mg3 .morph-desc{animation:labelUp .4s ease 1.1s forwards}
.morph-phase2.active .mg4 .morph-desc{animation:labelUp .4s ease 1.4s forwards}
</style>

<div style="position:absolute;top:0;left:0;right:0;bottom:0;z-index:5">

<!-- PHASE 1: 표지 복제 -->
<div id="morphPhase1" style="position:absolute;top:0;left:0;right:0;bottom:0;background:#fff;display:flex;justify-content:center;align-items:center;overflow:hidden;transition:opacity .4s">
<div style="position:absolute;top:80px;right:120px;font-size:14px;color:#1A1A1A;font-weight:700">HIVE MEDIA</div>
<div style="position:relative;text-align:center">
<div style="position:absolute;top:-68px;left:50%;transform:translateX(-50%);font-size:14px;color:#A0A0A5;font-weight:700;white-space:nowrap">SERIAL NO.</div>
<div style="font-size:var(--fs-display);font-weight:700;line-height:0.9;color:#1A1A1A;font-variant-numeric:tabular-nums;text-align:center">0825503</div>
</div>
<div style="position:absolute;bottom:0;left:0;right:0;height:8px;background:#E84E10"></div>
<div style="position:absolute;bottom:28px;right:40px;font-size:14px;font-weight:700;color:#6E6E73">07</div>
</div>

<!-- PHASE 2: 숫자 분리 + 화살표 (초기에 숨김) -->
<div id="morphPhase2" class="morph-phase2" style="position:absolute;top:0;left:0;right:0;bottom:0;background:#fff;display:none;flex-direction:column;justify-content:center;align-items:center;overflow:hidden">

<div style="font-size:14px;color:#6E6E73;letter-spacing:4px;font-weight:700;margin-bottom:var(--s-5)">SERIAL NO. 0825503</div>

<div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:var(--s-5);max-width:1200px;width:90%;margin-bottom:var(--s-3)">

<div class="mg1" style="display:flex;flex-direction:column;align-items:center;gap:var(--s-2)">
<div style="font-size:96px;font-weight:700;color:#1A1A1A;line-height:1;font-variant-numeric:tabular-nums">08</div>
<div class="morph-brush" style="position:relative;width:100%;height:32px">
<svg viewBox="0 0 160 32" width="160" height="32" style="display:block;margin:0 auto"><path d="M10,22 C30,4 60,4 80,16 C100,28 130,8 150,14" stroke="#E84E10" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M140,6 L150,14 L140,20" stroke="#E84E10" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
</div>
<div class="morph-desc" style="text-align:center"><div style="font-size:20px;font-weight:700;color:#1A1A1A;line-height:1.3">연구력 세계 8위</div><div style="font-size:13px;color:#6E6E73;margin-top:4px">국내 1위</div></div>
</div>

<div class="mg2" style="display:flex;flex-direction:column;align-items:center;gap:var(--s-2)">
<div style="font-size:96px;font-weight:700;color:#1A1A1A;line-height:1;font-variant-numeric:tabular-nums">25</div>
<div class="morph-brush" style="position:relative;width:100%;height:32px">
<svg viewBox="0 0 160 32" width="160" height="32" style="display:block;margin:0 auto"><path d="M10,20 C40,6 70,6 90,18 C110,30 140,10 150,16" stroke="#E84E10" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M140,8 L150,16 L142,22" stroke="#E84E10" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
</div>
<div class="morph-desc" style="text-align:center"><div style="font-size:20px;font-weight:700;color:#1A1A1A;line-height:1.3">총지배인 25명</div><div style="font-size:13px;color:#6E6E73;margin-top:4px">호텔업계 배출</div></div>
</div>

<div class="mg3" style="display:flex;flex-direction:column;align-items:center;gap:var(--s-2)">
<div style="font-size:96px;font-weight:700;color:#1A1A1A;line-height:1;font-variant-numeric:tabular-nums">55</div>
<div class="morph-brush" style="position:relative;width:100%;height:32px">
<svg viewBox="0 0 160 32" width="160" height="32" style="display:block;margin:0 auto"><path d="M10,18 C35,4 65,8 85,20 C105,32 135,6 150,12" stroke="#E84E10" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M140,4 L150,12 L140,18" stroke="#E84E10" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
</div>
<div class="morph-desc" style="text-align:center"><div style="font-size:20px;font-weight:700;color:#1A1A1A;line-height:1.3">QS 호스피탈리티</div><div style="font-size:13px;color:#6E6E73;margin-top:4px">세계 55위</div></div>
</div>

<div class="mg4" style="display:flex;flex-direction:column;align-items:center;gap:var(--s-2)">
<div style="font-size:96px;font-weight:700;color:#1A1A1A;line-height:1;font-variant-numeric:tabular-nums">03</div>
<div class="morph-brush" style="position:relative;width:100%;height:32px">
<svg viewBox="0 0 160 32" width="160" height="32" style="display:block;margin:0 auto"><path d="M10,22 C30,6 65,4 85,18 C105,30 130,8 150,14" stroke="#E84E10" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M140,6 L150,14 L140,20" stroke="#E84E10" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
</div>
<div class="morph-desc" style="text-align:center"><div style="font-size:20px;font-weight:700;color:#1A1A1A;line-height:1.3">한국 호텔관광</div><div style="font-size:13px;color:#6E6E73;margin-top:4px">TOP 3</div></div>
</div>

</div>

<div style="position:absolute;bottom:0;left:0;right:0;height:8px;background:#E84E10"></div>
<div style="position:absolute;bottom:28px;right:40px;font-size:14px;font-weight:700;color:#6E6E73">07</div>
</div>

</div>"""


def main():
    conn = sqlite3.connect(str(DB))

    # 1) P7(idx=6) 통합 콘텐츠로 교체
    conn.execute(
        "UPDATE sections SET content=?, title=? WHERE proposal_id=? AND order_idx=6",
        (P7_MERGED, "0825503 → 08/25/55/03 트랜지션", PID),
    )
    print("[1] P7 (idx=6) 서브스텝 트랜지션으로 교체")

    # 2) P8 모프 슬라이드(idx=7) 삭제
    conn.execute(
        "DELETE FROM sections WHERE proposal_id=? AND order_idx=7 AND title='0825503 해독 트랜지션'",
        (PID,),
    )
    print("[2] P8 (idx=7) 별도 모프 슬라이드 삭제")

    # 3) idx >= 8 전부 -1 시프트
    rows = conn.execute(
        "SELECT id, order_idx FROM sections WHERE proposal_id=? AND order_idx >= 8 ORDER BY order_idx ASC",
        (PID,),
    ).fetchall()
    for rid, idx in rows:
        conn.execute("UPDATE sections SET order_idx=? WHERE id=?", (idx - 1, rid))
    print(f"[3] idx >= 8 인 {len(rows)}개 row -1 시프트")

    conn.commit()

    rows = conn.execute(
        "SELECT order_idx, title FROM sections WHERE proposal_id=? AND order_idx BETWEEN 5 AND 10 ORDER BY order_idx",
        (PID,),
    ).fetchall()
    for r in rows:
        print(f"  idx={r[0]}: {r[1]}")

    conn.close()
    print("\n완료")


if __name__ == "__main__":
    main()
