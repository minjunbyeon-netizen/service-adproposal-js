# -*- coding: utf-8 -*-
"""P10 이퀄라이저 웨이브폼 + P11 Before↻After 도식."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 138

# 20개 bar 높이 (랜덤하게 배치, 소음 느낌)
BAR_HEIGHTS = [35, 55, 22, 70, 45, 88, 30, 62, 40, 95,
               25, 58, 78, 38, 28, 68, 20, 52, 72, 42]
bars = "".join(
    f'<div style="width:6px;background:#E84E10;height:{h}%;border-radius:2px"></div>'
    for h in BAR_HEIGHTS
)

P10 = f"""<!--PARENT:III 세부 과업 수행 계획--><!--TAG:소음--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-4)">모든 대학이 같은 말을 하면,</div><div style="display:flex;align-items:flex-end;justify-content:center;gap:4px;height:96px;margin-bottom:var(--s-4);width:420px">{bars}</div><div class="t-display" style="color:#E84E10;margin-bottom:var(--s-5)">소음</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-4)"></div><div class="t-caption is-muted" style="font-style:italic">정보 나열은 광고가 아닙니다</div></div><!--SCRIPT_START-->"모든 대학이 같은 말을 하면, 결과는 <strong>소음</strong>입니다<br><br>정보 나열은 광고가 아닙니다<br>수험생과 학부모는 이미 이 소음에 지쳐 있습니다<br><br>그래서 저희는, <strong>뒤집었습니다</strong>"<!--SCRIPT_END-->"""

P11 = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:접근법--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-headline" style="margin-bottom:var(--s-5)">그래서 우리는,<br><span class="is-accent">뒤집었습니다</span></div><div style="display:flex;align-items:center;justify-content:center;gap:var(--s-4);margin-bottom:var(--s-5)"><div style="border:1px solid #E8E8E8;border-radius:8px;padding:24px 36px;text-align:center;min-width:280px;background:#F9F9F9"><div class="t-caption is-muted" style="margin-bottom:8px;letter-spacing:2px;font-weight:700">BEFORE</div><div style="font-size:26px;font-weight:700;color:#A0A0A5;line-height:1.2">취업률 96.4%</div><div class="t-caption is-muted" style="margin-top:8px;font-style:italic">소음으로 묻힘</div></div><div style="font-size:56px;color:#E84E10;font-weight:700;line-height:1">↻</div><div style="border:2px solid #E84E10;border-radius:8px;padding:24px 36px;text-align:center;min-width:280px;background:#FFF5F0"><div class="t-caption w-bold is-accent" style="margin-bottom:8px;letter-spacing:2px">AFTER</div><div style="font-size:30px;font-weight:700;color:#E84E10;line-height:1.2">탈락률 3.6%</div><div class="t-caption is-ink" style="margin-top:8px;font-style:italic">기억에 꽂힘</div></div></div><div style="width:80px;height:1px;background:#E8E8E8;margin:0 auto var(--s-4)"></div><div class="t-subtitle w-regular is-muted">같은 사실, <span class="is-ink w-bold">다른 언어로</span></div></div><!--SCRIPT_START-->"소음에 지친 청중에게, 저희는 똑같이 외칠 수 없었습니다<br><br>그래서 <strong>뒤집었습니다</strong><br>같은 사실을, <strong>다른 언어</strong>로 옮겨왔습니다<br><br>예를 들어, <strong>취업률 96.4%</strong>가 아니라 <strong>탈락률 3.6%</strong>입니다<br>지금부터, 그 방법의 이름과 세 가지 사례를 보여드리겠습니다"<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.execute("UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=9", (P10, PID))
    conn.execute("UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=10", (P11, PID))
    conn.commit()
    conn.close()
    print("P10 wave / P11 Before-After ok")


if __name__ == "__main__":
    main()
