# -*- coding: utf-8 -*-
"""V101 P15를 2장으로 분할.

P15-1 (idx=14)  BEFORE 크게 — 영산대의 3가지 숫자 (자랑만 나열)
P15-2 (idx=15)  기존 BEFORE → AFTER 도식 + 하단 통합 슬로건
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

# =============================================================================
# P15-1 — BEFORE 크게 (자랑 3행)
# =============================================================================
P15_1_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:영산대의 숫자--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-5)">영산대의 <span class="is-accent">3가지 숫자</span></div><div style="display:flex;flex-direction:column;gap:0;max-width:1000px;width:94%;margin:0 auto"><div style="display:grid;grid-template-columns:80px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-4) var(--s-2);border-top:1px solid #E8E8E8"><div style="font-size:36px;color:#E84E10;font-weight:700;letter-spacing:-1px;text-align:left">01</div><div style="font-size:26px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:left;letter-spacing:-0.5px">총지배인 25명 · 승무원 동남권 최다 · 셰프 오브 더 셰프 4명</div></div><div style="display:grid;grid-template-columns:80px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-4) var(--s-2);border-top:1px solid #E8E8E8"><div style="font-size:36px;color:#E84E10;font-weight:700;letter-spacing:-1px;text-align:left">02</div><div style="font-size:26px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:left;letter-spacing:-0.5px">QS 호스피탈리티 세계 55위 · 국내 3위 · 세종·경희 Top 3</div></div><div style="display:grid;grid-template-columns:80px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-4) var(--s-2);border-top:1px solid #E8E8E8;border-bottom:1px solid #E8E8E8"><div style="font-size:36px;color:#E84E10;font-weight:700;letter-spacing:-1px;text-align:left">03</div><div style="font-size:26px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:left;letter-spacing:-0.5px">호텔 총지배인 25명 배출</div></div></div><div class="t-caption is-muted" style="margin-top:var(--s-4);font-style:italic">이대로 외치면, 또 소음이 됩니다</div></div><!--SCRIPT_START-->"영산대에는 <strong>3가지 숫자</strong>가 있습니다.<br><br>총지배인·승무원·셰프, 세계 랭킹, 호텔 총지배인 25명 배출.<br><br>그러나 이대로 외치면, <strong>또 소음</strong>이 됩니다.<br><br>그래서 — 뒤집습니다."<!--SCRIPT_END-->"""

# =============================================================================
# P15-2 — 기존 도식 + 통합 슬로건
# =============================================================================
P15_2_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:프리뷰--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-3)">3가지 <span class="is-accent">리프레이밍</span></div><div style="display:grid;grid-template-columns:60px 1fr 80px 1.2fr;gap:var(--s-3);max-width:1240px;width:96%;margin:0 auto var(--s-1);padding:0 var(--s-1);align-items:center;text-align:center"><div></div><div style="font-size:15px;color:#6E6E73;letter-spacing:3px;font-weight:700;text-align:center">BEFORE &nbsp;—&nbsp; 자랑</div><div></div><div style="font-size:15px;color:#E84E10;letter-spacing:3px;font-weight:700;text-align:center">AFTER &nbsp;—&nbsp; 각인</div></div><div style="display:grid;grid-template-columns:60px 1fr 80px 1.2fr;gap:var(--s-3);max-width:1240px;width:96%;margin:0 auto;align-items:center;padding:var(--s-2) var(--s-1);border-top:1px solid #E8E8E8;text-align:center"><div style="font-size:22px;color:#C5C5C9;font-weight:700;letter-spacing:2px;text-align:center">01</div><div style="font-size:16px;color:#A0A0A5;line-height:1.6;text-align:center">총지배인 25명<br>승무원 동남권 최다<br>셰프 오브 더 셰프 4명</div><div style="font-size:44px;color:#E84E10;font-weight:700;line-height:1;text-align:center">→</div><div style="font-size:26px;color:#1A1A1A;font-weight:700;line-height:1.35;text-align:center;letter-spacing:-0.5px">"대학이 아니라,<br><span class="is-accent">산업이 선택한 대학</span>"</div></div><div style="display:grid;grid-template-columns:60px 1fr 80px 1.2fr;gap:var(--s-3);max-width:1240px;width:96%;margin:0 auto;align-items:center;padding:var(--s-2) var(--s-1);border-top:1px solid #E8E8E8;text-align:center"><div style="font-size:22px;color:#C5C5C9;font-weight:700;letter-spacing:2px;text-align:center">02</div><div style="font-size:16px;color:#A0A0A5;line-height:1.6;text-align:center">QS 호스피탈리티<br>세계 55위 · 국내 3위<br>세종·경희 Top 3</div><div style="font-size:44px;color:#E84E10;font-weight:700;line-height:1;text-align:center">→</div><div style="font-size:26px;color:#1A1A1A;font-weight:700;line-height:1.35;text-align:center;letter-spacing:-0.5px">"세계 55위라 죄송합니다?<br>국내는 3위지만,<br><span class="is-accent">글로벌 1위가 될 때까지</span>"</div></div><div style="display:grid;grid-template-columns:60px 1fr 80px 1.2fr;gap:var(--s-3);max-width:1240px;width:96%;margin:0 auto;align-items:center;padding:var(--s-2) var(--s-1);border-top:1px solid #E8E8E8;border-bottom:1px solid #E8E8E8;text-align:center"><div style="font-size:22px;color:#C5C5C9;font-weight:700;letter-spacing:2px;text-align:center">03</div><div style="font-size:16px;color:#A0A0A5;line-height:1.6;text-align:center">호텔 총지배인<br>25명 배출</div><div style="font-size:44px;color:#E84E10;font-weight:700;line-height:1;text-align:center">→</div><div style="font-size:26px;color:#1A1A1A;font-weight:700;line-height:1.35;text-align:center;letter-spacing:-0.5px">"25명이 끝이 아닙니다.<br><span class="is-accent">26번째가, 당신이 될 때까지</span>"</div></div><div style="margin-top:var(--s-4);padding-top:var(--s-3);border-top:2px solid #E84E10;max-width:1000px;width:94%;margin-left:auto;margin-right:auto"><div style="font-size:22px;font-weight:700;color:#1A1A1A;line-height:1.5;letter-spacing:-0.5px">3가지는, 하나의 메시지입니다</div><div style="font-size:16px;color:#6E6E73;margin-top:var(--s-1);letter-spacing:-0.3px">'<span class="is-accent w-bold">증명</span>'을, '<span class="is-accent w-bold">리프레이밍</span>'으로 말합니다</div></div></div><!--SCRIPT_START-->"저희가 뒤집을 <strong>3가지 리프레이밍</strong>입니다.<br><br>첫째, <strong>'대학이 아니라, 산업이 선택한 대학.'</strong><br>둘째, <strong>'세계 55위라 죄송합니다? 국내는 3위지만, 글로벌 1위가 될 때까지.'</strong><br>셋째, <strong>'25명이 끝이 아닙니다. 26번째가, 당신이 될 때까지.'</strong><br><br>3가지는, <strong>하나의 메시지</strong>입니다 — <strong>'증명'</strong>을, <strong>'리프레이밍'</strong>으로 말합니다."<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    try:
        # 1. idx=15~ 모두 +1 시프트
        conn.execute(
            "UPDATE sections SET order_idx = -(order_idx + 1) "
            "WHERE proposal_id=? AND order_idx >= 15",
            (PID,),
        )
        conn.execute(
            "UPDATE sections SET order_idx = -order_idx "
            "WHERE proposal_id=? AND order_idx < 0",
            (PID,),
        )
        print("idx 15+ 모두 +1 시프트")

        # 2. 레퍼런스 (level, status)
        sample = conn.execute(
            "SELECT level, status FROM sections WHERE proposal_id=? AND order_idx=14",
            (PID,),
        ).fetchone()

        # 3. idx=14를 P15-1 (BEFORE 크게)로 교체
        conn.execute(
            "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=14",
            ("영산대의 3가지 숫자 (BEFORE)", P15_1_CONTENT, PID),
        )
        print("idx=14 → P15-1 (BEFORE 크게)")

        # 4. idx=15에 P15-2 INSERT
        conn.execute(
            """INSERT INTO sections (proposal_id, level, title, order_idx, content, status)
               VALUES (?,?,?,?,?,?)""",
            (PID, sample["level"], "3가지 리프레이밍 + 통합 슬로건", 15, P15_2_CONTENT, sample["status"]),
        )
        print("idx=15 신규: P15-2 (BEFORE/AFTER + 슬로건)")

        conn.commit()

        rows = conn.execute(
            "SELECT order_idx, title FROM sections WHERE proposal_id=? AND order_idx BETWEEN 12 AND 20 ORDER BY order_idx",
            (PID,),
        ).fetchall()
        print(f"\n=== V101 P13~P21 주변 ===")
        for r in rows:
            print(f"  P{r['order_idx']+1:2d} (idx={r['order_idx']:2d}) | {r['title']}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
