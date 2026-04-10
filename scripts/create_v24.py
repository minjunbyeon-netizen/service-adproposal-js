"""V24: 시안2를 QS 랭킹 리스트 방식으로 교체."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.db import get_conn, init_db, migrate_db
from scripts.create_v8_to_v14 import RFP, SUMMARY, CONCEPTS, concept_A
from scripts.create_v18 import sian_slide, grid16x9, grid9x16, S_PRINT, S_DIGITAL, S_SNS, S_PRESS, S_CONSULT, S_FEEDBACK
from scripts.create_v19 import S_GANTT
from scripts.create_v20 import S_OPERATION, S_JIHYE
from scripts.create_v21 import S_COMPANY
from scripts.create_v22 import S_LOSS_V22, S_COCKTAIL_V22, S_YOUTUBE_V22
from scripts.create_v23 import S_BACKGROUND, S_NUMBERS, S_TRANSITION, S_DOCU

init_db()
migrate_db()

cb, sb_body = concept_A()
cc = "이름을 가려봐."
tl = "이름을 가려도 보이는 대학."
combined = f"**컨셉:** {cc}\n\n{cb}\n\n---\n\n**슬로건:** {tl}\n\n{sb_body}"

# ===== 시안 2 교체: QS 랭킹 리스트 =====
S_QS_RANKING = (
    f"**{cc}**\n\n"
    "이 리스트에 어떤 대학이 있는지 보십시오.\n\n"
    '<div style="max-width:700px;margin:0 auto;padding:20px 0">'

    # 상위권 (작고 회색)
    '<div style="text-align:center;font-size:15px;color:#999;line-height:2.2">'
    '1st. MIT / USA<br>'
    '2nd. Imperial College London / UK<br>'
    '3rd. Stanford University / USA'
    '</div>'

    # 점점점 (생략)
    '<div style="text-align:center;padding:24px 0;font-size:18px;color:#ccc;letter-spacing:8px">'
    '.<br>.<br>.'
    '</div>'

    # 55위 -- 영산대 (크고 검정, 강조)
    '<div style="text-align:center;padding:20px 0">'
    '<span style="font-size:72px;font-weight:700;color:#1A1A1A;font-family:Roboto,sans-serif">'
    '55<span style="font-size:36px;color:#58595B">th</span>'
    '</span>'
    '<span style="font-size:48px;font-weight:700;color:#E84E10;margin-left:24px">'
    'YsU'
    '</span>'
    '<span style="font-size:24px;color:#58595B;margin-left:12px">'
    '/ BUSAN'
    '</span>'
    '</div>'

    # 하위 (작아지며 흐려짐)
    '<div style="text-align:center;font-size:14px;color:#bbb;line-height:2">'
    '56th. Oxford Brookes University / UK<br>'
    '<span style="color:#ccc">57th. Universidade de Lisboa / Portugal</span><br>'
    '<span style="color:#ddd;font-size:13px">58th. Kyung Hee University / Korea</span>'
    '</div>'

    '</div>\n\n'

    '<div style="text-align:center;margin-top:16px;font-size:14px;color:#6E6E73">'
    'QS World University Rankings by Subject 2025: Hospitality &amp; Leisure Management'
    '</div>\n\n'

    # 이미지 그리드
    '<div class="sian-row">'
    + grid16x9("QS 55위 랭킹 리스트",
               "Minimal ranking list, top universities fading small, 55th bold large center, YsU highlighted orange, clean white background, 16:9")
    + grid9x16("QS 55위 (숏폼)",
               "Ranking list vertical scroll, universities fading, 55th YsU bold center, 9:16")
    + '</div>\n\n'

    '<div class="img-prompt"><span class="prompt-label">AI PROMPT</span>\n'
    '<div class="prompt-cmd">Clean white background, university ranking list scrolling down, '
    'top entries (MIT, Imperial, Stanford) small gray text at top, dotted line indicating skip, '
    'then "55th: YsU / BUSAN" in large bold black text with orange accent, '
    'below entries fading smaller and lighter, minimalist typography poster, 16:9</div></div>'
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
        # 시안
        (2, '"3.6%"', 9, sian_slide(cc, "3.6%",
            "탈락률 3.6%. 영산대 항공서비스학과.",
            "Airport gate, '3.6%' large white typography center, cinematic, 16:9, no people",
            "Airport gate vertical, '3.6%' typography, 9:16 mobile format")),
        (2, '"QS 55위"', 10, S_QS_RANKING),
        (2, '"Room 1201"', 11, sian_slide(cc, "Room 1201",
            "호텔 복도 25개의 문. 전부 총지배인.",
            "Luxury hotel corridor, 25 doors, warm lighting, one-point perspective, 16:9",
            "Hotel corridor vertical, 9:16")),
        # 영상/과업
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
        ("V24", "V24", "ready", RFP, SUMMARY, SUMMARY, "A"))
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
    print(f"V24: id={pid}")
