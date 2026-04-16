# -*- coding: utf-8 -*-
"""V101 REV4 빌드업 재구성 (8장).

P1  표지 (유지)
P2  평가 2축 (idx=1 유지)
P3  시장 현황 — 생존 (idx=2 유지)
P4  경쟁 지도 (idx=3 교체, 구 광고 시안 가로형 자리)
P5  질문 "그럼 영산대학교는요!?" (idx=4 교체)
P6  답 — 호텔관광 특성화 + 0825503 (idx=5 교체)
P7  체험 — 숫자 사라진 후 "기억나십니까?" (idx=6 교체)
P8  결론 — 기억 넘어 각인 = 전부 (idx=7 교체)

삭제: 기존 idx 8~10 (영산대 움직임 + 똑같이 외치지 않음 + 각인 선언 — 전부)
이후 idx 11~ 는 -3 시프트하여 idx 8~ 로 이동
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

# =============================================================================
# P4 — 경쟁 지도
# =============================================================================
P4_COMPETITORS = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-4) 0"><div class="t-heading" style="margin-bottom:var(--s-3);line-height:1.35">같은 무대에서, <span class="is-accent">각자의 무기</span>로 싸우고 있습니다</div><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-5);font-style:italic">부산·경남 주요 사립대 특성화 지도</div><div style="display:flex;flex-direction:column;gap:0;max-width:820px;width:100%;margin:0 auto"><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:22px;font-weight:700;color:#1A1A1A;min-width:130px;text-align:left">동의대</div><div style="font-size:16px;color:#1A1A1A;text-align:left;flex:1"><span class="is-accent w-bold">한의학</span> <span style="color:#6E6E73">— 한의대 전통</span></div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:22px;font-weight:700;color:#1A1A1A;min-width:130px;text-align:left">부경대</div><div style="font-size:16px;color:#1A1A1A;text-align:left;flex:1"><span class="is-accent w-bold">해양·수산</span> <span style="color:#6E6E73">— 국립의 규모</span></div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:22px;font-weight:700;color:#1A1A1A;min-width:130px;text-align:left">신라대</div><div style="font-size:16px;color:#1A1A1A;text-align:left;flex:1"><span class="is-accent w-bold">종합대학</span> <span style="color:#6E6E73">— 사범·의료 중심</span></div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:22px;font-weight:700;color:#1A1A1A;min-width:130px;text-align:left">고신대</div><div style="font-size:16px;color:#1A1A1A;text-align:left;flex:1"><span class="is-accent w-bold">의과대학</span> <span style="color:#6E6E73">— 기독교 전통</span></div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:22px;font-weight:700;color:#1A1A1A;min-width:130px;text-align:left">경성대</div><div style="font-size:16px;color:#1A1A1A;text-align:left;flex:1"><span class="is-accent w-bold">약학·예술</span> <span style="color:#6E6E73">— 통합 캠퍼스</span></div></div></div></div><!--SCRIPT_START-->"경쟁의 무대를 보겠습니다. 부산·경남의 주요 사립대는, 각자의 무기로 싸우고 있습니다.<br><br>동의대는 <strong>한의학</strong>, 부경대는 <strong>해양·수산</strong>, 신라대는 <strong>종합대학</strong>, 고신대는 <strong>의과대학</strong>, 경성대는 <strong>약학·예술</strong>.<br><br>같은 무대, 다른 무기입니다."<!--SCRIPT_END-->"""


# =============================================================================
# P5 — 질문 "그럼 영산대학교는요!?"
# =============================================================================
P5_QUESTION = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-5);font-style:italic">그럼 —</div><div style="font-size:104px;font-weight:700;color:#1A1A1A;line-height:1.2;letter-spacing:-3px">영산대학교<span class="is-accent">는요!?</span></div></div><!--SCRIPT_START-->"그럼 — <strong>영산대학교는요!?</strong><br><br>(3초 침묵 — 평가위원이 스스로 떠올릴 시간)"<!--SCRIPT_END-->"""


# =============================================================================
# P6 — 답: 호텔관광 특성화 + 0825503 + 4가지 사실
# =============================================================================
P6_ANSWER = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-2)">영산대는 —</div><div class="t-title" style="margin-bottom:var(--s-4);line-height:1.35"><span class="is-accent">호텔관광대학 특성화 대학</span></div><div style="font-size:84px;font-weight:700;color:#1A1A1A;letter-spacing:-3px;font-family:'Roboto Mono','Courier New',monospace;line-height:1;margin-bottom:var(--s-2);font-variant-numeric:tabular-nums">0825503</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-3)"></div><div style="display:flex;flex-direction:column;gap:0;max-width:820px;width:100%;margin:0 auto"><div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:36px;font-weight:700;color:#E84E10;line-height:1;min-width:72px;text-align:left;font-family:Roboto,sans-serif;font-variant-numeric:tabular-nums">08</div><div style="font-size:18px;color:#1A1A1A;text-align:left;flex:1">연구력 <strong>세계 8위</strong> <span style="color:#6E6E73;font-size:13px">(국내 1위)</span></div></div><div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:36px;font-weight:700;color:#E84E10;line-height:1;min-width:72px;text-align:left;font-family:Roboto,sans-serif;font-variant-numeric:tabular-nums">25</div><div style="font-size:18px;color:#1A1A1A;text-align:left;flex:1">호텔 총지배인 <strong>25명</strong> 배출</div></div><div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:36px;font-weight:700;color:#E84E10;line-height:1;min-width:72px;text-align:left;font-family:Roboto,sans-serif;font-variant-numeric:tabular-nums">55</div><div style="font-size:18px;color:#1A1A1A;text-align:left;flex:1">QS 호스피탈리티 <strong>세계 55위</strong> <span style="color:#6E6E73;font-size:13px">(비수도권 1위)</span></div></div><div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:36px;font-weight:700;color:#E84E10;line-height:1;min-width:72px;text-align:left;font-family:Roboto,sans-serif;font-variant-numeric:tabular-nums">03</div><div style="font-size:18px;color:#1A1A1A;text-align:left;flex:1">세종·경희와 <strong>한국 Top 3</strong></div></div></div></div><!--SCRIPT_START-->"영산대는 — <strong>호텔관광대학 특성화 대학</strong>입니다.<br><br>표지에서 보신 시리얼 <strong>0825503</strong>의 정체가 바로 이것입니다.<br><br>연구력 <strong>세계 8위</strong> (국내 1위), 호텔 총지배인 <strong>25명</strong> 배출, QS 호스피탈리티 <strong>세계 55위</strong> (비수도권 1위), 세종·경희와 <strong>한국 Top 3</strong>."<!--SCRIPT_END-->"""


# =============================================================================
# P7 — 체험: 숫자가 사라진 후 "기억나십니까?"
# =============================================================================
P7_RECALL = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-6);font-style:italic">방금 보여드린 숫자 —</div><div style="font-size:80px;font-weight:700;color:#1A1A1A;line-height:1.3;letter-spacing:-2.5px;max-width:1100px">몇 개가 <span class="is-accent">기억나십니까?</span></div></div><!--SCRIPT_START-->"(화면의 숫자들이 사라지고, 질문만 남습니다)<br><br>방금 보여드린 숫자 — <strong>몇 개가 기억나십니까?</strong><br><br>(5초 침묵 — 평가위원이 스스로 떠올릴 시간을 줍니다)<br><br>솔직히, 쉽지 않으실 겁니다."<!--SCRIPT_END-->"""


# =============================================================================
# P8 — 결론: 기억 넘어 각인 = 전부
# =============================================================================
P8_CONCLUSION = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-3)">우리는 —</div><div class="t-title" style="margin-bottom:var(--s-4);line-height:1.4">이 숫자를 <span class="is-accent">기억시켜야</span> 합니다</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-4)"></div><div class="t-title" style="line-height:1.4;margin-bottom:var(--s-5);max-width:1100px">기억을 넘어,<br>'<span class="is-accent">각인</span>'시키는 것</div><div class="t-subtitle w-regular is-muted">그것이, 이 제안의 <span class="is-accent w-bold">전부</span>입니다</div></div><!--SCRIPT_START-->"우리는 — 이 숫자를 <strong>기억시켜야</strong> 합니다.<br><br>기억을 넘어, '<strong>각인</strong>'시키는 것.<br><br>그것이, 이 제안의 <strong>전부</strong>입니다."<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    try:
        # 1. P4~P8 내용 교체 (idx 3~7)
        updates = [
            (3, "경쟁 지도", P4_COMPETITORS),
            (4, "영산대학교는요!?", P5_QUESTION),
            (5, "호텔관광 특성화 + 0825503", P6_ANSWER),
            (6, "기억나십니까?", P7_RECALL),
            (7, "각인 = 전부", P8_CONCLUSION),
        ]
        for idx, title, content in updates:
            conn.execute(
                "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=?",
                (title, content, PID, idx),
            )
            print(f"idx={idx}: {title}")

        # 2. 기존 idx 8~10 삭제 (영산대 움직임 + 똑같이 외치지 않음 + 각인 선언 — 전부)
        deleted = conn.execute(
            "DELETE FROM sections WHERE proposal_id=? AND order_idx BETWEEN 8 AND 10",
            (PID,),
        ).rowcount
        print(f"기존 idx 8~10 삭제: {deleted}개")

        # 3. idx 11~ 모두 -3 시프트
        conn.execute(
            "UPDATE sections SET order_idx = order_idx - 3 "
            "WHERE proposal_id=? AND order_idx >= 11",
            (PID,),
        )
        print("idx 11~ 전체 -3 시프트")

        conn.commit()

        # 4. 확인
        rows = conn.execute(
            "SELECT order_idx, title FROM sections WHERE proposal_id=? ORDER BY order_idx LIMIT 16",
            (PID,),
        ).fetchall()
        print(f"\n=== V101 REV4 ===")
        for r in rows:
            print(f"  idx={r['order_idx']:2d} | {r['title']}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
