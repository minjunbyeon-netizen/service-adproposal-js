# -*- coding: utf-8 -*-
"""P4 4단계 morph (9645525 recall) + P5.5 브릿지 질문 삽입."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 138

# ---------- P4: 4단계 morph ----------
# Stage 1: 9645525 (표지 recall, 회색)
# Stage 2: 964 · 55 · 25 (spread)
# Stage 3: 96.4% / 55위 / 25명 / 校訓 (완성, 순차 fade in)
# Stage 4: "영산대학교는, 숫자입니다" (하단 결론)
P4 = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0;position:relative">
<div class="fx-p4-s1"><div style="font-size:220px;font-weight:700;color:#D0D0D0;letter-spacing:-10px;font-family:Roboto,sans-serif;font-variant-numeric:tabular-nums;line-height:1">9645525</div></div>
<div class="fx-p4-s2"><div style="font-size:160px;font-weight:700;color:#D0D0D0;letter-spacing:-4px;font-family:Roboto,sans-serif;line-height:1;font-variant-numeric:tabular-nums">964<span style="margin:0 36px;color:#A0A0A5;font-size:96px;vertical-align:0.12em">·</span>55<span style="margin:0 36px;color:#A0A0A5;font-size:96px;vertical-align:0.12em">·</span>25</div></div>
<div style="padding-top:var(--s-2)"><div class="t-subtitle w-regular" style="line-height:2.3;display:inline-block;text-align:left"><span class="fx-p4-fact1"><span class="is-accent w-bold" style="font-size:34px">96.4%</span> 항공서비스학과 취업률</span><br><span class="fx-p4-fact2"><span class="is-accent w-bold" style="font-size:34px">55위</span> QS 호스피탈리티 글로벌</span><br><span class="fx-p4-fact3"><span class="is-accent w-bold" style="font-size:34px">25명</span> 호텔 총지배인 국내 최다 동문</span><br><span class="fx-p4-fact4"><span class="is-accent w-bold" style="font-size:28px">校訓</span> 지혜로운 가치를 배우는 대학</span></div></div>
<div class="fx-p4-conclusion" style="position:absolute;bottom:var(--s-5);left:0;right:0;text-align:center"><div class="t-heading">영산대학교는, <span class="is-accent">숫자</span>입니다</div></div>
</div><!--SCRIPT_START-->(6초 morph 애니 — 발표자 무발화)<br><br>"…표지에서 보신 이 숫자."<br><br>(Stage 2 분해)<br><br>"96.4%. 55위. 25명."<br>"그리고 校訓."<br><br>(결론 등장 시)<br>"영산대학교는 — <strong>숫자</strong>입니다."<!--SCRIPT_END-->"""

# ---------- P5.5 브릿지 질문 ----------
P55_TITLE = ""
P55 = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-caption is-muted" style="letter-spacing:3px;margin-bottom:var(--s-5)">그런데 —</div><div class="t-heading fx-p55-q" style="line-height:1.5;max-width:1100px;font-size:40px">왜 이 사실이, 수험생·학부모의 머릿속엔<br><span class="is-accent">아직 도착하지 못했을까요?</span></div></div><!--SCRIPT_START-->"그런데 —<br><br>왜 이 사실이, 수험생·학부모의 머릿속엔 <strong>아직 도착하지 못했을까요?</strong>"<br><br>(3초 침묵, 대답하지 않고 다음 장으로)<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    try:
        # 1. P4 교체 (order 3)
        conn.execute(
            "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=3",
            (P4, PID),
        )
        print("P4 (order=3) 4단계 morph 교체 완료")

        # 2. order 5+ 한 칸씩 shift (P5.5 자리 확보)
        conn.execute(
            "UPDATE sections SET order_idx = order_idx + 1 WHERE proposal_id=? AND order_idx >= 5",
            (PID,),
        )
        print("order 5+ shift +1")

        # 3. P5.5 삽입 (order 5)
        conn.execute(
            """INSERT INTO sections (proposal_id, level, title, order_idx, content, status)
               VALUES (?, 2, ?, 5, ?, 'pending')""",
            (PID, P55_TITLE, P55),
        )
        print("P5.5 브릿지 삽입 완료 (order=5)")

        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
