# -*- coding: utf-8 -*-
"""V101 - P5 뒤에 새 페이지 삽입 (경성대 밑에 호텔관광 영산대)."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


NEW_CONTENT = """<!--PARENT:Ⅰ. 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-4) 0"><div style="display:flex;flex-direction:column;gap:0;max-width:860px;width:100%;margin:0 auto var(--s-4)"><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:20px;color:#1A1A1A;text-align:left;flex:1"><span style="font-weight:700;color:#1A1A1A">한의학</span> <span style="color:#6E6E73">한의대 전통</span></div><div style="font-size:24px;font-weight:700;color:#1A1A1A;min-width:140px;text-align:right">동의대</div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:20px;color:#1A1A1A;text-align:left;flex:1"><span style="font-weight:700;color:#1A1A1A">해양·수산</span> <span style="color:#6E6E73">국립의 규모</span></div><div style="font-size:24px;font-weight:700;color:#1A1A1A;min-width:140px;text-align:right">부경대</div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:20px;color:#1A1A1A;text-align:left;flex:1"><span style="font-weight:700;color:#1A1A1A">종합대학</span> <span style="color:#6E6E73">사범·의료 중심</span></div><div style="font-size:24px;font-weight:700;color:#1A1A1A;min-width:140px;text-align:right">신라대</div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:20px;color:#1A1A1A;text-align:left;flex:1"><span style="font-weight:700;color:#1A1A1A">의과대학</span> <span style="color:#6E6E73">기독교 전통</span></div><div style="font-size:24px;font-weight:700;color:#1A1A1A;min-width:140px;text-align:right">고신대</div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:20px;color:#1A1A1A;text-align:left;flex:1"><span style="font-weight:700;color:#1A1A1A">약학·예술</span> <span style="color:#6E6E73">통합 캠퍼스</span></div><div style="font-size:24px;font-weight:700;color:#1A1A1A;min-width:140px;text-align:right">경성대</div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:2px solid #E84E10;background:#FFF8F3"><div style="font-size:20px;color:#1A1A1A;text-align:left;flex:1;padding-left:var(--s-2)"><span style="font-weight:700;color:#E84E10">호텔관광</span> <span style="color:#6E6E73">특성화 대학</span></div><div style="font-size:24px;font-weight:700;color:#E84E10;min-width:140px;text-align:right;padding-right:var(--s-2)">영산대</div></div></div><div style="width:80px;height:1px;background:#E0E0E0;margin:0 auto var(--s-4)"></div><div class="t-headline">영산대는 <span class="w-bold">호텔관광</span>으로 자리잡았습니다</div></div>"""


def main():
    conn = sqlite3.connect(str(DB))

    # 1) idx >= 5 인 모든 row를 +1 시프트 (내림차순으로 UPDATE 해야 충돌 없음)
    rows = conn.execute(
        "SELECT id, order_idx FROM sections WHERE proposal_id=? AND order_idx >= 5 ORDER BY order_idx DESC",
        (PID,),
    ).fetchall()
    for rid, idx in rows:
        conn.execute("UPDATE sections SET order_idx=? WHERE id=?", (idx + 1, rid))
    print(f"idx >= 5 인 {len(rows)}개 row +1 시프트")

    # 2) 새 slide를 idx=5 에 삽입
    conn.execute(
        """INSERT INTO sections (proposal_id, order_idx, level, title, content)
           VALUES (?, 5, 2, '영산대는 호텔관광으로 자리잡았습니다', ?)""",
        (PID, NEW_CONTENT),
    )
    print("idx=5 새 슬라이드 삽입 완료")

    conn.commit()

    # 3) 확인
    rows = conn.execute(
        "SELECT order_idx, title FROM sections WHERE proposal_id=? AND order_idx BETWEEN 3 AND 8 ORDER BY order_idx",
        (PID,),
    ).fetchall()
    print("\n== 앞부분 ==")
    for r in rows:
        print(f"  idx={r[0]}: {r[1]}")

    conn.close()
    print("\n완료")


if __name__ == "__main__":
    main()
