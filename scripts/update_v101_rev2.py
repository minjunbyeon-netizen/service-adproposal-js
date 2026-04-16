# -*- coding: utf-8 -*-
"""V101 REV2 빌드업 재구성 (맥킨지 피라미드 적용).

변경:
  P2  본질           → 평가 2축 (1번, 2번 명시)
  P3  소음           → 시장·소음 2분할 그리드 (학령인구+소음)
  P4  시대 선언      → '대단한 대학' + 유사 광고 4개 증거
  P5  morph          → PIVOT 질문 "그래서, 지금 뭘 하고 있지?" (A안)
  P6  전략 선언      → morph 0825503 이동 (P5 질문의 답)
  P7  컨셉           → "각인이 제안의 전부"

핵심 설계: P5 질문 → (5초 침묵) → P6 morph 답 → P7 각인 선언
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179  # V101

# =============================================================================
# 빌드업 콘텐츠
# =============================================================================

P2_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-5)">THE ESSENCE</div><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-6)">광고대행사 선정은, 단 두 가지로 결정됩니다</div><div style="display:flex;flex-direction:column;gap:var(--s-3);max-width:780px;width:100%;margin-bottom:var(--s-6)"><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:48px;font-weight:700;color:#E84E10;line-height:1;letter-spacing:-2px;min-width:72px;text-align:left;font-family:Roboto,sans-serif">01</div><div style="font-size:36px;font-weight:700;color:#1A1A1A;line-height:1.2;text-align:left;flex:1">얼마나 <span style="color:#E84E10">많이 팔 것이냐</span></div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:48px;font-weight:700;color:#E84E10;line-height:1;letter-spacing:-2px;min-width:72px;text-align:left;font-family:Roboto,sans-serif">02</div><div style="font-size:36px;font-weight:700;color:#1A1A1A;line-height:1.2;text-align:left;flex:1">얼마나 <span style="color:#E84E10">각인시킬 것이냐</span></div></div></div><div class="t-caption is-muted" style="font-style:italic">나머지는, 모두 수단입니다</div></div><!--SCRIPT_START-->"광고대행사 선정은, 단 두 가지로 결정됩니다.<br><br><strong>하나. 얼마나 많이 팔 것이냐.</strong><br><strong>둘. 얼마나 각인시킬 것이냐.</strong><br><br>나머지는 모두 수단입니다. 이 2개로만 평가받습니다."<!--SCRIPT_END-->"""

P3_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-4) 0"><div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-3)">MARKET CONTEXT</div><div class="t-heading" style="margin-bottom:var(--s-5)">대학 광고 시장, 현재 좌표</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:0;max-width:1100px;width:100%;margin:0 auto"><div style="text-align:left;padding:var(--s-3) var(--s-5) var(--s-3) var(--s-3)"><div class="t-caption w-bold" style="color:#6E6E73;letter-spacing:3px;margin-bottom:var(--s-3)">COLD FACTS</div><div style="font-size:15px;line-height:2.4;color:#1A1A1A"><div style="display:flex;gap:var(--s-2);align-items:baseline"><span style="color:#E84E10;font-weight:700;min-width:80px;font-size:17px">-18%</span><span>부울경 수험생 (2018→2025)</span></div><div style="display:flex;gap:var(--s-2);align-items:baseline"><span style="color:#E84E10;font-weight:700;min-width:80px;font-size:17px">2.3배</span><span>지방 사립대 광고 경쟁</span></div><div style="display:flex;gap:var(--s-2);align-items:baseline"><span style="color:#E84E10;font-weight:700;min-width:80px;font-size:17px">38%</span><span>2030 폐교 위기 예측</span></div></div></div><div style="text-align:left;padding:var(--s-3) var(--s-3) var(--s-3) var(--s-5);border-left:1px solid #E8E8E8"><div class="t-caption w-bold" style="color:#6E6E73;letter-spacing:3px;margin-bottom:var(--s-3)">THE NOISE</div><div style="font-size:15px;line-height:2.2;color:#1A1A1A"><div><span class="is-accent" style="font-size:70%">●</span> &nbsp;"글로벌 경쟁력 1위"</div><div><span class="is-accent" style="font-size:70%">●</span> &nbsp;"최고의 교수진"</div><div><span class="is-accent" style="font-size:70%">●</span> &nbsp;"미래형 인재 양성"</div><div><span class="is-accent" style="font-size:70%">●</span> &nbsp;"4차 산업 선도"</div><div><span class="is-accent" style="font-size:70%">●</span> &nbsp;"최고 수준 취업률"</div></div></div></div><div class="t-caption is-muted" style="margin-top:var(--s-5);font-style:italic">다들 아시는 이야기입니다. 짚고 넘어갑니다.</div></div><!--SCRIPT_START-->"대학 광고 시장의 현재 좌표입니다.<br><br>왼쪽 — 부울경 수험생 18% 감소, 광고 경쟁 2.3배 격화, 2030년 38% 폐교 위기.<br>오른쪽 — 모든 대학이 같은 말을 외칩니다. 글로벌 1위, 최고 교수진, 미래형 인재, 4차산업 선도, 최고 취업률.<br><br>다들 아시는 이야기입니다. 짚고 넘어가겠습니다."<!--SCRIPT_END-->"""

P4_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-3)">BROKEN PLAYBOOK</div><div class="t-headline" style="margin-bottom:var(--s-3);line-height:1.3">'<span class="is-muted">대단한 대학</span>'은, 이제 통하지 않습니다</div><div class="t-subtitle w-regular is-muted" style="line-height:1.7;margin-bottom:var(--s-4);max-width:820px">'세계 최상위', '국내 최고' —<br>너무 많이 들어, 이제 놀라지 않습니다</div><div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:var(--s-2);max-width:1100px;width:100%;margin:0 auto var(--s-3)"><div style="aspect-ratio:16/10;background:#F5F5F5;border:1px solid #E0E0E0;display:flex;align-items:center;justify-content:center;color:#A0A0A5;font-size:11px;letter-spacing:2px;font-weight:700">AD SAMPLE 01</div><div style="aspect-ratio:16/10;background:#F5F5F5;border:1px solid #E0E0E0;display:flex;align-items:center;justify-content:center;color:#A0A0A5;font-size:11px;letter-spacing:2px;font-weight:700">AD SAMPLE 02</div><div style="aspect-ratio:16/10;background:#F5F5F5;border:1px solid #E0E0E0;display:flex;align-items:center;justify-content:center;color:#A0A0A5;font-size:11px;letter-spacing:2px;font-weight:700">AD SAMPLE 03</div><div style="aspect-ratio:16/10;background:#F5F5F5;border:1px solid #E0E0E0;display:flex;align-items:center;justify-content:center;color:#A0A0A5;font-size:11px;letter-spacing:2px;font-weight:700">AD SAMPLE 04</div></div><div class="t-caption is-muted" style="font-style:italic">이런 비슷한 광고, 너무 많습니다</div></div><!--SCRIPT_START-->"그래서 '대단한 대학'은, 이제 통하지 않습니다.<br><br>'세계 최상위', '국내 최고' — 너무 많이 들어, 이제 놀라지 않습니다.<br><br>(광고 시안 4개를 가리키며)<br>이런 비슷한 광고가, 지금도 매일 쏟아지고 있습니다."<!--SCRIPT_END-->"""

P5_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0;position:relative"><div class="t-caption is-muted" style="letter-spacing:4px;position:absolute;top:var(--s-5)">THE ONLY QUESTION</div><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-6);font-style:italic">이제, 한 문장이 모든 것을 결정합니다</div><div style="font-size:80px;font-weight:700;color:#1A1A1A;line-height:1.35;letter-spacing:-2.5px;max-width:1100px">"그래서 —<br><span class="is-accent">지금 뭘 하고 있지?"</span></div><div class="t-caption is-muted" style="letter-spacing:3px;font-style:italic;position:absolute;bottom:var(--s-4)">5 SECONDS OF SILENCE</div></div><!--SCRIPT_START-->"이제, 한 문장이 모든 것을 결정합니다.<br><br><strong>'그래서 — 지금 뭘 하고 있지?'</strong><br><br>(5초 침묵 — 평가위원이 스스로 질문을 끝까지 곱씹게 합니다)"<!--SCRIPT_END-->"""

P7_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-5)">THE ENTIRE PROPOSAL</div><div class="t-title" style="line-height:1.4;margin-bottom:var(--s-5);max-width:1100px">이 움직임을,<br>수험생과 학부모에게 <span class="is-accent">각인시키는 것.</span></div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div class="t-subtitle w-regular is-muted">그것이, 이번 제안의 <span class="is-accent w-bold">전부</span>입니다</div></div><!--SCRIPT_START-->"이 움직임을 — 수험생과 학부모에게 <strong>각인시키는 것.</strong><br><br>그것이, 이번 제안의 <strong>전부</strong>입니다."<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    try:
        # 1. 기존 idx=4 (morph) content 백업
        morph_row = conn.execute(
            "SELECT title, content FROM sections WHERE proposal_id=? AND order_idx=4",
            (PID,),
        ).fetchone()
        if not morph_row:
            raise RuntimeError(f"V101 idx=4 morph 섹션 없음")
        morph_title = morph_row["title"]
        morph_content = morph_row["content"]
        print(f"morph 백업 완료: {morph_title}, len={len(morph_content)}")

        # 2. idx=5 (전략 선언) → morph 내용으로 덮어쓰기
        conn.execute(
            "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=5",
            (morph_title, morph_content, PID),
        )
        print(f"idx=5: morph 0825503 (이동)")

        # 3. idx=4 → P5 PIVOT 질문
        conn.execute(
            "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=4",
            ("PIVOT 질문", P5_CONTENT, PID),
        )
        print(f"idx=4: PIVOT 질문")

        # 4. idx=1,2,3,6 업데이트
        updates = [
            (1, "평가 2축", P2_CONTENT),
            (2, "시장·소음", P3_CONTENT),
            (3, "대단한 대학의 한계", P4_CONTENT),
            (6, "제안의 전부", P7_CONTENT),
        ]
        for order_idx, title, content in updates:
            conn.execute(
                "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=?",
                (title, content, PID, order_idx),
            )
            print(f"idx={order_idx}: {title}")

        conn.commit()

        # 5. 결과
        rows = conn.execute(
            "SELECT order_idx, title FROM sections WHERE proposal_id=? ORDER BY order_idx LIMIT 12",
            (PID,),
        ).fetchall()
        print(f"\n=== V101 REV2 빌드업 ===")
        for r in rows:
            print(f"  idx={r['order_idx']:2d} | {r['title']}")
        print(f"\n완료! http://localhost:8881/api/proposals/{PID}/export-html")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
