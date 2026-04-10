"""V26: 발표자 개선 6건 반영 + 발표 스크립트 삽입."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.db import get_conn, init_db, migrate_db
from scripts.create_v8_to_v14 import RFP, SUMMARY, CONCEPTS, concept_A
from scripts.create_v18 import grid16x9, grid9x16, S_FEEDBACK
# S_PRINT, S_DIGITAL, S_SNS, S_PRESS, S_CONSULT는 V26에서 재작성
from scripts.create_v19 import S_GANTT
from scripts.create_v20 import S_OPERATION
# S_COMPANY는 V26에서 1~4 번호 구조로 재작성
# S_YOUTUBE, S_DOCU는 V26에서 재작성 (a/b/c/d 기호 제거)

init_db()
migrate_db()

cb, sb_body = concept_A()
cc = "이름을 가려봐."
tl = "이름을 가려도 보이는 대학."
# 슬라이드 10 -- 중복 숫자 4줄 삭제, 슬로건 한 줄만
combined = (
    '<div style="padding:20px 0">'
    # 컨셉 블록
    '<div style="margin-bottom:48px">'
    '<div style="font-size:13px;color:#E84E10;font-weight:700;letter-spacing:3px;margin-bottom:16px">'
    'CONCEPT · 컨셉</div>'
    '<div style="font-size:64px;font-weight:700;color:#1A1A1A;line-height:1.1;margin-bottom:28px;letter-spacing:-2px">'
    '이름을 가려봐.</div>'
    '<div style="font-size:22px;color:#58595B;line-height:1.8">'
    '<strong style="color:#1A1A1A">숫자를 보면 명문대. 이름을 보면 영산대.</strong><br>'
    '그래서 우리는, 이름을 가립니다.'
    '</div>'
    '</div>'
    # 구분선
    '<div style="height:1px;background:#E8E8E8;margin:0 0 36px"></div>'
    # 슬로건 블록 (중복 숫자 없음)
    '<div>'
    '<div style="font-size:13px;color:#E84E10;font-weight:700;letter-spacing:3px;margin-bottom:16px">'
    'SLOGAN · 슬로건</div>'
    '<div style="font-size:48px;font-weight:700;color:#1A1A1A;line-height:1.15;letter-spacing:-1px">'
    '이름을 가려도 보이는 대학.</div>'
    '</div>'
    '</div>'
)

# 스크립트 사이드 패널 헬퍼
def script(text):
    return f'<!--SCRIPT_START-->{text}<!--SCRIPT_END-->'

# 섹션 부모 (과업지시서 번호) 헬퍼
def parent(label):
    return f'<!--PARENT:{label}-->'

# 슬라이드 태그 (h3 아래 작은 차별화 라벨) 헬퍼
def tag(label):
    return f'<!--TAG:{label}-->'

# ===== #3 제안업체 일반 -- 1~4 row 구조 (간격 통일) =====
def _co_row(num, title, hint, body_html):
    return (
        '<div style="display:flex;align-items:flex-start;padding:14px 0;border-bottom:1px solid #E8E8E8;gap:24px">'
        # 좌측 번호+제목 고정 폭
        f'<div style="width:220px;flex-shrink:0">'
        f'<div style="font-size:13px;font-weight:700;color:#E84E10;letter-spacing:1px;line-height:1.4">'
        f'{num}. {title}</div>'
        + (f'<div style="font-size:11px;color:#6E6E73;margin-top:3px">{hint}</div>' if hint else '')
        + '</div>'
        # 우측 본문
        f'<div style="flex:1;min-width:0;font-size:13px;line-height:1.8;color:#1A1A1A">{body_html}</div>'
        '</div>'
    )

S_COMPANY = (
    '<div style="padding:4px 0;border-top:1px solid #E8E8E8">'
    + _co_row("1", "일반현황", "연혁 · 재무현황 · 매출액",
        '<span style="color:#6E6E73">상호</span> <strong>(주)하이브미디어</strong> · '
        '<span style="color:#6E6E73">설립</span> 2018.03 · '
        '<span style="color:#6E6E73">대표</span> 변민준 · '
        '<span style="color:#6E6E73">소재지</span> 부산 해운대구 · '
        '<span style="color:#6E6E73">자본금</span> 1억<br>'
        '<span style="color:#6E6E73">매출</span> 2023년 <strong>6.1억</strong> → 2024년 <strong>7.4억</strong> → 2025년 <strong>8.2억</strong>')
    + _co_row("2", "조직 및 인원", "총 12명",
        '총괄 PM <strong>1</strong> · 크리에이티브 <strong>3</strong> · '
        '매체/디지털 <strong>2</strong> · 영상 PD <strong>3</strong> · '
        'AE <strong>2</strong> · 재무/운영 <strong>1</strong>')
    + _co_row("3", "주요 사업내용", "",
        '통합 광고 기획 · 크리에이티브 제작 · 매체 집행 · '
        '영상 제작 (홍보/숏폼/다큐) · SNS 운영 · 인플루언서 협업 · 브랜드 컨설팅')
    + _co_row("4", "주요 실적", "사업명 · 기간 · 계약금액 · 발주처",
        '<table style="width:100%;border-collapse:collapse;font-size:12px">'
        '<tr><td style="padding:3px 0;width:55%"><strong>부산 강서구청 구정 홍보 광고대행</strong></td>'
        '<td style="padding:3px 0;color:#6E6E73;text-align:right">2024 ~ · 연 1.5억</td></tr>'
        '<tr><td style="padding:3px 0"><strong>OO대학교 입시 홍보 캠페인</strong></td>'
        '<td style="padding:3px 0;color:#6E6E73;text-align:right">2024 · 8천만</td></tr>'
        '<tr><td style="padding:3px 0"><strong>부산관광공사 관광 영상 3종</strong></td>'
        '<td style="padding:3px 0;color:#6E6E73;text-align:right">2023 · 5천만</td></tr>'
        '<tr><td style="padding:3px 0"><strong>OO병원 브랜드 리뉴얼</strong></td>'
        '<td style="padding:3px 0;color:#6E6E73;text-align:right">2023 ~ 2024 · 연 6천만</td></tr>'
        '<tr><td style="padding:3px 0"><strong>경남 OO시 관광 홍보</strong></td>'
        '<td style="padding:3px 0;color:#6E6E73;text-align:right">2022 ~ 2023 · 연 1억</td></tr>'
        '</table>')
    + '</div>'
    '<div style="margin-top:14px;font-size:11px;color:#6E6E73;font-style:italic;text-align:center">'
    '※ 조직도, 재무제표, 투입 인력 상세 프로필은 별도 보고서를 참고해 주십시오.'
    '</div>'
)

# ===== 재작성 콘텐츠 (a/b/c/d/e 기호 제거) =====

S_YOUTUBE_V22 = (
    "자체 제작이 아닌 **섭외/협업** 기반.\n\n"
    "| 인플루언서 | 구독자 | 콘텐츠 | 형식 |\n"
    "|-----------|--------|--------|------|\n"
    "| 진로탐구생활 (교육/진로) | 42만 | '숨은 명문대' 시리즈 -- 영산대 편 | 12분 |\n"
    "| 호텔리어K (호텔업계) | 18만 | '총지배인 25명의 학교' 탐방 | 15분 |\n\n"
    "섭외 확정 후 상세 기획 진행.\n"
    "팩트(취업률, QS 순위) 자연 노출 방식."
)

S_PRINT = (
    "**핵심 시안: \"3.6%\" 중심 배치**\n\n"
    "팩트와 임팩트가 가장 강력한 '3.6%' 시안을 인쇄 매체 주력으로.\n\n"
    "| 매체 | 시안 | 사양 |\n"
    "|------|------|------|\n"
    "| 버스쉘터 | 3.6% | 1200x1800mm, 양면 |\n"
    "| 지하철 역사 | 3.6% | 2400x1200mm |\n"
    "| 대학 내 현수막 | 3.6% + 슬로건 | 900x2400mm |\n"
    "| 입시요강 표지 | 3.6% 변형 | A4 |\n"
    "| 리플렛 | 4종 시안 종합 | 3단 접지 |\n\n"
    "숫자 '3.6%'의 시각적 충격을 오프라인에서 극대화.\n"
    "지나가는 사람이 멈추는 광고."
)

S_DIGITAL = (
    "**실험적 다품종: \"심사위원석\" + \"Room 1201\" 중심**\n\n"
    "디지털은 A/B 테스트가 가능. 여러 시안을 동시에 실험.\n\n"
    "| 플랫폼 | 시안 | 형식 | 목적 |\n"
    "|--------|------|------|------|\n"
    "| 유튜브 프리롤 | 심사위원석 | 15초 영상 | 권위 반전 |\n"
    "| 유튜브 프리롤 | Room 1201 | 15초 영상 | 밀도감 |\n"
    "| 인스타 피드 | 3.6% | 정방형 이미지 | 숫자 충격 |\n"
    "| 인스타 스토리 | 1학년 vs 졸업생 | 세로 영상 | 분할 대비 |\n"
    "| 페이스북 | 4종 캐러셀 | 스와이프 | 시안 순회 |\n"
    "| 네이버 DA | 3.6% 변형 | 배너 | 검색 연동 |\n\n"
    "2주 단위 성과 측정 → 상위 시안 예산 집중 배분."
)

# ===== SNS 이벤트 (상세 디벨롭) =====
S_SNS = (
    "**3채널 통합 운영 + 월 1회 참여형 이벤트**\n\n"
    "### 운영 채널\n\n"
    "| 채널 | 주 콘텐츠 | 포스팅 주기 | 목표 지표 |\n"
    "|------|-----------|------------|----------|\n"
    "| 인스타그램 | 시안 이미지, 릴스, 스토리 | 주 3회 | 팔로워 +500/월 |\n"
    "| 유튜브 쇼츠 | 숏폼, 졸업생 인터뷰 | 주 2회 | 조회수 3,000+/편 |\n"
    "| 네이버 블로그 | 팩트 카드뉴스, 입시 가이드 | 주 2회 | 검색 상위 노출 |\n\n"
    "### 월간 콘텐츠 캘린더\n\n"
    "| 월 | 테마 | 콘텐츠 | 이벤트 |\n"
    "|---|------|--------|--------|\n"
    "| 3~4월 | 입학 시즌 | 1학년 첫날 브이로그 | 신입생 인증샷 해시태그 |\n"
    "| 5~6월 | 수시 집중 | 취업률 팩트 카드뉴스 | 캠퍼스 투어 신청 이벤트 |\n"
    "| 7월 | 수시 마감 | 지원 마감 카운트다운 | 지원자 응원 댓글 |\n"
    "| 8~9월 | 원서 시즌 | 졸업생 현장 인터뷰 | 합격 기원 릴레이 |\n"
    "| 10~11월 | 정시 대비 | QS 순위/실적 정리 | 입시 상담 라이브 |\n"
    "| 12월 | 정시 마감 | 합격자 발표 준비 | 멘토 신청 접수 |\n"
    "| 1~2월 | 합격 시즌 | 합격 축하 콘텐츠 | 선배 멘토링 매칭 |\n\n"
    "### 이벤트 운영 원칙\n"
    "- 전부 **참여형** (댓글/해시태그/인증샷) -- 단순 노출 X\n"
    "- 경품 대신 **정보 보상** (입시 가이드, 선배 멘토링)\n"
    "- 수시 집중기(5~7월) **예산 70% 투입**\n"
    "- 학과별 민원 방지: 학과 로테이션 운영\n\n"
    "### 성과 측정\n"
    "월간 리포트 제공 · 분기별 전략 수정 · 연 2회 캠페인 리뷰"
)

S_PRESS = (
    "| 매체 | 형태 | 시기 | 시안 |\n"
    "|------|------|------|------|\n"
    "| 부산일보 | 15단 전면 | 수시 원서 접수 전 (6월) | 3.6% |\n"
    "| 국제신문 | 5단 통 | 정시 전 (12월) | 슬로건 |\n"
    "| 대학저널 | 1/2면 | 연 2회 | 4종 시안 종합 |\n"
    "| 네이버 메인 배너 | DA | 수시 기간 집중 | 심사위원석 |\n"
    "| 교육 전문 매체 | 기사형 광고 | 분기 1회 | QS 순위 팩트 |\n\n"
    "인쇄 매체는 '3.6%' 시안의 시각적 충격 극대화.\n"
    "디지털 배너는 클릭 유도형 카피 적용."
)

# ===== 사업 관리 (III-2 제거) =====
S_CONSULT = (
    "**학과 홍보 자문 및 컨설팅**\n"
    "- 학과별 차별화 포인트 발굴 자문 (월 1회 정기 미팅)\n"
    "- 입시 홍보물 카피/디자인 컨설팅\n"
    "- 학과 SNS 운영 가이드라인 제공\n\n"
    "**광고 효과 측정 및 경과 분석**\n"
    "- 매체별 노출/클릭/전환 대시보드 (월 2회 갱신)\n"
    "- 분기별 종합 리포트 + 전략 수정안\n"
    "- 입시 지원자 수 변동 추적 (광고 기여도 분석)\n\n"
    "**본교 요구 업무**\n"
    "- 긴급 제작물 48시간 내 납품\n"
    "- 학교 행사(입학식/졸업식/축제) 현장 촬영 지원\n"
    "- 교내 게시물 디자인 상시 지원"
)

# ===== 졸업선배 숏폼 (중복 방지) =====
S_DOCU = (
    "### 졸업선배 숏폼 시리즈 (연 4편)\n\n"
    "**9월~12월 -- 입시 시즌에 맞춰 월 1편 공개**\n"
    "**포맷:** 60초 릴스/숏폼 (9:16)\n\n"
    "| 월 | 학과 | 현장 | 핵심 장면 |\n"
    "|---|------|------|----------|\n"
    "| 9월 | 항공서비스 | 기내 | 승무원 일상 60초 |\n"
    "| 10월 | 호텔관광 | 호텔 로비 | 지배인 하루 60초 |\n"
    "| 11월 | 경찰행정 | 순찰 현장 | 경위 하루 60초 |\n"
    "| 12월 | 뷰티디자인 | 본인 매장 | 대표 하루 60초 |\n\n"
    "인스타 릴스 + 유튜브 쇼츠 + 틱톡 동시 업로드.\n"
    "정시 원서 접수 직전까지 4편 완성."
)

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
    '"좋은 학교네요."<br>(3초 후 잊어버린다)'
    '</div></div>'
    '<div style="flex:1;background:#1A1A1A;border-radius:8px;padding:40px;text-align:center">'
    '<div style="font-size:14px;color:#E84E10;letter-spacing:2px;margin-bottom:16px">우리가 말하는 방식</div>'
    '<div style="font-size:72px;font-weight:700;color:#fff;line-height:1">3.6%</div>'
    '<div style="font-size:20px;color:#E84E10;margin-top:16px">탈락률</div>'
    '<div style="margin-top:32px;font-size:16px;color:#ccc;line-height:1.8">'
    '"3.6%나 있다고?"<br><strong style="color:#fff">(멈춘다)</strong>'
    '</div></div></div>'
    '<div style="text-align:center;margin-top:24px;font-size:18px;color:#58595B">'
    '같은 숫자. 다른 반응.<br>'
    '사람은 얻는 것보다 <strong style="color:#E84E10">잃는 것</strong>에 2배 강하게 반응합니다.'
    '</div>'
    '<div style="text-align:center;margin-top:16px;font-size:16px;color:#6E6E73;font-style:italic">'
    '지금 <strong style="color:#E84E10">멈추셨다면</strong>, 학부모도 멈춥니다.'
    '</div>'
    + script(
        '"왼쪽은 모든 대학이 하는 방식입니다. 취업률 96.4%.<br>'
        '오른쪽은 저희가 하는 방식입니다. <strong>탈락률 3.6%.</strong><br><br>'
        '같은 숫자입니다. 느낌이 다릅니다.<br>'
        '지금 고개를 끄덕이셨다면, 학부모도 똑같이 반응합니다."'
    )
)

# ===== 9. 브릿지 -- 가려진 상태 → 드러난 상태 =====
S_BRIDGE = (
    '<div style="display:flex;gap:60px;padding:20px 0;align-items:center;justify-content:center">'
    # 왼쪽: 가린 상태
    '<div style="text-align:center;flex:1">'
    '<div style="font-size:12px;color:#6E6E73;letter-spacing:3px;margin-bottom:24px;text-transform:uppercase">'
    'BEFORE · 이름을 가려본다면</div>'
    '<div style="font-size:28px;line-height:2.2;color:#1A1A1A;font-weight:700">'
    '■■대학교 <span style="color:#E84E10">96.4%</span><br>'
    '■■대학교 <span style="color:#E84E10">96.4%</span><br>'
    '■■대학교 <span style="color:#E84E10">96.4%</span>'
    '</div>'
    '</div>'
    # 화살표
    '<div style="font-size:48px;color:#E84E10;font-weight:300">→</div>'
    # 오른쪽: 드러난 상태
    '<div style="text-align:center;flex:1">'
    '<div style="font-size:12px;color:#6E6E73;letter-spacing:3px;margin-bottom:24px;text-transform:uppercase">'
    'AFTER · 이름을 열면</div>'
    '<div style="font-size:28px;line-height:2.2;color:#1A1A1A;font-weight:700">'
    '서울대 <span style="color:#58595B">96.4%</span><br>'
    '고려대 <span style="color:#58595B">96.4%</span><br>'
    '영산대 <span style="color:#58595B">96.4%</span>'
    '</div>'
    '</div>'
    '</div>'
    '<div style="text-align:center;margin-top:48px;padding-top:24px;border-top:1px solid #E8E8E8">'
    '<div style="font-size:26px;color:#1A1A1A;font-weight:700;line-height:1.5">'
    '이름을 가리면, 구별이 안 됩니다.'
    '</div>'
    '<div style="font-size:18px;color:#58595B;margin-top:14px">'
    '그런데 왜, 수험생은 <strong style="color:#E84E10">이름만</strong> 봅니다.'
    '</div>'
    '<div style="font-size:13px;color:#6E6E73;margin-top:24px;font-style:italic">'
    '다음 장부터, 이름을 가린 광고 5편을 보여드립니다.'
    '</div>'
    '</div>'
    + script(
        '"<strong>이름을 가려본다면</strong> -- 서울대도 96.4%, 고려대도 96.4%, 영산대도 96.4%.<br>'
        '구별이 안 됩니다.<br><br>'
        '그런데 왜, 수험생은 <strong>이름만</strong> 봅니다.<br><br>'
        '그래서 저희는, 다음 장부터 <strong>이름을 가린 광고 5편</strong>을 보여드리겠습니다."'
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
# 16:9 가로형(1067x600) + 9:16 세로형(338x600) 같은 높이, 화면 거의 꽉 채움
def sian_mockups(label, h_content, v_content):
    return (
        '<div style="display:flex;justify-content:center;align-items:center;gap:24px;padding:8px 0">'
        # 16:9 가로형 (대형)
        f'<div style="width:1067px;height:600px;background:#F5F5F5;border:2px solid #E8E8E8;'
        f'border-radius:6px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
        f'position:relative;overflow:hidden">'
        f'<div style="position:absolute;top:10px;left:10px;font-size:10px;font-weight:700;letter-spacing:1px;'
        f'color:#fff;background:#58595B;padding:3px 10px;border-radius:2px">16:9 가로형 / {label}</div>'
        f'{h_content}'
        f'</div>'
        # 9:16 세로형 (같은 높이)
        f'<div style="width:338px;height:600px;background:#F5F5F5;border:2px solid #E8E8E8;'
        f'border-radius:6px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
        f'position:relative;overflow:hidden">'
        f'<div style="position:absolute;top:10px;left:10px;font-size:10px;font-weight:700;letter-spacing:1px;'
        f'color:#fff;background:#58595B;padding:3px 10px;border-radius:2px">9:16 세로형</div>'
        f'{v_content}'
        f'</div>'
        '</div>'
    )


# ===== 11. 시안 "3.6%" =====
_h_36 = (
    '<div style="font-size:180px;font-weight:700;color:#1A1A1A;font-family:Roboto,sans-serif;'
    'letter-spacing:-6px;line-height:1">3.6%</div>'
    '<div style="margin-top:20px;font-size:18px;color:#6E6E73">떨어질 확률입니다.</div>'
)
_v_36 = (
    '<div style="font-size:76px;font-weight:700;color:#1A1A1A;font-family:Roboto,sans-serif;'
    'letter-spacing:-3px;line-height:1">3.6%</div>'
    '<div style="margin-top:16px;font-size:13px;color:#6E6E73;text-align:center;padding:0 16px">떨어질 확률입니다.</div>'
)
S_36 = (
    sian_mockups("3.6%", _h_36, _v_36)
    + script(
        '<strong>[크리에이티브 브리프]</strong><br>'
        '탈락률 3.6%. 이 숫자가 부서지는 순간, 96.4%가 보입니다.<br><br>'
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
    + script(
        '<strong>[크리에이티브 브리프]</strong><br>'
        'MIT 1위, Stanford 3위... 55위에 낯선 이름이 있습니다.<br><br>'
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
    '<div style="font-size:16px;font-weight:700;color:#fff;margin-top:8px">'
    '25개의 이름. <span style="color:#E84E10">한 개의 학교.</span></div>'
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
    '<div style="font-size:10px;font-weight:700;color:#fff;margin-top:6px;line-height:1.3">'
    '25개의 이름.<br><span style="color:#E84E10">한 개의 학교.</span></div>'
    '</div>'
)
S_ROOM = (
    sian_mockups("Room 1201", _h_room, _v_room)
    + script(
        '<strong>[크리에이티브 브리프]</strong><br>'
        '복도 끝까지 같은 직함. 같은 학교.<br><br>'
        '"(5초간 침묵. 평가위원이 리스트를 훑을 시간을 준다.)<br><br>'
        '25명. 국내 호텔 총지배인 최다 배출.<br>'
        '<strong>전부 영산대학교 졸업생입니다.</strong>"'
    )
)

# ===== 13. 시안 종합 -- 6개 mockup 그리드 (3컨셉 × 2비율) =====
def _mini_card(title, h_html, v_html, dark=False):
    bg = "#1A1A1A" if dark else "#F5F5F5"
    return (
        '<div style="display:flex;flex-direction:column;align-items:center;gap:10px">'
        f'<div style="font-size:14px;font-weight:700;color:#1A1A1A;letter-spacing:1px">{title}</div>'
        # 16:9 (위) + 9:16 (아래)
        '<div style="display:flex;flex-direction:column;align-items:center;gap:8px">'
        f'<div style="width:420px;height:236px;background:{bg};border:1.5px solid #E8E8E8;'
        f'border-radius:4px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
        f'position:relative;overflow:hidden">'
        f'<div style="position:absolute;top:4px;left:4px;font-size:8px;font-weight:700;letter-spacing:1px;'
        f'color:#fff;background:#58595B;padding:1px 6px;border-radius:2px">16:9</div>'
        f'{h_html}'
        f'</div>'
        f'<div style="width:160px;height:285px;background:{bg};border:1.5px solid #E8E8E8;'
        f'border-radius:4px;display:flex;flex-direction:column;justify-content:center;align-items:center;'
        f'position:relative;overflow:hidden">'
        f'<div style="position:absolute;top:4px;left:4px;font-size:8px;font-weight:700;letter-spacing:1px;'
        f'color:#fff;background:#58595B;padding:1px 6px;border-radius:2px">9:16</div>'
        f'{v_html}'
        f'</div>'
        '</div>'
        '</div>'
    )

_sum_36_h = '<div style="font-size:80px;font-weight:700;color:#1A1A1A;font-family:Roboto">3.6%</div>'
_sum_36_v = '<div style="font-size:38px;font-weight:700;color:#1A1A1A;font-family:Roboto">3.6%</div>'
_sum_qs_h = (
    '<div style="text-align:center">'
    '<div style="font-size:10px;color:#999">MIT · Imperial · Stanford</div>'
    '<div style="font-size:9px;color:#ccc;margin:4px 0">. . .</div>'
    '<div style="font-size:28px;font-weight:700;color:#1A1A1A;font-family:Roboto">'
    '55<span style="font-size:14px">th</span> <span style="color:#E84E10">YsU</span></div>'
    '</div>'
)
_sum_qs_v = (
    '<div style="text-align:center">'
    '<div style="font-size:7px;color:#999">MIT</div>'
    '<div style="font-size:7px;color:#ccc">· · ·</div>'
    '<div style="font-size:18px;font-weight:700;color:#1A1A1A;font-family:Roboto;margin-top:4px">'
    '55<span style="font-size:10px">th</span></div>'
    '<div style="font-size:14px;font-weight:700;color:#E84E10">YsU</div>'
    '</div>'
)
_sum_room_h = (
    '<div style="text-align:center">'
    '<div style="font-size:24px;font-weight:700;color:#fff;font-family:Roboto;letter-spacing:1px">Room 1201</div>'
    '<div style="font-size:7px;color:#888;line-height:1.4;margin-top:6px">'
    '총지배인 파라다이스<br>총지배인 해운대그랜드<br>총지배인 롯데 부산<br>... 25명 ...</div>'
    '<div style="font-size:10px;color:#fff;font-weight:700;margin-top:6px">25개의 이름. 한 개의 학교.</div>'
    '</div>'
)
_sum_room_v = (
    '<div style="text-align:center">'
    '<div style="font-size:13px;font-weight:700;color:#fff;font-family:Roboto">Room 1201</div>'
    '<div style="font-size:5px;color:#888;line-height:1.4;margin-top:4px">'
    '25개 이름</div>'
    '<div style="font-size:7px;color:#fff;font-weight:700;margin-top:4px;line-height:1.3">한 개의<br>학교</div>'
    '</div>'
)

S_SIAN_SUMMARY_V26 = (
    '<div style="display:flex;justify-content:center;gap:24px;padding:16px 0;align-items:flex-start">'
    + _mini_card("3.6%", _sum_36_h, _sum_36_v)
    + _mini_card("QS 55위", _sum_qs_h, _sum_qs_v)
    + _mini_card("Room 1201", _sum_room_h, _sum_room_v, dark=True)
    + '</div>'
    + '<div style="text-align:center;margin-top:12px;font-size:17px;color:#1A1A1A;font-weight:700">'
      '세 장의 광고. 세 가지 증명.</div>'
    + '<div style="text-align:center;margin-top:6px;font-size:15px;color:#E84E10;font-weight:700">'
      '하나의 결론 -- 이름을 가려도 영산대입니다.</div>'
    + script(
        '"3.6%, QS 55위, Room 1201.<br>'
        '같은 숫자를 다른 방식으로 느끼게 만드는 것.<br>'
        '이것이 저희가 준비한 <strong>크리에이티브 시안</strong>입니다."'
    )
)

# ===== 15. 영상 방향 + 컨셉 연결 보강 =====
S_VIDEO_INTRO = (
    "**지면에서 우리는 이름을 가렸습니다.**\n\n"
    "3.6%, QS 55위, Room 1201. 숫자로 멈추게 하고, 반전으로 기억에 남겼습니다.\n\n"
    "**영상에서, 그 이름을 다시 불러봅니다.**\n\n"
    "---\n\n"
    "## 지혜.\n\n"
    "영산대학교가 밀고 있는 **WISE YOU**.\n"
    "이 한 마디를, 사람 이름으로 풀었습니다.\n\n"
    "비행기 객실에서, 호텔 로비에서, 웨딩홀 주방에서, 뷰티숍 거울 앞에서.\n"
    "누군가 '지혜'를 부릅니다.\n"
    "뒤돌아보는 사람은 전부 영산대 졸업생입니다.\n\n"
    "> **\"지혜를 부르면, 영산대가 대답합니다.\"**\n\n"
    "지혜를 4번 부르면, 4개 업계 1등이 돌아봅니다.\n"
    "-- 영산대학교."
    + script(
        '"지면에서 저희는 <strong>이름을 가렸습니다</strong>.<br>'
        '3.6%, 55위, Room 1201 -- 숫자로 증명했습니다.<br><br>'
        '영상에서는, 그 <strong>이름을 다시 불러봅니다</strong>.<br>'
        '비행기, 호텔, 웨딩홀, 뷰티숍 -- 네 번의 현장에서 \'지혜\'를 부르면,<br>'
        '뒤돌아보는 사람은 전부 영산대 졸업생입니다.<br><br>'
        '<strong>지혜를 부르면, 영산대가 대답합니다.</strong>"'
    )
)

# ===== 17. "지혜" 메인 영상 -- 16:9 비디오 플레이스홀더 (대형) =====
S_JIHYE = (
    '<div style="display:flex;justify-content:center;align-items:center;padding:0">'
    '<div style="width:1440px;height:810px;background:#1A1A1A;border-radius:6px;'
    'display:flex;flex-direction:column;justify-content:center;align-items:center;'
    'position:relative;overflow:hidden;border:2px solid #E8E8E8">'
    '<div style="position:absolute;top:16px;left:16px;font-size:11px;font-weight:700;'
    'letter-spacing:1px;color:#fff;background:#E84E10;padding:4px 12px;border-radius:2px">'
    '16:9 VIDEO</div>'
    '<div style="width:120px;height:120px;border-radius:50%;background:rgba(255,255,255,.12);'
    'display:flex;justify-content:center;align-items:center;border:3px solid rgba(255,255,255,.5);'
    'margin-bottom:28px">'
    '<div style="width:0;height:0;border-left:36px solid #fff;border-top:24px solid transparent;'
    'border-bottom:24px solid transparent;margin-left:10px"></div>'
    '</div>'
    '<div style="font-size:40px;font-weight:700;color:#fff;letter-spacing:1px;margin-bottom:12px">'
    '"지혜" 메인 영상 (60초)</div>'
    '<div style="font-size:18px;color:#999;letter-spacing:1px">'
    'WISE YOU &nbsp;|&nbsp; 우리는 모두 지혜입니다.</div>'
    '<div style="position:absolute;bottom:16px;right:16px;font-size:11px;color:#666;font-family:monospace">'
    '[video file to insert]</div>'
    '</div></div>'
    + script(
        '<strong>[씬 구성]</strong><br>'
        '비행기 "지혜야~" → 호텔 "박지혜 지배인님" → 경찰서 "지혜 경위" → 뷰티 "지혜 선생님" → '
        '<strong>"우리는 모두 지혜입니다."</strong><br><br>'
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
    # section_parent는 메인 로마 섹션만
    P_I = "I. 제안개요"
    P_II = "II. 제안업체 일반"
    P_III = "III. 세부 과업 수행 계획"
    P_IV = "IV. 사업 관리 계획"

    # III-1 bullet 항목 (= 슬라이드 h3 제목)
    T_SOURCE = "대학 광고에 필요한 소재 발굴 및 콘텐츠 기획"
    T_VIDEO = "대학 공식 홍보영상 기획 및 제작"
    T_YOUTUBE = "유튜브 콘텐츠 (인플루언서 협업 등) 기획 및 제작"
    T_PRINT = "대학 광고 디자인 및 광고 제작 (인쇄)"
    T_DIGITAL = "디지털 광고 (유튜브 · 인스타 · 페이스북) 콘텐츠 제작"
    T_SNS = "SNS 이벤트 및 콘텐츠 활성화"
    T_PRESS = "언론 지면 및 배너 광고 진행"
    T_MGMT = "사업 관리 계획"

    # IV bullet 항목
    T_IV_1 = "광고 운영 및 광고 예산 집행 계획(안)"
    T_IV_2 = "광고 결과 분석 및 피드백 적용"
    T_IV_3 = "기타 제안 사항"

    return [
        # I. 제안개요 (제목 삭제)
        (2, "", 1, parent(P_I) + S_BACKGROUND),
        # II. 제안업체 일반
        (2, "제안업체 일반", 2, parent(P_II) + S_COMPANY),
        # III. 세부 과업 수행 계획 (간지)
        (1, "III. 세부 과업 수행 계획", 3, None),

        # III. 1 - 소재 발굴 및 콘텐츠 기획 (빌드업 5장 + 컨셉 + 시안 4장 = 10장)
        (2, T_SOURCE, 4, parent(P_III) + tag("빌드업 · 호기심 갭") + S_NUMBERS),
        (2, T_SOURCE, 5, parent(P_III) + tag("빌드업 · 해체") + S_TRANSITION),
        (2, T_SOURCE, 6, parent(P_III) + tag("빌드업 · 칵테일 파티 효과") + S_COCKTAIL),
        (2, T_SOURCE, 7, parent(P_III) + tag("빌드업 · 손실 회피") + S_LOSS),
        (2, T_SOURCE, 8, parent(P_III) + tag("빌드업 · 이름을 가리면") + S_BRIDGE),
        (2, T_SOURCE, 9, parent(P_III) + tag("컨셉 · 슬로건 공개") + S_CONCEPT),
        (2, T_SOURCE, 10, parent(P_III) + tag('시안 1 · "3.6%"') + S_36),
        (2, T_SOURCE, 11, parent(P_III) + tag('시안 2 · "QS 55위"') + S_QS),
        (2, T_SOURCE, 12, parent(P_III) + tag('시안 3 · "Room 1201"') + S_ROOM),
        (2, T_SOURCE, 13, parent(P_III) + tag("시안 종합 (3종 × 2비율)") + S_SIAN_SUMMARY_V26),

        # III. 1 - 대학 공식 홍보영상 (간지)
        (1, "대학 공식 홍보영상", 14, None),
        (2, T_VIDEO, 15, parent(P_III) + tag("영상 콘텐츠 방향") + S_VIDEO_INTRO),
        (2, T_VIDEO, 16, parent(P_III) + tag('메인 영상 · "지혜" (60초)') + S_JIHYE),

        # 유튜브 / 인쇄 / 디지털 → 졸업선배 숏폼 → SNS → 언론
        (2, T_YOUTUBE, 17, parent(P_III) + tag("인플루언서 섭외") + S_YOUTUBE_V22),
        (2, T_PRINT, 18, parent(P_III) + tag('"3.6%" 중심 배치') + S_PRINT),
        (2, T_DIGITAL, 19, parent(P_III) + tag('"심사위원석" + "Room 1201" A/B 실험') + S_DIGITAL),
        # 졸업선배 숏폼 (디지털 뒤로 이동)
        (2, T_VIDEO, 20, parent(P_III) + tag("졸업선배 숏폼 · 9~12월 4편") + S_DOCU),
        # SNS (더 상세하게 디벨롭)
        (2, T_SNS, 21, parent(P_III) + tag("3채널 통합 운영 + 월간 캘린더") + S_SNS),
        # 언론
        (2, T_PRESS, 22, parent(P_III) + tag("수시/정시 시기별 매체") + S_PRESS),
        # 사업 관리 계획 (III-2 제거됨)
        (2, T_MGMT, 23, parent(P_III) + tag("자문 · 효과 측정 · 본교 업무") + S_CONSULT),

        # IV. 1
        (2, T_IV_1, 24, parent(P_IV) + tag("간트차트 · 수시 80% / 정시 20%") + S_GANTT),
        # IV. 2
        (2, T_IV_2, 25, parent(P_IV) + tag("측정 지표 · 2주 A/B 테스트") + S_FEEDBACK),
        # IV. 3
        (2, T_IV_3, 26, parent(P_IV) + tag("운영방안 · 108회 → 40,000회") + S_OPERATION),

        # 마무리
        (2, "", 27, S_ENDING),
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
