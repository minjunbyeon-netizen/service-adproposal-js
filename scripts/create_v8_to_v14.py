"""V8~V14 연속 디벨롭 + 회사 보고서.

V8:  Cold open (3.6% 선제)
V9:  질문형 빌드업 ("이 학교를 아십니까?")
V10: 대비 구조 ("다른 대행사가 보여줄 것 vs 우리")
V11: V8+V9+V10 장점 통합, 콘텐츠 1차 정제
V12: 콘텐츠 2차 정제, 클리셰 완전 제거 검증
V13: 발표자 톤 최적화, 타이밍 메모
V14-1/V14-2/V14-3: 최종 3컨셉 (A/B/C)
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.db import get_conn, init_db, migrate_db

init_db()
migrate_db()

RFP = json.dumps({
    "client_name":"영산대학교(와이즈유)","project_name":"2026~2027학년도 광고대행사 선정",
    "budget":"연 1.25억 (2년 2.5억, VAT 별도)","deadline":"2026-04-20 17:00",
    "duration":"2년 (2026~2027학년도)",
    "tasks":["크리에이티브 시안 (배점 30점)","홍보 전략/환경 분석","매체 전략/예산 운영","영상 콘텐츠 제작","캠페인 기획/실행"]
}, ensure_ascii=False)
SUMMARY = "영산대학교(와이즈유) 광고대행사 선정. 예산 연 1.25억. 배점 최고: 크리에이티브 시안 30점."

CONCEPTS = [
    ("A","이름을 가려봐.","결과만 놓고 이름을 가리면 명문대. 이름 열면 영산대. 편견 제거 축."),
    ("B","같은 학교.","25명 같은 학교, 심사위원 같은 학교. 반복할수록 밀도. 밀도/집중 축."),
    ("C","이 사람은 배우가 아닙니다.","매 시안마다 배우 아님 -> 영산대 졸업생 반전. 진짜 vs 연출 축."),
]

# ===== 이미지 프롬프트 =====
def img(label,rows,prompt,copies):
    r="\n".join(f"| {k} | {v} |" for k,v in rows)
    c="\n".join(f"- {x}" for x in copies)
    return (f'<div class="img-prompt"><span class="prompt-label">{label}</span>\n\n'
            f"| 요소 | 설명 |\n|------|------|\n{r}\n\n**카피 배치**\n{c}\n\n"
            f'<div class="prompt-cmd">{prompt}</div></div>')

def img_36(cc,tl):
    return img("시안: 3.6%",[("배경","공항 출발 게이트, 밝은 조명"),("중앙",'"3.6%" 200pt 흰색 타이포'),("분위기","미니멀, 블루-화이트")],
        "Airport departure gate, bright lighting, '3.6%' large white typography center, cinematic, 16:9, no people",
        [f'상단 좌 (12pt): "{cc}"','중앙 (200pt Bold): "3.6%"','중앙 하 (24pt): "떨어질 확률입니다."',f'하단 우: 로고+"{tl}"'])
def img_jg(cc,tl):
    return img("시안: 심사위원석",[("배경","심사위원 테이블, 어두운 홀, 스포트라이트 4개"),("구도","정면 대칭, 3석 강조"),("분위기","권위, 스포트라이트 대비")],
        "Judging panel table dark auditorium, four chairs, three spotlights, WACS nameplate, symmetrical, cinematic, 16:9, no people",
        [f'상단 좌: "{cc}"','중앙 (48pt Bold): "4석 중 3석."','중앙 하: "WACS 심사위원. 영산대 교수."',f'하단 우: 로고+"{tl}"'])
def img_rm(cc,tl):
    return img("시안: Room 1201",[("배경","특급호텔 복도, 25개 문, 따뜻한 조명"),("구도","1점 투시, 소실점"),("분위기","고급, 반복 밀도감")],
        "Luxury hotel corridor, 25 doors, warm lighting, one-point perspective, golden tone, cinematic, 16:9, no people",
        [f'상단 좌: "{cc}"','중앙 (72pt Bold): "Room 1201"','중앙 하: "25개의 문. 전부 총지배인."',f'하단 우: 로고+"{tl}"'])
def img_sp(cc,tl):
    return img("시안: 1학년 vs 졸업생",[("레이아웃","수직 50:50 분할"),("왼쪽","캠퍼스, 청량톤, 교복 행거"),("오른쪽","호텔 로비, 따뜻한톤, 유니폼 행거")],
        "Split screen, left: campus blue tone suit hanger, right: hotel lobby warm tone uniform hanger, orange divider, 16:9, no people",
        [f'상단 좌: "{cc}"','왼쪽 중앙: "1학년"','오른쪽 중앙: "졸업생"','하단 중앙: "같은 사람. 4년의 차이."',f'하단 우: 로고+"{tl}"'])

# ===== 공통 슬라이드 =====
BUDGET = ("**연 1.25억. 2년 총 2.5억 (VAT 별도)**\n\n"
    "| 매체 | 비중 | 금액 | 목적 |\n|------|------|------|------|\n"
    "| 옥외 | 30% | 3,750만 | 시안 노출 |\n| 디지털 | 35% | 4,375만 | 영상+타겟 |\n"
    "| 검색 | 15% | 1,875만 | 입시 시즌 |\n| 캠퍼스 | 10% | 1,250만 | 직접 접점 |\n"
    "| 제작비 | 10% | 1,250만 | 시안/영상 |")
COMPANY = ("**하이브미디어**\n\n광고 기획, 매체 집행, 크리에이티브 제작 종합 광고대행사.\n\n"
    "상세 회사 소개, 조직도, 실적, 재무현황, 투입 인력은 별도 보고서에 정리되어 있습니다.\n\n"
    "*앞에 놓인 보고서를 참고해 주십시오.*")
def video_slide(cc):
    return ("**메인 60초 + 숏폼 3종 + 학부모 90초**\n\n"
        f"### 메인 (60초)\n'{cc}' 톤. 4종 시안 옴니버스. 실제 졸업생 출연 (배우 금지).\n\n"
        "### 숏폼 3종 (각 15초)\n- 3.6% 편: 숫자 타이포\n- 심사위원석 편: 클로즈업\n- Room 1201 편: 원테이크\n\n"
        "### 학부모 (90초)\n학부모 시점 다큐. 입학식->수업->실습->취업.")
def campaign_slide():
    return ("**2년 연속 캠페인**\n\n"
        "### 1단계 (2026 상반기)\n4종 시안 동시. 버스쉘터, 지하철, 유튜브.\n\n"
        "### 2단계 (2026 하반기)\n팩트 검증. QS 55위, 연구력 8위. SNS, 검색광고.\n\n"
        "### 3단계 (2027)\n브랜드 고정. 졸업생 인터뷰 시리즈.")
def summary_slide(cc,tl):
    return (f"**'{cc}' 프레임 종합**\n\n"
        "| 시안 | 카피 | 비주얼 |\n|------|------|--------|\n"
        f"| 3.6% | {cc} 탈락률 3.6%. | 공항 게이트 |\n"
        f"| 심사위원석 | {cc} 4석 중 3석. | 심사위원 테이블 |\n"
        f"| Room 1201 | {cc} 25개의 문. | 호텔 복도 |\n"
        f"| 1학년 vs 졸업생 | {cc} 같은 사람. | 분할화면 |\n\n"
        f"공통 마무리: '{tl}'")

# ===== 팩트 (클리셰 제거 버전) =====
FACT = ("**영산대학교는 이런 학교입니다.**\n\n"
    "| | |\n|---|---|\n"
    "| QS 호스피탈리티 | **세계 55위** |\n| 연구력 | **세계 8위** |\n"
    "| 항공서비스 취업률 | **96.4%** |\n| 뷰티디자인 취업률 | **94.1%** |\n"
    "| 경찰행정 취업률 | **93.7%** |\n| 호텔 총지배인 배출 | **25명 (국내 최다)** |\n"
    "| WACS 심사위원 | **4명 중 3명** |\n| 부울경 사립대 취업률 | **1위** |")
PROBLEM = ("**팩트는 있었습니다. 광고가 없었습니다.**\n\n"
    "지금까지 이 숫자들은\n입학처 홈페이지 한 줄.\n대학요람 표 한 칸.\n입시설명회 PPT 한 장.\n\n"
    "96.4%라는 숫자를 보고\n가슴이 뛴 학부모가 있었습니까.\n\n"
    "숫자를 나열하는 것은 보고서입니다.\n숫자를 느끼게 만드는 것이 광고입니다.")
TRANSITION = ("**그래서 이렇게 준비했습니다.**\n\n같은 숫자.\n다른 방식.\n\n"
    "읽는 광고가 아니라, 느끼는 광고.\n보는 순간 멈추는 광고.\n보고 난 뒤 기억에 남는 광고.")


# ==========================
# V8: Cold Open
# ==========================
def v8_sections(cc,tl,concept_body,slogan_body):
    return [
        (2,'"3.6%"',1, f"**{cc}**\n\n탈락률 3.6%.\n\n"+img_36(cc,tl)),  # cold open
        (2,"팩트",2, "**방금 보신 3.6%는 영산대학교 항공서비스학과의 탈락률입니다.**\n\n"
            "96.4%가 취업합니다. 고용노동부 공시.\n\n"
            "| | |\n|---|---|\n| QS 호스피탈리티 | **세계 55위** |\n| 연구력 | **세계 8위** |\n"
            "| 호텔 총지배인 배출 | **25명** |\n| WACS 심사위원 | **4명 중 3명** |\n| 부울경 사립대 취업률 | **1위** |"),
        (2,"문제 제기",3, PROBLEM),
        (2,"전환",4, TRANSITION),
        (2,"컨셉",5, concept_body),
        (2,"슬로건",6, slogan_body),
        (2,'"심사위원석"',7, f"**{cc}**\n\n4석 중 3석. 영산대학교 교수.\n\n"+img_jg(cc,tl)),
        (2,'"Room 1201"',8, f"**{cc}**\n\n25개의 문. 전부 총지배인.\n\n"+img_rm(cc,tl)),
        (2,'"1학년 vs 졸업생"',9, f"**{cc}**\n\n입학 -> 졸업. 같은 사람.\n\n"+img_sp(cc,tl)),
        (2,"지면 시안 종합",10, summary_slide(cc,tl)),
        (2,"영상",11, video_slide(cc)),
        (2,"캠페인 3단계",12, campaign_slide()),
        (2,"매체/예산",13, BUDGET),
        (2,"회사소개",14, COMPANY),
    ]

# ==========================
# V9: 질문형 빌드업
# ==========================
def v9_sections(cc,tl,concept_body,slogan_body):
    return [
        (2,"질문",1, "**이 대학을 아십니까?**\n\nQS 호스피탈리티 세계 55위.\n"
            "연구력 세계 8위.\n항공서비스 취업률 96.4%.\n호텔 총지배인 25명 배출.\n\n"
            "이 대학의 이름을 아십니까?"),
        (2,"답",2, "**영산대학교입니다.**\n\n부울경 사립대 취업률 1위.\n"
            "WACS 심사위원 4명 중 3명이 이 학교 교수.\n\n"
            "이 팩트를 처음 들으셨다면,\n그것이 바로 문제입니다."),
        (2,"문제 제기",3, "**좋은 팩트. 없는 광고.**\n\n"
            "지금까지 이 숫자들은\n대학요람 표 한 칸, 입시설명회 PPT 한 장으로 소비되었습니다.\n\n"
            "96.4%를 보고 가슴이 뛴 학부모가 있었습니까.\n"
            "숫자를 느끼게 만드는 것이 광고입니다."),
        (2,"전환",4, TRANSITION),
        (2,"컨셉",5, concept_body),
        (2,"슬로건",6, slogan_body),
        (2,'"3.6%"',7, f"**{cc}**\n\n탈락률 3.6%.\n\n"+img_36(cc,tl)),
        (2,'"심사위원석"',8, f"**{cc}**\n\n4석 중 3석.\n\n"+img_jg(cc,tl)),
        (2,'"Room 1201"',9, f"**{cc}**\n\n25개의 문.\n\n"+img_rm(cc,tl)),
        (2,'"1학년 vs 졸업생"',10, f"**{cc}**\n\n같은 사람.\n\n"+img_sp(cc,tl)),
        (2,"지면 시안 종합",11, summary_slide(cc,tl)),
        (2,"영상",12, video_slide(cc)),
        (2,"캠페인 3단계",13, campaign_slide()),
        (2,"매체/예산",14, COMPANY+"\n\n---\n\n"+BUDGET),
    ]

# ==========================
# V10: 대비 구조 ("다른 대행사 vs 우리")
# ==========================
def v10_sections(cc,tl,concept_body,slogan_body):
    return [
        (2,"다른 대행사",1, "**다른 대행사가 보여줄 것.**\n\n"
            "학령인구 감소 그래프.\n글로벌 경쟁력 강화 전략.\nMZ세대 감성 마케팅.\n"
            "오고 싶은 학교 만들기.\n브랜드 가치 제고.\n\n"
            "5개 업체가 거의 같은 목차를 가져올 겁니다.\n"
            "평가위원은 이미 다 아는 내용입니다."),
        (2,"우리의 선택",2, "**우리는 그런 이야기를 하지 않겠습니다.**\n\n"
            "학령인구 감소는 교육부가 할 이야기입니다.\n"
            "글로벌 경쟁력은 신문 사설에 있습니다.\n"
            "MZ세대 감성은 이미 낡은 단어입니다.\n\n"
            "우리는 영산대학교가 가진 팩트만 가져왔습니다.\n"
            "그리고 그 팩트를 느끼게 만들었습니다."),
        (2,"팩트",3, FACT),
        (2,"컨셉",4, concept_body),
        (2,"슬로건",5, slogan_body),
        (2,'"3.6%"',6, f"**{cc}**\n\n탈락률 3.6%.\n\n"+img_36(cc,tl)),
        (2,'"심사위원석"',7, f"**{cc}**\n\n4석 중 3석.\n\n"+img_jg(cc,tl)),
        (2,'"Room 1201"',8, f"**{cc}**\n\n25개의 문.\n\n"+img_rm(cc,tl)),
        (2,'"1학년 vs 졸업생"',9, f"**{cc}**\n\n같은 사람.\n\n"+img_sp(cc,tl)),
        (2,"지면 시안 종합",10, summary_slide(cc,tl)),
        (2,"영상",11, video_slide(cc)),
        (2,"캠페인 3단계",12, campaign_slide()),
        (2,"매체/예산",13, BUDGET),
        (2,"회사소개",14, COMPANY),
    ]

# ==========================
# V11: V8+V9+V10 통합 (cold open + 질문 + 대비)
# ==========================
def v11_sections(cc,tl,concept_body,slogan_body):
    return [
        (2,'"3.6%"',1, f"**{cc}**\n\n"+img_36(cc,tl)),  # cold open, 텍스트 최소
        (2,"질문",2, "**이 숫자의 학교를 아십니까?**\n\n"
            "QS 호스피탈리티 세계 55위.\n호텔 총지배인 25명.\nWACS 심사위원 4명 중 3명.\n\n"
            "이 학교의 이름을 아십니까?"),
        (2,"답 + 문제",3, "**영산대학교입니다.**\n\n"
            "이 팩트를 처음 들으셨다면, 그것이 광고의 부재입니다.\n"
            "숫자는 있었습니다. 광고가 없었습니다.\n\n"
            "우리는 학령인구 감소를 말하지 않겠습니다.\n"
            "글로벌 경쟁력을 말하지 않겠습니다.\n"
            "팩트를 느끼게 만들겠습니다."),
        (2,"컨셉",4, concept_body),
        (2,"슬로건",5, slogan_body),
        (2,'"심사위원석"',6, f"**{cc}**\n\n4석 중 3석. 영산대학교 교수.\n\n"+img_jg(cc,tl)),
        (2,'"Room 1201"',7, f"**{cc}**\n\n25개의 문. 전부 총지배인.\n\n"+img_rm(cc,tl)),
        (2,'"1학년 vs 졸업생"',8, f"**{cc}**\n\n입학 -> 졸업. 같은 사람.\n\n"+img_sp(cc,tl)),
        (2,"지면 시안 종합",9, summary_slide(cc,tl)),
        (2,"영상",10, video_slide(cc)),
        (2,"캠페인 3단계",11, campaign_slide()),
        (2,"매체/예산",12, BUDGET),
        (2,"회사소개",13, COMPANY),
        (2,"약속",14, f"**2년 후, 이 질문의 답이 달라집니다.**\n\n"
            "'이 대학을 아십니까?'\n\n"
            f"'{tl}'\n\n영산대학교."),
    ]

# ==========================
# V12: 콘텐츠 정제 + 클리셰 제거 검증
# ==========================
def v12_sections(cc,tl,concept_body,slogan_body):
    # V11 구조 + 콘텐츠 더 간결 + 마지막 슬라이드 강화
    return [
        (2,'"3.6%"',1, img_36(cc,tl)),  # 이미지만. 텍스트 제로.
        (2,"질문",2, "**이 숫자의 학교 이름을 아십니까?**\n\n"
            "| | |\n|---|---|\n| QS 호스피탈리티 | **55위** |\n| 연구력 | **8위** |\n"
            "| 호텔 총지배인 | **25명** |\n| WACS 심사위원 | **4명 중 3명** |"),
        (2,"진단",3, "**영산대학교입니다.**\n\n"
            "팩트를 처음 들으셨다면, 그것이 문제입니다.\n"
            "숫자는 있었습니다. 광고가 없었습니다.\n\n"
            "우리는 뻔한 이야기를 하지 않겠습니다.\n"
            "팩트를 느끼게 만들겠습니다."),
        (2,"컨셉",4, concept_body),
        (2,"슬로건",5, slogan_body),
        (2,'"심사위원석"',6, f"**{cc}**\n\n"+img_jg(cc,tl)),
        (2,'"Room 1201"',7, f"**{cc}**\n\n"+img_rm(cc,tl)),
        (2,'"1학년 vs 졸업생"',8, f"**{cc}**\n\n"+img_sp(cc,tl)),
        (2,"지면 시안 종합",9, summary_slide(cc,tl)),
        (2,"영상",10, video_slide(cc)),
        (2,"캠페인",11, campaign_slide()),
        (2,"매체/예산",12, BUDGET),
        (2,"회사소개",13, COMPANY),
        (2,"약속",14, f"**2년 후.**\n\n'이 대학을 아십니까?'\n\n모두가 답할 수 있게 만들겠습니다.\n\n{tl}\n\n영산대학교."),
    ]

# V13 = V12 동일 구조 + 발표자 톤 메모 (콘텐츠에 <!-- 발표 메모 --> 삽입)
def v13_sections(cc,tl,concept_body,slogan_body):
    base = v12_sections(cc,tl,concept_body,slogan_body)
    # 타이밍 메모를 각 슬라이드에 추가
    notes = {
        1: "(2초 정지. 화면만 보여주고 아무 말 하지 않는다.)",
        2: "(천천히 읽어준다. '아십니까?'에서 잠시 멈춘다.)",
        3: "('광고가 없었습니다'에서 강조. 톤을 낮춘다.)",
        4: "(자신감 있게. 이 슬라이드가 PT의 핵심이다.)",
        5: "(슬로건을 천천히, 한 번만 읽는다. 반복하지 않는다.)",
        14: "('영산대학교'를 말하고 3초 정지. PT 종료.)",
    }
    result = []
    for level, title, idx, content in base:
        if idx in notes:
            content = content + f"\n\n---\n*{notes[idx]}*"
        result.append((level, title, idx, content))
    return result

# V14 = V13 최종 (발표 메모 제거, 클린 버전)
v14_sections = v12_sections  # 가장 깔끔한 구조


# ===== 컨셉별 콘텐츠 =====
def concept_A():
    return (
        "**이름을 가려봐.**\n\n"
        "취업률 96.4%의 학교. 이름을 가려봐.\n"
        "WACS 심사위원 3명의 학교. 이름을 가려봐.\n"
        "호텔 총지배인 25명의 학교. 이름을 가려봐.\n\n"
        "결과만 놓으면 명문대.\n이름을 열면 영산대.\n\n"
        "이제 이름을 가려도 보이는 대학.",
        "**이름을 가려도 보이는 대학.**\n\n"
        "QS 호스피탈리티 세계 55위.\n연구력 세계 8위.\n"
        "호텔 총지배인 배출 국내 1위.\n부울경 사립대 취업률 1위.\n\n"
        "이름을 가려도 보이는 대학.\n영산대학교.")
def concept_B():
    return (
        "**같은 학교.**\n\n"
        "25명의 호텔 총지배인. 같은 학교.\nWACS 심사위원 3명. 같은 학교.\n"
        "취업률 96.4%. 같은 학교.\n\n"
        "반복될수록 밀도가 생깁니다.\n밀도가 곧 브랜드입니다.\n\n같은 학교. 영산대학교.",
        "**같은 학교. 영산대학교.**\n\n"
        "총지배인이 물으면, 같은 학교.\n심사위원이 물으면, 같은 학교.\n"
        "취업률을 물으면, 같은 학교.\n\n"
        "두 글자가 반복될 때마다\n영산대학교의 무게가 쌓입니다.")
def concept_C():
    return (
        "**이 사람은 배우가 아닙니다.**\n\n"
        "심사위원석의 교수. 배우가 아닙니다.\n복도의 총지배인. 배우가 아닙니다.\n"
        "유니폼의 졸업생. 배우가 아닙니다.\n\n"
        "영산대학교는 배우를 쓸 필요가 없습니다.\n진짜가 있으니까.",
        "**이 사람은 배우가 아닙니다.**\n\n"
        "모든 시안의 마지막 한 줄.\n'이 사람은 배우가 아닙니다.'\n\n"
        "반전의 순간. 광고가 끝나고 기억에 남는 한 줄.\n\n"
        "이 사람은 배우가 아닙니다.\n영산대학교 졸업생입니다.")

# ===== 생성 =====
def create(conn, title, version, concept_label, sections_fn, cc, tl, cb, sb):
    cur = conn.execute(
        "INSERT INTO proposals (title,version,status,rfp_json,rfp_summary,raw_text,selected_concept) VALUES (?,?,?,?,?,?,?)",
        (title, version, "ready", RFP, SUMMARY, SUMMARY, concept_label))
    pid = cur.lastrowid
    for lv, t, idx, content in sections_fn(cc, tl, cb, sb):
        conn.execute("INSERT INTO sections (proposal_id,level,title,order_idx,content,status) VALUES (?,?,?,?,?,?)",
            (pid, lv, t, idx, content, "done" if content else "pending"))
    for label, ctitle, body in CONCEPTS:
        conn.execute("INSERT OR REPLACE INTO concepts (proposal_id,label,title,body) VALUES (?,?,?,?)",
            (pid, label, ctitle, body))
    return pid

conn = get_conn()

# 컨셉 A 기본으로 V8~V13
ca_cb, ca_sb = concept_A()
cc_a, tl_a = "이름을 가려봐.", "이름을 가려도 보이는 대학."

versions = [
    ("V8: Cold Open", "V8", v8_sections),
    ("V9: 질문형 빌드업", "V9", v9_sections),
    ("V10: 대비 구조", "V10", v10_sections),
    ("V11: 통합 구조", "V11", v11_sections),
    ("V12: 콘텐츠 정제", "V12", v12_sections),
    ("V13: 발표자 톤", "V13", v13_sections),
]

for title, ver, fn in versions:
    pid = create(conn, title, ver, "A", fn, cc_a, tl_a, ca_cb, ca_sb)
    print(f"{ver}: id={pid}")

# V14: 3컨셉
for label, cc, tl, cfn in [
    ("A","이름을 가려봐.","이름을 가려도 보이는 대학.", concept_A),
    ("B","같은 학교.","같은 학교. 영산대학교.", concept_B),
    ("C","이 사람은 배우가 아닙니다.","이 사람은 배우가 아닙니다.", concept_C),
]:
    cb, sb = cfn()
    pid = create(conn, f"V14-{label[-1]}: {cc}", f"V14-{label[-1]}", label[-1] if label[-1] in "ABC" else label,
                 v14_sections, cc, tl, cb, sb)
    # Fix: label for concept selection
    conn.execute("UPDATE proposals SET selected_concept=? WHERE id=?", (label, pid))
    print(f"V14-{label[-1]}: id={pid}")

conn.commit()
conn.close()
print("Done: V8~V14 created.")
