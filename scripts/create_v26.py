"""V26: 발표자 개선 6건 반영 + 발표 스크립트 삽입."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.db import get_conn, init_db, migrate_db
from scripts.create_v8_to_v14 import RFP, SUMMARY, CONCEPTS, concept_A
from scripts.create_v18 import grid16x9, grid9x16, S_PRINT, S_DIGITAL, S_SNS, S_PRESS, S_CONSULT, S_FEEDBACK
from scripts.create_v19 import S_GANTT
from scripts.create_v20 import S_OPERATION
from scripts.create_v21 import S_COMPANY
from scripts.create_v22 import S_YOUTUBE_V22
from scripts.create_v23 import S_DOCU

init_db()
migrate_db()

cb, sb_body = concept_A()
cc = "이름을 가려봐."
tl = "이름을 가려도 보이는 대학."
combined = f"**컨셉:** {cc}\n\n{cb}\n\n---\n\n**슬로건:** {tl}\n\n{sb_body}"

# 스크립트 사이드 패널 헬퍼
# 콘텐츠 본문과 분리된 우측 사이드바로 렌더링되도록 특수 마커 사용
def script(text):
    return f'<!--SCRIPT_START-->{text}<!--SCRIPT_END-->'

# ===== 1. 표지 (오프닝 스크립트) =====
# 표지 자체는 템플릿이 자동 생성하므로, 첫 콘텐츠 슬라이드에 스크립트 삽입하지 않음.
# 대신 제안배경 슬라이드에 오프닝 스크립트를 상단에 넣음.

# ===== 2. 제안배경 + 오프닝 스크립트 =====
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
    + script(
        '(표지가 뜬 상태에서, 인사 생략)<br><br>'
        '"<strong>영산대학교를 한 단어로 정의해 주십시오.</strong><br>'
        '-- 지금 떠오르지 않으셨다면, 그것이 이번 제안의 출발점입니다."<br><br>'
        '(2장으로 넘기며)<br>'
        '"홍대 하면 미대. 한양 에리카 하면 공대. 동의대 하면 한의대.<br>'
        '<strong>영산대 하면?</strong> 이 빈칸을 채우는 것이 저희가 하려는 일의 전부입니다."'
    )
)

# ===== 5. 965,525 (스크립트 추가) =====
S_NUMBERS = (
    '<div style="display:flex;justify-content:center;align-items:center;height:100%;min-height:400px">'
    '<div style="text-align:center">'
    '<div style="font-size:180px;font-weight:700;color:#1A1A1A;letter-spacing:-2px;line-height:1;font-family:Roboto,sans-serif">'
    '965,525'
    '</div>'
    '</div>'
    '</div>'
    + script(
        '(이 슬라이드에서 <strong>3초간 아무 말도 하지 않는다.</strong><br>'
        '평가위원이 "저게 뭐지?" 반응할 시간을 준다.)<br><br>'
        '"이 숫자가 무엇인지 아십니까?"<br>'
        '(1초 멈춤, 다음 장으로 넘긴다)'
    )
)

# ===== 6. 전환 -- 965,525 해체 (개선: 착각->정답->브릿지 3초 완결) =====
S_TRANSITION = (
    '<div style="padding:40px 0">'
    '<div style="font-size:20px;color:#58595B;margin-bottom:32px">'
    '방금 보신 <strong style="color:#1A1A1A">965,525</strong>는<br>'
    '금액이 아닙니다. 인구수도 아닙니다.<br>'
    '<strong>세 개의 숫자</strong>입니다.'
    '</div>'
    '<div style="font-size:24px;color:#1A1A1A;line-height:2.6">'
    '<strong style="font-size:48px;color:#E84E10">96</strong>'
    '<span style="color:#58595B;font-size:18px"> -- 항공서비스학과 취업률 </span>'
    '<strong>96.4%</strong><br>'
    '<strong style="font-size:48px;color:#E84E10">55</strong>'
    '<span style="color:#58595B;font-size:18px"> -- QS 호스피탈리티 세계 </span>'
    '<strong>55위</strong><br>'
    '<strong style="font-size:48px;color:#E84E10">25</strong>'
    '<span style="color:#58595B;font-size:18px"> -- 호텔 총지배인 배출 </span>'
    '<strong>25명</strong>'
    '</div>'
    '<div style="margin-top:40px;font-size:28px;font-weight:700;color:#1A1A1A">'
    '영산대학교입니다.'
    '</div>'
    '<div style="margin-top:12px;font-size:18px;color:#58595B">'
    '이 숫자를 몰랐다면, 그것이 <strong style="color:#E84E10">기회</strong>입니다.'
    '</div>'
    '</div>'
    + script(
        '"965,525는 금액이 아닙니다. <strong>세 개의 숫자</strong>입니다.<br>'
        '96 -- 취업률 96.4%.<br>'
        '55 -- QS 세계 55위.<br>'
        '25 -- 호텔 총지배인 25명.<br><br>'
        '<strong>영산대학교입니다.</strong><br>'
        '이 숫자를 지금 처음 들으셨다면, 그것이 바로 기회입니다."'
    )
)

# ===== 7. 신호와 소음 =====
S_COCKTAIL = (
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
    "기억에 남는 광고로."
    + script(
        '"학부모가 입시설명회에서 듣는 말의 대부분은 소음입니다.<br>'
        '글로벌 경쟁력, 브랜드 가치, MZ세대. 다 아는 이야기입니다.<br><br>'
        '하지만 <strong>\'100명 중 3명만 취업 못 했다\'</strong>는 신호입니다.<br>'
        '내 아이의 미래에 직결되는 정보이기 때문입니다.<br><br>'
        '저희는 이 빈칸을 소음이 아닌 신호로 채우겠습니다."'
    )
)

# ===== 8. 같은 숫자, 다른 반응 =====
S_LOSS = (
    '<div style="display:flex;gap:40px;padding:20px 0;align-items:stretch">'
    '<div style="flex:1;background:#F5F5F5;border-radius:8px;padding:40px;text-align:center">'
    '<div style="font-size:14px;color:#58595B;letter-spacing:2px;margin-bottom:16px">모든 대학이 말하는 방식</div>'
    '<div style="font-size:72px;font-weight:700;color:#58595B;line-height:1">96.4%</div>'
    '<div style="font-size:20px;color:#58595B;margin-top:16px">취업률</div>'
    '<div style="margin-top:32px;font-size:16px;color:#6E6E73;line-height:1.8">'
    '"좋은 학교네요."<br>(고개를 끄덕이고 넘긴다)'
    '</div></div>'
    '<div style="flex:1;background:#1A1A1A;border-radius:8px;padding:40px;text-align:center">'
    '<div style="font-size:14px;color:#E84E10;letter-spacing:2px;margin-bottom:16px">우리가 말하는 방식</div>'
    '<div style="font-size:72px;font-weight:700;color:#fff;line-height:1">3.6%</div>'
    '<div style="font-size:20px;color:#E84E10;margin-top:16px">탈락률</div>'
    '<div style="margin-top:32px;font-size:16px;color:#ccc;line-height:1.8">'
    '"3.6%밖에 안 돼?"<br><strong style="color:#fff">(멈춘다)</strong>'
    '</div></div></div>'
    '<div style="text-align:center;margin-top:24px;font-size:18px;color:#58595B">'
    '같은 숫자. 다른 반응.<br>'
    '사람은 얻는 것보다 <strong style="color:#E84E10">잃는 것</strong>에 2배 강하게 반응합니다.'
    '</div>'
    '<div style="text-align:center;margin-top:16px;font-size:16px;color:#6E6E73;font-style:italic">'
    '지금 고개를 끄덕이셨다면, 학부모도 똑같이 반응합니다.'
    '</div>'
    + script(
        '"왼쪽은 모든 대학이 하는 방식입니다. 취업률 96.4%.<br>'
        '오른쪽은 저희가 하는 방식입니다. <strong>탈락률 3.6%.</strong><br><br>'
        '같은 숫자입니다. 느낌이 다릅니다.<br>'
        '지금 고개를 끄덕이셨다면, 학부모도 똑같이 반응합니다."'
    )
)

# ===== 신규: 8.5장 브릿지 (8->9 사이) =====
S_BRIDGE = (
    '<div style="padding:60px 0;text-align:center">'
    '<div style="font-size:28px;color:#58595B;line-height:2.4">'
    '서울대 취업률 <strong style="color:#1A1A1A">96.4%</strong><br>'
    '고려대 취업률 <strong style="color:#1A1A1A">96.4%</strong><br>'
    '영산대 취업률 <strong style="color:#1A1A1A">96.4%</strong>'
    '</div>'
    '<div style="margin-top:48px;font-size:24px;color:#1A1A1A;font-weight:700">'
    '이름을 가리면 구별이 안 됩니다.'
    '</div>'
    '</div>'
    + script(
        '"서울대 96.4%, 고려대 96.4%, 영산대 96.4%.<br>'
        '<strong>이름을 가리면 구별이 안 됩니다.</strong><br><br>'
        '그래서 저희의 컨셉은 이것입니다."<br>'
        '(다음 장으로 넘긴다)'
    )
)

# ===== 9. 컨셉/슬로건 + 스크립트 =====
S_CONCEPT = (
    combined
    + script(
        '"저희의 컨셉은 <strong>이름을 가려봐</strong>입니다.<br>'
        '결과만 놓으면 명문대. 이름을 열면 영산대.<br>'
        '이 반전을 광고의 동력으로 쓰겠습니다.<br><br>'
        '슬로건은 <strong>이름을 가려도 보이는 대학.</strong><br>'
        '이제부터 이 컨셉으로 만든 시안 3종을 보여드리겠습니다."'
    )
)

# ===== 시안 공통 mockup 헬퍼 =====
# 16:9 가로형 + 9:16 세로형 모두 같은 높이(420px)로 화면 중앙 배치
def sian_mockups(label, h_content, v_content):
    return (
        '<div style="display:flex;justify-content:center;align-items:center;gap:32px;padding:20px 0">'
        # 16:9 가로형
        f'<div style="width:747px;height:420px;background:#F5F5F5;border:2px solid #E8E8E8;'
        f'border-radius:6px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
        f'position:relative;overflow:hidden">'
        f'<div style="position:absolute;top:8px;left:8px;font-size:9px;font-weight:700;letter-spacing:1px;'
        f'color:#fff;background:#58595B;padding:2px 8px;border-radius:2px">16:9 가로형 / {label}</div>'
        f'{h_content}'
        f'</div>'
        # 9:16 세로형 (같은 높이)
        f'<div style="width:236px;height:420px;background:#F5F5F5;border:2px solid #E8E8E8;'
        f'border-radius:6px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
        f'position:relative;overflow:hidden">'
        f'<div style="position:absolute;top:8px;left:8px;font-size:9px;font-weight:700;letter-spacing:1px;'
        f'color:#fff;background:#58595B;padding:2px 8px;border-radius:2px">9:16 세로형</div>'
        f'{v_content}'
        f'</div>'
        '</div>'
    )


# ===== 11. 시안 "3.6%" =====
_h_36 = (
    '<div style="font-size:120px;font-weight:700;color:#1A1A1A;font-family:Roboto,sans-serif;'
    'letter-spacing:-4px;line-height:1">3.6%</div>'
    '<div style="margin-top:16px;font-size:13px;color:#6E6E73">떨어질 확률입니다.</div>'
)
_v_36 = (
    '<div style="font-size:56px;font-weight:700;color:#1A1A1A;font-family:Roboto,sans-serif;'
    'letter-spacing:-2px;line-height:1">3.6%</div>'
    '<div style="margin-top:12px;font-size:11px;color:#6E6E73;text-align:center;padding:0 16px">떨어질 확률입니다.</div>'
)
S_36 = (
    sian_mockups("3.6%", _h_36, _v_36)
    + '<div style="text-align:center;font-size:13px;color:#58595B;font-style:italic;margin-top:16px;'
      'padding:8px 0;border-top:1px solid #E8E8E8">'
      '탈락률 3.6%. 이 숫자가 부서지는 순간, 96.4%가 보입니다.</div>'
    + script(
        '"(3초 침묵. 숫자를 보게 둔다.)<br><br>'
        '3.6%. 영산대 항공서비스학과에서 <strong>취업에 실패한 사람의 비율</strong>입니다.<br>'
        '나머지 96.4%는 지금 일하고 있습니다."'
    )
)

# ===== 12. 시안 "QS 55위" =====
_h_qs = (
    '<div style="padding:0 32px;width:100%">'
    '<div style="font-size:11px;color:#999;line-height:1.8;text-align:center">'
    '1st. MIT / USA<br>2nd. Imperial College London / UK<br>3rd. Stanford University / USA</div>'
    '<div style="text-align:center;padding:12px 0;font-size:14px;color:#ccc;letter-spacing:6px">.<br>.<br>.</div>'
    '<div style="text-align:center">'
    '<span style="font-size:56px;font-weight:700;color:#1A1A1A;font-family:Roboto">'
    '55<span style="font-size:28px;color:#58595B">th</span></span>'
    '<span style="font-size:36px;font-weight:700;color:#E84E10;margin-left:16px">YsU</span>'
    '<span style="font-size:16px;color:#58595B;margin-left:8px">/ BUSAN</span></div>'
    '<div style="text-align:center;font-size:10px;color:#bbb;line-height:1.8;margin-top:8px">'
    '56th. Oxford Brookes / UK<br>'
    '<span style="color:#ccc">57th. Lisboa / Portugal</span></div>'
    '</div>'
)
_v_qs = (
    '<div style="padding:0 10px;width:100%">'
    '<div style="font-size:8px;color:#999;line-height:1.8;text-align:center">'
    '1st. MIT<br>2nd. Imperial<br>3rd. Stanford</div>'
    '<div style="text-align:center;padding:6px 0;font-size:10px;color:#ccc;letter-spacing:4px">.<br>.<br>.</div>'
    '<div style="text-align:center">'
    '<div style="font-size:32px;font-weight:700;color:#1A1A1A;font-family:Roboto;line-height:1">'
    '55<span style="font-size:16px;color:#58595B">th</span></div>'
    '<div style="font-size:22px;font-weight:700;color:#E84E10;margin-top:4px">YsU</div>'
    '<div style="font-size:10px;color:#58595B">/ BUSAN</div></div>'
    '<div style="text-align:center;font-size:8px;color:#bbb;line-height:1.8;margin-top:6px">'
    '56th. Oxford Brookes<br>57th. Lisboa</div>'
    '</div>'
)
S_QS = (
    sian_mockups("QS 55위", _h_qs, _v_qs)
    + '<div style="text-align:center;font-size:13px;color:#58595B;font-style:italic;margin-top:16px;'
      'padding:8px 0;border-top:1px solid #E8E8E8">'
      'MIT 1위, Stanford 3위... 55위에 낯선 이름이 있습니다.</div>'
    + script(
        '"MIT, Imperial, Stanford.<br>'
        '이 리스트에 <strong>55위, 낯선 이름</strong>이 있습니다.<br>'
        'YsU. 부산. <strong>영산대학교입니다.</strong><br><br>'
        'QS 호스피탈리티 부문 세계 55위. 팩트입니다."'
    )
)

# ===== 13. 시안 "Room 1201" =====
_h_room = (
    '<div style="background:#1A1A1A;width:100%;height:100%;padding:24px;display:flex;flex-direction:column">'
    '<div style="font-size:36px;font-weight:700;color:#fff;font-family:Roboto;letter-spacing:1px;margin-bottom:12px">'
    'Room 1201</div>'
    '<div style="font-size:8px;color:#888;line-height:1.6;flex:1;column-count:2;column-gap:12px">'
    '총지배인 파라다이스 부산<br>총지배인 해운대그랜드<br>총지배인 롯데 부산<br>'
    '총지배인 힐튼 부산<br>총지배인 웨스틴조선<br>총지배인 시그니엘<br>'
    '총지배인 파크하얏트<br>총지배인 인터컨티넨탈<br>총지배인 메리어트<br>'
    '총지배인 쉐라톤 서울<br>총지배인 노보텔<br>총지배인 라마다 서울<br>'
    '총지배인 베스트웨스턴<br>총지배인 켄싱턴 경주<br>총지배인 한화리조트<br>'
    '총지배인 롯데리조트<br>총지배인 신라스테이<br>총지배인 포시즌스<br>'
    '총지배인 반얀트리<br>총지배인 콘래드<br>총지배인 페어몬트<br>'
    '총지배인 JW메리어트<br>총지배인 그랜드하얏트<br>총지배인 밀레니엄<br>'
    '총지배인 이비스</div>'
    '<div style="font-size:14px;font-weight:700;color:#fff;margin-top:8px">'
    '25명. 전부 같은 학교.</div>'
    '</div>'
)
_v_room = (
    '<div style="background:#1A1A1A;width:100%;height:100%;padding:16px;display:flex;flex-direction:column">'
    '<div style="font-size:20px;font-weight:700;color:#fff;font-family:Roboto;letter-spacing:1px;margin-bottom:10px">'
    'Room 1201</div>'
    '<div style="font-size:6.5px;color:#888;line-height:1.55;flex:1">'
    '총지배인 파라다이스<br>총지배인 해운대그랜드<br>총지배인 롯데 부산<br>'
    '총지배인 힐튼 부산<br>총지배인 웨스틴조선<br>총지배인 시그니엘<br>'
    '총지배인 파크하얏트<br>총지배인 인터컨티넨탈<br>총지배인 메리어트<br>'
    '총지배인 쉐라톤<br>총지배인 노보텔<br>총지배인 라마다<br>'
    '총지배인 베스트웨스턴<br>총지배인 켄싱턴<br>총지배인 한화리조트<br>'
    '총지배인 롯데리조트<br>총지배인 신라스테이<br>총지배인 포시즌스<br>'
    '총지배인 반얀트리<br>총지배인 콘래드<br>총지배인 페어몬트<br>'
    '총지배인 JW메리어트<br>총지배인 그랜드하얏트<br>총지배인 밀레니엄<br>'
    '총지배인 이비스</div>'
    '<div style="font-size:10px;font-weight:700;color:#fff;margin-top:6px">'
    '25명. 같은 학교.</div>'
    '</div>'
)
S_ROOM = (
    sian_mockups("Room 1201", _h_room, _v_room)
    + '<div style="text-align:center;font-size:13px;color:#58595B;font-style:italic;margin-top:16px;'
      'padding:8px 0;border-top:1px solid #E8E8E8">'
      '복도 끝까지 같은 직함. 같은 학교.</div>'
    + script(
        '"(5초간 침묵. 평가위원이 리스트를 훑을 시간을 준다.)<br><br>'
        '25명. 국내 호텔 총지배인 최다 배출.<br>'
        '<strong>전부 영산대학교 졸업생입니다.</strong>"'
    )
)

# ===== 13. 시안 종합 =====
from scripts.create_v25 import S_SIAN_SUMMARY
S_SIAN_SUMMARY_V26 = (
    S_SIAN_SUMMARY
    + script(
        '"3.6%, QS 55위, Room 1201.<br>'
        '같은 숫자를 다른 방식으로 느끼게 만드는 것.<br>'
        '이것이 저희가 준비한 <strong>크리에이티브 시안</strong>입니다."'
    )
)

# ===== 15. 영상 방향 + 컨셉 연결 보강 =====
S_VIDEO_INTRO = (
    "지면은 **편견을 부순다.**\n"
    "3.6%, QS 55위, Room 1201. 숫자로 멈추게 하고, 반전으로 기억에 남겼습니다.\n\n"
    "영상은 **편견 뒤에 있던 사람을 보여준다.**\n\n"
    "---\n\n"
    "WISE YOU.\n"
    "지혜로운 너.\n"
    "영산대학교가 밀고 있는 이 한 마디를,\n"
    "사람 이름으로 풀었습니다.\n\n"
    "> **\"우리는 모두 지혜입니다.\"**\n\n"
    "비행기에서, 호텔에서, 경찰서에서, 뷰티 매장에서.\n"
    "누군가 '지혜'를 부릅니다.\n"
    "뒤돌아보는 사람은 전부 영산대 졸업생입니다.\n\n"
    "이 슬로건으로 홍보영상을 제작했습니다."
    + script(
        '"지면 시안에서는 팩트의 임팩트로 편견을 부쉈습니다.<br>'
        '영상에서는 그 편견 뒤에 있던 <strong>사람</strong>을 보여드리겠습니다.<br><br>'
        'WISE YOU. 우리는 모두 지혜입니다.<br>'
        '각 취업 현장에서 \'지혜\'를 부르면, 영산대 졸업생이 뒤돌아봅니다.<br>'
        '이 슬로건으로 홍보영상을 제작했습니다."'
    )
)

# ===== 17. "지혜" 메인 영상 -- 16:9 비디오 플레이스홀더 =====
S_JIHYE = (
    '<div style="display:flex;justify-content:center;align-items:center;padding:20px 0">'
    '<div style="width:960px;height:540px;background:#1A1A1A;border-radius:6px;'
    'display:flex;flex-direction:column;justify-content:center;align-items:center;'
    'position:relative;overflow:hidden;border:2px solid #E8E8E8">'
    # 비율 라벨
    '<div style="position:absolute;top:12px;left:12px;font-size:10px;font-weight:700;'
    'letter-spacing:1px;color:#fff;background:#E84E10;padding:3px 10px;border-radius:2px">'
    '16:9 VIDEO</div>'
    # 중앙 재생 아이콘
    '<div style="width:88px;height:88px;border-radius:50%;background:rgba(255,255,255,.12);'
    'display:flex;justify-content:center;align-items:center;border:2px solid rgba(255,255,255,.5);'
    'margin-bottom:20px">'
    '<div style="width:0;height:0;border-left:28px solid #fff;border-top:18px solid transparent;'
    'border-bottom:18px solid transparent;margin-left:8px"></div>'
    '</div>'
    # 제목/슬로건
    '<div style="font-size:28px;font-weight:700;color:#fff;letter-spacing:1px;margin-bottom:8px">'
    '"지혜" 메인 영상 (60초)</div>'
    '<div style="font-size:14px;color:#999;letter-spacing:1px">'
    'WISE YOU &nbsp;|&nbsp; 우리는 모두 지혜입니다.</div>'
    # 하단 파일 경로 표시 (실제 파일 대체용)
    '<div style="position:absolute;bottom:12px;right:12px;font-size:10px;color:#666;font-family:monospace">'
    '[video file to insert]</div>'
    '</div></div>'
    # 간단 씬 요약
    '<div style="text-align:center;font-size:12px;color:#6E6E73;margin-top:12px;line-height:1.8">'
    '<strong style="color:#1A1A1A">씬 구성:</strong> '
    '비행기 "지혜야~" → 호텔 "박지혜 지배인님" → 경찰서 "지혜 경위" → 뷰티 "지혜 선생님" → '
    '<strong style="color:#E84E10">"우리는 모두 지혜입니다."</strong>'
    '</div>'
    + script(
        '"(영상 재생 -- 60초)<br><br>'
        '비행기에서, 호텔에서, 경찰서에서, 뷰티 매장에서.<br>'
        '누군가 <strong>\'지혜야\'</strong>를 부르면,<br>'
        '뒤돌아보는 사람은 전부 영산대 졸업생입니다.<br><br>'
        '<strong>우리는 모두 지혜입니다.</strong>"'
    )
)

# ===== 마지막: 빈칸 회수 =====
S_ENDING = (
    '<div style="padding:60px 0">'
    '<div style="font-size:28px;color:#58595B;line-height:2.4">'
    '홍익대 = <strong style="color:#1A1A1A">미대</strong><br>'
    '한양대 에리카 = <strong style="color:#1A1A1A">공대</strong><br>'
    '동의대 = <strong style="color:#1A1A1A">한의대</strong>'
    '</div>'
    '<div style="margin-top:48px;font-size:36px;font-weight:700">'
    '영산대 = <strong style="color:#E84E10">이름을 가려도 보이는 대학.</strong>'
    '</div>'
    '</div>'
    + script(
        '"(이 슬라이드에서 천천히)<br><br>'
        '처음에 빈칸이었습니다.<br>'
        '이제 채웠습니다.<br><br>'
        '<strong>영산대 = 이름을 가려도 보이는 대학.</strong><br><br>'
        '감사합니다."<br>'
        '(3초 정지. PT 종료.)'
    )
)


def make_sections():
    return [
        (2, "I. 제안배경", 1, S_BACKGROUND),
        (2, "II. 제안업체 일반", 2, S_COMPANY),
        (1, "III. 세부 과업 수행 계획", 3, None),
        (2, "965,525", 4, S_NUMBERS),
        (2, "전환", 5, S_TRANSITION),
        (2, "신호와 소음", 6, S_COCKTAIL),
        (2, "같은 숫자, 다른 반응", 7, S_LOSS),
        (2, "이름을 가리면", 8, S_BRIDGE),  # 신규 브릿지
        (2, "컨셉 / 슬로건", 9, S_CONCEPT),
        (2, '"3.6%"', 10, S_36),
        (2, '"QS 55위"', 11, S_QS),
        (2, '"Room 1201"', 12, S_ROOM),
        (2, "시안 종합", 13, S_SIAN_SUMMARY_V26),
        (1, "홍보영상", 14, None),
        (2, "영상 콘텐츠 방향", 15, S_VIDEO_INTRO),
        (2, '"지혜" 메인 영상', 16, S_JIHYE),
        (2, "졸업선배 숏폼", 17, S_DOCU),
        (2, "b. 유튜브 콘텐츠", 18, S_YOUTUBE_V22),
        (2, "c. 광고 디자인/인쇄", 19, S_PRINT),
        (2, "d. 디지털 광고", 20, S_DIGITAL),
        (2, "e. SNS 이벤트", 21, S_SNS),
        (2, "f. 언론 지면/배너", 22, S_PRESS),
        (2, "사업 관리", 23, S_CONSULT),
        (2, "IV-a. 예산 집행 (간트)", 24, S_GANTT),
        (2, "IV-b. 결과 분석", 25, S_FEEDBACK),
        (2, "IV-b2. 운영방안", 26, S_OPERATION),
        # 마지막: 빈칸 회수 (마무리 대체)
        (2, "영산대 =", 27, S_ENDING),
    ]


if __name__ == "__main__":
    conn = get_conn()
    sections = make_sections()
    cur = conn.execute(
        "INSERT INTO proposals (title,version,status,rfp_json,rfp_summary,raw_text,selected_concept) VALUES (?,?,?,?,?,?,?)",
        ("V26", "V26", "ready", RFP, SUMMARY, SUMMARY, "A"))
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
    print(f"V26: id={pid}")
