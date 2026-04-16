# -*- coding: utf-8 -*-
"""V101 컨셉 슬라이드를 divider 이후로 이동 + '증명' 네이밍 추가.

변경 전:
  idx 6  제안의 전부 (각인 선언)
  idx 7  제안업체
  idx 8  divider
  idx 9  프리뷰

변경 후:
  idx 6  제안업체
  idx 7  divider
  idx 8  컨셉 "증명" (신규 — 각인+증명 네이밍)
  idx 9  프리뷰 (유지)

논리 체인: 질문→답(P6) / 회사(P7) / divider(P8) / 컨셉 증명(P9) / 프리뷰(P10)
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

CONCEPT_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-4)">앞서 보신 영산대의 움직임을 —</div><div class="t-title" style="margin-bottom:var(--s-5);line-height:1.3">수험생과 학부모에게 <span class="is-accent">각인시키는 것</span></div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div style="display:flex;align-items:baseline;justify-content:center;gap:var(--s-3);margin-bottom:var(--s-5)"><div style="font-size:48px;font-weight:700;color:#1A1A1A;line-height:1">=</div><div class="t-hero" style="color:#E84E10">증명</div></div><div class="t-subtitle w-regular is-muted" style="line-height:1.8">주장이 아닌, <span class="is-ink w-bold">숫자가 기억에 박히는 일</span><br>이것이, 저희의 광고 <span class="is-accent w-bold">컨셉</span>입니다</div></div><!--SCRIPT_START-->"앞서 보신 영산대의 움직임을 — 수험생과 학부모에게 <strong>각인시키는 것.</strong><br><br>저희는 이것을 한 단어로 <strong>'증명'</strong>이라 부릅니다.<br><br>주장이 아닌, <strong>숫자가 기억에 박히는 일</strong>. 이것이 저희의 광고 <strong>컨셉</strong>입니다."<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    try:
        # 1. 기존 idx=6 "제안의 전부" 삭제
        conn.execute(
            "DELETE FROM sections WHERE proposal_id=? AND order_idx=6",
            (PID,),
        )
        print("기존 idx=6 '제안의 전부' 삭제")

        # 2. idx 7 (제안업체), idx 8 (divider) → idx 6, 7로 시프트
        # (idx 9 프리뷰는 그대로, idx 10~ 시안도 그대로)
        # 주의: 7→6, 8→7 순서로 해야 충돌 없음
        conn.execute(
            "UPDATE sections SET order_idx=6 WHERE proposal_id=? AND order_idx=7",
            (PID,),
        )
        conn.execute(
            "UPDATE sections SET order_idx=7 WHERE proposal_id=? AND order_idx=8",
            (PID,),
        )
        print("제안업체 idx 7→6, divider idx 8→7 시프트")

        # 3. 기존 proposal level 참고해서 신규 컨셉 section INSERT
        sample = conn.execute(
            "SELECT level, status FROM sections WHERE proposal_id=? AND order_idx=9",
            (PID,),
        ).fetchone()
        lvl = sample["level"]
        st = sample["status"]

        # 4. 새 컨셉 슬라이드 idx=8 삽입
        conn.execute(
            """INSERT INTO sections (proposal_id, level, title, order_idx, content, status)
               VALUES (?,?,?,?,?,?)""",
            (PID, lvl, "컨셉 — 증명", 8, CONCEPT_CONTENT, st),
        )
        print("신규 컨셉 슬라이드 idx=8 삽입 (증명)")

        conn.commit()

        # 5. 결과
        rows = conn.execute(
            "SELECT order_idx, title FROM sections WHERE proposal_id=? ORDER BY order_idx LIMIT 12",
            (PID,),
        ).fetchall()
        print(f"\n=== V101 재구성 후 ===")
        for r in rows:
            print(f"  idx={r['order_idx']:2d} | {r['title']}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
