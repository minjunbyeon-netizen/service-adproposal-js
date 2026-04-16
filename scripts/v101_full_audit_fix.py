# -*- coding: utf-8 -*-
"""V101 전체 점검 - 한글 태그 -> 영어 + P16 오버레이 제거."""
import sqlite3
import re
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


KOR_TO_EN = {
    "숫자를 기억으로": "Reframing",
    "사례 1-1": "Reframing #01",
    "사례 1-2": "Reframing #01",
    "사례 1-3": "Reframing #01",
    "사례 2-1": "Reframing #02",
    "사례 2-2": "Reframing #02",
    "사례 2-3": "Reframing #02",
    "사례 3-1": "Reframing #03",
    "사례 3-2": "Reframing #03",
    "사례 3-3": "Reframing #03",
    "확장 개요": "Expansion Overview",
    "매체 전략": "Media Strategy",
    "인플루언서": "Influencer",
    "인쇄 매체": "Print Media",
    "디지털 매체 (1)": "Digital Media I",
    "디지털 매체 (2)": "Digital Media II",
    "숏폼 기획": "Short Form",
    "공식 홍보영상": "Official Video",
    "소셜 미디어": "SNS Operation",
    "언론 매체": "Press & Media",
    "Ⅲ-2 사업 관리 계획": "Management Plan",
    "일정 계획": "Timeline",
    "매체별 예산": "Budget Allocation",
    "비용 효율": "Cost Efficiency",
    "월별 집행": "Monthly Execution",
    "3계층 측정": "3-Tier Measurement",
    "상시 보고": "Ongoing Report",
    "리스크 대응": "Risk Response",
    "수미상관": "Bookend",
    "클로징": "Closing",
    "0825503 해독": "Serial No. 0825503",
}


def main():
    conn = sqlite3.connect(str(DB))
    rows = conn.execute(
        "SELECT id, order_idx, level, content FROM sections WHERE proposal_id=? ORDER BY order_idx",
        (PID,),
    ).fetchall()

    tag_fixed = 0
    for rid, idx, level, content in rows:
        if level == 1 or not content:
            continue
        new = content
        for ko, en in KOR_TO_EN.items():
            new = new.replace(f"<!--TAG:{ko}-->", f"<!--TAG:{en}-->")
        if new != content:
            conn.execute("UPDATE sections SET content=? WHERE id=?", (new, rid))
            tag_fixed += 1

    print(f"한글 -> 영어 태그 변환: {tag_fixed}개")

    # P16 (3가지 숫자 서브스텝) - 오버레이 제거하여 헤더 표시되게 수정
    r = conn.execute(
        "SELECT content FROM sections WHERE proposal_id=? AND order_idx=15",
        (PID,),
    ).fetchone()
    if r:
        c = r[0]
        # position:absolute;top:0;left:0;right:0;bottom:0;...z-index:5 -> 일반 레이아웃
        c = c.replace(
            'position:absolute;top:0;left:0;right:0;bottom:0;background:#fff;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0;z-index:5',
            'height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0'
        )
        conn.execute("UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=15", (c, PID))
        print("P16 (3가지 숫자) 오버레이 제거 - 헤더/태그/오렌지 바 표시")

    # P7 (0825503 morph) 이미 표준 레이아웃임 -- skip

    conn.commit()
    conn.close()
    print("완료")


if __name__ == "__main__":
    main()
