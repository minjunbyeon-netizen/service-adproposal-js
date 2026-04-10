"""V22: 5번 호기심갭 강화 + 6번 공감 추가 + 8번 대비 반전 + 14번 현실화 + 15번 삭제 + 16번 축소."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.db import get_conn, init_db, migrate_db
from scripts.create_v8_to_v14 import RFP, SUMMARY, CONCEPTS, concept_A
from scripts.create_v18 import sian_slide, S_PRINT, S_DIGITAL, S_SNS, S_PRESS, S_CONSULT, S_FEEDBACK, S_ETC
from scripts.create_v19 import S_GANTT
from scripts.create_v20 import S_OPERATION
from scripts.create_v21 import S_BACKGROUND, S_COMPANY, S_LOSS

init_db()
migrate_db()

cb, sb_body = concept_A()
cc = "이름을 가려봐."
tl = "이름을 가려도 보이는 대학."
combined = f"**컨셉:** {cc}\n\n{cb}\n\n---\n\n**슬로건:** {tl}\n\n{sb_body}"

# ===== #5 숫자 -- 호기심 갭 강화 =====
# 숫자를 이어 붙여서 의미 불명으로 만든다. "뭐지?" 반응 유도.
S_NUMBERS = (
    '<div style="text-align:center;padding:60px 0">'
    '<div style="font-size:160px;font-weight:700;color:#1A1A1A;letter-spacing:4px;line-height:1;font-family:Roboto,sans-serif">'
    '96<span style="color:#E84E10">.</span>'
    '55<span style="color:#E84E10">.</span>'
    '25'
    '</div>'
    '<div style="margin-top:60px;font-size:20px;color:#58595B">'
    '이 숫자가 무엇인지 아십니까?'
    '</div>'
    '</div>'
)

# ===== #6 전환 -- 호기심 갭 답 + 피크 =====
# 5번의 답을 여기서 준다. 그러나 바로 주지 않고 한 줄씩.
S_TRANSITION = (
    '<div style="padding:40px 0">'
    '<div style="font-size:22px;color:#58595B;line-height:2.6">'
    '96 -- 항공서비스학과 취업률 <strong style="color:#1A1A1A">96.4%</strong><br>'
    '55 -- QS 호스피탈리티 <strong style="color:#1A1A1A">세계 55위</strong><br>'
    '25 -- 호텔 총지배인 배출 <strong style="color:#1A1A1A">25명 (국내 최다)</strong>'
    '</div>'
    '<div style="margin:48px 0">'
    '<span style="font-size:42px;font-weight:700;color:#1A1A1A">영산대학교입니다.</span>'
    '</div>'
    '<div style="font-size:22px;color:#58595B;line-height:2">'
    '이 숫자를 처음 들으셨다면,<br>'
    '그것이 문제입니다.<br><br>'
    '그리고 그것이 <strong style="color:#E84E10">기회</strong>입니다.'
    '</div>'
    '</div>'
)

# ===== #7 같은 숫자, 다른 반응 -- 공감 한 줄 추가 =====
S_LOSS_V22 = (
    '<div style="display:flex;gap:40px;padding:20px 0;align-items:stretch">'
    '<div style="flex:1;background:#F5F5F5;border-radius:8px;padding:40px;text-align:center">'
    '<div style="font-size:14px;color:#58595B;letter-spacing:2px;margin-bottom:16px">모든 대학이 말하는 방식</div>'
    '<div style="font-size:72px;font-weight:700;color:#58595B;line-height:1">96.4%</div>'
    '<div style="font-size:20px;color:#58595B;margin-top:16px">취업률</div>'
    '<div style="margin-top:32px;font-size:16px;color:#6E6E73;line-height:1.8">'
    '"좋은 학교네요."<br>(고개를 끄덕이고 넘긴다)'
    '</div>'
    '</div>'
    '<div style="flex:1;background:#1A1A1A;border-radius:8px;padding:40px;text-align:center">'
    '<div style="font-size:14px;color:#E84E10;letter-spacing:2px;margin-bottom:16px">우리가 말하는 방식</div>'
    '<div style="font-size:72px;font-weight:700;color:#fff;line-height:1">3.6%</div>'
    '<div style="font-size:20px;color:#E84E10;margin-top:16px">탈락률</div>'
    '<div style="margin-top:32px;font-size:16px;color:#ccc;line-height:1.8">'
    '"3.6%밖에 안 돼?"<br><strong style="color:#fff">(멈춘다)</strong>'
    '</div>'
    '</div>'
    '</div>'
    '<div style="text-align:center;margin-top:24px;font-size:18px;color:#58595B">'
    '같은 숫자. 다른 반응.<br>'
    '사람은 얻는 것보다 <strong style="color:#E84E10">잃는 것</strong>에 2배 강하게 반응합니다.'
    '</div>'
    '<div style="text-align:center;margin-top:16px;font-size:16px;color:#6E6E73;font-style:italic">'
    '지금 고개를 끄덕이셨다면, 학부모도 똑같이 반응합니다.'
    '</div>'
)

# ===== #8 신호와 소음 -- 대비 반전 + 연결 =====
S_COCKTAIL_V22 = (
    "**시끄러운 파티장에서도 내 이름은 들립니다.**\n\n"
    "심리학에서 이것을 **칵테일 파티 효과**라고 합니다.\n"
    "사람은 자신과 관련된 정보에만 반응합니다.\n\n"
    "수험생에게 '글로벌 경쟁력 강화'는 소음입니다.\n"
    "학부모에게 '브랜드 가치 제고'는 소음입니다.\n\n"
    "하지만,\n\n"
    "> \"이 학교 졸업생 100명 중 3명은 취업하지 못했습니다.\"\n\n"
    "이것은 소음이 아닙니다.\n"
    "내 아이의 미래에 직결되는 **신호**입니다.\n\n"
    "---\n\n"
    "우리는 앞서 말한 **빈칸** -- 영산대 = ?\n\n"
    "이것을 **소음이 아닌 신호**로 채우겠습니다.\n"
    "정보 전달이 아닌 **IMPACT**로.\n"
    "스쳐 지나가는 광고가 아닌, **기억에 남는 광고**로."
)

# ===== #13 "지혜" 영상 =====
from scripts.create_v20 import S_JIHYE

# ===== #14 졸업선배 다큐 -- 현실화 (10,11,12월 1편씩) =====
S_DOCU_V22 = (
    "### 월간 졸업선배 다큐 (연 3편)\n\n"
    "**10월, 11월, 12월 -- 정시 시즌에 맞춰 1편씩 공개**\n\n"
    "| 월 | 학과 | 졸업생 | 현장 |\n|---|------|--------|------|\n"
    "| 10월 | 항공서비스 | 대한항공 승무원 | 기내+공항 |\n"
    "| 11월 | 호텔관광 | 특급호텔 지배인 | 호텔 현장 |\n"
    "| 12월 | 경찰행정 | 해운대서 경위 | 순찰+사무실 |\n\n"
    "**포맷:** 하루 밀착 취재 -> 30분 풀버전(유튜브) + 3분 하이라이트(SNS) + 15초 숏폼\n\n"
    "정시 원서 접수 직전(12월)까지 3편 완성.\n"
    "수험생과 학부모가 가장 고민하는 시기에 '실제 졸업생의 현장'을 보여줍니다."
)

# ===== #15 (원래 16) 유튜브 -- 섭외 기반, 가상 2건만 =====
S_YOUTUBE_V22 = (
    "### b. 유튜브 콘텐츠 (인플루언서 협업)\n\n"
    "자체 제작이 아닌 **섭외/협업** 기반.\n\n"
    "| 인플루언서 | 구독자 | 콘텐츠 | 형식 |\n"
    "|-----------|--------|--------|------|\n"
    "| 진로탐구생활 (교육/진로) | 42만 | '숨은 명문대' 시리즈 -- 영산대 편 | 12분 |\n"
    "| 호텔리어K (호텔업계) | 18만 | '총지배인 25명의 학교' 탐방 | 15분 |\n\n"
    "섭외 확정 후 상세 기획 진행.\n"
    "팩트(취업률, QS 순위) 자연 노출 방식."
)


def make_sections():
    return [
        (2, "I. 제안배경", 1, S_BACKGROUND),
        (2, "II. 제안업체 일반", 2, S_COMPANY),
        (1, "III. 세부 과업 수행 계획", 3, None),
        (2, "96.55.25", 4, S_NUMBERS),
        (2, "전환", 5, S_TRANSITION),
        (2, "같은 숫자, 다른 반응", 6, S_LOSS_V22),
        (2, "신호와 소음", 7, S_COCKTAIL_V22),
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
        (2, "졸업선배 다큐", 13, S_DOCU_V22),
        # 15번(1학년vs졸업생) 삭제
        (2, "b. 유튜브 콘텐츠", 14, S_YOUTUBE_V22),
        (2, "c. 광고 디자인/인쇄", 15, S_PRINT),
        (2, "d. 디지털 광고", 16, S_DIGITAL),
        (2, "e. SNS 이벤트", 17, S_SNS),
        (2, "f. 언론 지면/배너", 18, S_PRESS),
        (2, "사업 관리", 19, S_CONSULT),
        (2, "IV-a. 예산 집행 (간트)", 20, S_GANTT),
        (2, "IV-b. 결과 분석", 21, S_FEEDBACK),
        (2, "IV-b2. 운영방안", 22, S_OPERATION),
        (2, "IV-c. 홍보단 운영", 23, S_ETC),
    ]


if __name__ == "__main__":
    conn = get_conn()
    sections = make_sections()
    cur = conn.execute(
        "INSERT INTO proposals (title,version,status,rfp_json,rfp_summary,raw_text,selected_concept) VALUES (?,?,?,?,?,?,?)",
        ("V22", "V22", "ready", RFP, SUMMARY, SUMMARY, "A"))
    pid = cur.lastrowid
    for lv, t, idx, content in sections:
        conn.execute(
            "INSERT INTO sections (proposal_id,level,title,order_idx,content,status) VALUES (?,?,?,?,?,?)",
            (pid, lv, t, idx, content, "done" if content else "pending"))
    for lb, ct, bd in CONCEPTS:
        conn.execute("INSERT OR REPLACE INTO concepts (proposal_id,label,title,body) VALUES (?,?,?,?)",
            (pid, lb, ct, bd))
    conn.commit()
    conn.close()
    print(f"V22: id={pid}")
