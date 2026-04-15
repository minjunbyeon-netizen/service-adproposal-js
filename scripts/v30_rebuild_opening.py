# -*- coding: utf-8 -*-
"""V30 오프닝 7장 재구성 + 슬로건 교체.
P1 표지 0825503 유지, P2 신규 시장 진단, P3 특성화 경쟁 지도, P4 완화 질문,
P5 morph 0825503 재작성, P6 단일 화두, P7 차별화 답, P31 슬로건 변경.
"""
import sqlite3
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 138


P2_MARKET = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-4)">MARKET CONTEXT</div><div class="t-title" style="margin-bottom:var(--s-5)">대학은, 지금 <span class="is-accent">생존의 시간</span>입니다.</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--s-4);max-width:1000px;width:100%;margin-bottom:var(--s-4)"><div style="text-align:left;padding:var(--s-3)"><div class="t-caption w-bold is-accent" style="margin-bottom:var(--s-1);letter-spacing:2px">2025</div><div style="font-size:48px;font-weight:700;color:#E84E10;line-height:1;letter-spacing:-2px">−18%</div><div class="t-caption is-ink" style="margin-top:8px">부울경 수험생 수 (2018 대비)</div></div><div style="text-align:left;padding:var(--s-3);border-left:1px solid #E8E8E8;border-right:1px solid #E8E8E8"><div class="t-caption w-bold is-accent" style="margin-bottom:var(--s-1);letter-spacing:2px">2026</div><div style="font-size:48px;font-weight:700;color:#E84E10;line-height:1;letter-spacing:-2px">2.3배</div><div class="t-caption is-ink" style="margin-top:8px">지방 사립대 광고 경쟁 격화</div></div><div style="text-align:left;padding:var(--s-3)"><div class="t-caption w-bold is-accent" style="margin-bottom:var(--s-1);letter-spacing:2px">2030</div><div style="font-size:48px;font-weight:700;color:#E84E10;line-height:1;letter-spacing:-2px">38%</div><div class="t-caption is-ink" style="margin-top:8px">폐교 위기 예측 (교육부)</div></div></div><div class="t-subtitle w-regular is-muted" style="font-style:italic">모두가 특성화로 살아남고 있습니다</div></div><!--SCRIPT_START-->"대학은, 지금 <strong>생존의 시간</strong>입니다.<br><br>부울경 수험생은 18% 줄었고, 2026년 광고 경쟁은 2.3배 격화되고 있습니다. 2030년까지 38%가 폐교 위기입니다.<br><br>모두가 <strong>특성화</strong>로 살아남고 있습니다."<!--SCRIPT_END-->"""

P3_MAP = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-4)">POSITIONING MAP</div><div class="t-title" style="margin-bottom:var(--s-4)">모두, <span class="is-accent">특성화로 기억</span>되고 있습니다</div><div style="width:520px;height:1px;background:#E8E8E8;margin:0 auto var(--s-5)"></div><div class="t-subtitle w-regular" style="line-height:2.2;text-align:center"><strong>동의대</strong> &nbsp;<span class="is-accent">한의대</span><br><strong>동서대</strong> &nbsp;<span class="is-accent">영상·IT</span><br><strong>부경대</strong> &nbsp;<span class="is-accent">국립 규모</span><br><strong>신라대</strong> &nbsp;<span class="is-accent">종합대학</span><br><strong>영산대</strong> &nbsp;<span class="is-accent">호텔관광</span></div><div style="width:520px;height:1px;background:#E8E8E8;margin:var(--s-4) auto 0"></div><div class="t-caption is-muted" style="margin-top:var(--s-3);font-style:italic">같은 무대, 다른 무기</div></div><!--SCRIPT_START-->"그래서 모두, <strong>특성화로 기억</strong>되고 있습니다.<br><br>동의대는 한의대, 동서대는 영상·IT, 부경대는 국립 규모, 신라대는 종합대학, 그리고 <strong>영산대는 호텔관광</strong>.<br><br>같은 무대, 다른 무기입니다."<!--SCRIPT_END-->"""

P4_Q = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-heading is-muted" style="margin-bottom:var(--s-5);font-weight:400">그렇다면 —</div><div class="t-title" style="font-size:56px;line-height:1.4;max-width:1100px">영산대학교는,<br>호텔관광으로 얼마나<br><span class="is-accent fx-cursor">바로</span> 떠오르고 있을까요?</div></div><!--SCRIPT_START-->"그렇다면 —<br><br>영산대학교는, 호텔관광으로 얼마나 <strong>'바로' 떠오르고 있을까요?</strong><br><br>(3초 침묵)"<!--SCRIPT_END-->"""

P5_MORPH = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0;position:relative">
<div class="fx-p4-s1"><div style="font-size:220px;font-weight:700;color:#D0D0D0;letter-spacing:-10px;font-family:'Roboto Mono','Courier New',monospace;font-variant-numeric:tabular-nums;line-height:1">0825503</div></div>
<div class="fx-p4-s2"><div style="font-size:140px;font-weight:700;color:#D0D0D0;letter-spacing:-4px;font-family:'Roboto Mono','Courier New',monospace;line-height:1;font-variant-numeric:tabular-nums">08<span style="margin:0 28px;color:#A0A0A5;font-size:80px;vertical-align:0.12em">·</span>25<span style="margin:0 28px;color:#A0A0A5;font-size:80px;vertical-align:0.12em">·</span>55<span style="margin:0 28px;color:#A0A0A5;font-size:80px;vertical-align:0.12em">·</span>03</div></div>
<div style="padding-top:var(--s-2)"><div class="t-subtitle w-regular" style="line-height:2.3;display:inline-block;text-align:left"><span class="fx-p4-fact1"><span class="is-accent w-bold" style="font-size:30px">08</span> &nbsp;연구 세계 8위 · 호스피탈리티</span><br><span class="fx-p4-fact2"><span class="is-accent w-bold" style="font-size:30px">25</span> &nbsp;총지배인 25명 · 호텔관광학과</span><br><span class="fx-p4-fact3"><span class="is-accent w-bold" style="font-size:30px">55</span> &nbsp;QS 세계 55위 · 2026 호스피탈리티</span><br><span class="fx-p4-fact4"><span class="is-accent w-bold" style="font-size:30px">03</span> &nbsp;한국 호텔관광 Top 3</span></div></div>
<div class="fx-p4-conclusion" style="position:absolute;bottom:var(--s-5);left:0;right:0;text-align:center"><div class="t-heading">세계가 주목하는 호텔관광,<br>그 중심 — <span class="is-accent">부산 영산대학교</span></div></div>
</div><!--SCRIPT_START-->(6초 morph 애니 — 발표자 무발화)<br><br>"…표지에서 보신 이 시리얼."<br><br>(Stage 2 분해)<br><br>"연구 세계 8위. 총지배인 25명. QS 세계 55위. 한국 호텔관광 Top 3."<br><br>(결론 등장 시)<br>"세계가 주목하는 호텔관광 — 그 중심은, <strong>부산 영산대학교</strong>입니다."<!--SCRIPT_END-->"""

P6_ISSUE = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-body is-muted" style="margin-bottom:var(--s-5)">근거는, 단단합니다.</div><div style="width:520px;height:1px;background:#E8E8E8;margin:0 auto var(--s-5)"></div><div class="t-title" style="line-height:1.5;font-size:42px;max-width:1100px">그런데 —<br>같은 호텔관광 무대에서<br>이 숫자들을 어떻게<br><span class="is-accent">차별화된 기억</span>으로 만들까요?</div></div><!--SCRIPT_START-->"근거는, 단단합니다.<br><br>그런데 — 같은 호텔관광 무대에서 이 숫자들을 어떻게 <strong>차별화된 기억</strong>으로 만들까요?"<!--SCRIPT_END-->"""

P7_ANSWER = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-title" style="line-height:1.4;margin-bottom:var(--s-5);max-width:1100px">차별화된 영산대를,<br>수험생·학부모에게 <span class="is-accent">각인시키는 것.</span></div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-4)"></div><div class="t-subtitle w-regular is-muted">그것이, 이번 제안의 <span class="is-accent w-bold">전부</span>입니다</div></div><!--SCRIPT_START-->"차별화된 영산대를, 수험생·학부모에게 <strong>각인시키는 것.</strong><br><br>그것이, 이번 제안의 <strong>전부</strong>입니다."<!--SCRIPT_END-->"""

SLOGAN = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:슬로건--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-headline" style="line-height:1.3;font-size:84px"><span class="fx-slogan-1">호텔관광,</span><br><span class="fx-slogan-2"><span class="is-accent fx-zihye-punch">영산</span>으로 기억됩니다.</span></div></div><!--SCRIPT_START-->"이번 영상의 슬로건은 한 문장입니다.<br><br><strong>호텔관광, 영산으로 기억됩니다.</strong><br><br>(3초 침묵)"<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    try:
        # 1. 기존 V30 모든 section +1 shift
        conn.execute("UPDATE sections SET order_idx = order_idx + 1 WHERE proposal_id=?", (PID,))
        print("1. order_idx +1 shift")

        # 2. NEW P2 (order 1) 시장 진단 삽입
        conn.execute(
            """INSERT INTO sections (proposal_id,level,title,order_idx,content,status)
               VALUES (?,2,?,1,?,'pending')""",
            (PID, "시장 진단", P2_MARKET),
        )
        print("2. P2 시장 진단 (order 1) 삽입")

        # 3. order 2 (구 P2) 특성화 경쟁 지도 교체
        conn.execute(
            "UPDATE sections SET content=?, title=? WHERE proposal_id=? AND order_idx=2",
            (P3_MAP, "특성화 경쟁 지도", PID),
        )
        print("3. P3 특성화 경쟁 지도 교체")

        # 4. order 3 (구 P3 영산대는?) 완화 질문
        conn.execute(
            "UPDATE sections SET content=?, title=? WHERE proposal_id=? AND order_idx=3",
            (P4_Q, "영산대는 바로 떠오르는가", PID),
        )
        print("4. P4 완화 질문 교체")

        # 5. order 4 (구 P4 morph) 0825503 재작성
        conn.execute(
            "UPDATE sections SET content=?, title=? WHERE proposal_id=? AND order_idx=4",
            (P5_MORPH, "morph 0825503", PID),
        )
        print("5. P5 morph 0825503 재작성")

        # 6. order 5 (구 P5 선언+질문) 단일 화두
        conn.execute(
            "UPDATE sections SET content=?, title=? WHERE proposal_id=? AND order_idx=5",
            (P6_ISSUE, "차별화·각인 화두", PID),
        )
        print("6. P6 단일 화두 교체")

        # 7. order 6 (구 P6 답) 차별화 답
        conn.execute(
            "UPDATE sections SET content=?, title=? WHERE proposal_id=? AND order_idx=6",
            (P7_ANSWER, "차별화·각인 답", PID),
        )
        print("7. P7 차별화 답 교체")

        # 8. 슬로건 (구 order 30 → shift 후 order 31) 교체
        # P30/P31 스왑 적용 후 현재 슬로건은 order 31 (P32)
        conn.execute(
            "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=31",
            (SLOGAN, PID),
        )
        print("8. 슬로건 교체: 호텔관광, 영산으로 기억됩니다")

        conn.commit()
        print("\n완료")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
