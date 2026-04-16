# -*- coding: utf-8 -*-
"""V101 P15 리프레이밍 프리뷰를 BEFORE → AFTER 도식으로 재작성."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

P15_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:프리뷰--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-1)">3가지 <span class="is-accent">리프레이밍</span></div><div class="t-body is-muted" style="margin-bottom:var(--s-4);font-style:italic">자랑을, 증명으로 뒤집다</div><div style="display:grid;grid-template-columns:48px 1fr 52px 1.25fr;gap:var(--s-3);max-width:1200px;width:94%;margin:0 auto var(--s-2);padding:0 var(--s-1);align-items:center"><div></div><div style="font-size:11px;color:#6E6E73;letter-spacing:3px;font-weight:700;text-align:left">BEFORE &nbsp;—&nbsp; 자랑</div><div></div><div style="font-size:11px;color:#E84E10;letter-spacing:3px;font-weight:700;text-align:left">AFTER &nbsp;—&nbsp; 각인</div></div><div style="display:grid;grid-template-columns:48px 1fr 52px 1.25fr;gap:var(--s-3);max-width:1200px;width:94%;margin:0 auto;align-items:center;padding:var(--s-3) var(--s-1);border-top:1px solid #E8E8E8"><div style="font-size:14px;color:#C5C5C9;font-weight:700;letter-spacing:2px;text-align:left">01</div><div style="font-size:13px;color:#A0A0A5;line-height:1.7;text-align:left">총지배인 25명 · 승무원 동남권 최다 · 셰프 오브 더 셰프 4명</div><div style="font-size:30px;color:#E84E10;font-weight:700;line-height:1;text-align:center">→</div><div style="font-size:22px;color:#1A1A1A;font-weight:700;line-height:1.45;text-align:left;letter-spacing:-0.3px">"대학이 아니라,<br><span class="is-accent">산업이 선택한 대학</span>"</div></div><div style="display:grid;grid-template-columns:48px 1fr 52px 1.25fr;gap:var(--s-3);max-width:1200px;width:94%;margin:0 auto;align-items:center;padding:var(--s-3) var(--s-1);border-top:1px solid #E8E8E8"><div style="font-size:14px;color:#C5C5C9;font-weight:700;letter-spacing:2px;text-align:left">02</div><div style="font-size:13px;color:#A0A0A5;line-height:1.7;text-align:left">QS 호스피탈리티 세계 55위 · 국내 3위 · 세종·경희와 Top 3</div><div style="font-size:30px;color:#E84E10;font-weight:700;line-height:1;text-align:center">→</div><div style="font-size:22px;color:#1A1A1A;font-weight:700;line-height:1.45;text-align:left;letter-spacing:-0.3px">"세계 55위라 죄송합니다?<br>국내는 3위지만,<br><span class="is-accent">글로벌 1위가 될 때까지</span>"</div></div><div style="display:grid;grid-template-columns:48px 1fr 52px 1.25fr;gap:var(--s-3);max-width:1200px;width:94%;margin:0 auto;align-items:center;padding:var(--s-3) var(--s-1);border-top:1px solid #E8E8E8;border-bottom:1px solid #E8E8E8"><div style="font-size:14px;color:#C5C5C9;font-weight:700;letter-spacing:2px;text-align:left">03</div><div style="font-size:13px;color:#A0A0A5;line-height:1.7;text-align:left">호텔 총지배인 25명 배출</div><div style="font-size:30px;color:#E84E10;font-weight:700;line-height:1;text-align:center">→</div><div style="font-size:22px;color:#1A1A1A;font-weight:700;line-height:1.45;text-align:left;letter-spacing:-0.3px">"25명이 끝이 아닙니다.<br><span class="is-accent">26번째가, 당신이 될 때까지</span>"</div></div></div><!--SCRIPT_START-->"저희가 뒤집을 <strong>3가지</strong>입니다.<br><br>첫째, 총지배인·승무원·셰프 — <strong>'대학이 아니라, 산업이 선택한 대학.'</strong><br><br>둘째, 세계 55위·국내 3위 — <strong>'세계 55위라 죄송합니다? 국내는 3위지만, 글로벌 1위가 될 때까지.'</strong><br><br>셋째, 총지배인 25명 — <strong>'25명이 끝이 아닙니다. 26번째가, 당신이 될 때까지.'</strong><br><br>지금부터, 각 시안으로 보여드리겠습니다."<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.execute(
        "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=14",
        ("리프레이밍 프리뷰 — BEFORE/AFTER", P15_CONTENT, PID),
    )
    conn.commit()
    print("P15 (idx=14) BEFORE→AFTER 도식 재작성 완료")
    conn.close()


if __name__ == "__main__":
    main()
