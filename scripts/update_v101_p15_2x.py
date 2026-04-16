# -*- coding: utf-8 -*-
"""V101 P15 폰트 2배 + 중앙 정렬 + 부제목 수정.

- 부제목: "자랑을, 증명으로 뒤집다" → "자랑을, 증명으로 각인시키다"
- 모든 텍스트 중앙 정렬
- 폰트 크기 2배
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

P15_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:프리뷰--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-1)">3가지 <span class="is-accent">리프레이밍</span></div><div class="t-body is-muted" style="margin-bottom:var(--s-3);font-style:italic">자랑을, 증명으로 <span class="is-accent w-bold">각인시키다</span></div><div style="display:grid;grid-template-columns:60px 1fr 80px 1.2fr;gap:var(--s-3);max-width:1240px;width:96%;margin:0 auto var(--s-1);padding:0 var(--s-1);align-items:center;text-align:center"><div></div><div style="font-size:15px;color:#6E6E73;letter-spacing:3px;font-weight:700;text-align:center">BEFORE &nbsp;—&nbsp; 자랑</div><div></div><div style="font-size:15px;color:#E84E10;letter-spacing:3px;font-weight:700;text-align:center">AFTER &nbsp;—&nbsp; 각인</div></div><div style="display:grid;grid-template-columns:60px 1fr 80px 1.2fr;gap:var(--s-3);max-width:1240px;width:96%;margin:0 auto;align-items:center;padding:var(--s-3) var(--s-1);border-top:1px solid #E8E8E8;text-align:center"><div style="font-size:22px;color:#C5C5C9;font-weight:700;letter-spacing:2px;text-align:center">01</div><div style="font-size:18px;color:#A0A0A5;line-height:1.6;text-align:center">총지배인 25명<br>승무원 동남권 최다<br>셰프 오브 더 셰프 4명</div><div style="font-size:48px;color:#E84E10;font-weight:700;line-height:1;text-align:center">→</div><div style="font-size:30px;color:#1A1A1A;font-weight:700;line-height:1.35;text-align:center;letter-spacing:-0.5px">"대학이 아니라,<br><span class="is-accent">산업이 선택한 대학</span>"</div></div><div style="display:grid;grid-template-columns:60px 1fr 80px 1.2fr;gap:var(--s-3);max-width:1240px;width:96%;margin:0 auto;align-items:center;padding:var(--s-3) var(--s-1);border-top:1px solid #E8E8E8;text-align:center"><div style="font-size:22px;color:#C5C5C9;font-weight:700;letter-spacing:2px;text-align:center">02</div><div style="font-size:18px;color:#A0A0A5;line-height:1.6;text-align:center">QS 호스피탈리티<br>세계 55위 · 국내 3위<br>세종·경희 Top 3</div><div style="font-size:48px;color:#E84E10;font-weight:700;line-height:1;text-align:center">→</div><div style="font-size:30px;color:#1A1A1A;font-weight:700;line-height:1.35;text-align:center;letter-spacing:-0.5px">"세계 55위라 죄송합니다?<br>국내는 3위지만,<br><span class="is-accent">글로벌 1위가 될 때까지</span>"</div></div><div style="display:grid;grid-template-columns:60px 1fr 80px 1.2fr;gap:var(--s-3);max-width:1240px;width:96%;margin:0 auto;align-items:center;padding:var(--s-3) var(--s-1);border-top:1px solid #E8E8E8;border-bottom:1px solid #E8E8E8;text-align:center"><div style="font-size:22px;color:#C5C5C9;font-weight:700;letter-spacing:2px;text-align:center">03</div><div style="font-size:18px;color:#A0A0A5;line-height:1.6;text-align:center">호텔 총지배인<br>25명 배출</div><div style="font-size:48px;color:#E84E10;font-weight:700;line-height:1;text-align:center">→</div><div style="font-size:30px;color:#1A1A1A;font-weight:700;line-height:1.35;text-align:center;letter-spacing:-0.5px">"25명이 끝이 아닙니다.<br><span class="is-accent">26번째가, 당신이 될 때까지</span>"</div></div></div><!--SCRIPT_START-->"저희가 뒤집을 <strong>3가지</strong>입니다. 자랑을, 증명으로 <strong>각인시키다</strong>.<br><br>첫째, 총지배인·승무원·셰프 — <strong>'대학이 아니라, 산업이 선택한 대학.'</strong><br><br>둘째, 세계 55위·국내 3위 — <strong>'세계 55위라 죄송합니다? 국내는 3위지만, 글로벌 1위가 될 때까지.'</strong><br><br>셋째, 총지배인 25명 — <strong>'25명이 끝이 아닙니다. 26번째가, 당신이 될 때까지.'</strong>"<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=14",
        (P15_CONTENT, PID),
    )
    conn.commit()
    print("P15 폰트 2배 + 중앙 정렬 + 부제목 '각인시키다' 변경 완료")
    conn.close()


if __name__ == "__main__":
    main()
