# -*- coding: utf-8 -*-
"""V101 P16을 둘로 분리:
  - 원 P16 (idx=15): 트랜지션 제거, static 텍스트만
  - 신규 P18 (idx=17 삽입): 현재 P16의 트랜지션 버전 복사"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


# 새 P16 - static: 3가지 숫자 + 01/02/03 텍스트만
P16_STATIC = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:Three Numbers--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0">

<div class="t-heading" style="margin-bottom:var(--s-4)"><span class="w-bold">3가지 숫자</span></div>

<div style="display:flex;flex-direction:column;gap:0;max-width:1100px;width:94%;margin:0 auto">

<div style="display:grid;grid-template-columns:80px 1fr;gap:var(--s-3);align-items:center;padding:var(--s-3) var(--s-2);border-top:1px solid #E8E8E8">
<div style="font-size:24px;font-weight:700;text-align:center">01</div>
<div style="font-size:20px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:left">총지배인 25명 · 승무원 동남권 최다 · 셰프 4명</div>
</div>

<div style="display:grid;grid-template-columns:80px 1fr;gap:var(--s-3);align-items:center;padding:var(--s-3) var(--s-2);border-top:1px solid #E8E8E8">
<div style="font-size:24px;font-weight:700;text-align:center">02</div>
<div style="font-size:20px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:left">QS 호스피탈리티 세계 55위 · 국내 3위</div>
</div>

<div style="display:grid;grid-template-columns:80px 1fr;gap:var(--s-3);align-items:center;padding:var(--s-3) var(--s-2);border-top:1px solid #E8E8E8;border-bottom:1px solid #E8E8E8">
<div style="font-size:24px;font-weight:700;text-align:center">03</div>
<div style="font-size:20px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:left">호텔 총지배인 25명 배출</div>
</div>

</div>
</div>"""


def main():
    conn = sqlite3.connect(str(DB))

    # 1) 현재 P16 콘텐츠 백업 (트랜지션 버전)
    row = conn.execute(
        "SELECT content FROM sections WHERE proposal_id=? AND order_idx=15",
        (PID,),
    ).fetchone()
    P16_TRANSITION_CONTENT = row[0]
    print("P16 트랜지션 버전 백업")

    # 2) idx >= 17 전부 +1 시프트 (새 P18 자리 확보)
    rows = conn.execute(
        "SELECT id, order_idx FROM sections WHERE proposal_id=? AND order_idx >= 17 ORDER BY order_idx DESC",
        (PID,),
    ).fetchall()
    for rid, idx in rows:
        conn.execute("UPDATE sections SET order_idx=? WHERE id=?", (idx + 1, rid))
    print(f"idx >= 17 인 {len(rows)}개 row +1 시프트")

    # 3) idx=17에 트랜지션 P16 복사 삽입 (신규 P18)
    conn.execute(
        """INSERT INTO sections (proposal_id, order_idx, level, title, content)
           VALUES (?, 17, 2, '3가지 숫자 → 기억 리프레이밍', ?)""",
        (PID, P16_TRANSITION_CONTENT),
    )
    print("신규 P18 (idx=17) 삽입 - 트랜지션 버전")

    # 4) P16 (idx=15) static 버전으로 교체
    conn.execute(
        "UPDATE sections SET content=?, title=? WHERE proposal_id=? AND order_idx=15",
        (P16_STATIC, "3가지 숫자 — static", PID),
    )
    print("P16 (idx=15) static 버전 교체")

    conn.commit()
    rows = conn.execute(
        "SELECT order_idx, title FROM sections WHERE proposal_id=? AND order_idx BETWEEN 14 AND 19 ORDER BY order_idx",
        (PID,),
    ).fetchall()
    print("\n== 현재 순서 ==")
    for r in rows:
        print(f"  idx={r[0]}: {r[1]}")
    conn.close()


if __name__ == "__main__":
    main()
