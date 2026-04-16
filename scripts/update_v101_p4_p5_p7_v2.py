# -*- coding: utf-8 -*-
"""V101 P4 / P5 / P7 문구 강화.

P4  "많은 대학이, 대단한 사실을 정보 나열형으로 외치고만 있습니다" + 광고 4개
P5  "'똑같이'만 말하는 대학은 더 이상 기억되지 않습니다" + PIVOT 질문
P7  "'똑같이' 외치지 않는 것 / 기억을 넘어, 각인시키는 것 / 이번 제안의 전부"
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

# =============================================================================
# P4 (idx=3) — 소음의 증거
# =============================================================================
P4_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-headline" style="margin-bottom:var(--s-5);line-height:1.35;max-width:1100px">많은 대학이, 자신들의 대단한 사실을<br><span class="is-accent">정보 나열형</span>으로 외치고만 있습니다</div><div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:var(--s-2);max-width:1100px;width:100%;margin:0 auto var(--s-3)"><div style="aspect-ratio:16/10;background:#F5F5F5;border:1px solid #E0E0E0;display:flex;align-items:center;justify-content:center;color:#A0A0A5;font-size:11px;letter-spacing:2px;font-weight:700">AD SAMPLE 01</div><div style="aspect-ratio:16/10;background:#F5F5F5;border:1px solid #E0E0E0;display:flex;align-items:center;justify-content:center;color:#A0A0A5;font-size:11px;letter-spacing:2px;font-weight:700">AD SAMPLE 02</div><div style="aspect-ratio:16/10;background:#F5F5F5;border:1px solid #E0E0E0;display:flex;align-items:center;justify-content:center;color:#A0A0A5;font-size:11px;letter-spacing:2px;font-weight:700">AD SAMPLE 03</div><div style="aspect-ratio:16/10;background:#F5F5F5;border:1px solid #E0E0E0;display:flex;align-items:center;justify-content:center;color:#A0A0A5;font-size:11px;letter-spacing:2px;font-weight:700">AD SAMPLE 04</div></div><div class="t-caption is-muted" style="font-style:italic">이런 비슷한 광고, 너무 많습니다</div></div><!--SCRIPT_START-->"많은 대학이, 자신들의 대단한 사실을 <strong>정보 나열형</strong>으로 외치고만 있습니다.<br><br>(광고 시안 4개를 가리키며)<br>이런 비슷한 광고가, 지금도 매일 쏟아지고 있습니다."<!--SCRIPT_END-->"""

# =============================================================================
# P5 (idx=4) — "똑같이" 기억 안됨 + PIVOT
# =============================================================================
P5_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-headline" style="margin-bottom:var(--s-3);line-height:1.35;max-width:1100px">'<span class="is-accent">똑같이</span>'만 말하는 대학은,<br>더 이상 기억되지 않습니다</div><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-6);font-style:italic">이제 사람들은 — 다음에 집중합니다</div><div style="width:60px;height:1px;background:#E0E0E0;margin:0 auto var(--s-6)"></div><div style="font-size:68px;font-weight:700;color:#1A1A1A;line-height:1.4;letter-spacing:-2px;max-width:1100px">"그래서 —<br><span class="is-accent">지금 뭘 하고 있지?"</span></div></div><!--SCRIPT_START-->"'<strong>똑같이</strong>'만 말하는 대학은, 더 이상 기억되지 않습니다.<br>이제 사람들은 — 다음에 집중합니다.<br><br><strong>'그래서 — 지금 뭘 하고 있지?'</strong><br><br>(5초 침묵)"<!--SCRIPT_END-->"""

# =============================================================================
# P7 (idx=6) — 각인 선언 (강화)
# =============================================================================
P7_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-3)">영산대의 이 움직임을 —</div><div class="t-title" style="line-height:1.4;margin-bottom:var(--s-5);max-width:1100px">'<span class="is-accent">똑같이</span>' 외치지 않는 것</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div class="t-title" style="line-height:1.4;margin-bottom:var(--s-5);max-width:1100px">기억을 넘어,<br><span class="is-accent">각인시키는 것</span></div><div class="t-subtitle w-regular is-muted">그것이, 이번 제안의 <span class="is-accent w-bold">전부</span>입니다</div></div><!--SCRIPT_START-->"영산대의 이 움직임을 — <strong>'똑같이' 외치지 않는 것.</strong><br><br>기억을 넘어, <strong>각인시키는 것.</strong><br><br>그것이, 이번 제안의 <strong>전부</strong>입니다."<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    try:
        conn.execute(
            "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=3",
            ("소음의 증거", P4_CONTENT, PID),
        )
        print("P4 (idx=3) 문구 강화: 정보 나열형")

        conn.execute(
            "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=4",
            ("PIVOT 질문", P5_CONTENT, PID),
        )
        print("P5 (idx=4) 문구 교체: '똑같이' 기억 안됨 + PIVOT")

        conn.execute(
            "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=6",
            ("각인 선언", P7_CONTENT, PID),
        )
        print("P7 (idx=6) 문구 강화: 똑같이 외치지 않는 / 기억 넘어 각인")

        conn.commit()
        print("완료")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
