# -*- coding: utf-8 -*-
"""V101 최종 폴리싱 — 맥킨지 베테랑 검수 지적 일괄 반영."""
import sqlite3
import re
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


def main():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row

    # =========================================================================
    # HIGH 1: P3 (idx=2) -18% 마이너스 기호 복원
    # =========================================================================
    row = conn.execute("SELECT content FROM sections WHERE proposal_id=? AND order_idx=2", (PID,)).fetchone()
    c = row["content"]
    # "18%" → "-18%" (맥락: 부울경 수험생 감소)
    # 현재 수치 크기 56/40 어느거든 '18%' 단독 텍스트에만 적용
    c = c.replace(">18%<", ">-18%<")
    conn.execute("UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=2", (c, PID))
    print("[HIGH 1] P3: -18% 마이너스 복원")

    # =========================================================================
    # HIGH 2: P6 (idx=5) morph 4행 prefix 08/25/55/03 복원
    # =========================================================================
    P6_CONTENT = """<!--PARENT:Ⅰ. 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div style="font-size:48px;font-weight:700;color:#1A1A1A;line-height:1.2;margin-bottom:var(--s-3)">호텔관광대학 특성화 대학</div><div style="font-size:120px;font-weight:700;color:#1A1A1A;line-height:1;margin-bottom:var(--s-5);font-variant-numeric:tabular-nums">0825503</div><div style="display:flex;flex-direction:column;gap:0;max-width:820px;width:100%;margin:0 auto"><div style="display:grid;grid-template-columns:72px 1fr;gap:var(--s-3);align-items:center;padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:40px;font-weight:700;color:#E84E10;line-height:1;text-align:left">08</div><div style="font-size:20px;color:#1A1A1A;text-align:left">연구력 세계 8위 <span style="color:#6E6E73;font-size:14px">국내 1위</span></div></div><div style="display:grid;grid-template-columns:72px 1fr;gap:var(--s-3);align-items:center;padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:40px;font-weight:700;color:#E84E10;line-height:1;text-align:left">25</div><div style="font-size:20px;color:#1A1A1A;text-align:left">호텔 총지배인 25명 배출</div></div><div style="display:grid;grid-template-columns:72px 1fr;gap:var(--s-3);align-items:center;padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:40px;font-weight:700;color:#E84E10;line-height:1;text-align:left">55</div><div style="font-size:20px;color:#1A1A1A;text-align:left">QS 호스피탈리티 세계 55위 <span style="color:#6E6E73;font-size:14px">비수도권 1위</span></div></div><div style="display:grid;grid-template-columns:72px 1fr;gap:var(--s-3);align-items:center;padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:40px;font-weight:700;color:#E84E10;line-height:1;text-align:left">03</div><div style="font-size:20px;color:#1A1A1A;text-align:left">세종 경희와 한국 Top 3</div></div></div></div>"""
    conn.execute("UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=5", (P6_CONTENT, PID))
    print("[HIGH 2] P6: 08/25/55/03 prefix 복원")

    # =========================================================================
    # HIGH 3: P7 (idx=6) 기억나십니까 폰트 축소 + 부제 복원
    # =========================================================================
    P7_CONTENT = """<!--PARENT:Ⅰ. 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div style="font-size:24px;color:#6E6E73;margin-bottom:var(--s-5)">방금 보여드린 숫자</div><div style="font-size:56px;font-weight:700;color:#1A1A1A;line-height:1.3;max-width:1280px">몇 개가 <span style="color:#E84E10">기억나십니까</span></div></div>"""
    conn.execute("UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=6", (P7_CONTENT, PID))
    print("[HIGH 3] P7: 폰트 56px + 부제 복원")

    # =========================================================================
    # MID 4: P4 (idx=3) 대학 특성 오렌지 → 검정 bold
    # =========================================================================
    row = conn.execute("SELECT content FROM sections WHERE proposal_id=? AND order_idx=3", (PID,)).fetchone()
    c = row["content"]
    # is-accent w-bold → 그냥 w-bold (검정 bold)
    c = re.sub(
        r'<span class="is-accent" style="font-weight:700">([^<]+)</span>',
        r'<span style="font-weight:700;color:#1A1A1A">\1</span>',
        c,
    )
    # 혹시 'is-accent' class만 단독인 경우도
    c = re.sub(
        r'<span class="is-accent">([^<]+)</span>',
        r'<span style="font-weight:700;color:#1A1A1A">\1</span>',
        c,
    )
    conn.execute("UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=3", (c, PID))
    print("[MID 4] P4: 5대학 특성 오렌지 → 검정 bold")

    # =========================================================================
    # MID 5: P16 (idx=15) AFTER 헤더 복원 확인
    # =========================================================================
    row = conn.execute("SELECT content FROM sections WHERE proposal_id=? AND order_idx=15", (PID,)).fetchone()
    c = row["content"]
    # AFTER 헤더가 누락됐는지 확인. 'AFTER' 라벨이 없으면 추가
    if "AFTER" not in c and "증명 (각인)" not in c:
        print("[MID 5] P16 AFTER 헤더 누락 — 확인 필요")
    else:
        print("[MID 5] P16 AFTER 헤더 정상 — skip")

    # =========================================================================
    # LOW 8: Haiku 톤 수정 지적 반영
    # =========================================================================
    tone_fixes = [
        # P40, P41, P42, P45, P47 등의 카피 개선
        ("클릭 유도형 카피 적용", "클릭 유도형 카피를 적용합니다"),
        ("학과별 차별화 포인트 발굴 자문", "학과별 차별화 포인트 발굴 자문을 제공합니다"),
        ("이렇게 씁니다", "이렇게 배분합니다"),
        ("같은 예산으로 더 많이 보여드리겠습니다", "같은 예산으로 더 높은 성과를 보여드리겠습니다"),
        ("왜 이 조합 인가", "왜 이런 조합입니까"),
        ("증명을 이렇게 확장 합니다", "증명을 이렇게 확장합니다"),
    ]
    rows = conn.execute("SELECT id, content FROM sections WHERE proposal_id=?", (PID,)).fetchall()
    tone_count = 0
    for r in rows:
        c = r["content"]
        if not c:
            continue
        new = c
        for old, new_text in tone_fixes:
            new = new.replace(old, new_text)
        if new != c:
            conn.execute("UPDATE sections SET content=? WHERE id=?", (new, r["id"]))
            tone_count += 1
    print(f"[LOW 8] Haiku 톤 수정 {tone_count}개 섹션 반영")

    conn.commit()
    conn.close()
    print("\n완료")


if __name__ == "__main__":
    main()
