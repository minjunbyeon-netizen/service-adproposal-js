"""V23: 5번 호기심갭 극대화 + 14번 숏폼화 + 홍보단 삭제 + 2번 중앙대 삭제. 24장."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.db import get_conn, init_db, migrate_db
from scripts.create_v8_to_v14 import RFP, SUMMARY, CONCEPTS, concept_A
from scripts.create_v18 import sian_slide, S_PRINT, S_DIGITAL, S_SNS, S_PRESS, S_CONSULT, S_FEEDBACK
from scripts.create_v19 import S_GANTT
from scripts.create_v20 import S_OPERATION, S_JIHYE
from scripts.create_v21 import S_COMPANY
from scripts.create_v22 import S_LOSS_V22, S_COCKTAIL_V22, S_YOUTUBE_V22

init_db()
migrate_db()

cb, sb_body = concept_A()
cc = "이름을 가려봐."
tl = "이름을 가려도 보이는 대학."
combined = f"**컨셉:** {cc}\n\n{cb}\n\n---\n\n**슬로건:** {tl}\n\n{sb_body}"

# ===== #2 제안배경 -- 중앙대 삭제 =====
S_BACKGROUND = (
    '<div style="padding:60px 0">'
    '<div style="font-size:28px;color:#58595B;line-height:2.4">'
    '홍익대 = <strong style="color:#1A1A1A">미대</strong><br>'
    '한양대 에리카 = <strong style="color:#1A1A1A">공대</strong><br>'
    '동의대 = <strong style="color:#1A1A1A">한의대</strong>'
    '</div>'
    '<div style="margin-top:48px;font-size:36px;color:#1A1A1A;font-weight:700">'
    '영산대 = <span style="display:inline-block;width:200px;border-bottom:3px solid #E84E10">&nbsp;</span>'
    '</div>'
    '<div style="margin-top:48px;font-size:22px;color:#58595B;line-height:1.8">'
    '이 빈칸을 채우는 것이<br>이번 제안의 전부입니다.'
    '</div>'
    '</div>'
)

# ===== #5 숫자 -- 호기심 갭 극대화 =====
# 965,525 -- 쉼표 하나 넣어서 금액이나 인구수처럼 보이게.
# 슬라이드에 이 숫자 외에 아무것도 없음. 완전한 침묵.
S_NUMBERS = (
    '<div style="display:flex;justify-content:center;align-items:center;height:100%;min-height:400px">'
    '<div style="text-align:center">'
    '<div style="font-size:180px;font-weight:700;color:#1A1A1A;letter-spacing:-2px;line-height:1;font-family:Roboto,sans-serif">'
    '965,525'
    '</div>'
    '</div>'
    '</div>'
)

# ===== #6 전환 -- 965,525 해체 =====
S_TRANSITION = (
    '<div style="padding:40px 0">'
    '<div style="font-size:20px;color:#58595B;margin-bottom:40px">'
    '방금 보신 <strong style="color:#1A1A1A">965,525</strong>는<br>'
    '금액이 아닙니다. 인구수도 아닙니다.'
    '</div>'
    '<div style="font-size:24px;color:#1A1A1A;line-height:2.6">'
    '<strong style="font-size:48px;color:#E84E10">96</strong>'
    '<span style="color:#58595B;font-size:18px"> -- 항공서비스학과 취업률 </span>'
    '<strong>96.4%</strong><br>'
    '<strong style="font-size:48px;color:#E84E10">5,5</strong>'
    '<span style="color:#58595B;font-size:18px"> -- QS 호스피탈리티 세계 </span>'
    '<strong>55위</strong><br>'
    '<strong style="font-size:48px;color:#E84E10">25</strong>'
    '<span style="color:#58595B;font-size:18px"> -- 호텔 총지배인 배출 </span>'
    '<strong>25명</strong>'
    '</div>'
    '<div style="margin-top:48px;font-size:28px;font-weight:700;color:#1A1A1A">'
    '영산대학교입니다.'
    '</div>'
    '<div style="margin-top:16px;font-size:18px;color:#58595B">'
    '이 숫자를 몰랐다면, 그것이 기회입니다.'
    '</div>'
    '</div>'
)

# ===== #14 졸업선배 숏폼 (4편, 9-12월, 릴스/숏폼) =====
S_DOCU = (
    "### 졸업선배 숏폼 시리즈 (연 4편)\n\n"
    "**9월~12월 -- 입시 시즌에 맞춰 월 1편 공개**\n"
    "**포맷:** 60초 릴스/숏폼 (9:16)\n\n"
    "| 월 | 학과 | 현장 | 핵심 장면 |\n|---|------|------|----------|\n"
    "| 9월 | 항공서비스 | 기내 | 승무원 일상 60초 |\n"
    "| 10월 | 호텔관광 | 호텔 로비 | 지배인 하루 60초 |\n"
    "| 11월 | 경찰행정 | 순찰 현장 | 경위 하루 60초 |\n"
    "| 12월 | 뷰티디자인 | 본인 매장 | 대표 하루 60초 |\n\n"
    "인스타 릴스 + 유튜브 쇼츠 + 틱톡 동시 업로드.\n"
    "정시 원서 접수 직전까지 4편 완성."
)


def make_sections():
    return [
        (2, "I. 제안배경", 1, S_BACKGROUND),
        (2, "II. 제안업체 일반", 2, S_COMPANY),
        (1, "III. 세부 과업 수행 계획", 3, None),
        (2, "965,525", 4, S_NUMBERS),
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
        (2, "졸업선배 숏폼", 13, S_DOCU),
        (2, "b. 유튜브 콘텐츠", 14, S_YOUTUBE_V22),
        (2, "c. 광고 디자인/인쇄", 15, S_PRINT),
        (2, "d. 디지털 광고", 16, S_DIGITAL),
        (2, "e. SNS 이벤트", 17, S_SNS),
        (2, "f. 언론 지면/배너", 18, S_PRESS),
        (2, "사업 관리", 19, S_CONSULT),
        (2, "IV-a. 예산 집행 (간트)", 20, S_GANTT),
        (2, "IV-b. 결과 분석", 21, S_FEEDBACK),
        (2, "IV-b2. 운영방안", 22, S_OPERATION),
        # 홍보단 삭제
    ]


if __name__ == "__main__":
    conn = get_conn()
    sections = make_sections()
    cur = conn.execute(
        "INSERT INTO proposals (title,version,status,rfp_json,rfp_summary,raw_text,selected_concept) VALUES (?,?,?,?,?,?,?)",
        ("V23", "V23", "ready", RFP, SUMMARY, SUMMARY, "A"))
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
    print(f"V23: id={pid}")
