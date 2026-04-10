"""V21: 심리효과 적용 디벨롭 (2,5,6페이지)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.db import get_conn, init_db, migrate_db
from scripts.create_v8_to_v14 import RFP, SUMMARY, CONCEPTS, concept_A
from scripts.create_v18 import sian_slide, S_YOUTUBE, S_PRINT, S_DIGITAL, S_SNS, S_PRESS, S_CONSULT, S_FEEDBACK, S_ETC
from scripts.create_v19 import S_GANTT
from scripts.create_v20 import S_COMPANY, S_NUMBERS, S_COCKTAIL, S_JIHYE, S_DOCU, S_OPERATION

init_db()
migrate_db()

cb, sb_body = concept_A()
cc = "이름을 가려봐."
tl = "이름을 가려도 보이는 대학."
combined = f"**컨셉:** {cc}\n\n{cb}\n\n---\n\n**슬로건:** {tl}\n\n{sb_body}"

# ===== #2 제안배경 -- 초두효과 + 인지적 용이성 =====
# 한 메시지. 여백. 빈칸이 메시지.
S_BACKGROUND = (
    '<div style="padding:60px 0">'
    '<div style="font-size:28px;color:#58595B;line-height:2.4">'
    '홍익대 = <strong style="color:#1A1A1A">미대</strong><br>'
    '한양대 에리카 = <strong style="color:#1A1A1A">공대</strong><br>'
    '동의대 = <strong style="color:#1A1A1A">한의대</strong><br>'
    '중앙대 = <strong style="color:#1A1A1A">연극영화</strong>'
    '</div>'
    '<div style="margin-top:48px;font-size:36px;color:#1A1A1A;font-weight:700">'
    '영산대 = <span style="display:inline-block;width:200px;border-bottom:3px solid #E84E10">&nbsp;</span>'
    '</div>'
    '<div style="margin-top:48px;font-size:22px;color:#58595B;line-height:1.8">'
    '이 빈칸을 채우는 것이<br>이번 제안의 전부입니다.'
    '</div>'
    '</div>'
)

# ===== #5 전환 -- 피크-엔드 + 호기심 갭 =====
# 질문으로 긴장, 빈 공간으로 멈춤, 답은 마지막에
S_TRANSITION = (
    '<div style="padding:40px 0">'
    '<div style="font-size:28px;color:#1A1A1A;line-height:2.2">'
    '방금 보신 숫자의 학교를<br>'
    '아직도 모르십니까?'
    '</div>'
    '<div style="margin:48px 0;font-size:28px;color:#58595B;line-height:2.2">'
    '그 학교의 광고를<br>'
    '본 적이 있으십니까?'
    '</div>'
    '<div style="margin:48px 0">'
    '<span style="font-size:48px;font-weight:700;color:#E84E10">없습니다.</span>'
    '</div>'
    '<div style="font-size:22px;color:#1A1A1A;line-height:2">'
    '그것이 문제입니다.<br>'
    '그리고 그것이 <strong>기회</strong>입니다.'
    '</div>'
    '</div>'
)

# ===== #6 손실 회피 -- 대비 효과 =====
# 좌우 대비. 텍스트가 아닌 시각으로 보여줌.
S_LOSS = (
    '<div style="display:flex;gap:40px;padding:20px 0;align-items:stretch">'
    # 왼쪽: 96.4%
    '<div style="flex:1;background:#F5F5F5;border-radius:8px;padding:40px;text-align:center">'
    '<div style="font-size:14px;color:#58595B;letter-spacing:2px;margin-bottom:16px">모든 대학이 말하는 방식</div>'
    '<div style="font-size:72px;font-weight:700;color:#58595B;line-height:1">96.4%</div>'
    '<div style="font-size:20px;color:#58595B;margin-top:16px">취업률</div>'
    '<div style="margin-top:32px;font-size:16px;color:#6E6E73;line-height:1.8">'
    '"좋은 학교네요."<br>(고개를 끄덕이고 넘긴다)'
    '</div>'
    '</div>'
    # 오른쪽: 3.6%
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
)


def make_sections():
    return [
        (2, "I. 제안배경", 1, S_BACKGROUND),
        (2, "II. 제안업체 일반", 2, S_COMPANY),
        (1, "III. 세부 과업 수행 계획", 3, None),
        (2, "96 / 55 / 25", 4, S_NUMBERS),
        (2, "전환", 5, S_TRANSITION),
        (2, "같은 숫자, 다른 반응", 6, S_LOSS),
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
        ("V21", "V21", "ready", RFP, SUMMARY, SUMMARY, "A"))
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
    print(f"V21: id={pid}")
