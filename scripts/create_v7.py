"""V7-1, V7-2, V7-3 제안서 생성 -- 빌드업 구조 + 디바이더 제거 + 순서 확정."""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.db import get_conn, init_db, migrate_db

init_db()
migrate_db()

RFP_JSON = json.dumps({
    "client_name": "영산대학교(와이즈유)",
    "project_name": "2026~2027학년도 광고대행사 선정",
    "budget": "연 1.25억 (2년 2.5억, VAT 별도)",
    "deadline": "2026-04-20 17:00",
    "duration": "2년 (2026~2027학년도)",
    "tasks": [
        "크리에이티브 시안 (배점 30점)",
        "홍보 전략/환경 분석",
        "매체 전략/예산 운영",
        "영상 콘텐츠 제작",
        "캠페인 기획/실행",
    ],
}, ensure_ascii=False)

RFP_SUMMARY = (
    "영산대학교(와이즈유) 2026~2027학년도 광고대행사 선정 입찰.\n"
    "예산 연 1.25억(2년 2.5억, VAT별도). 제출기한 2026-04-20 17:00.\n"
    "배점 최고: 크리에이티브 시안 창의성/독창성 30점."
)

CONCEPTS = [
    ("A", "이름을 가려봐.",
     "결과만 놓고 대학 이름을 가리면 명문대. 이름 열면 영산대. 편견 제거 축."),
    ("B", "같은 학교.",
     "25명 같은 학교, 심사위원 같은 학교. 반복할수록 밀도. 밀도/집중 축."),
    ("C", "이 사람은 배우가 아닙니다.",
     "매 시안마다 배우 아님 -> 영산대 졸업생 반전. 진짜 vs 연출 축."),
]

# ========== 공통 슬라이드 ==========

SLIDE_FACT = (
    "**영산대학교는 이런 학교입니다.**\n\n"
    "| | |\n"
    "|---|---|\n"
    "| QS 호스피탈리티 | **세계 55위** |\n"
    "| 연구력 | **세계 8위** |\n"
    "| 항공서비스 취업률 | **96.4%** |\n"
    "| 뷰티디자인 취업률 | **94.1%** |\n"
    "| 경찰행정 취업률 | **93.7%** |\n"
    "| 호텔 총지배인 배출 | **25명 (국내 최다)** |\n"
    "| WACS 심사위원 | **4명 중 3명** |\n"
    "| 부울경 사립대 취업률 | **1위 (66.2%)** |"
)

SLIDE_PROBLEM = (
    "**팩트는 있었습니다. 광고가 없었습니다.**\n\n"
    "지금까지 이 숫자들은 이렇게 쓰였습니다.\n\n"
    "입학처 홈페이지 한 줄.\n"
    "대학요람 표 한 칸.\n"
    "입시설명회 PPT 한 장.\n\n"
    "96.4%라는 숫자를 보고\n"
    "가슴이 뛴 학부모가 있었습니까.\n\n"
    "숫자를 나열하는 것은 보고서입니다.\n"
    "숫자를 느끼게 만드는 것이 광고입니다."
)

SLIDE_TRANSITION = (
    "**그래서 이렇게 준비했습니다.**\n\n"
    "같은 숫자.\n"
    "다른 방식.\n\n"
    "읽는 광고가 아니라,\n"
    "느끼는 광고.\n\n"
    "보는 순간 멈추는 광고.\n"
    "보고 난 뒤 기억에 남는 광고."
)

COMMON_BUDGET = (
    "**연 1.25억. 2년 총 2.5억 (VAT 별도)**\n\n"
    "| 매체 | 비중 | 금액 | 목적 |\n"
    "|------|------|------|------|\n"
    "| 옥외 (버스쉘터/지하철) | 30% | 3,750만 | 시안 노출 |\n"
    "| 디지털 (유튜브/SNS) | 35% | 4,375만 | 영상 + 타겟 도달 |\n"
    "| 검색 (네이버/구글) | 15% | 1,875만 | 입시 시즌 집중 |\n"
    "| 캠퍼스/입시설명회 | 10% | 1,250만 | 직접 접점 |\n"
    "| 제작비 | 10% | 1,250만 | 시안/영상 제작 |\n\n"
    "Year 2는 1단계(충격) 비중 축소, 3단계(정착) 비중 확대."
)

COMMON_COMPANY = (
    "**하이브미디어**\n\n"
    "광고 기획, 매체 집행, 크리에이티브 제작을 일괄 수행하는 종합 광고대행사.\n\n"
    "상세 회사 소개, 조직도, 실적, 재무현황, 투입 인력은 "
    "별도 보고서에 정리되어 있습니다.\n\n"
    "*앞에 놓인 보고서를 참고해 주십시오.*"
)


# ========== 이미지 프롬프트 그리드 ==========

def img(label, table_rows, prompt, copy_lines):
    rows = "\n".join(f"| {k} | {v} |" for k, v in table_rows)
    copies = "\n".join(f"- {c}" for c in copy_lines)
    return (
        f'<div class="img-prompt">'
        f'<span class="prompt-label">{label}</span>\n\n'
        f"| 요소 | 설명 |\n|------|------|\n{rows}\n\n"
        f"**카피 배치**\n{copies}\n\n"
        f'<div class="prompt-cmd">{prompt}</div>'
        f"</div>"
    )


def img_36(concept_copy, tagline):
    return img("시안: 3.6%", [
        ("배경", "공항 출발 게이트, 밝은 조명, 현대적 인테리어, 탑승구 번호판"),
        ("중앙", '"3.6%" 거대 타이포 (200pt, Roboto Bold, 흰색, 약간 투명)'),
        ("분위기", "미니멀, 시네마틱, 차가운 톤 (블루-화이트)"),
        ("비율", "16:9 가로형"),
    ],
        "Modern airport departure gate interior, bright fluorescent lighting, "
        "empty gate seating, boarding sign visible, clean minimal atmosphere, "
        "large floating white typography '3.6%' semi-transparent in center, "
        "cinematic wide shot, blue-white color grade, 16:9, ad poster style, no people",
        [f'상단 좌 (12pt, 흰색): "{concept_copy}"',
         '중앙 (200pt, Roboto Bold, 흰색): "3.6%"',
         '중앙 하 (24pt, 흰색): "영산대학교 항공서비스학과에 떨어질 확률입니다."',
         f'하단 우: 영산대 로고 + "{tagline}" (14pt, #E84E10)'])


def img_judge(concept_copy, tagline):
    return img("시안: 심사위원석", [
        ("배경", "고급 심사위원 테이블, 어두운 홀, 스포트라이트 4개"),
        ("구도", "정면 대칭, 4개 의자 중 3개에 스포트라이트 강조"),
        ("소품", "WACS 로고 명패, 흰 테이블보"),
        ("분위기", "권위적, 엄숙, 따뜻한 스포트라이트 vs 어두운 배경"),
    ],
        "Prestigious judging panel table in dark auditorium, four empty chairs "
        "behind long table with white tablecloth, three spotlights illuminating "
        "three of four chairs, WACS logo nameplate, symmetrical front view, "
        "warm spotlight vs dark background, authoritative, cinematic, 16:9, no people",
        [f'상단 좌 (12pt, 흰색): "{concept_copy}"',
         '중앙 상 (48pt, Roboto Bold, 흰색): "4석 중 3석."',
         '중앙 하 (24pt, 흰색): "WACS 세계조리사연맹 심사위원. 영산대학교 교수."',
         f'하단 우: 영산대 로고 + "{tagline}" (14pt, #E84E10)'])


def img_room(concept_copy, tagline):
    return img("시안: Room 1201", [
        ("배경", "특급호텔 복도, 따뜻한 조명, 카펫, 25개 문이 양쪽 늘어선 긴 복도"),
        ("구도", "1점 투시, 복도 끝 소실점 향해 촬영"),
        ("조명", "각 문 앞 벽등 ON, 복도 끝 약간 밝게"),
        ("분위기", "고급스러움, 반복의 밀도감, 영화적 구도"),
    ],
        "Luxury hotel long corridor, warm ambient lighting, rich carpet, "
        "25 identical doors on both sides stretching to vanishing point, "
        "wall sconces lit beside each door, one-point perspective, "
        "cinematic depth of field, warm golden tone, no people, 16:9, ad poster style",
        [f'상단 좌 (12pt, 흰색): "{concept_copy}"',
         '중앙 (72pt, Roboto Bold, 흰색, 소실점 배치): "Room 1201"',
         '중앙 하 (24pt, 흰색): "25개의 문. 전부 총지배인. 전부 같은 학교."',
         f'하단 우: 영산대 로고 + "{tagline}" (14pt, #E84E10)'])


def img_split(concept_copy, tagline):
    return img("시안: 1학년 vs 졸업생", [
        ("레이아웃", "정중앙 수직 분할 (50:50)"),
        ("왼쪽", "대학 캠퍼스, 밝고 청량한 톤, 빈 교복/정장 행거"),
        ("오른쪽", "호텔 로비, 따뜻하고 프로페셔널한 톤, 유니폼 행거"),
        ("경계", "수직 분할선 (2px, #E84E10)"),
    ],
        "Split screen ad poster, left: bright campus with formal suit on hanger, "
        "blue tone; right: luxury hotel lobby with uniform on hanger, warm golden; "
        "sharp vertical divide with thin orange line, no people, 16:9, ad style",
        [f'상단 좌 (12pt, 흰색): "{concept_copy}"',
         '왼쪽 중앙 (32pt, Bold): "1학년"',
         '오른쪽 중앙 (32pt, Bold): "졸업생"',
         '하단 중앙 (24pt, 흰색): "같은 사람입니다. 4년이 만든 차이."',
         f'하단 우: 영산대 로고 + "{tagline}" (14pt, #E84E10)'])


# ============================================================
# 16장 구조 (디바이더 없음)
# 1.표지 2.팩트 3.문제제기 4.전환 5.컨셉 6.슬로건
# 7.시안3.6% 8.심사위원석 9.Room1201 10.1학년vs졸업생
# 11.지면종합 12.영상 13.캠페인 14.매체예산 15.회사소개 16.마무리
# ============================================================

def make_sections(concept_copy, tagline, concept_content, slogan_content):
    """16장 구조 섹션 리스트 생성. 모두 L2 (디바이더 없음)."""
    return [
        # 빌드업
        (2, "팩트", 1, SLIDE_FACT),
        (2, "문제 제기", 2, SLIDE_PROBLEM),
        (2, "전환", 3, SLIDE_TRANSITION),
        # 컨셉 + 슬로건
        (2, "컨셉", 4, concept_content),
        (2, "슬로건", 5, slogan_content),
        # 시안 4종
        (2, '"3.6%"', 6,
         f"**{concept_copy}**\n\n"
         "어느 대학의 취업률입니다. 탈락률 3.6%.\n"
         "96.4%. 고용노동부 공시 데이터.\n\n"
         + img_36(concept_copy, tagline)),
        (2, '"심사위원석"', 7,
         f"**{concept_copy}**\n\n"
         "WACS 심사위원석. 4석 중 3석.\n"
         "영산대학교 교수입니다.\n\n"
         + img_judge(concept_copy, tagline)),
        (2, '"Room 1201"', 8,
         f"**{concept_copy}**\n\n"
         "호텔 복도 25개의 문. 전부 총지배인.\n"
         "전부 영산대학교 졸업생.\n\n"
         + img_room(concept_copy, tagline)),
        (2, '"1학년 vs 졸업생"', 9,
         f"**{concept_copy}**\n\n"
         "입학식의 18살 -> 졸업 후 프로.\n"
         "같은 사람. 부울경 사립대 취업률 1위.\n\n"
         + img_split(concept_copy, tagline)),
        # 실행
        (2, "지면 시안 4종", 10,
         f"**4개 시안 종합 -- '{concept_copy}' 프레임**\n\n"
         "| 시안 | 카피 | 비주얼 |\n"
         "|------|------|--------|\n"
         f"| 3.6% | {concept_copy} 탈락률 3.6%. | 공항 게이트 + 숫자 |\n"
         f"| 심사위원석 | {concept_copy} 4석 중 3석. | 심사위원 테이블 |\n"
         f"| Room 1201 | {concept_copy} 25개의 문. | 호텔 복도 |\n"
         f"| 1학년 vs 졸업생 | {concept_copy} 같은 사람. | 분할화면 |\n\n"
         f"공통 마무리: '{tagline}'"),
        (2, "영상", 11,
         "**메인 영상 60초 + 숏폼 3종 + 학부모 영상 90초**\n\n"
         "### 메인 영상 (60초)\n"
         f"'{concept_copy}' 톤. 4종 시안 핵심 장면 옴니버스.\n"
         "촬영: 영산대 캠퍼스 + 실제 취업 현장.\n\n"
         "### 숏폼 3종 (각 15초)\n"
         "- 3.6% 편: 숫자 타이포 모션\n"
         "- 심사위원석 편: 심사위원석 클로즈업\n"
         "- Room 1201 편: 복도 워킹 원테이크\n\n"
         "### 학부모 영상 (90초)\n"
         "학부모 시점. 입학식 -> 수업 -> 실습 -> 취업."),
        (2, "캠페인 3단계", 12,
         "**Year 1 + Year 2. 2년 연속 캠페인.**\n\n"
         "### 1단계 (2026 상반기)\n"
         "4종 시안 동시 집행.\n"
         "버스쉘터, 지하철 랩핑, 유튜브 프리롤.\n\n"
         "### 2단계 (2026 하반기)\n"
         "팩트 검증 콘텐츠. QS 55위, 연구력 8위.\n"
         "SNS 카드뉴스, 네이버 검색광고.\n\n"
         "### 3단계 (2027)\n"
         "브랜드 고정. 재학생/졸업생 인터뷰 시리즈.\n"
         "유튜브, 인스타그램, 입시설명회 연동."),
        # 근거
        (2, "매체/예산", 13, COMMON_BUDGET),
        (2, "회사소개", 14, COMMON_COMPANY),
    ]


# ============================================================
# V7-1: "이름을 가려봐"
# ============================================================
V7_1 = {
    "title": "V7-1: 이름을 가려봐",
    "version": "V7-1",
    "concept": "A",
    "sections": make_sections(
        "이름을 가려봐.",
        "이름을 가려도 보이는 대학.",
        # 컨셉 슬라이드
        "**이름을 가려봐.**\n\n"
        "취업률 96.4%의 학교. 이름을 가려봐.\n"
        "WACS 심사위원 3명의 학교. 이름을 가려봐.\n"
        "호텔 총지배인 25명의 학교. 이름을 가려봐.\n\n"
        "결과만 놓으면 명문대입니다.\n"
        "이름을 열면 영산대입니다.\n\n"
        "이제 이름을 가려도 보이는 대학.",
        # 슬로건 슬라이드
        "**이름을 가려도 보이는 대학.**\n\n"
        "QS 호스피탈리티 세계 55위.\n"
        "연구력 세계 8위.\n"
        "호텔 총지배인 배출 국내 1위.\n"
        "부울경 사립대 취업률 1위.\n\n"
        "이름을 가려도 보이는 대학.\n"
        "영산대학교.",
    ),
}

# ============================================================
# V7-2: "같은 학교"
# ============================================================
V7_2 = {
    "title": "V7-2: 같은 학교",
    "version": "V7-2",
    "concept": "B",
    "sections": make_sections(
        "같은 학교.",
        "같은 학교. 영산대학교.",
        "**같은 학교.**\n\n"
        "25명의 호텔 총지배인. 같은 학교.\n"
        "WACS 심사위원 3명. 같은 학교.\n"
        "취업률 96.4%. 같은 학교.\n\n"
        "반복될수록 밀도가 생깁니다.\n"
        "밀도가 곧 브랜드입니다.\n\n"
        "같은 학교. 영산대학교.",
        "**같은 학교. 영산대학교.**\n\n"
        "총지배인이 물으면, 같은 학교.\n"
        "심사위원이 물으면, 같은 학교.\n"
        "취업률을 물으면, 같은 학교.\n\n"
        "두 글자가 반복될 때마다\n"
        "영산대학교의 무게가 쌓입니다.\n\n"
        "같은 학교.",
    ),
}

# ============================================================
# V7-3: "이 사람은 배우가 아닙니다"
# ============================================================
V7_3 = {
    "title": "V7-3: 이 사람은 배우가 아닙니다",
    "version": "V7-3",
    "concept": "C",
    "sections": make_sections(
        "이 사람은 배우가 아닙니다.",
        "이 사람은 배우가 아닙니다.",
        "**이 사람은 배우가 아닙니다.**\n\n"
        "광고에 나오는 모든 사람이 진짜입니다.\n\n"
        "심사위원석의 교수. 배우가 아닙니다.\n"
        "복도의 총지배인. 배우가 아닙니다.\n"
        "유니폼의 졸업생. 배우가 아닙니다.\n\n"
        "영산대학교는 배우를 쓸 필요가 없습니다.\n"
        "진짜가 있으니까.",
        "**이 사람은 배우가 아닙니다.**\n\n"
        "모든 시안의 마지막 한 줄.\n"
        "'이 사람은 배우가 아닙니다.'\n\n"
        "반전의 순간. 관객이 깨닫는 순간.\n"
        "광고가 끝나고 기억에 남는 한 줄.\n\n"
        "이 사람은 배우가 아닙니다.\n"
        "영산대학교 졸업생입니다.",
    ),
}


def create_proposal(conn, spec):
    cur = conn.execute(
        "INSERT INTO proposals (title, version, status, rfp_json, rfp_summary, "
        "raw_text, selected_concept) VALUES (?,?,?,?,?,?,?)",
        (spec["title"], spec["version"], "ready", RFP_JSON, RFP_SUMMARY,
         RFP_SUMMARY, spec["concept"]),
    )
    pid = cur.lastrowid
    for level, title, order_idx, content in spec["sections"]:
        status = "done" if content else "pending"
        conn.execute(
            "INSERT INTO sections (proposal_id, level, title, order_idx, "
            "content, status) VALUES (?,?,?,?,?,?)",
            (pid, level, title, order_idx, content, status),
        )
    for label, ctitle, body in CONCEPTS:
        conn.execute(
            "INSERT OR REPLACE INTO concepts (proposal_id, label, title, body) "
            "VALUES (?,?,?,?)",
            (pid, label, ctitle, body),
        )
    return pid


conn = get_conn()
pid1 = create_proposal(conn, V7_1)
pid2 = create_proposal(conn, V7_2)
pid3 = create_proposal(conn, V7_3)
conn.commit()
conn.close()

print(f"V7-1: id={pid1}")
print(f"V7-2: id={pid2}")
print(f"V7-3: id={pid3}")
print("Done.")
