"""V20: 제안배경(포지셔닝 선점) + 숫자 타이포 + "지혜" 영상 + 운영방안."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.db import get_conn, init_db, migrate_db
from scripts.create_v8_to_v14 import RFP, SUMMARY, CONCEPTS, concept_A
from scripts.create_v18 import (
    grid16x9, grid9x16, sian_slide, sb_frame,
    S_YOUTUBE, S_PRINT, S_DIGITAL, S_SNS, S_PRESS, S_CONSULT,
    S_FEEDBACK, S_ETC,
)
from scripts.create_v19 import S_GANTT

init_db()
migrate_db()

# ===== #2 제안배경 =====
S_BACKGROUND = (
    "### I. 제안배경\n\n"
    "대한민국의 대학에는 각자의 **=** 이 있습니다.\n\n"
    "| 대학 | 포지셔닝 |\n|------|----------|\n"
    "| 홍익대 | = **미대** |\n"
    "| 한양대 에리카 | = **공대** |\n"
    "| 동의대 | = **한의대** |\n"
    "| 중앙대 | = **연극영화** |\n"
    "| 경희대 | = **호텔관광** |\n"
    "| **영산대** | = **?** |\n\n"
    "영산대학교는 이미 충분한 실적을 가지고 있습니다.\n"
    "QS 55위, 취업률 96.4%, 호텔 총지배인 25명.\n\n"
    "하지만 '영산대 하면 OO'이라는 한 줄이 아직 없습니다.\n"
    "이름은 알릴 대로 알렸습니다.\n"
    "이제 필요한 것은 **포지셔닝**입니다.\n\n"
    "지금은 선점의 시대입니다.\n"
    "한 번 잡히면 바꿀 수 없는 것이 대학의 이미지입니다.\n\n"
    "**우리가 이것을 선점하겠습니다.**"
)

# ===== #3 제안업체 =====
S_COMPANY = (
    "### II. 제안업체 일반\n\n"
    "| 항목 | 내용 |\n|------|------|\n"
    "| 상호 | (주)하이브미디어 | 설립 2018 | 대표 변민준 |\n"
    "| 소재지 | 부산 해운대구 | 임직원 12명 | 연매출 8.2억(2025) |\n\n"
    "**투입 인력:** 총괄PM + 크리에이티브(3) + 매체(2) + 영상PD(3) + AE(2)\n\n"
    "**주요 실적:** 부산 강서구청 광고대행(연1.5억), OO대학교 입시홍보(8천만), 부산관광공사 영상(5천만)\n\n"
    "*조직도, 재무현황, 투입인력 상세는 별도 보고서를 참고해 주십시오.*"
)

# ===== #5 숫자 타이포 =====
S_NUMBERS = (
    '<div style="text-align:center;padding:40px 0">'
    '<div style="font-size:120px;font-weight:700;color:#E84E10;letter-spacing:8px;line-height:1">96</div>'
    '<div style="font-size:16px;color:#58595B;margin-bottom:40px">항공서비스 취업률 96.4%</div>'
    '<div style="font-size:120px;font-weight:700;color:#1A1A1A;letter-spacing:8px;line-height:1">55</div>'
    '<div style="font-size:16px;color:#58595B;margin-bottom:40px">QS 호스피탈리티 세계 55위</div>'
    '<div style="font-size:120px;font-weight:700;color:#E84E10;letter-spacing:8px;line-height:1">25</div>'
    '<div style="font-size:16px;color:#58595B">호텔 총지배인 25명 배출 (국내 최다)</div>'
    '</div>'
)

# ===== #6 전환 =====
S_TRANSITION = (
    "**영산대학교입니다.**\n\n"
    "이 숫자들을 처음 들으셨다면, 그것이 문제입니다.\n\n"
    "지금까지의 광고는 정보 전달형이었습니다.\n"
    "숫자를 나열하고, 슬로건을 붙이고, 캠퍼스 사진을 넣었습니다.\n\n"
    "이제는 직접 느낄 수 있는 IMPACT가 필요합니다."
)

# ===== #7 손실 회피 =====
S_LOSS = (
    "**사람은 얻는 것보다 잃는 것에 2배 강하게 반응합니다.**\n\n"
    "행동경제학에서 이것을 **손실 회피(Loss Aversion)**라고 합니다.\n\n"
    "> 취업률 96.4%\n\n"
    "이 숫자는 좋은 숫자입니다. 하지만 익숙합니다.\n"
    "모든 대학이 취업률을 자랑합니다.\n\n"
    "> 탈락률 3.6%\n\n"
    "같은 숫자입니다. 하지만 느낌이 다릅니다.\n"
    "'떨어질 확률이 3.6%밖에 안 된다고?'\n\n"
    "사람은 '96.4%가 성공한다'보다\n"
    "'3.6%만 실패한다'에 멈춥니다."
)

# ===== #8 신호와 소음 =====
S_COCKTAIL = (
    "**시끄러운 파티장에서도 내 이름은 들립니다.**\n\n"
    "심리학에서 이것을 **칵테일 파티 효과**라고 합니다.\n"
    "사람은 자신과 관련된 정보에만 반응합니다.\n\n"
    "수험생에게 '글로벌 경쟁력 강화'는 소음입니다.\n"
    "학부모에게 '브랜드 가치 제고'는 소음입니다.\n\n"
    "하지만,\n\n"
    "> \"이 학교 졸업생 100명 중 96명이 취업합니다.\"\n\n"
    "이것은 소음이 아닙니다.\n"
    "내 아이의 미래에 직결되는 신호입니다.\n\n"
    "**우리 광고는 소음이 아닌 신호를 만듭니다.**"
)

# ===== #13 "지혜" 메인 영상 60초 스토리보드 =====
S_JIHYE = (
    "### a. 대학 공식 홍보영상 -- \"지혜\" (60초)\n\n"
    "**컨셉:** 다른 현장, 다른 직업, 같은 이름. '지혜'는 이름이자 영산대의 가치.\n\n"
    '<div class="storyboard">'
    + sb_frame("0-3초", "[검은 화면]", "텍스트만: '지혜.'", "무음 -> 피아노 한 음")
    + sb_frame("3-15초", "[비행기 기내]",
               "승무원이 카트를 밀며 일하는 중.\n"
               "뒤에서 \"지혜야~\" 부른다.\n"
               "여자가 뒤돌아보며 웃고 걸어간다.",
               '"지혜야~"')
    + sb_frame("15-28초", "[호텔 회의실]",
               "회의 중인 고급 회의실.\n"
               "\"박지혜 지배인님!\" 부른다.\n"
               "같은 느낌으로 웃으며 걸어간다.",
               '"박지혜 지배인님!"')
    + sb_frame("28-40초", "[경찰서]",
               "사무실에서 서류 검토 중.\n"
               "\"지혜 경위!\" 부른다.\n"
               "같은 패턴으로 뒤돌아봄.",
               '"지혜 경위!"')
    + sb_frame("40-52초", "[뷰티 매장]",
               "고객 시술 중.\n"
               "\"지혜 선생님!\" 부른다.\n"
               "같은 패턴. 미소. 걸어감.",
               '"지혜 선생님!"')
    + sb_frame("52-60초", "[4분할 엔딩]",
               "네 명의 지혜가 동시에 뒤돌아본다.\n"
               "텍스트: \"우리는 모두 지혜입니다.\"\n"
               "영산대학교 로고.",
               '"우리는 모두 지혜입니다." -- 영산대학교')
    + '</div>'
)

# ===== #14 월간 졸업선배 다큐 =====
S_DOCU = (
    "### a. 월간 졸업선배 다큐 시리즈\n\n"
    "**매월 1편. 각 과 졸업생의 현장을 취재하는 다큐멘터리.**\n\n"
    "| 월 | 학과 | 졸업생 | 현장 | 러닝타임 |\n|---|------|--------|------|----------|\n"
    "| 4월 | 항공서비스 | 대한항공 승무원 | 기내+공항 | 30분 |\n"
    "| 5월 | 호텔관광 | 파라다이스호텔 지배인 | 호텔 현장 | 30분 |\n"
    "| 6월 | 경찰행정 | 해운대서 경위 | 순찰+사무실 | 30분 |\n"
    "| 7월 | 뷰티디자인 | 본인 매장 대표 | 매장+시술 | 30분 |\n"
    "| 8월 | 호텔조리 | WACS 심사위원 교수 | 조리실+심사장 | 30분 |\n"
    "| 9월 | 사회복지 | 복지관 팀장 | 현장 | 30분 |\n\n"
    "**포맷:** 하루 밀착 취재 -> 30분 풀버전(유튜브) + 3분 하이라이트(SNS) + 15초 숏폼\n\n"
    "졸업생이 실제로 일하는 모습을 보여줍니다.\n"
    "배우가 아닙니다. 광고가 아닙니다. 다큐멘터리입니다."
)

# ===== #24 운영방안 =====
S_OPERATION = (
    "### IV-b2. 채널 운영방안\n\n"
    "**현재 상태:** 영산대학교 공식 유튜브 평균 조회수 **108회**\n\n"
    "| 지표 | 현재 (2026.04) | 6개월 후 | 1년 후 | 2년 후 |\n"
    "|------|---------------|----------|--------|--------|\n"
    "| 유튜브 구독자 | 2,400 | 8,000 | 25,000 | 50,000 |\n"
    "| 영상 평균 조회수 | 108 | 3,000 | 15,000 | 40,000 |\n"
    "| 인스타 팔로워 | 1,200 | 5,000 | 15,000 | 30,000 |\n"
    "| 월 콘텐츠 수 | 2 | 12 | 16 | 20 |\n"
    "| 입시 홈페이지 유입 | 측정 안 됨 | 월 500 | 월 3,000 | 월 8,000 |\n\n"
    "**운영 전략**\n\n"
    "| 단계 | 기간 | 핵심 |\n|------|------|------|\n"
    "| 기반 구축 | 1~3개월 | 채널 리브랜딩, 콘텐츠 포맷 확립, 주 3회 업로드 |\n"
    "| 성장 가속 | 4~8개월 | 졸업선배 다큐 시리즈, 인플루언서 콜라보, 숏폼 집중 |\n"
    "| 자체 유입 | 9~12개월 | 검색 최적화, 시리즈 정착, 입시 시즌 집중 부스트 |\n"
    "| 브랜드 채널 | 2년차 | 자체 팬층 확보, 재학생 참여 콘텐츠, 라이브 |\n\n"
    "조회수 108회 -> **2년 내 40,000회.** 370배 성장.\n"
    "콘텐츠의 양이 아닌 '보는 이유가 있는 콘텐츠'로."
)

# ===== 컨셉 (추후 확정, 일단 A 기반) =====
cb, sb_body = concept_A()
cc = "이름을 가려봐."
tl = "이름을 가려도 보이는 대학."
combined = f"**컨셉:** {cc}\n\n{cb}\n\n---\n\n**슬로건:** {tl}\n\n{sb_body}"


def make_sections():
    return [
        (2, "I. 제안배경", 1, S_BACKGROUND),
        (2, "II. 제안업체 일반", 2, S_COMPANY),
        (1, "III. 세부 과업 수행 계획", 3, None),
        (2, "96 / 55 / 25", 4, S_NUMBERS),
        (2, "전환", 5, S_TRANSITION),
        (2, "손실 회피", 6, S_LOSS),
        (2, "신호와 소음", 7, S_COCKTAIL),
        (2, "컨셉 / 슬로건", 8, combined),
        (2, '"3.6%"', 9, sian_slide(cc, "3.6%",
            "탈락률 3.6%. 영산대 항공서비스학과.",
            "Airport gate, '3.6%' large white typography center, cinematic, 16:9, no people",
            "Airport gate vertical, '3.6%' typography, 9:16 mobile format")),
        (2, '"심사위원석"', 10, sian_slide(cc, "심사위원석",
            "WACS 심사위원 4석 중 3석. 영산대 교수.",
            "Judging panel dark auditorium, four chairs, three spotlights, 16:9",
            "Judging panel vertical, spotlight on three chairs, 9:16")),
        (2, '"Room 1201"', 11, sian_slide(cc, "Room 1201",
            "호텔 복도 25개의 문. 전부 총지배인.",
            "Luxury hotel corridor, 25 doors, warm lighting, one-point perspective, 16:9",
            "Hotel corridor vertical, 9:16")),
        (2, '"지혜" 메인 영상', 12, S_JIHYE),
        (2, "월간 졸업선배 다큐", 13, S_DOCU),
        (2, '"1학년 vs 졸업생"', 14, sian_slide(cc, "1학년 vs 졸업생",
            "입학 -> 졸업. 같은 사람. 4년의 차이.",
            "Split screen, left campus blue, right hotel warm, vertical divide, 16:9",
            "Split screen vertical, top freshman bottom graduate, 9:16")),
        (2, "b. 유튜브 콘텐츠", 15, S_YOUTUBE),
        (2, "c. 광고 디자인/인쇄", 16, S_PRINT),
        (2, "d. 디지털 광고", 17, S_DIGITAL),
        (2, "e. SNS 이벤트", 18, S_SNS),
        (2, "f. 언론 지면/배너", 19, S_PRESS),
        (2, "사업 관리", 20, S_CONSULT),
        (2, "IV-a. 예산 집행 (간트)", 21, S_GANTT),
        (2, "IV-b. 결과 분석", 22, S_FEEDBACK),
        (2, "IV-b2. 운영방안", 23, S_OPERATION),
        (2, "IV-c. 홍보단 운영", 24, S_ETC),
    ]


if __name__ == "__main__":
    conn = get_conn()
    sections = make_sections()
    cur = conn.execute(
        "INSERT INTO proposals (title,version,status,rfp_json,rfp_summary,raw_text,selected_concept) VALUES (?,?,?,?,?,?,?)",
        ("V20", "V20", "ready", RFP, SUMMARY, SUMMARY, "A"))
    pid = cur.lastrowid
    for lv, t, idx, content in sections:
        conn.execute(
            "INSERT INTO sections (proposal_id,level,title,order_idx,content,status) VALUES (?,?,?,?,?,?)",
            (pid, lv, t, idx, content, "done" if content else "pending"))
    for lb, ct, bd in CONCEPTS:
        conn.execute(
            "INSERT OR REPLACE INTO concepts (proposal_id,label,title,body) VALUES (?,?,?,?)",
            (pid, lb, ct, bd))
    conn.commit()
    conn.close()
    print(f"V20: id={pid}")
    print("Done.")
