# -*- coding: utf-8 -*-
"""V101 P27 삭제 + P29 삭제 + P28-P30 합침.

작업:
  - idx 26 (P27 시안) 삭제
  - idx 28 (P29 슬로건) 삭제
  - idx 29 (P30 써머리) 삭제
  - idx 27 (P28 전환) → 합쳐진 (전환 + 써머리) 페이지로 교체
  - idx 27 → idx 26 이동
  - idx 30~ → -3 시프트

결과:
  - 새 P27 (idx=26): 전환 + 써머리 합본
  - 새 P28 (idx=27): 영상 (기존 idx=30)
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

# =============================================================================
# 합본 — 상단 전환 멘트 + 하단 써머리
# =============================================================================
COMBINED_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:전환 + 요약--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-caption is-muted" style="letter-spacing:3px;margin-bottom:var(--s-3)">— SHIFT —</div><div style="font-size:38px;font-weight:700;color:#1A1A1A;line-height:1.4;margin-bottom:var(--s-2);letter-spacing:-0.8px">지면으로 <span style="color:#6E6E73;font-weight:400">임팩트</span>를 주었다면,</div><div style="font-size:38px;font-weight:700;color:#1A1A1A;line-height:1.4;margin-bottom:var(--s-4);letter-spacing:-0.8px">영상으로는 <span class="is-accent">스토리</span>를 풀어냅니다</div><div style="width:120px;height:1px;background:#E0E0E0;margin:0 auto var(--s-4)"></div><div style="display:flex;flex-direction:column;gap:0;max-width:880px;width:94%;margin:0 auto"><div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #F0F0F0"><div style="font-size:11px;font-weight:700;color:#E84E10;letter-spacing:3px;min-width:100px;text-align:left">컨셉</div><div style="font-size:16px;font-weight:700;color:#1A1A1A;text-align:left;flex:1">증명 <span style="font-size:12px;color:#6E6E73;font-weight:400;margin-left:8px">— 주장이 아닌, 숫자가 박히는 일</span></div></div><div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #F0F0F0"><div style="font-size:11px;font-weight:700;color:#E84E10;letter-spacing:3px;min-width:100px;text-align:left">기법</div><div style="font-size:16px;font-weight:700;color:#1A1A1A;text-align:left;flex:1">리프레이밍 <span style="font-size:12px;color:#6E6E73;font-weight:400;margin-left:8px">— 같은 숫자, 다른 프레임으로</span></div></div><div style="display:flex;align-items:flex-start;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #F0F0F0"><div style="font-size:11px;font-weight:700;color:#E84E10;letter-spacing:3px;min-width:100px;text-align:left;padding-top:2px">시안</div><div style="font-size:13px;color:#1A1A1A;text-align:left;flex:1;line-height:1.7">산업이 선택한 대학 · 글로벌 1위가 될 때까지 · 26번째가 당신이 될 때까지</div></div><div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #F0F0F0"><div style="font-size:11px;font-weight:700;color:#E84E10;letter-spacing:3px;min-width:100px;text-align:left">영상</div><div style="font-size:14px;color:#1A1A1A;text-align:left;flex:1">호텔관광 특성화의 생생한 현장 — 취업과 글로벌 무대로 가는 길</div></div><div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0"><div style="font-size:11px;font-weight:700;color:#E84E10;letter-spacing:3px;min-width:100px;text-align:left">효과</div><div style="font-size:14px;color:#1A1A1A;text-align:left;flex:1">기억 <span style="font-size:18px;color:#E84E10;margin:0 6px">→</span> <strong>각인</strong> <span style="font-size:18px;color:#E84E10;margin:0 6px">→</span> <strong>지원</strong></div></div></div></div><!--SCRIPT_START-->"지금까지 지면광고로 <strong>임팩트</strong>를 보여드렸습니다.<br>이제부터 영상광고로 <strong>스토리</strong>를 풀어내겠습니다.<br><br>그전에, 전체 제안을 한 눈에 정리하면 —<br><br>컨셉은 <strong>증명</strong>, 기법은 <strong>리프레이밍</strong>.<br>3가지 시안과 영상으로 영산대의 자랑을 각인시키고,<br>기억을 <strong>지원</strong>으로 전환시키겠습니다."<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    try:
        # 1. idx 27 (P28 전환) → 합쳐진 content로 UPDATE
        conn.execute(
            "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=27",
            ("전환 + 전체 요약", COMBINED_CONTENT, PID),
        )
        print("idx=27 합본 content로 UPDATE")

        # 2. idx 26 (P27 시안), idx 28 (P29 슬로건), idx 29 (P30 써머리) DELETE
        deleted = conn.execute(
            "DELETE FROM sections WHERE proposal_id=? AND order_idx IN (26, 28, 29)",
            (PID,),
        ).rowcount
        print(f"DELETE idx 26, 28, 29 ({deleted}개)")

        # 3. idx 27 → idx 26으로 이동 (한 칸 당김)
        conn.execute(
            "UPDATE sections SET order_idx=26 WHERE proposal_id=? AND order_idx=27",
            (PID,),
        )
        print("idx 27 → idx 26 (합본 위치 정렬)")

        # 4. idx 30~ → -3 시프트
        conn.execute(
            "UPDATE sections SET order_idx = order_idx - 3 "
            "WHERE proposal_id=? AND order_idx >= 30",
            (PID,),
        )
        print("idx 30~ -3 시프트")

        conn.commit()

        # 결과
        rows = conn.execute(
            "SELECT order_idx, title FROM sections WHERE proposal_id=? AND order_idx BETWEEN 22 AND 32 ORDER BY order_idx",
            (PID,),
        ).fetchall()
        print(f"\n=== V101 P22~P32 주변 ===")
        for r in rows:
            pagenum = r["order_idx"] + 1
            print(f"  P{pagenum:2d} (idx={r['order_idx']:2d}) | {r['title']}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
