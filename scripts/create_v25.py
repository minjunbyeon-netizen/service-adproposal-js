"""V25: 시안 10,12 크리에이티브 디렉션 반영."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.db import get_conn, init_db, migrate_db
from scripts.create_v8_to_v14 import RFP, SUMMARY, CONCEPTS, concept_A
from scripts.create_v18 import grid16x9, grid9x16, S_PRINT, S_DIGITAL, S_SNS, S_PRESS, S_CONSULT, S_FEEDBACK
from scripts.create_v19 import S_GANTT
from scripts.create_v20 import S_OPERATION, S_JIHYE
from scripts.create_v21 import S_COMPANY
from scripts.create_v22 import S_LOSS_V22, S_COCKTAIL_V22, S_YOUTUBE_V22
from scripts.create_v23 import S_BACKGROUND, S_NUMBERS, S_TRANSITION, S_DOCU
from scripts.create_v24 import S_QS_RANKING

init_db()
migrate_db()

cb, sb_body = concept_A()
cc = "이름을 가려봐."
tl = "이름을 가려도 보이는 대학."
combined = f"**컨셉:** {cc}\n\n{cb}\n\n---\n\n**슬로건:** {tl}\n\n{sb_body}"

# ===== 시안 1: "3.6%" -- 오길비+머스크 종합 =====
S_36 = (
    # 순백 배경, 숫자만 떠 있는 구조. HTML로 직접 레이아웃.
    '<div style="display:flex;flex-direction:column;align-items:flex-start;padding:20px 0;min-height:420px">'

    # 메인 숫자 -- 부서져 떨어지는 듯한 느낌 (글자 간격, 기울기 미세 변화)
    '<div style="position:relative;margin-bottom:12px">'
    '<span style="font-size:200px;font-weight:700;color:#000;font-family:Roboto,sans-serif;letter-spacing:-4px;line-height:1;'
    'display:inline-block;'
    'background:linear-gradient(180deg,#000 60%,rgba(0,0,0,0.15) 100%);'
    '-webkit-background-clip:text;-webkit-text-fill-color:transparent">'
    '3.6%'
    '</span>'
    '</div>'

    # 서브 카피 1 -- 건조한 설명
    '<div style="font-size:18px;color:#6E6E73;line-height:1.8;margin-bottom:24px">'
    '항공서비스학과를 졸업하고,<br>'
    '취업하지 못한 사람의 비율.'
    '</div>'

    # 서브 카피 2 -- 반전 (검정 Bold)
    '<div style="font-size:24px;color:#000;font-weight:700;margin-bottom:48px">'
    '나머지 <span style="color:#E84E10">96.4%</span>는 일하고 있습니다.'
    '</div>'

    # 슬로건 서명
    '<div style="font-size:14px;color:#6E6E73;letter-spacing:1px">'
    '이름을 가려도 보이는 대학.'
    '</div>'

    '</div>\n\n'

    # 이미지 그리드
    '<div class="sian-row">'
    + grid16x9("3.6%",
               "Pure white background, giant '3.6%' black typography center, "
               "letters slightly crumbling/dissolving at bottom edges like falling apart, "
               "minimal, cinematic, 16:9, no people")
    + grid9x16("3.6% (숏폼)",
               "White background, '3.6%' large dissolving typography, 9:16 vertical")
    + '</div>\n\n'

    '<div class="img-prompt"><span class="prompt-label">AI PROMPT</span>\n'
    '<div class="prompt-cmd">Pure white background, extremely large "3.6%" in black bold Roboto font, '
    'positioned center-left, the bottom edges of each character are subtly crumbling and dissolving '
    'into fine particles falling downward, like sand or ash breaking away, '
    'creating a sense of fragility and loss, minimal composition, '
    'no other elements, cinematic, 16:9 ratio, advertising poster style</div></div>'
)

# ===== 시안 3: "Room 1201" -- 머스크+드러커 종합 =====
S_ROOM = (
    # 다크 배경. 좌측 텍스트 + 우측 빈 공간(복도의 어둠)
    '<div style="background:#1A1A1A;color:#fff;padding:40px;border-radius:8px;min-height:420px;position:relative">'

    # Room 1201 메인
    '<div style="font-size:72px;font-weight:700;font-family:Roboto,sans-serif;letter-spacing:2px;margin-bottom:32px">'
    'Room 1201'
    '</div>'

    # 25줄 반복 리스트 -- 총지배인 명단
    '<div style="font-size:11px;color:#888;line-height:1.8;margin-bottom:24px;max-width:50%">'
    '총지배인 &nbsp; 파라다이스호텔 부산<br>'
    '총지배인 &nbsp; 해운대그랜드호텔<br>'
    '총지배인 &nbsp; 롯데호텔 부산<br>'
    '총지배인 &nbsp; 힐튼 부산<br>'
    '총지배인 &nbsp; 웨스틴조선 부산<br>'
    '총지배인 &nbsp; 시그니엘 부산<br>'
    '총지배인 &nbsp; 파크하얏트 부산<br>'
    '총지배인 &nbsp; 인터컨티넨탈 서울<br>'
    '총지배인 &nbsp; 메리어트 서울<br>'
    '총지배인 &nbsp; 쉐라톤 서울<br>'
    '총지배인 &nbsp; 노보텔 앰배서더<br>'
    '총지배인 &nbsp; 라마다 서울<br>'
    '총지배인 &nbsp; 베스트웨스턴 제주<br>'
    '총지배인 &nbsp; 켄싱턴호텔 경주<br>'
    '총지배인 &nbsp; 한화리조트 설악<br>'
    '총지배인 &nbsp; 롯데리조트 속초<br>'
    '총지배인 &nbsp; 신라스테이 광화문<br>'
    '총지배인 &nbsp; 포시즌스 서울<br>'
    '총지배인 &nbsp; 반얀트리 서울<br>'
    '총지배인 &nbsp; 콘래드 서울<br>'
    '총지배인 &nbsp; 페어몬트 앰배서더<br>'
    '총지배인 &nbsp; JW메리어트 서울<br>'
    '총지배인 &nbsp; 그랜드하얏트 서울<br>'
    '총지배인 &nbsp; 밀레니엄힐튼 서울<br>'
    '총지배인 &nbsp; 이비스 앰배서더'
    '</div>'

    # 펀치라인
    '<div style="font-size:28px;font-weight:700;color:#fff;margin-bottom:16px">'
    '25명. 전부 같은 학교.'
    '</div>'

    # 슬로건 서명
    '<div style="font-size:14px;color:#6E6E73;letter-spacing:1px">'
    '이름을 가려도 보이는 대학.'
    '</div>'

    # 우측 빈 공간은 CSS에서 자연스럽게 -- 텍스트가 좌측 50%만 차지

    '</div>\n\n'

    # 이미지 그리드
    '<div class="sian-row">'
    + grid16x9("Room 1201",
               "Dark background #1A1A1A, 'Room 1201' large white text top-left, "
               "25 lines of 'General Manager + Hotel Name' in small gray text listed below, "
               "right half completely empty dark space like hotel corridor darkness, "
               "minimal, cinematic, 16:9")
    + grid9x16("Room 1201 (숏폼)",
               "Dark background, Room 1201 top, 25 GM lines cascading down, 9:16")
    + '</div>\n\n'

    '<div class="img-prompt"><span class="prompt-label">AI PROMPT</span>\n'
    '<div class="prompt-cmd">Black background #1A1A1A, "Room 1201" in large white bold Roboto font top-left, '
    'below it 25 lines of small gray text listing "General Manager + Hotel Name" in Korean, '
    'right half of frame is pure empty darkness suggesting hotel corridor, '
    'bottom left "25. All from the same university." in white bold, '
    'luxury hotel lobby nameplate aesthetic, no people, no photos, 16:9</div></div>'
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
        (2, '"3.6%"', 9, S_36),
        (2, '"QS 55위"', 10, S_QS_RANKING),
        (2, '"Room 1201"', 11, S_ROOM),
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
    ]


if __name__ == "__main__":
    conn = get_conn()
    sections = make_sections()
    cur = conn.execute(
        "INSERT INTO proposals (title,version,status,rfp_json,rfp_summary,raw_text,selected_concept) VALUES (?,?,?,?,?,?,?)",
        ("V25", "V25", "ready", RFP, SUMMARY, SUMMARY, "A"))
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
    print(f"V25: id={pid}")
