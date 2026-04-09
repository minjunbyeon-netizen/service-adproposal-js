"""V17-1/V17-2/V17-3: 과업지시서 목차 형식 준수 (I~IV 구조).

표지 -> I.제안개요(1장) -> II.제안업체일반(1장) -> III.세부과업수행계획(기존) -> IV.사업관리계획 -> 마무리
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.db import get_conn, init_db, migrate_db
from scripts.create_v8_to_v14 import (
    RFP, SUMMARY, CONCEPTS,
    concept_A, concept_B, concept_C,
    img_36, img_jg, img_rm, img_sp,
    BUDGET,
)

init_db()
migrate_db()

# ===== I. 제안개요 (1장) =====
SLIDE_OVERVIEW = (
    "### I. 제안개요\n\n"
    "| 항목 | 내용 |\n"
    "|------|------|\n"
    "| 사업명 | 2026~2027학년도 영산대학교 광고대행사 선정 |\n"
    "| 발주처 | 영산대학교 (와이즈유) |\n"
    "| 사업기간 | 2년 (2026~2027학년도) |\n"
    "| 예산 | 연 1.25억 (2년 총 2.5억, VAT 별도) |\n"
    "| 제출기한 | 2026-04-20 17:00 |\n"
    "| 제안업체 | (주)하이브미디어 |\n\n"
    "본 제안서는 영산대학교 광고대행사 선정을 위한 "
    "크리에이티브 시안, 매체 전략, 캠페인 기획, 영상 제작 계획을 포함합니다."
)

# ===== II. 제안업체 일반 (1장) =====
SLIDE_COMPANY_BRIEF = (
    "### II. 제안업체 일반\n\n"
    "| 항목 | 내용 |\n"
    "|------|------|\n"
    "| 상호 | (주)하이브미디어 |\n"
    "| 설립 | 2018년 3월 |\n"
    "| 대표 | 변민준 |\n"
    "| 소재지 | 부산광역시 해운대구 |\n"
    "| 임직원 | 12명 |\n"
    "| 주요 사업 | 종합 광고대행 (기획/크리에이티브/매체/영상/디지털) |\n"
    "| 연매출 | 8.2억 (2025) |\n\n"
    "**주요 실적:** 부산 강서구청 광고대행(2024~), OO대학교 입시 홍보(2024), "
    "부산관광공사 영상 제작(2023)\n\n"
    "*조직도, 재무현황, 투입 인력 상세는 별도 보고서를 참고해 주십시오.*"
)

# ===== IV. 사업 관리 계획 (1장) =====
SLIDE_MGMT = (
    "### IV. 사업 관리 계획\n\n"
    "**1. 광고 운영 및 예산 집행 계획**\n\n"
    "| 구분 | 내용 |\n"
    "|------|------|\n"
    "| 월간 | 매체 집행 현황, 노출/클릭/전환 리포트 |\n"
    "| 분기 | 캠페인 성과 분석, 전략 수정안, 다음 분기 계획 |\n"
    "| 연간 | 연간 종합 보고, Year 2 전략 수립 |\n\n"
    "**2. 광고 결과 분석 및 피드백 적용**\n"
    "- 매체별 성과 데이터 대시보드 제공 (월 2회 갱신)\n"
    "- A/B 테스트 기반 시안 최적화\n"
    "- 입시 시즌(9~12월) 집중 모니터링 체제\n\n"
    "**3. 기타 제안 사항**\n"
    "- 학과 홍보 자문 및 컨설팅 상시 지원\n"
    "- 본교 요구 시 긴급 제작물 48시간 내 납품\n"
    "- 광고 효과 측정 결과를 차년도 전략에 반영"
)


def make_v17_sections(cc, tl, concept_body, slogan_body):
    """V17 구조: I.제안개요 + II.제안업체 + III.세부과업(기존) + IV.사업관리."""
    return [
        # I. 제안개요
        (2, "I. 제안개요", 1, SLIDE_OVERVIEW),
        # II. 제안업체 일반
        (2, "II. 제안업체 일반", 2, SLIDE_COMPANY_BRIEF),
        # III. 세부 과업 수행 계획 (기존 V14 구조)
        (2, '"3.6%"', 3, img_36(cc, tl)),
        (2, "질문", 4,
         "**이 숫자의 학교 이름을 아십니까?**\n\n"
         "| | |\n|---|---|\n| QS 호스피탈리티 | **55위** |\n| 연구력 | **8위** |\n"
         "| 호텔 총지배인 | **25명** |\n| WACS 심사위원 | **4명 중 3명** |"),
        (2, "진단", 5,
         "**영산대학교입니다.**\n\n"
         "팩트를 처음 들으셨다면, 그것이 문제입니다.\n"
         "숫자는 있었습니다. 광고가 없었습니다.\n\n"
         "우리는 뻔한 이야기를 하지 않겠습니다.\n"
         "팩트를 느끼게 만들겠습니다."),
        (2, "컨셉", 6, concept_body),
        (2, "슬로건", 7, slogan_body),
        (2, '"심사위원석"', 8, f"**{cc}**\n\n" + img_jg(cc, tl)),
        (2, '"Room 1201"', 9, f"**{cc}**\n\n" + img_rm(cc, tl)),
        (2, '"1학년 vs 졸업생"', 10, f"**{cc}**\n\n" + img_sp(cc, tl)),
        (2, "영상", 11,
         "**메인 60초 + 숏폼 3종 + 학부모 90초**\n\n"
         f"### 메인 (60초)\n'{cc}' 톤. 4종 시안 옴니버스. 실제 졸업생 출연.\n\n"
         "### 숏폼 3종 (각 15초)\n- 3.6% 편 / 심사위원석 편 / Room 1201 편\n\n"
         "### 학부모 (90초)\n학부모 시점 다큐. 입학->수업->실습->취업."),
        (2, "캠페인", 12,
         "**2년 연속 캠페인**\n\n"
         "### 1단계 (2026 상반기)\n4종 시안 동시. 버스쉘터, 지하철, 유튜브.\n\n"
         "### 2단계 (2026 하반기)\n팩트 검증. SNS, 검색광고.\n\n"
         "### 3단계 (2027)\n브랜드 고정. 졸업생 인터뷰 시리즈."),
        (2, "매체/예산", 13, BUDGET),
        # IV. 사업 관리 계획
        (2, "IV. 사업 관리 계획", 14, SLIDE_MGMT),
    ]


def create(conn, title, version, label, sections):
    cur = conn.execute(
        "INSERT INTO proposals (title,version,status,rfp_json,rfp_summary,raw_text,selected_concept) VALUES (?,?,?,?,?,?,?)",
        (title, version, "ready", RFP, SUMMARY, SUMMARY, label))
    pid = cur.lastrowid
    for lv, t, idx, content in sections:
        conn.execute(
            "INSERT INTO sections (proposal_id,level,title,order_idx,content,status) VALUES (?,?,?,?,?,?)",
            (pid, lv, t, idx, content, "done" if content else "pending"))
    for lb, ct, bd in CONCEPTS:
        conn.execute(
            "INSERT OR REPLACE INTO concepts (proposal_id,label,title,body) VALUES (?,?,?,?)",
            (pid, lb, ct, bd))
    return pid


conn = get_conn()
for title, ver, label, cc, tl, cfn in [
    ("V17-1: 이름을 가려봐", "V17-1", "A", "이름을 가려봐.", "이름을 가려도 보이는 대학.", concept_A),
    ("V17-2: 같은 학교", "V17-2", "B", "같은 학교.", "같은 학교. 영산대학교.", concept_B),
    ("V17-3: 이 사람은 배우가 아닙니다", "V17-3", "C", "이 사람은 배우가 아닙니다.", "이 사람은 배우가 아닙니다.", concept_C),
]:
    cb, sb = cfn()
    pid = create(conn, title, ver, label, make_v17_sections(cc, tl, cb, sb))
    print(f"{ver}: id={pid}")

conn.commit()
conn.close()
print("Done.")
