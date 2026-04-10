"""V18-1/V18-2/V18-3: 과업지시서 준수 + 시안 이미지그리드 + 영상 스토리보드 2장.

총 23장: 표지 + 20 content + 간지1 + 마무리
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.db import get_conn, init_db, migrate_db
from scripts.create_v8_to_v14 import (
    RFP, SUMMARY, CONCEPTS, concept_A, concept_B, concept_C,
)

init_db()
migrate_db()


def grid16x9(label, prompt):
    return (
        f'<div class="img-grid ratio-16-9">'
        f'<span class="grid-label">{label} -- 16:9</span>'
        f'<div class="grid-placeholder">이미지를 클릭하여 교체<br>{prompt}</div>'
        f'</div>'
    )

def grid9x16(label, prompt):
    return (
        f'<div class="img-grid ratio-9-16">'
        f'<span class="grid-label">{label} -- 9:16</span>'
        f'<div class="grid-placeholder">이미지를 클릭하여 교체<br>{prompt}</div>'
        f'</div>'
    )

def sian_slide(cc, label, desc, prompt_16, prompt_9):
    return (
        f"**{cc}**\n\n"
        f"{desc}\n\n"
        f'{grid16x9(label, prompt_16)}\n\n'
        f'{grid9x16(label + " (숏폼)", prompt_9)}\n\n'
        f'<div class="img-prompt"><span class="prompt-label">AI PROMPT</span>\n'
        f'<div class="prompt-cmd">{prompt_16}</div></div>'
    )

# ===== 스토리보드 프레임 =====
def sb_frame(time, scene, desc, audio=""):
    a = f'<div class="sb-audio">{audio}</div>' if audio else ''
    return (
        f'<div class="sb-frame">'
        f'<div class="sb-img">{scene}</div>'
        f'<div class="sb-time">{time}</div>'
        f'<div class="sb-desc">{desc}</div>{a}</div>'
    )

S_OVERVIEW = (
    "### I. 제안개요\n\n"
    "| 항목 | 내용 |\n|------|------|\n"
    "| 사업명 | 2026~2027학년도 영산대학교 광고대행사 선정 |\n"
    "| 발주처 | 영산대학교 (와이즈유) |\n"
    "| 사업기간 | 2년 (2026~2027학년도) |\n"
    "| 예산 | 연 1.25억 (2년 총 2.5억, VAT 별도) |\n"
    "| 제출기한 | 2026-04-20 17:00 |\n"
    "| 제안업체 | (주)하이브미디어 |"
)

S_COMPANY = (
    "### II. 제안업체 일반\n\n"
    "| 항목 | 내용 |\n|------|------|\n"
    "| 상호 | (주)하이브미디어 | 설립 2018 | 대표 변민준 |\n"
    "| 소재지 | 부산 해운대구 | 임직원 12명 | 연매출 8.2억(2025) |\n\n"
    "**투입 인력:** 총괄PM + 크리에이티브(3) + 매체(2) + 영상PD(3) + AE(2)\n\n"
    "**주요 실적:** 부산 강서구청 광고대행(연1.5억), OO대학교 입시홍보(8천만), 부산관광공사 영상(5천만)\n\n"
    "*조직도, 재무현황, 투입인력 상세는 별도 보고서를 참고해 주십시오.*"
)

S_QUESTION = (
    "**이 숫자의 학교 이름을 아십니까?**\n\n"
    "| | |\n|---|---|\n"
    "| QS 호스피탈리티 | **세계 55위** |\n| 연구력 | **세계 8위** |\n"
    "| 호텔 총지배인 | **25명 (국내 최다)** |\n| WACS 심사위원 | **4명 중 3명** |\n"
    "| 부울경 사립대 취업률 | **1위** |"
)

S_TRANSITION = (
    "**영산대학교입니다.**\n\n"
    "이 팩트를 처음 들으셨다면, 그것이 문제입니다.\n\n"
    "지금까지의 광고는 정보 전달형이었습니다.\n"
    "이제는 직접 느낄 수 있는 IMPACT가 필요합니다.\n\n"
    "같은 숫자. 다른 방식.\n"
    "그래서 이렇게 준비했습니다."
)

# 영상 스토리보드 2장
S_VIDEO_1 = (
    "### a. 대학 공식 홍보영상 -- 스토리보드 (1/2)\n\n"
    "**메인 영상 60초 + 학부모 영상 90초**\n\n"
    "#### 메인 영상 (60초)\n\n"
    '<div class="storyboard">'
    + sb_frame("0-5초", "캠퍼스 전경 (해운대)", "오프닝. 텍스트만 등장.", "차분한 피아노")
    + sb_frame("5-18초", "항공사 채용담당자 인터뷰", "\"처음엔 영산대를 크게 신경 쓰지 않았어요.\"", "배경음 유지")
    + sb_frame("18-32초", "졸업생 유니폼 + 담당자", "\"3년간 중도탈락 0명. 다른 학교는 10-15%.\"", "현악 추가")
    + sb_frame("32-44초", "뷰티회사 대표 인터뷰", "\"시간 약속, 책임감이 달라요.\"", "")
    + sb_frame("44-54초", "경찰청 담당자 인터뷰", "\"영산대 출신이면 신뢰합니다.\"", "")
    + sb_frame("54-60초", "3분할 화면 + 브랜드", "무음. 영산대학교 와이즈유.", "풀 사운드 페이드아웃")
    + '</div>'
)

S_VIDEO_2 = (
    "### a. 대학 공식 홍보영상 -- 스토리보드 (2/2)\n\n"
    "#### 숏폼 3종 (각 15초, 9:16)\n\n"
    '<div class="storyboard">'
    + sb_frame("3.6% 편", "숫자 타이포 모션", "0-2초 후킹 -> 반전 증거 -> 브랜드", "")
    + sb_frame("심사위원석 편", "심사위원석 클로즈업", "0-2초 후킹 -> 4석 중 3석 -> 브랜드", "")
    + sb_frame("Room 1201 편", "복도 원테이크", "0-2초 후킹 -> 25명 -> 브랜드", "")
    + '</div>\n\n'
    "#### 학부모 영상 (90초)\n\n"
    '<div class="storyboard">'
    + sb_frame("0-8초", "학부모 거실 인터뷰", "\"처음엔 영산대? 라는 생각이...\"", "따뜻한 피아노")
    + sb_frame("8-35초", "캠퍼스 + 학생 인터뷰", "\"입학 후 1학기, 아이가 달라 보였어요.\"", "")
    + sb_frame("35-78초", "학부모+자녀 함께", "\"시간 약속, 과제 태도, 현장 실습이 달라요.\"", "")
    + sb_frame("78-90초", "학부모 클로즈업 + 브랜드", "\"이 학교를 선택해서 잘했다.\"", "페이드아웃")
    + '</div>'
)

S_YOUTUBE = (
    "### b. 유튜브 콘텐츠 (인플루언서 협업)\n\n"
    "**\"1학년 vs 졸업생\" 스토리텔링 활용**\n\n"
    "| 콘텐츠 | 형식 | 핵심 |\n|--------|------|------|\n"
    "| 졸업생 하루 브이로그 | 10분 | 호텔/항공/경찰 현장 밀착 |\n"
    "| 1학년 vs 졸업생 대담 | 8분 | 같은 사람, 4년의 차이 |\n"
    "| 교수 인터뷰 | 5분 | WACS 심사위원 교수 일상 |\n"
    "| 캠퍼스 투어 | 7분 | 해운대 캠퍼스 |\n\n"
    "**인플루언서:** 교육/진로 유튜버 '숨은 명문대' 시리즈."
)

S_PRINT = (
    "### c. 대학 광고 디자인 및 인쇄 제작\n\n"
    "**핵심 시안: \"3.6%\" -- 팩트+임팩트 최강**\n\n"
    "| 매체 | 시안 | 사양 |\n|------|------|------|\n"
    "| 버스쉘터 | 3.6% | 1200x1800mm 양면 |\n"
    "| 지하철 역사 | 3.6% | 2400x1200mm |\n"
    "| 대학 내 현수막 | 3.6%+슬로건 | 900x2400mm |\n"
    "| 입시요강 표지 | 3.6% 변형 | A4 |\n"
    "| 리플렛 | 4종 종합 | 3단 접지 |"
)

S_DIGITAL = (
    "### d. 디지털 광고 콘텐츠 제작\n\n"
    "**실험적 다품종: \"심사위원석\" + \"Room 1201\"**\n\n"
    "| 플랫폼 | 시안 | 형식 |\n|--------|------|------|\n"
    "| 유튜브 프리롤 | 심사위원석 | 15초 영상 |\n"
    "| 유튜브 프리롤 | Room 1201 | 15초 영상 |\n"
    "| 인스타 피드 | 3.6% | 정방형 |\n"
    "| 인스타 스토리 | 1학년vs졸업생 | 세로 영상 |\n"
    "| 페이스북 | 4종 캐러셀 | 스와이프 |\n"
    "| 네이버 DA | 3.6% 변형 | 배너 |\n\n"
    "2주 단위 A/B 테스트 -> 상위 시안 예산 집중."
)

S_SNS = (
    "### e. SNS 이벤트 및 콘텐츠 활성화\n\n"
    "| 월 | 테마 | 콘텐츠 | 이벤트 |\n|---|------|--------|--------|\n"
    "| 3~4월 | 입학 | 1학년 첫날 | 인증샷 |\n"
    "| 5~7월 | 수시 집중 | 취업률 팩트 | 캠퍼스 투어 |\n"
    "| 8~9월 | 원서 | 졸업생 인터뷰 | 댓글 이벤트 |\n"
    "| 10~12월 | 정시 | QS 순위 정리 | 상담 라이브 |\n"
    "| 1~2월 | 합격 | 축하 콘텐츠 | 멘토링 |\n\n"
    "인스타/유튜브/블로그 3채널. 주 3회 포스팅."
)

S_PRESS = (
    "### f. 언론 지면 및 배너광고\n\n"
    "| 매체 | 형태 | 시기 | 시안 |\n|------|------|------|------|\n"
    "| 부산일보 | 15단 전면 | 6월 수시 전 | 3.6% |\n"
    "| 국제신문 | 5단 통 | 12월 정시 전 | 슬로건 |\n"
    "| 대학저널 | 1/2면 | 연 2회 | 4종 종합 |\n"
    "| 네이버 메인 | DA 배너 | 수시 집중 | 심사위원석 |"
)

S_CONSULT = (
    "### III-2. 사업 관리\n\n"
    "**학과 홍보 자문 및 컨설팅**\n"
    "- 학과별 차별화 포인트 발굴 (월 1회 정기 미팅)\n"
    "- 입시 홍보물 카피/디자인 컨설팅\n\n"
    "**광고 효과 측정 및 경과 분석**\n"
    "- 매체별 노출/클릭/전환 대시보드 (월 2회)\n"
    "- 분기별 종합 리포트 + 전략 수정안\n\n"
    "**본교 요구 업무**\n"
    "- 긴급 제작물 48시간 내 납품\n"
    "- 학교 행사 현장 촬영 지원"
)

S_GANTT = (
    "### IV-1. 광고 운영 및 예산 집행 계획\n\n"
    "**2년 간트차트 (수시 5,6,7월 집중)**\n\n"
    "| 월 | 2026 | 2027 | 예산 |\n|---|------|------|------|\n"
    "| 1-2월 | 기획/합격 콘텐츠 | Year2 수립/합격 | |\n"
    "| 3-4월 | 시안 제작/촬영/옥외 | 시안 리뉴얼 | |\n"
    "| **5월** | **수시 집중 -- 전매체** | **수시 집중** | **25%** |\n"
    "| **6월** | **원서 접수 -- 검색+SNS 최대** | **원서 접수** | **25%** |\n"
    "| **7월** | **수시 마감 -- 리타겟팅** | **수시 마감** | **20%** |\n"
    "| 8-10월 | 성과 분석/정시 대비 | 성과 분석 | |\n"
    "| 11-12월 | 정시 집중/연간 결산 | 정시/결산 | **15%+15%** |"
)

S_FEEDBACK = (
    "### IV-2. 광고 결과 분석 및 피드백\n\n"
    "| 지표 | 주기 | 도구 |\n|------|------|------|\n"
    "| 노출/클릭률 | 주간 | GA, Meta |\n"
    "| 영상 조회/완시청 | 주간 | YouTube Studio |\n"
    "| SNS 인게이지먼트 | 월간 | 인사이트 |\n"
    "| 입시 홈페이지 유입 | 월간 | GA4 |\n"
    "| 지원자 수 | 분기 | 입학처 |\n\n"
    "2주 A/B 테스트 -> 상위 시안 집중 -> 분기 수정."
)

S_ETC = (
    "### IV-3. 기타 제안 -- 홍보단 운영\n\n"
    "| 항목 | 내용 |\n|------|------|\n"
    "| 인원 | 학과별 2~3명, 총 20명 |\n"
    "| 활동 | 캠퍼스 브이로그, SNS, 입시설명회 서포터즈 |\n"
    "| 교육 | 월 1회 워크숍 (하이브미디어 진행) |\n"
    "| 혜택 | 포트폴리오 지원, 우수자 인턴십 |\n"
    "| 관리 | AE 주간 피드백, 월간 우수작 선정 |\n\n"
    "진짜 학생이 만든 진짜 콘텐츠로 신뢰도 확보."
)


def make_sections(cc, tl, cb, sb):
    combined = f"**컨셉:** {cc}\n\n{cb}\n\n---\n\n**슬로건:** {tl}\n\n{sb}"
    return [
        (2, "I. 제안개요", 1, S_OVERVIEW),
        (2, "II. 제안업체 일반", 2, S_COMPANY),
        (1, "III. 세부 과업 수행 계획", 3, None),
        (2, '"3.6%"', 4, sian_slide(cc, "3.6%",
            "탈락률 3.6%. 영산대 항공서비스학과.",
            "Airport gate, '3.6%' large white typography center, cinematic, 16:9, no people",
            "Airport gate vertical, '3.6%' typography, 9:16 mobile format")),
        (2, "질문", 5, S_QUESTION),
        (2, "전환", 6, S_TRANSITION),
        (2, "컨셉 / 슬로건", 7, combined),
        (2, '"심사위원석"', 8, sian_slide(cc, "심사위원석",
            "WACS 심사위원 4석 중 3석. 영산대 교수.",
            "Judging panel dark auditorium, four chairs, three spotlights, WACS nameplate, symmetrical, 16:9",
            "Judging panel vertical crop, spotlight on three chairs, 9:16")),
        (2, '"Room 1201"', 9, sian_slide(cc, "Room 1201",
            "호텔 복도 25개의 문. 전부 총지배인.",
            "Luxury hotel corridor, 25 doors, warm lighting, one-point perspective, 16:9",
            "Hotel corridor vertical, doors stretching upward, 9:16")),
        (2, '"1학년 vs 졸업생"', 10, sian_slide(cc, "1학년 vs 졸업생",
            "입학 -> 졸업. 같은 사람. 4년의 차이.",
            "Split screen, left campus blue, right hotel warm, vertical divide, 16:9",
            "Split screen vertical, top freshman bottom graduate, 9:16")),
        (2, "a. 홍보영상 (1/2)", 11, S_VIDEO_1),
        (2, "a. 홍보영상 (2/2)", 12, S_VIDEO_2),
        (2, "b. 유튜브 콘텐츠", 13, S_YOUTUBE),
        (2, "c. 광고 디자인/인쇄", 14, S_PRINT),
        (2, "d. 디지털 광고", 15, S_DIGITAL),
        (2, "e. SNS 이벤트", 16, S_SNS),
        (2, "f. 언론 지면/배너", 17, S_PRESS),
        (2, "사업 관리", 18, S_CONSULT),
        (2, "IV-a. 예산 집행 (간트)", 19, S_GANTT),
        (2, "IV-b. 결과 분석", 20, S_FEEDBACK),
        (2, "IV-c. 홍보단 운영", 21, S_ETC),
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


if __name__ == "__main__":
    # 기존 V18 삭제
    conn = get_conn()
    conn.execute("DELETE FROM proposals WHERE version LIKE 'V18%'")
    conn.commit()

    for title, ver, label, cc, tl, cfn in [
        ("V18-1: 이름을 가려봐", "V18-1", "A", "이름을 가려봐.", "이름을 가려도 보이는 대학.", concept_A),
        ("V18-2: 같은 학교", "V18-2", "B", "같은 학교.", "같은 학교. 영산대학교.", concept_B),
        ("V18-3: 배우가 아닙니다", "V18-3", "C", "이 사람은 배우가 아닙니다.", "이 사람은 배우가 아닙니다.", concept_C),
    ]:
        cb, sb_body = cfn()
        pid = create(conn, title, ver, label, make_sections(cc, tl, cb, sb_body))
        print(f"{ver}: id={pid}")

    conn.commit()
    conn.close()
    print("Done.")
