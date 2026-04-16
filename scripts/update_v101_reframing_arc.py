# -*- coding: utf-8 -*-
"""V101 리프레이밍 아크 삽입 (P10/P11 신규 + P12 재작성).

P9   컨셉 '증명' (유지)
P10  자랑 시연 (신규) — "보통의 광고였다면"
P11  기법 '리프레이밍' (신규) — "그러나 우리는"
P12  리프레이밍 프리뷰 (재작성) — 3가지 뒤집힌 카피

기존 idx 9 (프리뷰)는 idx 11로 이동 + 내용 재작성.
기존 idx 10~ 시안은 +2 시프트.
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

# =============================================================================
# P10 자랑 시연 — "보통 광고라면"
# =============================================================================
P10_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:자랑의 언어--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-4) 0"><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-5);font-style:italic">만약, 보통의 광고였다면 —</div><div style="display:flex;flex-direction:column;gap:var(--s-3);max-width:1000px;width:100%;margin:0 auto var(--s-5)"><div style="font-size:36px;font-weight:700;color:#E84E10;line-height:1.3;letter-spacing:-1px">연구력 세계 <span style="font-size:120%">8위!</span></div><div style="font-size:36px;font-weight:700;color:#E84E10;line-height:1.3;letter-spacing:-1px">QS 호스피탈리티 세계 <span style="font-size:120%">55위!</span></div><div style="font-size:36px;font-weight:700;color:#E84E10;line-height:1.3;letter-spacing:-1px">호텔 총지배인 <span style="font-size:120%">25명</span> 배출!</div><div style="font-size:36px;font-weight:700;color:#E84E10;line-height:1.3;letter-spacing:-1px">한국 호텔관광 <span style="font-size:120%">TOP 3!</span></div></div><div style="width:60px;height:1px;background:#E0E0E0;margin:0 auto var(--s-3)"></div><div class="t-caption is-muted" style="font-style:italic">... 자랑은, 소음이 됩니다</div></div><!--SCRIPT_START-->"만약, 저희가 보통의 광고였다면 이렇게 말할 겁니다.<br><br><strong>연구력 세계 8위!</strong><br><strong>QS 호스피탈리티 세계 55위!</strong><br><strong>호텔 총지배인 25명 배출!</strong><br><strong>한국 호텔관광 TOP 3!</strong><br><br>(짧은 멈춤)<br><br>...자랑은, 소음이 됩니다.<br>이미 2분 전에 보신 그대로입니다."<!--SCRIPT_END-->"""

# =============================================================================
# P11 기법 '리프레이밍' — "그러나 우리는"
# =============================================================================
P11_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:기법--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-4) 0"><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-3)">그러나, 우리는 —</div><div class="t-hero" style="margin-bottom:var(--s-5);color:#E84E10">리프레이밍</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div style="display:flex;flex-direction:column;gap:var(--s-2);max-width:680px;width:100%;margin:0 auto var(--s-4)"><div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #F0F0F0"><div class="t-caption w-bold is-muted" style="letter-spacing:3px;min-width:80px;text-align:left">컨셉</div><div style="font-size:24px;font-weight:700;color:#1A1A1A;text-align:left;flex:1">증명 <span class="t-caption is-muted" style="margin-left:var(--s-2);font-weight:400">기억에 박힘</span></div></div><div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0"><div class="t-caption w-bold is-muted" style="letter-spacing:3px;min-width:80px;text-align:left">기법</div><div style="font-size:24px;font-weight:700;color:#E84E10;text-align:left;flex:1">리프레이밍 <span class="t-caption is-muted" style="margin-left:var(--s-2);font-weight:400;color:#6E6E73">같은 숫자, 다른 프레임으로</span></div></div></div></div><!--SCRIPT_START-->"그러나, 저희는 자랑하지 않습니다.<br><br>저희의 기법은 <strong>리프레이밍</strong>입니다.<br><br>컨셉은 <strong>증명</strong> — 기억에 박히게 하는 것.<br>기법은 <strong>리프레이밍</strong> — 같은 숫자를, 다른 프레임에.<br><br>자, 그럼 실제로 어떻게 뒤집는지 —"<!--SCRIPT_END-->"""

# =============================================================================
# P12 리프레이밍 프리뷰 — 3가지 뒤집힌 카피
# =============================================================================
P12_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:프리뷰--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-2)">3가지 <span class="is-accent">리프레이밍</span></div><div class="t-body is-muted" style="margin-bottom:var(--s-4);font-style:italic">자랑을, 증명으로 뒤집다</div><div style="display:flex;flex-direction:column;gap:var(--s-3);max-width:1080px;width:100%;margin:0 auto;text-align:left"><div class="fx-stagger-1" style="display:flex;align-items:flex-start;gap:var(--s-3);padding:var(--s-3) var(--s-4);border-left:3px solid #E84E10;background:#FAFAFA"><div style="font-size:13px;color:#C5C5C9;font-weight:700;letter-spacing:2px;min-width:36px;padding-top:6px">01</div><div style="flex:1"><div style="font-size:22px;font-weight:700;color:#1A1A1A;line-height:1.4;letter-spacing:-0.5px">"지역대학이 아니라,<br>산업이 선택하는 대학"</div><div class="t-caption is-muted" style="margin-top:6px">총지배인 25명 · 승무원 동남권 최다 · 셰프 오브 더 셰프 4명</div></div></div><div class="fx-stagger-2" style="display:flex;align-items:flex-start;gap:var(--s-3);padding:var(--s-3) var(--s-4);border-left:3px solid #E84E10;background:#FAFAFA"><div style="font-size:13px;color:#C5C5C9;font-weight:700;letter-spacing:2px;min-width:36px;padding-top:6px">02</div><div style="flex:1"><div style="font-size:22px;font-weight:700;color:#1A1A1A;line-height:1.4;letter-spacing:-0.5px">"지금 국내 3위입니다.<br>그러나 글로벌 55위입니다.<br><span class="is-accent">글로벌 1위가 될 때까지.</span>"</div><div class="t-caption is-muted" style="margin-top:6px">연구력 세계 8위 · QS 호스피탈리티 55위 · 세종·경희 Top 3</div></div></div><div class="fx-stagger-3" style="display:flex;align-items:flex-start;gap:var(--s-3);padding:var(--s-3) var(--s-4);border-left:3px solid #E84E10;background:#FAFAFA"><div style="font-size:13px;color:#C5C5C9;font-weight:700;letter-spacing:2px;min-width:36px;padding-top:6px">03</div><div style="flex:1"><div style="font-size:22px;font-weight:700;color:#1A1A1A;line-height:1.4;letter-spacing:-0.5px">"25개 호텔의 꼭대기,<br>그리고 <span class="is-accent">26번째는 당신.</span>"</div><div class="t-caption is-muted" style="margin-top:6px">호텔 총지배인 25명 배출</div></div></div></div></div><!--SCRIPT_START-->"저희가 보여드릴 <strong>3가지 리프레이밍</strong>입니다.<br><br>첫째, 지역대학이 아니라 <strong>산업이 선택하는 대학</strong>.<br>둘째, 지금 국내 3위입니다. 그러나 글로벌 55위입니다. <strong>글로벌 1위가 될 때까지</strong>.<br>셋째, 25개 호텔의 꼭대기, 그리고 <strong>26번째는 당신</strong>.<br><br>지금부터, 각 시안으로 보여드리겠습니다."<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    try:
        # 1. 기존 idx 10~44 시안을 +2 시프트 (역순으로: 44→46, ..., 10→12)
        # SQLite는 single UPDATE 순서 제약 있지만, ORDER BY 가능
        # 간단하게: max를 먼저 처리하려면 일단 모든 idx를 음수로 보냈다가 다시 +
        conn.execute(
            "UPDATE sections SET order_idx = -(order_idx + 2) "
            "WHERE proposal_id=? AND order_idx >= 10",
            (PID,),
        )
        conn.execute(
            "UPDATE sections SET order_idx = -order_idx "
            "WHERE proposal_id=? AND order_idx < 0",
            (PID,),
        )
        print("기존 시안 (idx 10~) → +2 시프트")

        # 2. 기존 idx 9 프리뷰 → idx 11로 이동 + 내용 재작성
        conn.execute(
            "UPDATE sections SET order_idx=11, title=?, content=? "
            "WHERE proposal_id=? AND order_idx=9",
            ("리프레이밍 프리뷰", P12_CONTENT, PID),
        )
        print("idx 9 프리뷰 → idx 11 (리프레이밍 프리뷰로 재작성)")

        # 3. 레퍼런스 section (level, status 추출용)
        sample = conn.execute(
            "SELECT level, status FROM sections WHERE proposal_id=? AND order_idx=11",
            (PID,),
        ).fetchone()
        lvl = sample["level"]
        st = sample["status"]

        # 4. 신규 idx 9 (P10 자랑 시연)
        conn.execute(
            """INSERT INTO sections (proposal_id, level, title, order_idx, content, status)
               VALUES (?,?,?,?,?,?)""",
            (PID, lvl, "자랑의 언어", 9, P10_CONTENT, st),
        )
        # 5. 신규 idx 10 (P11 리프레이밍 기법)
        conn.execute(
            """INSERT INTO sections (proposal_id, level, title, order_idx, content, status)
               VALUES (?,?,?,?,?,?)""",
            (PID, lvl, "기법 — 리프레이밍", 10, P11_CONTENT, st),
        )
        print("신규 idx 9 (자랑 시연), idx 10 (리프레이밍 기법) 삽입")

        conn.commit()

        # 6. 결과
        rows = conn.execute(
            "SELECT order_idx, title FROM sections WHERE proposal_id=? ORDER BY order_idx LIMIT 14",
            (PID,),
        ).fetchall()
        print(f"\n=== V101 리프레이밍 아크 ===")
        for r in rows:
            print(f"  idx={r['order_idx']:2d} | {r['title']}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
