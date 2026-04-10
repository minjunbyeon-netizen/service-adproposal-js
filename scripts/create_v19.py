"""V19: 5/6 위치 변경 + 빌드업 2장 추가 (심리효과) + 간트차트 바 + 제안개요 보강.

총 25장: 표지 + 22 content + 간지1 + 마무리
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.db import get_conn, init_db, migrate_db
from scripts.create_v8_to_v14 import RFP, SUMMARY, CONCEPTS, concept_A, concept_B, concept_C
from scripts.create_v18 import (
    grid16x9, grid9x16, sian_slide, S_COMPANY,
    S_VIDEO_1, S_VIDEO_2, S_YOUTUBE, S_PRINT, S_DIGITAL,
    S_SNS, S_PRESS, S_CONSULT, S_FEEDBACK, S_ETC,
)

init_db()
migrate_db()

# ===== 보강된 제안개요 =====
S_OVERVIEW = (
    "### I. 제안개요\n\n"
    "| 항목 | 내용 |\n|------|------|\n"
    "| 사업명 | 2026~2027학년도 영산대학교 광고대행사 선정 |\n"
    "| 발주처 | 영산대학교 (와이즈유) |\n"
    "| 사업기간 | 2년 (2026~2027학년도) |\n"
    "| 예산 | 연 1.25억 (2년 총 2.5억, VAT 별도) |\n"
    "| 제출기한 | 2026-04-20 17:00 |\n"
    "| 제안업체 | (주)하이브미디어 |\n\n"
    "본 제안서는 영산대학교의 2026~2027학년도 광고대행사 선정을 위해 "
    "작성되었습니다.\n\n"
    "크리에이티브 시안, 매체 전략, 캠페인 기획, 영상 제작, "
    "디지털 마케팅을 포괄하는 종합 광고대행 계획을 제안드립니다.\n\n"
    "하이브미디어는 영산대학교가 보유한 객관적 실적과 데이터를 기반으로, "
    "정보 전달을 넘어 직접 느낄 수 있는 광고를 기획하였습니다."
)

# ===== 5번(원래6): 질문 먼저 =====
S_QUESTION = (
    "**이 대학을 아십니까?**\n\n"
    "| | |\n|---|---|\n"
    "| QS 호스피탈리티 | **세계 55위** |\n| 연구력 | **세계 8위** |\n"
    "| 항공서비스 취업률 | **96.4%** |\n"
    "| 호텔 총지배인 배출 | **25명 (국내 최다)** |\n"
    "| WACS 심사위원 | **4명 중 3명** |\n"
    "| 부울경 사립대 취업률 | **1위** |\n\n"
    "이 학교의 이름을 아십니까?"
)

# ===== 7번: 전환 (정보전달 -> IMPACT) =====
S_TRANSITION = (
    "**영산대학교입니다.**\n\n"
    "이 팩트를 처음 들으셨다면, 그것이 문제입니다.\n\n"
    "지금까지의 광고는 정보 전달형이었습니다.\n"
    "숫자를 나열하고, 슬로건을 붙이고, 캠퍼스 사진을 넣었습니다.\n\n"
    "이제는 직접 느낄 수 있는 IMPACT가 필요합니다."
)

# ===== 8번: 빌드업 -- 손실 회피 심리 =====
S_LOSS = (
    "**사람은 얻는 것보다 잃는 것에 2배 강하게 반응합니다.**\n\n"
    "행동경제학에서 이것을 **손실 회피(Loss Aversion)**라고 합니다.\n\n"
    "> 취업률 96.4%\n\n"
    "이 숫자는 좋은 숫자입니다. 하지만 익숙합니다.\n"
    "모든 대학이 취업률을 자랑합니다. 시선이 멈추지 않습니다.\n\n"
    "> 탈락률 3.6%\n\n"
    "같은 숫자입니다. 하지만 느낌이 다릅니다.\n"
    "'떨어질 확률이 3.6%밖에 안 된다고?' -- 이 반응이 광고입니다.\n\n"
    "사람은 '96.4%가 성공한다'보다\n"
    "'3.6%만 실패한다'에 멈춥니다."
)

# ===== 9번: 빌드업 -- 칵테일 파티 효과 =====
S_COCKTAIL = (
    "**시끄러운 파티장에서도 내 이름은 들립니다.**\n\n"
    "심리학에서 이것을 **칵테일 파티 효과**라고 합니다.\n"
    "사람은 자신과 관련된 정보에만 반응합니다.\n\n"
    "수험생에게 '글로벌 경쟁력 강화'는 소음입니다.\n"
    "학부모에게 '브랜드 가치 제고'는 소음입니다.\n\n"
    "하지만,\n\n"
    "> \"이 학교 졸업생 100명 중 96명이 취업합니다.\"\n"
    "> \"호텔 총지배인 25명이 같은 학교 출신입니다.\"\n\n"
    "이것은 소음이 아닙니다. 내 아이의 미래에 직결되는 정보입니다.\n\n"
    "**우리 광고는 소음이 아닌 신호를 만듭니다.**\n"
    "그래서 이렇게 준비했습니다."
)

# ===== 간트차트 HTML (가로 막대 그래프) =====
def gantt_bar(left_pct, width_pct, cls, label):
    return f'<div class="gantt-bar {cls}" style="left:{left_pct}%;width:{width_pct}%">{label}</div>'

S_GANTT = (
    "### IV-1. 광고 운영 및 예산 집행 계획\n\n"
    "**2년 간트차트 -- 수시 80% / 정시 20%**\n\n"
    "#### 2026년 (Year 1) -- 4월 착수\n"
    '<div class="gantt">'
    '<div class="gantt-row"><span class="gantt-label">4월</span><div class="gantt-track">' + gantt_bar(0,11.1,'normal','협의/기획/킥오프') + '</div></div>'
    '<div class="gantt-row"><span class="gantt-label">5월</span><div class="gantt-track">' + gantt_bar(11.1,11.1,'peak','수시 집중 30%') + '</div></div>'
    '<div class="gantt-row"><span class="gantt-label">6월</span><div class="gantt-track">' + gantt_bar(22.2,11.1,'peak','원서 접수 30%') + '</div></div>'
    '<div class="gantt-row"><span class="gantt-label">7월</span><div class="gantt-track">' + gantt_bar(33.3,11.1,'peak','수시 마감 20%') + '</div></div>'
    '<div class="gantt-row"><span class="gantt-label">8-9월</span><div class="gantt-track">' + gantt_bar(44.4,22.2,'normal','성과 분석/콘텐츠 제작') + '</div></div>'
    '<div class="gantt-row"><span class="gantt-label">10-11월</span><div class="gantt-track">' + gantt_bar(66.6,22.2,'mid','정시 집중 20%') + '</div></div>'
    '<div class="gantt-row"><span class="gantt-label">12월</span><div class="gantt-track">' + gantt_bar(88.8,11.1,'normal','정시 마감/연간 결산') + '</div></div>'
    '</div>\n\n'
    "#### 2027년 (Year 2)\n"
    '<div class="gantt">'
    '<div class="gantt-row"><span class="gantt-label">1-3월</span><div class="gantt-track">' + gantt_bar(0,25,'normal','Year2 수립/시안 리뉴얼') + '</div></div>'
    '<div class="gantt-row"><span class="gantt-label">4월</span><div class="gantt-track">' + gantt_bar(25,8.3,'normal','제작/옥외 교체') + '</div></div>'
    '<div class="gantt-row"><span class="gantt-label">5-7월</span><div class="gantt-track">' + gantt_bar(33.3,25,'peak','수시 집중 80%') + '</div></div>'
    '<div class="gantt-row"><span class="gantt-label">8-10월</span><div class="gantt-track">' + gantt_bar(58.3,25,'normal','분석/정시 대비') + '</div></div>'
    '<div class="gantt-row"><span class="gantt-label">11-12월</span><div class="gantt-track">' + gantt_bar(83.3,16.6,'mid','정시 20%/결산') + '</div></div>'
    '</div>\n\n'
    '<div class="gantt-legend">'
    '<span class="lg-peak">수시 집중 (80%)</span>'
    '<span class="lg-mid">정시 (20%)</span>'
    '<span class="lg-normal">기획/제작/분석</span>'
    '</div>'
)


def make_sections(cc, tl, cb, sb):
    combined = f"**컨셉:** {cc}\n\n{cb}\n\n---\n\n**슬로건:** {tl}\n\n{sb}"
    return [
        (2, "I. 제안개요", 1, S_OVERVIEW),
        (2, "II. 제안업체 일반", 2, S_COMPANY),
        (1, "III. 세부 과업 수행 계획", 3, None),
        # 빌드업: 질문 -> 전환 -> 심리 -> 컨셉
        (2, "질문", 4, S_QUESTION),
        (2, "전환", 5, S_TRANSITION),
        (2, "손실 회피", 6, S_LOSS),
        (2, "신호와 소음", 7, S_COCKTAIL),
        (2, "컨셉 / 슬로건", 8, combined),
        # 시안 연타: 3.6% -> 심사위원석 -> Room 1201 -> 1학년vs졸업생
        (2, '"3.6%"', 9, sian_slide(cc, "3.6%",
            "탈락률 3.6%. 영산대 항공서비스학과.",
            "Airport gate, '3.6%' large white typography center, cinematic, 16:9, no people",
            "Airport gate vertical, '3.6%' typography, 9:16 mobile format")),
        (2, '"심사위원석"', 10, sian_slide(cc, "심사위원석",
            "WACS 심사위원 4석 중 3석. 영산대 교수.",
            "Judging panel dark auditorium, four chairs, three spotlights, WACS nameplate, 16:9",
            "Judging panel vertical, spotlight on three chairs, 9:16")),
        (2, '"Room 1201"', 11, sian_slide(cc, "Room 1201",
            "호텔 복도 25개의 문. 전부 총지배인.",
            "Luxury hotel corridor, 25 doors, warm lighting, one-point perspective, 16:9",
            "Hotel corridor vertical, doors stretching upward, 9:16")),
        (2, '"1학년 vs 졸업생"', 12, sian_slide(cc, "1학년 vs 졸업생",
            "입학 -> 졸업. 같은 사람. 4년의 차이.",
            "Split screen, left campus blue, right hotel warm, vertical divide, 16:9",
            "Split screen vertical, top freshman bottom graduate, 9:16")),
        # 과업
        (2, "a. 홍보영상 (1/2)", 13, S_VIDEO_1),
        (2, "a. 홍보영상 (2/2)", 14, S_VIDEO_2),
        (2, "b. 유튜브 콘텐츠", 15, S_YOUTUBE),
        (2, "c. 광고 디자인/인쇄", 16, S_PRINT),
        (2, "d. 디지털 광고", 17, S_DIGITAL),
        (2, "e. SNS 이벤트", 18, S_SNS),
        (2, "f. 언론 지면/배너", 19, S_PRESS),
        (2, "사업 관리", 20, S_CONSULT),
        # IV
        (2, "IV-a. 예산 집행 (간트)", 21, S_GANTT),
        (2, "IV-b. 결과 분석", 22, S_FEEDBACK),
        (2, "IV-c. 홍보단 운영", 23, S_ETC),
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
    conn = get_conn()
    for title, ver, label, cc, tl, cfn in [
        ("V19-1: 이름을 가려봐", "V19-1", "A", "이름을 가려봐.", "이름을 가려도 보이는 대학.", concept_A),
        ("V19-2: 같은 학교", "V19-2", "B", "같은 학교.", "같은 학교. 영산대학교.", concept_B),
        ("V19-3: 배우가 아닙니다", "V19-3", "C", "이 사람은 배우가 아닙니다.", "이 사람은 배우가 아닙니다.", concept_C),
    ]:
        cb, sb_body = cfn()
        pid = create(conn, title, ver, label, make_sections(cc, tl, cb, sb_body))
        print(f"{ver}: id={pid}")
    conn.commit()
    conn.close()
    print("Done.")
