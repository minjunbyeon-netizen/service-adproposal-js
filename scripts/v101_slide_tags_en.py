# -*- coding: utf-8 -*-
"""V101 - 모든 슬라이드에 영어 slide_tag 일괄 적용 (RFP 목차 기반)."""
import sqlite3
import re
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


# idx → (title키워드/parent 기반) 영어 태그 매핑
TAG_MAP = {
    # Ⅰ. 제안개요 (Overview)
    1: "Evaluation Axis",           # P2 평가 2축
    2: "Market Status",              # P3 시장 현황
    3: "Competitive Map",            # P4 경쟁 지도
    4: "About Youngsan",             # P5 영산대는?
    5: "Hospitality Specialty",      # P6 호텔관광 특성화
    6: "Serial No. 0825503",         # P7 0825503
    7: "Memory Challenge",           # P8 기억나십니까?
    8: "Core Imprint",               # P9 각인 = 전부

    # Ⅱ. 제안업체 일반
    9: "Company Profile",            # P10 제안업체 일반 하이브미디어

    # Ⅲ. 세부 과업 수행 계획 (Detailed Execution) - 디바이더 idx=10은 level=1이므로 제외

    11: "To Imprint",                # P12 기억시켜야 할 것
    12: "Ad Sample",                 # P13 영산대 광고 시안
    13: "Memory Test",               # P14 기억이 될까요?
    14: "Why Forgotten",             # P15 왜 기억되지 않는가
    15: "Reframing",                 # P16 숫자를 기억으로
    16: "The One Page",              # P17 한 장
    17: "Reframing #01",             # P18 사례 1
    18: "Reframing #01",             # P19
    19: "Reframing #01",             # P20
    20: "Reframing #02",             # P21
    21: "Reframing #02",             # P22
    22: "Reframing #02",             # P23
    23: "Reframing #03",             # P24
    24: "Reframing #03",             # P25
    25: "Reframing #03",             # P26

    # Divider idx=26 now is the 이제 실전입니다 (after P26 deleted, need to check)
    # Continue with content indexes
    26: "Transition",                # what was P26 video

    # Ⅳ. 사업 관리 계획
    27: "Execution Plan",            # Executive Summary
    # idx=28 is divider 이제 실전입니다? Let me not hardcode

    # 실전 파트
    28: "Expansion Overview",        # 확장 개요
    29: "Media Strategy",            # 매체 전략
    30: "YouTube Content",           # 인플루언서
    31: "Print Ad",                  # 인쇄 매체
    32: "Digital Ad",                # 디지털 매체 1
    33: "Digital Ad",                # 디지털 매체 2
    34: "Short Form",                # 숏폼
    35: "Official Video",            # 공식 홍보영상
    36: "SNS Operation",             # SNS
    37: "Media & Banner",            # 언론
    38: "Consulting",                # 자문 컨설팅

    # Ⅳ. 사업 관리 계획
    39: "Budget Timeline",           # 일정 계획
    40: "Budget Allocation",         # 매체별 예산
    41: "Cost Efficiency",           # 비용 효율
    42: "Monthly Execution",         # 월별 집행
    43: "3-Tier Measurement",        # 3계층 측정
    44: "Ongoing Report",            # 상시 보고
    45: "Risk Response",             # 리스크 대응

    # Epilogue (마지막 콘텐츠, 감사합니다 전)
    46: "",                          # 수미상관 - 태그 없음
}


def main():
    conn = sqlite3.connect(str(DB))

    rows = conn.execute(
        "SELECT id, order_idx, level, content FROM sections WHERE proposal_id=? ORDER BY order_idx",
        (PID,),
    ).fetchall()

    updated = 0
    skipped = 0
    for rid, idx, level, content in rows:
        if level == 1:
            skipped += 1
            continue
        if not content:
            continue

        new_tag = TAG_MAP.get(idx)
        if new_tag is None:
            # Map에 없으면 건너뛰기 (확실하지 않은 idx는 수동)
            continue

        # 기존 <!--TAG:...--> 제거 후 새 태그 삽입
        new_content = re.sub(r'<!--TAG:[^>]*?-->', '', content)

        if new_tag:  # 빈 문자열이면 TAG 자체 제거
            # PARENT 뒤에 새 TAG 삽입
            if '<!--PARENT:' in new_content:
                new_content = re.sub(
                    r'(<!--PARENT:[^>]*?-->)',
                    r'\1<!--TAG:' + new_tag + '-->',
                    new_content,
                    count=1,
                )
            else:
                new_content = f'<!--TAG:{new_tag}-->' + new_content

        if new_content != content:
            conn.execute("UPDATE sections SET content=? WHERE id=?", (new_content, rid))
            updated += 1

    conn.commit()
    conn.close()
    print(f"업데이트 {updated}개, 디바이더 제외 {skipped}개")


if __name__ == "__main__":
    main()
