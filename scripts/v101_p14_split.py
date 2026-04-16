# -*- coding: utf-8 -*-
"""V101 - P14 2장 분할 (3개씩) + P16 중앙정렬."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


P14 = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:Memory Test--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;padding:var(--s-4) var(--s-4) var(--s-3)">

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s-4);max-width:1400px;width:100%;margin:0 auto">
<div style="display:flex;flex-direction:column;align-items:center;gap:var(--s-2)"><img src="/assets/image/other_univ/u1.png" alt="동신대" style="width:100%;height:auto;max-height:460px;object-fit:contain;box-shadow:0 4px 16px rgba(0,0,0,0.15)"><div style="font-size:14px;color:#6E6E73">동신대 · 취업률 1위</div></div>
<div style="display:flex;flex-direction:column;align-items:center;gap:var(--s-2)"><img src="/assets/image/other_univ/u2.png" alt="수원여대" style="width:100%;height:auto;max-height:460px;object-fit:contain;box-shadow:0 4px 16px rgba(0,0,0,0.15)"><div style="font-size:14px;color:#6E6E73">수원여대 · 취업률 1위 달성</div></div>
<div style="display:flex;flex-direction:column;align-items:center;gap:var(--s-2)"><img src="/assets/image/other_univ/u3.png" alt="한국기술교육대" style="width:100%;height:auto;max-height:460px;object-fit:contain;box-shadow:0 4px 16px rgba(0,0,0,0.15)"><div style="font-size:14px;color:#6E6E73">한국기술교육대 · 4년제 대학 1위</div></div>
</div>

</div>"""


P14_NEW = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:Memory Test--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;padding:var(--s-4) var(--s-4) var(--s-3)">

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s-4);max-width:1400px;width:100%;margin:0 auto var(--s-4)">
<div style="display:flex;flex-direction:column;align-items:center;gap:var(--s-2)"><img src="/assets/image/other_univ/u5.png" alt="한양사이버대" style="width:100%;height:auto;max-height:400px;object-fit:contain;box-shadow:0 4px 16px rgba(0,0,0,0.15)"><div style="font-size:14px;color:#6E6E73">한양사이버대 · 1등 넘어 월등하게</div></div>
<div style="display:flex;flex-direction:column;align-items:center;gap:var(--s-2)"><img src="/assets/image/other_univ/u6.png" alt="대전 대학" style="width:100%;height:auto;max-height:400px;object-fit:contain;box-shadow:0 4px 16px rgba(0,0,0,0.15)"><div style="font-size:14px;color:#6E6E73">대전 · 국고 1,295억 확보</div></div>
<div style="display:flex;flex-direction:column;align-items:center;gap:var(--s-2)"><img src="/assets/image/other_univ/u8.png" alt="대관령대" style="width:100%;height:auto;max-height:400px;object-fit:contain;box-shadow:0 4px 16px rgba(0,0,0,0.15)"><div style="font-size:14px;color:#6E6E73">대관령 · 전국 4년제 1위</div></div>
</div>

<div style="text-align:center">
<div style="font-size:48px;font-weight:700;color:#1A1A1A;line-height:1.3">앞서 말씀드렸던 <span style="color:#E84E10">기억</span>이 될까요?</div>
</div>

</div>"""


P16_CENTER = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:Three Numbers--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0">

<div class="t-heading" style="margin-bottom:var(--s-4)"><span class="w-bold">3가지 숫자</span></div>

<div style="display:flex;flex-direction:column;gap:0;max-width:900px;width:94%;margin:0 auto">

<div style="display:grid;grid-template-columns:80px 1fr;gap:var(--s-3);align-items:center;padding:var(--s-3) var(--s-2);border-top:1px solid #E8E8E8">
<div style="font-size:24px;font-weight:700;text-align:center">01</div>
<div style="font-size:20px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:center">총지배인 25명 · 승무원 동남권 최다 · 셰프 4명</div>
</div>

<div style="display:grid;grid-template-columns:80px 1fr;gap:var(--s-3);align-items:center;padding:var(--s-3) var(--s-2);border-top:1px solid #E8E8E8">
<div style="font-size:24px;font-weight:700;text-align:center">02</div>
<div style="font-size:20px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:center">QS 호스피탈리티 세계 55위 · 국내 3위</div>
</div>

<div style="display:grid;grid-template-columns:80px 1fr;gap:var(--s-3);align-items:center;padding:var(--s-3) var(--s-2);border-top:1px solid #E8E8E8;border-bottom:1px solid #E8E8E8">
<div style="font-size:24px;font-weight:700;text-align:center">03</div>
<div style="font-size:20px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:center">호텔 총지배인 25명 배출</div>
</div>

</div>
</div>"""


def main():
    conn = sqlite3.connect(str(DB))

    # 1) P14 (idx=13) 3개만으로 교체
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=13",
        (P14, PID),
    )
    print("[1] P14 (idx=13) - 3개 광고만")

    # 2) idx >= 14 전부 +1 시프트 (새 P15 자리 확보)
    rows = conn.execute(
        "SELECT id, order_idx FROM sections WHERE proposal_id=? AND order_idx >= 14 ORDER BY order_idx DESC",
        (PID,),
    ).fetchall()
    for rid, idx in rows:
        conn.execute("UPDATE sections SET order_idx=? WHERE id=?", (idx + 1, rid))
    print(f"[2] idx >= 14 인 {len(rows)}개 +1 시프트")

    # 3) idx=14 신규 P15 삽입 (3개 광고 + 기억이 될까요)
    conn.execute(
        """INSERT INTO sections (proposal_id, order_idx, level, title, content)
           VALUES (?, 14, 2, '기억이 될까요 - 2페이지', ?)""",
        (PID, P14_NEW),
    )
    print("[3] 신규 P15 (idx=14) 삽입 - 3개 + 기억이 될까요")

    # 4) P16 (원래 idx=15 이었으나 시프트로 idx=16이 됨) static 중앙정렬
    # 실제로는 P16 idx=16이 '3가지 숫자 static' 위치. 확인 필요
    # 시프트 후: idx=15 was P16 static -> 이제 idx=16
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=16",
        (P16_CENTER, PID),
    )
    print("[4] P16 (idx=16 shifted) 중앙정렬")

    conn.commit()
    rows = conn.execute(
        "SELECT order_idx, title FROM sections WHERE proposal_id=? AND order_idx BETWEEN 12 AND 19 ORDER BY order_idx",
        (PID,),
    ).fetchall()
    print("\n== 현재 순서 ==")
    for r in rows:
        print(f"  idx={r[0]}: {r[1]}")
    conn.close()


if __name__ == "__main__":
    main()
