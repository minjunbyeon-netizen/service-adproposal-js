# -*- coding: utf-8 -*-
"""V101 P14/P15/P16 자연 화법 재작성 (질문-답 / 대구법 / 수미상관 강화)."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

# =============================================================================
# P14 — 질문·답 구조 (도식 해체 + 대화체)
# =============================================================================
P14_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-4) 0"><div style="font-size:56px;font-weight:700;color:#1A1A1A;line-height:1.35;letter-spacing:-1.5px;margin-bottom:var(--s-4)">왜 <span class="is-accent">각인되지 않을까요?</span></div><div class="t-subtitle w-regular is-muted" style="line-height:1.7;margin-bottom:var(--s-2)">모두가, 같은 말을 하기 때문입니다</div><div style="font-size:18px;color:#A0A0A5;letter-spacing:1px;margin-bottom:var(--s-5);font-style:italic">'1등', '최고', '글로벌' —</div><div style="width:80px;height:1px;background:#E0E0E0;margin:0 auto var(--s-5)"></div><div style="font-size:36px;font-weight:400;color:#1A1A1A;line-height:1.5;margin-bottom:var(--s-3);letter-spacing:-0.5px">그래서 우리는, <span class="is-accent w-bold">한번 꼬겠습니다</span></div><div class="t-hero" style="color:#E84E10;margin-bottom:var(--s-4)">리프레이밍</div><div class="t-subtitle w-regular is-muted" style="line-height:1.8">같은 숫자를, 다른 프레임에<br>우리 학교만 쓸 수 있는 말로</div></div><!--SCRIPT_START-->"왜 각인되지 않을까요?<br><br>모두가, 같은 말을 하기 때문입니다. '1등', '최고', '글로벌' —<br><br>그래서 우리는, <strong>한번 꼬겠습니다</strong>.<br><br><strong>리프레이밍</strong>.<br><br>같은 숫자를, 다른 프레임에. 우리 학교만 쓸 수 있는 말로."<!--SCRIPT_END-->"""

# =============================================================================
# P15 — 자산 선언 (대구: "또 소음" → "그대로면 똑같아집니다")
# =============================================================================
P15_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:영산대의 숫자--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-1)">영산대에게 있는,</div><div class="t-heading" style="margin-bottom:var(--s-5)"><span class="is-accent">3가지 숫자</span></div><div style="display:flex;flex-direction:column;gap:0;max-width:1000px;width:94%;margin:0 auto var(--s-4)"><div style="display:grid;grid-template-columns:80px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-3) var(--s-2);border-top:1px solid #E8E8E8"><div style="font-size:36px;color:#E84E10;font-weight:700;letter-spacing:-1px;text-align:left">01</div><div style="font-size:24px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:left;letter-spacing:-0.5px">총지배인 25명 · 승무원 동남권 최다 · 셰프 오브 더 셰프 4명</div></div><div style="display:grid;grid-template-columns:80px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-3) var(--s-2);border-top:1px solid #E8E8E8"><div style="font-size:36px;color:#E84E10;font-weight:700;letter-spacing:-1px;text-align:left">02</div><div style="font-size:24px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:left;letter-spacing:-0.5px">QS 호스피탈리티 세계 55위 · 국내 3위 · 세종·경희 Top 3</div></div><div style="display:grid;grid-template-columns:80px 1fr;gap:var(--s-4);align-items:center;padding:var(--s-3) var(--s-2);border-top:1px solid #E8E8E8;border-bottom:1px solid #E8E8E8"><div style="font-size:36px;color:#E84E10;font-weight:700;letter-spacing:-1px;text-align:left">03</div><div style="font-size:24px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:left;letter-spacing:-0.5px">호텔 총지배인 25명 배출</div></div></div><div class="t-subtitle w-regular is-muted" style="line-height:1.6">그러나 —<br>그대로 외치면, <span class="is-ink w-bold">다른 대학과 똑같습니다</span></div></div><!--SCRIPT_START-->"영산대에게 있는, <strong>3가지 숫자</strong>입니다.<br><br>총지배인·승무원·셰프. 세계 랭킹. 호텔 총지배인 25명.<br><br>그러나 — 그대로 외치면, <strong>다른 대학과 똑같습니다</strong>."<!--SCRIPT_END-->"""

# =============================================================================
# P16 — 해법 선언 + BEFORE/AFTER + 대구법 슬로건
# =============================================================================
P16_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:3가지 리프레이밍--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-1);font-style:italic">그래서 —</div><div class="t-heading" style="margin-bottom:var(--s-3)">우리만 쓸 수 있는 <span class="is-accent">말로</span></div><div style="display:grid;grid-template-columns:60px 1fr 80px 1.2fr;gap:var(--s-3);max-width:1240px;width:96%;margin:0 auto var(--s-1);padding:0 var(--s-1);align-items:center;text-align:center"><div></div><div style="font-size:14px;color:#6E6E73;letter-spacing:3px;font-weight:700;text-align:center">BEFORE &nbsp;—&nbsp; 자랑</div><div></div><div style="font-size:14px;color:#E84E10;letter-spacing:3px;font-weight:700;text-align:center">AFTER &nbsp;—&nbsp; 각인</div></div><div style="display:grid;grid-template-columns:60px 1fr 80px 1.2fr;gap:var(--s-3);max-width:1240px;width:96%;margin:0 auto;align-items:center;padding:var(--s-2) var(--s-1);border-top:1px solid #E8E8E8;text-align:center"><div style="font-size:20px;color:#C5C5C9;font-weight:700;letter-spacing:2px;text-align:center">01</div><div style="font-size:15px;color:#A0A0A5;line-height:1.6;text-align:center">총지배인 25명<br>승무원 동남권 최다<br>셰프 오브 더 셰프 4명</div><div style="font-size:40px;color:#E84E10;font-weight:700;line-height:1;text-align:center">→</div><div style="font-size:24px;color:#1A1A1A;font-weight:700;line-height:1.4;text-align:center;letter-spacing:-0.5px">"대학이 아니라,<br><span class="is-accent">산업이 선택한 대학</span>"</div></div><div style="display:grid;grid-template-columns:60px 1fr 80px 1.2fr;gap:var(--s-3);max-width:1240px;width:96%;margin:0 auto;align-items:center;padding:var(--s-2) var(--s-1);border-top:1px solid #E8E8E8;text-align:center"><div style="font-size:20px;color:#C5C5C9;font-weight:700;letter-spacing:2px;text-align:center">02</div><div style="font-size:15px;color:#A0A0A5;line-height:1.6;text-align:center">QS 호스피탈리티<br>세계 55위 · 국내 3위<br>세종·경희 Top 3</div><div style="font-size:40px;color:#E84E10;font-weight:700;line-height:1;text-align:center">→</div><div style="font-size:24px;color:#1A1A1A;font-weight:700;line-height:1.4;text-align:center;letter-spacing:-0.5px">"세계 55위라 죄송합니다?<br>국내는 3위지만,<br><span class="is-accent">글로벌 1위가 될 때까지</span>"</div></div><div style="display:grid;grid-template-columns:60px 1fr 80px 1.2fr;gap:var(--s-3);max-width:1240px;width:96%;margin:0 auto;align-items:center;padding:var(--s-2) var(--s-1);border-top:1px solid #E8E8E8;border-bottom:1px solid #E8E8E8;text-align:center"><div style="font-size:20px;color:#C5C5C9;font-weight:700;letter-spacing:2px;text-align:center">03</div><div style="font-size:15px;color:#A0A0A5;line-height:1.6;text-align:center">호텔 총지배인<br>25명 배출</div><div style="font-size:40px;color:#E84E10;font-weight:700;line-height:1;text-align:center">→</div><div style="font-size:24px;color:#1A1A1A;font-weight:700;line-height:1.4;text-align:center;letter-spacing:-0.5px">"25명이 끝이 아닙니다.<br><span class="is-accent">26번째가, 당신이 될 때까지</span>"</div></div><div style="margin-top:var(--s-4);padding-top:var(--s-3);border-top:2px solid #E84E10;max-width:1000px;width:94%;margin-left:auto;margin-right:auto"><div style="font-size:22px;font-weight:400;color:#6E6E73;line-height:1.6">1등도 아닙니다. 최고도 아닙니다.</div><div style="font-size:26px;font-weight:700;color:#1A1A1A;line-height:1.5;margin-top:var(--s-1);letter-spacing:-0.5px"><span class="is-accent">숫자</span> 그 자체가, <span class="is-accent">슬로건</span>이 됩니다</div></div></div><!--SCRIPT_START-->"그래서 — <strong>우리만 쓸 수 있는 말로</strong>.<br><br>첫째, 대학이 아니라 <strong>산업이 선택한 대학</strong>.<br>둘째, 세계 55위라 죄송합니다? 국내는 3위지만, <strong>글로벌 1위가 될 때까지</strong>.<br>셋째, 25명이 끝이 아닙니다. <strong>26번째가, 당신이 될 때까지</strong>.<br><br><strong>1등도 아닙니다. 최고도 아닙니다.</strong><br><strong>숫자</strong> 그 자체가, <strong>슬로건</strong>이 됩니다."<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    updates = [
        (13, "왜 각인되지 않는가 → 리프레이밍", P14_CONTENT),
        (14, "영산대의 3가지 숫자", P15_CONTENT),
        (15, "우리만 쓸 수 있는 말로 — BEFORE/AFTER", P16_CONTENT),
    ]
    for idx, title, content in updates:
        conn.execute(
            "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=?",
            (title, content, PID, idx),
        )
        print(f"idx={idx}: {title}")
    conn.commit()
    print("\nP14~P16 자연 화법 재작성 완료")
    conn.close()


if __name__ == "__main__":
    main()
