# -*- coding: utf-8 -*-
"""V101 - 9건 일괄 처리."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


def main():
    conn = sqlite3.connect(str(DB))

    # 1) P36 (idx=35) 관련 직종 담당자 -> 졸업생 + 인터뷰 콘텐츠 -> 인터뷰 콘텐츠 (예시)
    r = conn.execute("SELECT content FROM sections WHERE proposal_id=? AND order_idx=35", (PID,)).fetchone()
    c = r[0]
    c = c.replace("관련 직종 담당자를 섭외해", "관련 직종 졸업생을 섭외해")
    c = c.replace(
        "<th style=\"padding:12px 14px;text-align:left;font-weight:700;color:#6E6E73\">인터뷰 콘텐츠</th>",
        "<th style=\"padding:12px 14px;text-align:left;font-weight:700;color:#6E6E73\">인터뷰 콘텐츠 (예시)</th>"
    )
    conn.execute("UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=35", (c, PID))
    print("[1,2] P36: 담당자→졸업생, 인터뷰 콘텐츠→(예시)")

    # 3) P38 (idx=37) '가장 강력하게 작동하는 매체' 오렌지
    r = conn.execute("SELECT content FROM sections WHERE proposal_id=? AND order_idx=37", (PID,)).fetchone()
    c = r[0]
    c = c.replace(
        "각 슬로건이 가장 강력하게 작동하는 매체에 배치",
        "각 슬로건이 <span style=\"color:#E84E10;font-weight:700\">가장 강력하게 작동하는 매체</span>에 배치"
    )
    conn.execute("UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=37", (c, PID))
    print("[3] P38: 가장 강력하게 작동하는 매체 오렌지")

    # 4) P39 (idx=38) 'A/B 테스트' 오렌지
    r = conn.execute("SELECT content FROM sections WHERE proposal_id=? AND order_idx=38", (PID,)).fetchone()
    c = r[0]
    c = c.replace(
        "디지털은 A/B 테스트가 가능",
        "디지털은 <span style=\"color:#E84E10;font-weight:700\">A/B 테스트</span>가 가능"
    )
    conn.execute("UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=38", (c, PID))
    print("[4] P39: A/B 테스트 오렌지")

    # 5) P41 (idx=40) 삭제
    conn.execute("DELETE FROM sections WHERE proposal_id=? AND order_idx=40", (PID,))
    rows = conn.execute(
        "SELECT id, order_idx FROM sections WHERE proposal_id=? AND order_idx > 40 ORDER BY order_idx ASC",
        (PID,),
    ).fetchall()
    for rid, oi in rows:
        conn.execute("UPDATE sections SET order_idx=? WHERE id=?", (oi - 1, rid))
    print(f"[5] P41 삭제 + {len(rows)}개 -1 시프트")

    # 6) P42 (기존 idx=41 → 시프트 후 idx=40) 제목 - 실제 시안 이름 반영
    # 현재 내용: 매체 / 형태 / 시기 / 시안 테이블
    # 시안 칼럼을 실제 head copy 코드로 교체 (A-1, A-2 등)
    P42_NEW = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:Press & Media-->

**매체별 시안 배치**

| 매체 | 형태 | 시기 | 게재 시안 |
|------|------|------|-----------|
| 부산일보 | 15단 전면 | 수시 원서 접수 전 (6월) | C-3 · 신라가, 롯데가, 하얏트가 |
| 국제신문 | 5단 통 | 정시 전 (12월) | A-1 · 산업이 먼저 선택한 대학 |
| 대학저널 | 1/2면 | 연 2회 | A/B/C 시안 종합 |
| 네이버 메인 배너 | DA | 수시 기간 집중 | B-1 · 한국 3위가 아니라 세계 55위 |
| 교육 전문 매체 | 기사형 광고 | 분기 1회 | B-2 · 서울 기준 시대는 끝났다 |

인쇄 매체는 **C-3 시안**의 시각적 충격 극대화
디지털 배너는 **A-1** 카피 기반 클릭 유도형 적용
"""
    conn.execute("UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=40", (P42_NEW, PID))
    print("[6] P42 매체별 시안 배치 - 실제 시안 코드로 교체")

    # 7) P43 (기존 idx=42 → 시프트 후 idx=41) 영역 칼럼 넓이 조정
    r = conn.execute("SELECT content FROM sections WHERE proposal_id=? AND order_idx=41", (PID,)).fetchone()
    c = r[0]
    # 영역 140px → 180px, 세부항목 240px → 240px 유지
    # 내용 칼럼 (2번째 td) 좁히기
    c = c.replace(
        'width:140px;white-space:nowrap">영역',
        'width:200px;white-space:nowrap">영역'
    )
    conn.execute("UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=41", (c, PID))
    print("[7] P43 영역 칼럼 140px → 200px (자문 · 컨설팅 한 줄 유지)")

    # 8) P46 (기존 idx=45 → 시프트 후 idx=44) 제목 '1.25억의 가치 더 높이겠습니다'
    r = conn.execute("SELECT content FROM sections WHERE proposal_id=? AND order_idx=44", (PID,)).fetchone()
    c = r[0]
    c = c.replace("1.25억 효율 증대", "1.25억의 가치 더 높이겠습니다")
    c = c.replace("1억 2천 5백만 원의 가치", "1.25억의 가치 더 높이겠습니다")
    conn.execute("UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=44", (c, PID))
    print("[8] P46 1.25억의 가치 더 높이겠습니다")

    # 9) P48 (기존 idx=47 → 시프트 후 idx=46) 삭제 -- 원래 3계층 측정
    # 주의: P48 이었는데 시프트로 idx 변경. dom=47 이었던 P48 = idx=46 현재
    conn.execute("DELETE FROM sections WHERE proposal_id=? AND order_idx=46", (PID,))
    rows = conn.execute(
        "SELECT id, order_idx FROM sections WHERE proposal_id=? AND order_idx > 46 ORDER BY order_idx ASC",
        (PID,),
    ).fetchall()
    for rid, oi in rows:
        conn.execute("UPDATE sections SET order_idx=? WHERE id=?", (oi - 1, rid))
    print(f"[9] P48 삭제 + {len(rows)}개 -1 시프트")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
