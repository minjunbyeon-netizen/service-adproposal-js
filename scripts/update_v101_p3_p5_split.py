# -*- coding: utf-8 -*-
"""V101 P3/P5 재구성.

P3  시장 상황만 (학령인구·경쟁·폐교) — 소음 리스트 제거
P5  소음 리스트 + "기억되지 않습니다" + "그래서 지금 뭘 하고 있지?" 통합
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

# =============================================================================
# P3 — 시장 상황만
# =============================================================================
P3_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-4) 0"><div class="t-heading" style="margin-bottom:var(--s-6)">대학 광고 시장, 현재 좌표</div><div style="display:flex;flex-direction:column;gap:0;max-width:880px;width:100%;margin:0 auto var(--s-5)"><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:42px;font-weight:700;color:#E84E10;line-height:1;min-width:140px;text-align:left;letter-spacing:-1px">-18%</div><div style="font-size:20px;color:#1A1A1A;text-align:left;flex:1">부울경 수험생 (2018→2025)</div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:42px;font-weight:700;color:#E84E10;line-height:1;min-width:140px;text-align:left;letter-spacing:-1px">2.3배</div><div style="font-size:20px;color:#1A1A1A;text-align:left;flex:1">지방 사립대 광고 경쟁 격화</div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:42px;font-weight:700;color:#E84E10;line-height:1;min-width:140px;text-align:left;letter-spacing:-1px">38%</div><div style="font-size:20px;color:#1A1A1A;text-align:left;flex:1">2030 폐교 위기 예측</div></div></div><div class="t-caption is-muted" style="font-style:italic">다들 아시는 이야기입니다. 짚고 넘어갑니다.</div></div><!--SCRIPT_START-->"대학 광고 시장의 현재 좌표입니다.<br><br>부울경 수험생 18% 감소, 광고 경쟁 2.3배 격화, 2030년 38% 폐교 위기.<br><br>다들 아시는 이야기입니다. 짚고 넘어가겠습니다."<!--SCRIPT_END-->"""

# =============================================================================
# P5 — 소음 + 기억되지 않음 + PIVOT 질문 통합
# =============================================================================
P5_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-4) 0"><div class="t-caption is-muted" style="margin-bottom:var(--s-3);font-style:italic">모든 대학이, 이렇게 외쳐왔습니다</div><div style="font-size:15px;line-height:2.0;color:#A0A0A5;margin-bottom:var(--s-4);max-width:1100px">"글로벌 경쟁력 1위" &nbsp;·&nbsp; "최고의 교수진" &nbsp;·&nbsp; "미래형 인재 양성" &nbsp;·&nbsp; "4차 산업혁명 선도" &nbsp;·&nbsp; "국내 최고 수준 취업률"</div><div style="width:60px;height:1px;background:#E0E0E0;margin:0 auto var(--s-4)"></div><div class="t-subtitle w-regular" style="margin-bottom:var(--s-2)">이런 광고는, <span class="is-accent">더 이상 기억되지 않습니다</span></div><div class="t-body is-muted" style="margin-bottom:var(--s-6);font-style:italic">이제 사람들은 — 다음에 집중합니다</div><div style="font-size:64px;font-weight:700;color:#1A1A1A;line-height:1.4;letter-spacing:-2px;max-width:1100px">"그래서 —<br><span class="is-accent">지금 뭘 하고 있지?"</span></div></div><!--SCRIPT_START-->"모든 대학이, 이렇게 외쳐왔습니다.<br>'글로벌 경쟁력 1위', '최고의 교수진', '미래형 인재 양성', '4차 산업혁명 선도', '국내 최고 수준 취업률'.<br><br>그러나 이런 광고는, <strong>더 이상 기억되지 않습니다.</strong><br>이제 사람들은 — 다음에 집중합니다.<br><br><strong>'그래서 — 지금 뭘 하고 있지?'</strong><br><br>(5초 침묵)"<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    try:
        conn.execute(
            "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=2",
            ("시장 현황", P3_CONTENT, PID),
        )
        print("P3 (idx=2) 재작성: 시장 상황만")

        conn.execute(
            "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=4",
            ("PIVOT 질문", P5_CONTENT, PID),
        )
        print("P5 (idx=4) 재작성: 소음 + 기억안됨 + PIVOT")

        conn.commit()
        print("완료")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
