# -*- coding: utf-8 -*-
"""V101 P12 뒤에 '다른 학교 광고' 전환+그리드 3장 삽입.

P12  광고 시안 — 취업률 1위 (YSU 포스터, 기존 유지)
P13  [신규] TEXT 전환: "이제 다른 학교 광고도 보겠습니다"
P14  [신규] 다른 학교 광고 — 가로/정방형 4장 그리드
P15  [신규] 다른 학교 광고 — 세로형 3장 그리드
P16~ 기존 P13~ (+3 시프트)
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

# =============================================================================
# P13 신규: TEXT 전환
# =============================================================================
P13_TEXT = """<!--PARENT:III 세부 과업 수행 계획--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-5);font-style:italic">이제 —</div><div style="font-size:72px;font-weight:700;color:#1A1A1A;line-height:1.35;letter-spacing:-2px">다른 학교 광고도<br><span class="is-accent">보겠습니다</span></div></div><!--SCRIPT_START-->"이제 — <strong>다른 학교 광고도 보겠습니다.</strong><br><br>(다음 슬라이드로 전환)"<!--SCRIPT_END-->"""


# =============================================================================
# P14 신규: 가로/정방형 4장 (2x2 그리드)
# =============================================================================
P14_MIXED = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:다른 대학 광고--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-caption is-muted" style="letter-spacing:3px;margin-bottom:var(--s-3)">다른 대학 광고 예시</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--s-2);max-width:1000px;width:92%;margin:0 auto"><img src="/assets/image/ads/wide01.png" alt="광고" style="width:100%;height:auto;display:block;border:1px solid #E8E8E8"><img src="/assets/image/ads/wide02.png" alt="광고" style="width:100%;height:auto;display:block;border:1px solid #E8E8E8"><img src="/assets/image/ads/square01.png" alt="광고" style="width:100%;height:auto;display:block;border:1px solid #E8E8E8"><img src="/assets/image/ads/square02.png" alt="광고" style="width:100%;height:auto;display:block;border:1px solid #E8E8E8"></div></div><!--SCRIPT_START-->"(다른 대학 광고들을 훑듯이)<br><br>다른 대학들도 마찬가지입니다. 각자의 '1위'를 외치고 있습니다."<!--SCRIPT_END-->"""


# =============================================================================
# P15 신규: 세로형 3장 (3열 그리드)
# =============================================================================
P15_PORTRAITS = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:다른 대학 광고--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-caption is-muted" style="letter-spacing:3px;margin-bottom:var(--s-3)">다른 대학 광고 예시</div><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--s-2);max-width:1000px;width:92%;margin:0 auto"><img src="/assets/image/ads/portrait01.png" alt="광고" style="width:100%;height:auto;display:block;border:1px solid #E8E8E8"><img src="/assets/image/ads/portrait02.png" alt="광고" style="width:100%;height:auto;display:block;border:1px solid #E8E8E8"><img src="/assets/image/ads/portrait03.png" alt="광고" style="width:100%;height:auto;display:block;border:1px solid #E8E8E8"></div></div><!--SCRIPT_START-->"(세로 포스터 3장 훑기)<br><br>모두, 같은 방식의 광고입니다. 정보 나열형 자랑."<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    try:
        # 레퍼런스 (level, status)
        sample = conn.execute(
            "SELECT level, status FROM sections WHERE proposal_id=? AND order_idx=11",
            (PID,),
        ).fetchone()
        lvl = sample["level"]
        st = sample["status"]

        # 1. idx 12~ +3 시프트 (음수 경유)
        conn.execute(
            "UPDATE sections SET order_idx = -(order_idx + 3) "
            "WHERE proposal_id=? AND order_idx >= 12",
            (PID,),
        )
        conn.execute(
            "UPDATE sections SET order_idx = -order_idx "
            "WHERE proposal_id=? AND order_idx < 0",
            (PID,),
        )
        print("idx 12+ 모두 +3 시프트")

        # 2. idx 12, 13, 14 INSERT
        inserts = [
            (12, "다른 학교 광고 전환", P13_TEXT),
            (13, "다른 대학 광고 — 4장", P14_MIXED),
            (14, "다른 대학 광고 — 세로 3장", P15_PORTRAITS),
        ]
        for idx, title, content in inserts:
            conn.execute(
                """INSERT INTO sections (proposal_id, level, title, order_idx, content, status)
                   VALUES (?,?,?,?,?,?)""",
                (PID, lvl, title, idx, content, st),
            )
            print(f"idx={idx}: {title}")

        conn.commit()

        # 확인
        rows = conn.execute(
            "SELECT order_idx, title FROM sections WHERE proposal_id=? ORDER BY order_idx LIMIT 20",
            (PID,),
        ).fetchall()
        print(f"\n=== V101 P12~ 재구성 후 ===")
        for r in rows[9:20]:
            print(f"  idx={r['order_idx']:2d} | {r['title']}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
