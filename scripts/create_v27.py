"""V27: 9페이지 세련화(같은 사실, 다른 언어) + 컨셉 단순화(증명)."""
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
        '<div style="display:flex;align-items:flex-start;padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8;gap:var(--s-3)">'
        # 좌측 번호+제목 고정 폭
        f'<div style="width:220px;flex-shrink:0">'
        f'<div class="t-caption w-bold is-accent" style="letter-spacing:1px">{num}. {title}</div>'
        + (f'<div class="t-overline w-regular is-muted" style="letter-spacing:0;margin-top:3px">{hint}</div>' if hint else '')
        + '</div>'
        # 우측 본문
        f'<div class="t-caption is-ink" style="flex:1;min-width:0">{body_html}</div>'
        '</div>'
    )

S_COMPANY = (
    '<div style="padding:4px 0;border-top:1px solid #E8E8E8">'
    + _co_row("1", "일반현황", "연혁 · 재무현황 · 매출액",
        '<span class="is-muted">상호</span> <strong>(주)하이브미디어</strong> · '
        '<span class="is-muted">설립</span> 2018.03 · '
        '<span class="is-muted">대표</span> 변민준 · '
        '<span class="is-muted">소재지</span> 부산 해운대구 · '
        '<span class="is-muted">자본금</span> 1억<br>'
        '<span class="is-muted">매출</span> 2023년 <strong>6.1억</strong> → 2024년 <strong>7.4억</strong> → 2025년 <strong>8.2억</strong>')
    + _co_row("2", "조직 및 인원", "총 12명",
        '총괄 PM <strong>1</strong> · 크리에이티브 <strong>3</strong> · '
        '매체/디지털 <strong>2</strong> · 영상 PD <strong>3</strong> · '
        'AE <strong>2</strong> · 재무/운영 <strong>1</strong>')
    + _co_row("3", "주요 사업내용", "",
        '통합 광고 기획 · 크리에이티브 제작 · 매체 집행 · '
        '영상 제작 (홍보/숏폼/다큐) · SNS 운영 · 인플루언서 협업 · 브랜드 컨설팅')
    + _co_row("4", "주요 실적", "사업명 · 기간 · 계약금액 · 발주처",
        '<table class="t-overline w-regular" style="width:100%;border-collapse:collapse">'
        '<tr><td style="padding:3px 0;width:55%"><strong class="is-ink">부산 강서구청 구정 홍보 광고대행</strong></td>'
        '<td class="is-muted" style="padding:3px 0;text-align:right">2024 ~ · 연 1.5억</td></tr>'
        '<tr><td style="padding:3px 0"><strong class="is-ink">OO대학교 입시 홍보 캠페인</strong></td>'
        '<td class="is-muted" style="padding:3px 0;text-align:right">2024 · 8천만</td></tr>'
        '<tr><td style="padding:3px 0"><strong class="is-ink">부산관광공사 관광 영상 3종</strong></td>'
        '<td class="is-muted" style="padding:3px 0;text-align:right">2023 · 5천만</td></tr>'
        '<tr><td style="padding:3px 0"><strong class="is-ink">OO병원 브랜드 리뉴얼</strong></td>'
        '<td class="is-muted" style="padding:3px 0;text-align:right">2023 ~ 2024 · 연 6천만</td></tr>'
        '<tr><td style="padding:3px 0"><strong class="is-ink">경남 OO시 관광 홍보</strong></td>'
        '<td class="is-muted" style="padding:3px 0;text-align:right">2022 ~ 2023 · 연 1억</td></tr>'
        '</table>')
    + '</div>'
    '<div class="t-overline w-regular is-muted" style="letter-spacing:0;margin-top:var(--s-2);font-style:italic;text-align:center">'
    '※ 조직도, 재무제표, 투입 인력 상세 프로필은 별도 보고서를 참고해 주십시오'
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
    "팩트(취업률, QS 순위) 자연 노출 방식"
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
    "지나가는 사람이 멈추는 광고"
)

S_DIGITAL = (
    "**실험적 다품종: \"심사위원석\" + \"Room 1201\" 중심**\n\n"
    "디지털은 A/B 테스트가 가능 여러 시안을 동시에 실험.\n\n"
    "| 플랫폼 | 시안 | 형식 | 목적 |\n"
    "|--------|------|------|------|\n"
    "| 유튜브 프리롤 | 심사위원석 | 15초 영상 | 권위 반전 |\n"
    "| 유튜브 프리롤 | Room 1201 | 15초 영상 | 밀도감 |\n"
    "| 인스타 피드 | 3.6% | 정방형 이미지 | 숫자 충격 |\n"
    "| 인스타 스토리 | 1학년 vs 졸업생 | 세로 영상 | 분할 대비 |\n"
    "| 페이스북 | 4종 캐러셀 | 스와이프 | 시안 순회 |\n"
    "| 네이버 DA | 3.6% 변형 | 배너 | 검색 연동 |\n\n"
    "2주 단위 성과 측정 → 상위 시안 예산 집중 배분"
)

# ===== SNS 이벤트 (상세 디벨롭) =====
S_SNS = (
    '<div style="padding:4px 0">'
    '<div class="t-body w-bold" style="margin-bottom:var(--s-2)">'
    '3채널 통합 운영 + 참여형 이벤트 '
    '<span class="w-regular is-muted">· 수시 집중기(5~7월) 예산 70%</span></div>'
    # 운영 채널 (compact)
    '<table class="t-caption w-regular is-ink" style="width:100%;border-collapse:collapse;margin-bottom:var(--s-2)">'
    '<thead><tr>'
    '<th class="w-bold" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;text-align:left;width:22%">채널</th>'
    '<th class="w-bold" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;text-align:left">주 콘텐츠</th>'
    '<th class="w-bold" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;text-align:left;width:15%">주기</th>'
    '<th class="w-bold" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;text-align:left;width:20%">목표</th>'
    '</tr></thead><tbody>'
    '<tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8"><strong>인스타그램</strong></td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">시안 이미지 · 릴스 · 스토리</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">주 3회</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">팔로워 +500/월</td></tr>'
    '<tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8"><strong>유튜브 쇼츠</strong></td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">숏폼 · 졸업생 인터뷰</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">주 2회</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">조회수 3,000+/편</td></tr>'
    '<tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8"><strong>네이버 블로그</strong></td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">팩트 카드뉴스 · 입시 가이드</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">주 2회</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">검색 상위 노출</td></tr>'
    '</tbody></table>'
    # 월간 캘린더 (compact, 2컬럼 요약)
    '<div class="t-caption w-bold is-accent" style="margin-bottom:var(--s-1)">월간 콘텐츠 캘린더</div>'
    '<div class="t-caption w-regular is-ink" style="display:grid;grid-template-columns:1fr 1fr;gap:var(--s-1) var(--s-2);margin-bottom:var(--s-2)">'
    '<div>· <strong>3~4월</strong> 입학 -- 1학년 브이로그 / 인증샷 해시태그</div>'
    '<div>· <strong>5~6월</strong> 수시 -- 팩트 카드뉴스 / 캠퍼스 투어</div>'
    '<div>· <strong>7월</strong> 마감 -- 카운트다운 / 응원 댓글</div>'
    '<div>· <strong>8~9월</strong> 원서 -- 졸업생 인터뷰 / 합격 릴레이</div>'
    '<div>· <strong>10~11월</strong> 정시 -- QS 순위 / 상담 라이브</div>'
    '<div>· <strong>12월~2월</strong> 합격 -- 축하 콘텐츠 / 멘토 매칭</div>'
    '</div>'
    # 운영 원칙 (한 줄 박스)
    '<div class="t-caption w-regular is-ink" style="background:#F9F7F4;border-left:3px solid #E84E10;padding:var(--s-2) var(--s-2)">'
    '<strong>운영 원칙:</strong> 참여형 (댓글/해시태그/인증샷) · '
    '경품 대신 <strong class="is-accent">정보 보상</strong> (입시 가이드 DM) · '
    '학과 로테이션 · 월간 리포트 제공'
    '</div>'
    '</div>'
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
    "디지털 배너는 클릭 유도형 카피 적용"
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

# ===== 졸업선배 숏폼 #1: 계획 TEXT (V27 분할) =====
S_DOCU_PLAN = (
    '<div style="padding:var(--s-2) 0">'
    # 헤드라인
    '<div class="t-subtitle" style="margin-bottom:var(--s-1)">'
    '졸업선배 숏폼 시리즈 (연 4편)</div>'
    '<div class="t-caption is-muted" style="margin-bottom:var(--s-3)">'
    '9월~12월 · 입시 시즌 월 1편 공개 · 60초 세로형(9:16) · 인스타 릴스 + 유튜브 쇼츠 + 틱톡 동시 업로드</div>'
    # 상세 월별 테이블
    '<table class="t-caption w-regular is-ink" style="width:100%;border-collapse:collapse;margin-bottom:var(--s-3)">'
    '<thead><tr>'
    '<th class="w-bold" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;text-align:left;width:9%">월</th>'
    '<th class="w-bold" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;text-align:left;width:14%">학과</th>'
    '<th class="w-bold" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;text-align:left;width:14%">촬영 현장</th>'
    '<th class="w-bold" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;text-align:left">핵심 장면</th>'
    '<th class="w-bold" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;text-align:left;width:13%">업로드</th>'
    '<th class="w-bold" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;text-align:left;width:13%">목표 도달</th>'
    '</tr></thead>'
    '<tbody>'
    '<tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8"><strong>9월</strong></td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">항공서비스</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">기내</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">승무원의 하루 60초 (이륙부터 착륙까지)</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">9월 2주차</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">10,000+ 조회</td></tr>'
    '<tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8"><strong>10월</strong></td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">호텔관광</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">호텔 로비 · 룸</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">총지배인 아침 라운드 60초</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">10월 2주차</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">15,000+ 조회</td></tr>'
    '<tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8"><strong>11월</strong></td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">경찰행정</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">순찰 현장</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">경위 출근부터 순찰까지 60초</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">11월 2주차</td>'
    '<td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">8,000+ 조회</td></tr>'
    '<tr><td style="padding:var(--s-1) var(--s-2)"><strong>12월</strong></td>'
    '<td style="padding:var(--s-1) var(--s-2)">뷰티디자인</td>'
    '<td style="padding:var(--s-1) var(--s-2)">본인 매장</td>'
    '<td style="padding:var(--s-1) var(--s-2)">대표의 첫 손님부터 마감까지 60초</td>'
    '<td style="padding:var(--s-1) var(--s-2)">12월 1주차</td>'
    '<td style="padding:var(--s-1) var(--s-2)">12,000+ 조회</td></tr>'
    '</tbody></table>'
    # 운영 방침 박스
    '<div style="background:#F9F7F4;border-left:3px solid #E84E10;padding:var(--s-2) var(--s-2);margin-bottom:var(--s-2)">'
    '<div class="t-caption w-bold is-accent" style="margin-bottom:4px;letter-spacing:1px">운영 방침</div>'
    '<div class="t-caption is-ink">'
    '· 출연: 해당 업계 현직 <strong>영산대 졸업생</strong> 섭외 (섭외료 별도)<br>'
    '· 편집: 인트로 3초 훅 + 본편 50초 + 엔딩 7초 ("지혜가 실력이다")<br>'
    '· 채널: 인스타 릴스 / 유튜브 쇼츠 / 틱톡 <strong>3개 플랫폼 동시 업로드</strong><br>'
    '· 피드백: 업로드 후 2주차 성과 리포트 → 다음 편 기획 반영'
    '</div>'
    '</div>'
    '<div class="t-caption is-muted" style="text-align:center;font-style:italic">'
    '다음 장 → 9월·10월·11월 완성본 미리보기 (12월 편 제작 중)'
    '</div>'
    '</div>'
)

# ===== 졸업선배 숏폼 #2: 완성본 미리보기 (V27 신규) =====
S_DOCU_VIDEOS = (
    '<div style="padding:var(--s-1) 0">'
    # 헤드라인
    '<div class="t-subtitle" style="text-align:center;margin-bottom:var(--s-1)">'
    '졸업선배 숏폼 &nbsp;·&nbsp; 완성본 미리보기</div>'
    '<div class="t-caption is-muted" style="text-align:center;margin-bottom:var(--s-3)">'
    '9월·10월·11월 편 완성 · 12월 편 제작 중 · 각 60초 세로형 (9:16)</div>'
    # 3개 비디오 좌/중/우 가로 나란히
    '<div style="display:flex;justify-content:center;gap:var(--s-4);align-items:flex-start">'
    # 좌 · 9월 · 항공
    '<div style="display:flex;flex-direction:column;align-items:center">'
    '<div style="position:relative;width:340px;height:604px;background:#000;border-radius:6px;overflow:hidden;border:1px solid #E8E8E8">'
    '<video style="width:100%;height:100%;object-fit:cover;background:#000;display:block" '
    'src="/assets/video/KakaoTalk_20260410_151555089.mp4" controls preload="metadata"></video>'
    '<div class="t-overline" style="position:absolute;top:10px;left:10px;letter-spacing:1px;color:#fff;background:#E84E10;padding:3px 10px;border-radius:2px;pointer-events:none">'
    '9월</div>'
    '</div>'
    '<div class="t-caption w-bold is-ink" style="margin-top:var(--s-2)">항공서비스</div>'
    '<div class="t-overline is-muted" style="letter-spacing:1px;margin-top:2px">승무원의 하루</div>'
    '</div>'
    # 중 · 10월 · 호텔
    '<div style="display:flex;flex-direction:column;align-items:center">'
    '<div style="position:relative;width:340px;height:604px;background:#000;border-radius:6px;overflow:hidden;border:1px solid #E8E8E8">'
    '<video style="width:100%;height:100%;object-fit:cover;background:#000;display:block" '
    'src="/assets/video/KakaoTalk_20260410_180358236.mp4" controls preload="metadata"></video>'
    '<div class="t-overline" style="position:absolute;top:10px;left:10px;letter-spacing:1px;color:#fff;background:#E84E10;padding:3px 10px;border-radius:2px;pointer-events:none">'
    '10월</div>'
    '</div>'
    '<div class="t-caption w-bold is-ink" style="margin-top:var(--s-2)">호텔관광</div>'
    '<div class="t-overline is-muted" style="letter-spacing:1px;margin-top:2px">총지배인 아침 라운드</div>'
    '</div>'
    # 우 · 11월 · 경찰
    '<div style="display:flex;flex-direction:column;align-items:center">'
    '<div style="position:relative;width:340px;height:604px;background:#000;border-radius:6px;overflow:hidden;border:1px solid #E8E8E8">'
    '<video style="width:100%;height:100%;object-fit:cover;background:#000;display:block" '
    'src="/assets/video/KakaoTalk_20260410_182832774.mp4" controls preload="metadata"></video>'
    '<div class="t-overline" style="position:absolute;top:10px;left:10px;letter-spacing:1px;color:#fff;background:#E84E10;padding:3px 10px;border-radius:2px;pointer-events:none">'
    '11월</div>'
    '</div>'
    '<div class="t-caption w-bold is-ink" style="margin-top:var(--s-2)">경찰행정</div>'
    '<div class="t-overline is-muted" style="letter-spacing:1px;margin-top:2px">경위의 출근~순찰</div>'
    '</div>'
    '</div>'
    '</div>'
)

# ===== 1. 표지 (오프닝 스크립트) =====
# 표지 자체는 템플릿이 자동 생성하므로, 첫 콘텐츠 슬라이드에 스크립트 삽입하지 않음
# 대신 제안배경 슬라이드에 오프닝 스크립트를 상단에 넣음

# ===== 2-A. EVIDENCE: 사실은 이미 있다 =====
S_FACTS = (
    '<div style="padding:var(--s-5) 0;text-align:center">'
    '<div class="t-overline is-accent" style="margin-bottom:var(--s-5)">EVIDENCE</div>'
    # 진단 헤드라인 (page 3와 동일 스케일)
    '<div class="t-title" style="margin-bottom:var(--s-2)">'
    '영산대에는,<br>'
    '이미 <span class="is-accent">사실</span>이 있습니다</div>'
    '<div class="t-body is-muted" style="margin-bottom:var(--s-5)">'
    '— 말하지 않아도, 이미 있는 것들입니다</div>'
    # long divider (page 3 동일)
    '<div style="width:520px;height:1px;background:#E8E8E8;margin:0 auto var(--s-4)"></div>'
    # 화살표 (page 3 동일)
    '<div class="is-muted" style="font-size:32px;line-height:1;margin-bottom:var(--s-4)">↓</div>'
    # 4개 팩트 (t-subtitle -- page 3 미션과 동일 스케일)
    '<div class="t-subtitle w-regular" style="line-height:2">'
    '항공서비스학과 취업률 <span class="is-accent w-bold">96.4%</span><br>'
    'QS 호스피탈리티 부문 <span class="is-accent w-bold">글로벌 55위</span><br>'
    '호텔 총지배인 국내 최다 동문 <span class="is-accent w-bold">25명</span><br>'
    '校訓 <span class="is-accent w-bold">"지혜가 실력이다"</span>'
    '</div>'
    '</div>'
    + script(
        '(표지가 뜬 상태에서, 인사 생략)<br><br>'
        '"영산대학교에는 이미 <strong>사실</strong>이 있습니다<br><br>'
        '항공서비스학과 취업률 96.4% QS 호스피탈리티 부문 글로벌 55위 '
        '호텔 총지배인 국내 최다 동문 25명 그리고 校訓 <strong>지혜가 실력이다</strong>.<br><br>'
        '이것들은, 모두 <strong>이미 있는 것들</strong>입니다"'
    )
)

# ===== 2-B. PROBLEM: 사실 != 증명 + 미션 =====
S_PROBLEM = (
    '<div style="padding:var(--s-5) 0;text-align:center">'
    '<div class="t-overline is-accent" style="margin-bottom:var(--s-5)">PROBLEM</div>'
    # 진단 헤드라인
    '<div class="t-title" style="margin-bottom:var(--s-2)">'
    '그런데 사실만으로는,<br>'
    '아직 <span class="is-accent">증명</span>이 아닙니다</div>'
    '<div class="t-body is-muted" style="margin-bottom:var(--s-5)">'
    '— 보이지 않으면, 없는 것과 같습니다</div>'
    # long divider
    '<div style="width:520px;height:1px;background:#E8E8E8;margin:0 auto var(--s-4)"></div>'
    # 화살표
    '<div class="is-muted" style="font-size:32px;line-height:1;margin-bottom:var(--s-4)">↓</div>'
    # 미션
    '<div class="t-subtitle w-regular">'
    '사실을 <span class="is-accent w-bold">증명</span>으로 바꾸는 일<br>'
    '— 그것이, 이번 제안의 전부입니다'
    '</div>'
    '</div>'
    + script(
        '"그런데, <strong>사실만으로는 아직 증명이 아닙니다</strong>.<br>'
        '보이지 않으면, 없는 것과 같습니다<br><br>'
        '저희가 할 일은, 이 사실을 <strong>증명</strong>으로 바꾸는 것<br>'
        '그것이, 이번 제안의 전부입니다"'
    )
)

# ===== 5. 기억 테스트 -- "몇 개가 기억나십니까?" =====
S_NUMBERS = (
    '<div style="padding:var(--s-5) 0;text-align:center">'
    '<div class="t-overline is-accent" style="margin-bottom:var(--s-4)">TEST</div>'
    '<div class="t-heading" style="margin-bottom:var(--s-5)">'
    '2분 전, 여러분은<br>영산대학교의 사실을 보셨습니다</div>'
    '<div class="t-title">'
    '지금, <span class="is-accent">몇 개가 기억나십니까?</span></div>'
    '</div>'
    + script(
        '"2분 전, 저희는 영산대학교의 사실 네 가지를 보여드렸습니다<br><br>'
        '지금 이 자리에서, <strong>몇 개가 기억나시는지</strong> 여쭙고 싶습니다<br>'
        '(3초 멈춤 평가위원이 속으로 떠올릴 시간을 준다)<br><br>'
        '다 기억나지 않으셔도 괜찮습니다<br>'
        '이유는, 다음 장에서 말씀드리겠습니다"'
    )
)

# ===== 6. WHY -- 클리셰 진열 (1메시지) =====
S_TRANSITION = (
    '<div style="padding:var(--s-4) 0;text-align:center">'
    '<div class="t-overline is-accent" style="margin-bottom:var(--s-4)">WHY</div>'
    # 헤드라인
    '<div class="t-heading" style="margin-bottom:var(--s-3)">'
    '모든 대학이 <span class="is-accent">같은 말</span>을 하기 때문입니다</div>'
    # 주황 short bar
    '<div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div>'
    # 클리셰 박스
    '<div style="background:#F5F5F5;border-radius:8px;padding:var(--s-5) var(--s-6);max-width:760px;margin:0 auto">'
    '<div class="t-overline" style="margin-bottom:var(--s-3)">모든 대학이 이렇게 말합니다</div>'
    '<div class="t-body is-ink" style="line-height:2.2;text-align:left;padding:0 var(--s-2)">'
    '<span class="is-accent">●</span> &nbsp;글로벌 경쟁력 1위<br>'
    '<span class="is-accent">●</span> &nbsp;최고의 교수진<br>'
    '<span class="is-accent">●</span> &nbsp;미래형 인재 양성<br>'
    '<span class="is-accent">●</span> &nbsp;4차 산업혁명 선도<br>'
    '<span class="is-accent">●</span> &nbsp;국내 최고 수준 취업률'
    '</div>'
    '<div class="t-caption is-muted" style="margin-top:var(--s-3);padding-top:var(--s-2);border-top:1px solid #E0E0E0;font-style:italic">'
    '— 어느 대학인지 맞추실 수 있으십니까?</div>'
    '</div>'
    '</div>'
    + script(
        '"기억나지 않으셨다면, 당신 잘못이 아닙니다<br>'
        '사실이 많아서가 아니라, <strong>모든 대학이 같은 말</strong>을 하기 때문입니다<br><br>'
        '글로벌 경쟁력 1위, 최고의 교수진, 미래형 인재 양성, 4차 산업혁명 선도, 국내 최고 수준 취업률<br>'
        '이 카피가 어느 대학의 것인지, <strong>맞추실 수 있으십니까?</strong>"'
    )
)

# ===== 7. 기존 대학 광고 = 정보 나열형 =====
S_COCKTAIL = (
    '<div style="text-align:center;padding:var(--s-3) 0">'
    '<div class="t-body is-muted" style="letter-spacing:2px;margin-bottom:var(--s-5)">'
    '지금까지의 대학 광고는,</div>'
    # 중앙 거대 타이포
    '<div class="t-headline" style="margin-bottom:var(--s-6)">'
    '정보 나열형이었습니다</div>'
    # 5개 클리셰 (모든 대학이 하는 말)
    '<div style="background:#F5F5F5;border-radius:8px;padding:var(--s-5) var(--s-5);max-width:720px;margin:0 auto">'
    '<div class="t-overline" style="margin-bottom:var(--s-3)">'
    '모든 대학이 이렇게 말합니다</div>'
    '<div class="t-subtitle w-regular" style="line-height:2.2;text-align:left;padding:0 var(--s-3)">'
    '· &nbsp;글로벌 경쟁력 1위<br>'
    '· &nbsp;최고의 교수진<br>'
    '· &nbsp;미래형 인재 양성<br>'
    '· &nbsp;4차 산업혁명 선도<br>'
    '· &nbsp;국내 최고 수준 취업률'
    '</div>'
    '<div class="t-body is-muted" style="margin-top:var(--s-3);padding-top:var(--s-3);border-top:1px solid #E0E0E0;font-style:italic">'
    '어느 대학인지 맞추실 수 있으십니까?'
    '</div>'
    '</div>'
    '</div>'
    + script(
        '"지금까지의 대학 광고는 <strong>정보 나열형</strong>이었습니다<br><br>'
        '글로벌 경쟁력 1위, 최고의 교수진, 미래형 인재 양성, 4차 산업혁명 선도...<br>'
        '모든 대학이 이렇게 말합니다<br><br>'
        '어느 대학의 카피인지 <strong>맞출 수 있으십니까?</strong><br>'
        '아마 못 맞추실 겁니다 왜냐하면 -- "'
    )
)

# ===== 7. THE NOISE -- 2단 구조 (1메시지) =====
S_LOSS = (
    '<div style="padding:var(--s-5) 0;text-align:center">'
    '<div class="t-overline is-accent" style="margin-bottom:var(--s-6)">THE NOISE</div>'
    # 1단: 원인
    '<div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-5)">'
    '모든 대학이 같은 말을 하면,</div>'
    # 화살표
    '<div class="is-muted" style="font-size:32px;line-height:1;margin-bottom:var(--s-5)">↓</div>'
    # 2단: 결과 (거대)
    '<div class="t-display" style="color:#E84E10;margin-bottom:var(--s-5)">소음</div>'
    # short bar
    '<div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-4)"></div>'
    # 하단 한 줄
    '<div class="t-caption is-muted" style="font-style:italic">'
    '— 정보 나열은 광고가 아닙니다'
    '</div>'
    '</div>'
    + script(
        '"모든 대학이 같은 말을 하면, 결과는 <strong>소음</strong>입니다<br><br>'
        '정보 나열은 광고가 아닙니다<br>'
        '수험생과 학부모는 이미 이 소음에 지쳐 있습니다<br><br>'
        '그래서 저희는, <strong>뒤집었습니다</strong>."'
    )
)

# ===== 8. THE TURN -- 뒤집기 선언 =====
S_BRIDGE = (
    '<div style="padding:var(--s-5) 0;text-align:center">'
    '<div class="t-overline is-accent" style="margin-bottom:var(--s-6)">THE TURN</div>'
    '<div class="t-headline" style="margin-bottom:var(--s-6)">'
    '그래서 우리는,<br><span class="is-accent">뒤집었습니다</span></div>'
    '<div style="width:80px;height:1px;background:#E8E8E8;margin:0 auto var(--s-6)"></div>'
    '<div class="t-title w-regular is-muted">'
    '같은 사실,<br><span class="is-ink w-bold">다른 언어로</span></div>'
    '</div>'
    + script(
        '"소음에 지친 청중에게, 저희는 똑같이 외칠 수 없었습니다<br><br>'
        '그래서 <strong>뒤집었습니다</strong>.<br>'
        '같은 사실을, <strong>다른 언어</strong>로 옮겨왔습니다<br><br>'
        '지금부터, 그 방법의 이름과 세 가지 사례를 보여드리겠습니다"'
    )
)

# ===== 9-A. CONCEPT (증명 단독) =====
S_CONCEPT_ONLY = (
    '<div style="padding:var(--s-6) 0;text-align:center">'
    '<div class="t-overline is-accent" style="margin-bottom:var(--s-6)">CONCEPT</div>'
    '<div class="t-hero" style="margin-bottom:var(--s-5)">증명</div>'
    # 주황 short bar
    '<div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div>'
    '<div class="t-subtitle w-regular is-muted">'
    '— 주장이 아닌, 사실로 설득하는 일'
    '</div>'
    '</div>'
    + script(
        '"저희의 이번 광고 컨셉은, 한 단어입니다<br><br>'
        '<strong>증명</strong><br><br>'
        '주장이 아닌, <strong>사실로 설득하는 일</strong>입니다"'
    )
)

# ===== 9-B. METHOD (리프레이밍 단독) =====
S_METHOD_ONLY = (
    '<div style="padding:var(--s-5) 0;text-align:center">'
    '<div class="t-overline is-accent" style="margin-bottom:var(--s-5)">METHOD</div>'
    '<div class="t-title" style="margin-bottom:var(--s-4)">리프레이밍</div>'
    # 주황 short bar
    '<div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div>'
    '<div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-5);line-height:1.7">'
    '같은 사실을, 다른 프레임에 놓는 일<br>'
    '소음이 아닌, <span class="is-ink w-bold">각인</span>되게 만듭니다'
    '</div>'
    # long divider
    '<div style="width:520px;height:1px;background:#E8E8E8;margin:0 auto var(--s-4)"></div>'
    '<div class="t-caption" style="font-style:italic">'
    '<span class="is-accent">→</span> &nbsp;지금부터, 3가지 리프레이밍입니다'
    '</div>'
    '</div>'
    + script(
        '"앞 장의 \'다른 언어\'를, 저희는 <strong>리프레이밍(Re-framing)</strong>이라 부릅니다<br><br>'
        '행동경제학에서 검증된 기법으로, 같은 사실을 다른 프레임에 놓아 '
        '소음이 아닌 <strong>각인</strong>이 되게 합니다<br><br>'
        '지금부터, 3가지 리프레이밍을 보여드리겠습니다"'
    )
)

# ===== 브릿지: 3가지 리프레이밍 프리뷰 (소음 -> 각인) =====
S_REFRAMING_PREVIEW = (
    '<div style="padding:var(--s-4) 0;text-align:center">'
    '<div class="t-overline is-accent" style="margin-bottom:var(--s-4)">PREVIEW</div>'
    '<div class="t-heading" style="margin-bottom:var(--s-2)">'
    '3가지 리프레이밍</div>'
    '<div class="t-body is-muted" style="margin-bottom:var(--s-5)">'
    '— 같은 사실을, 다른 프레임에 놓는 일</div>'
    # 2-column bridge: 소음 -> 각인
    '<div style="display:grid;grid-template-columns:1fr 60px 1fr;'
    'align-items:center;max-width:1100px;margin:0 auto;gap:var(--s-2)">'
    # 헤더 행
    '<div class="t-overline is-muted" style="text-align:right">소음</div>'
    '<div></div>'
    '<div class="t-overline is-accent" style="text-align:left">각인</div>'
    # 구분선 행
    '<div style="height:1px;background:#E8E8E8"></div>'
    '<div></div>'
    '<div style="height:1px;background:#E84E10"></div>'
    # 1. 취업률 -> 탈락률
    '<div class="t-subtitle w-regular is-muted" style="text-align:right;padding:var(--s-2) var(--s-2)">'
    '<span class="t-caption is-subtle">01</span> &nbsp;96.4% 취업률</div>'
    '<div class="t-title is-accent" style="font-size:36px">→</div>'
    '<div class="t-subtitle w-bold is-ink" style="text-align:left;padding:var(--s-2) var(--s-2)">'
    '<span class="is-accent w-bold">3.6%</span> 탈락률</div>'
    # 2. 국내 55위 -> 글로벌 55위
    '<div class="t-subtitle w-regular is-muted" style="text-align:right;padding:var(--s-2) var(--s-2)">'
    '<span class="t-caption is-subtle">02</span> &nbsp;국내 55위 대학교</div>'
    '<div class="t-title is-accent" style="font-size:36px">→</div>'
    '<div class="t-subtitle w-bold is-ink" style="text-align:left;padding:var(--s-2) var(--s-2)">'
    '<span class="is-accent w-bold">글로벌 55위</span> 대학교</div>'
    # 3. 25명의 총지배인 -> 1개의 시스템
    '<div class="t-subtitle w-regular is-muted" style="text-align:right;padding:var(--s-2) var(--s-2)">'
    '<span class="t-caption is-subtle">03</span> &nbsp;25명의 총지배인</div>'
    '<div class="t-title is-accent" style="font-size:36px">→</div>'
    '<div class="t-subtitle w-bold is-ink" style="text-align:left;padding:var(--s-2) var(--s-2)">'
    '<span class="is-accent w-bold">1개의 시스템</span> (영산대)</div>'
    '</div>'
    '</div>'
    + script(
        '"저희가 보여드릴 3가지 리프레이밍입니다<br><br>'
        '첫째, 96.4% 취업률이 아니라 <strong>3.6% 탈락률</strong><br>'
        '둘째, 국내 55위가 아니라 <strong>글로벌 55위</strong><br>'
        '셋째, 25명의 총지배인이 아니라 <strong>1개의 시스템(영산대)</strong>입니다<br><br>'
        '지금부터, 각 시안으로 보여드리겠습니다"'
    )
)

# ===== 시안 이미지 공통 헬퍼 (V27: 16:9 이미지 1장 + 헤드라인 + 캡션) =====
def sian_image_slide(ref_num, headline_a, headline_b, image_path, caption):
    return (
        f'<div class="t-overline is-accent" style="text-align:center;margin-bottom:var(--s-2)">RE-FRAMING &nbsp;#{ref_num}</div>'
        f'<div class="t-title" style="text-align:center;margin-bottom:var(--s-3);line-height:1.25">'
        f'"{headline_a}"가 아니라,<br>'
        f'<span class="is-accent">"{headline_b}"</span>입니다</div>'
        # 16:9 이미지 프레임 (1067x600 ≈ 16:9)
        '<div style="display:flex;justify-content:center;padding:0">'
        '<div style="width:1067px;height:600px;background:#F5F5F5;border:1px solid #E8E8E8;'
        'border-radius:6px;overflow:hidden">'
        f'<img src="{image_path}" alt="{headline_b}" '
        'style="width:100%;height:100%;object-fit:cover;display:block">'
        '</div>'
        '</div>'
        f'<div class="t-body is-muted" style="text-align:center;margin-top:var(--s-3);font-style:italic">'
        f'{caption}'
        f'</div>'
    )

# ===== 시안 풀스크린 헬퍼 -- 검정 배경 + 모서리 그리드 (갤러리 스타일) =====
def sian_image_fullscreen(label, headline_a, headline_b, image_path, caption):
    # label "1-2" -> reframing_num "01", case_num "02"
    parts = label.split("-")
    reframing_num = parts[0].zfill(2)
    case_num = parts[1].zfill(2) if len(parts) > 1 else "01"
    # 시안별 미션 텍스트
    reframing_mission = {
        "1": "96.4% 취업률이 아니라, 3.6% 탈락률",
        "2": "국내 55위가 아니라, 글로벌 55위 대학교",
        "3": "25명의 총지배인이 아니라, 1개의 시스템",
    }.get(parts[0], "")
    return (
        '<div class="sian-full">'
        '<div class="sian-full__head">'
        f'<span class="sf-overline">RE-FRAMING &nbsp;#{reframing_num}</span>'
        f'<span class="sf-headline">{reframing_mission}</span>'
        '</div>'
        '<div class="sian-full__body">'
        '<div class="sian-full__frame">'
        f'<img src="{image_path}" alt="{headline_b}">'
        '<div class="corner-tr"></div>'
        '<div class="corner-bl"></div>'
        '</div>'
        '</div>'
        '<div class="sian-full__foot">'
        f'<span class="sf-label">CASE &nbsp;{reframing_num} · {case_num}</span>'
        '<span class="sf-mission">REFRAMING BY HIVE MEDIA</span>'
        '</div>'
        '</div>'
    )

# ===== 시안 1 · "3.6%" 이미지 3장 =====
SIAN_1_IMAGES = [
    "/assets/image/1/2.jpg",
    "/assets/image/1/Image_20260410_200932.jpg",
    "/assets/image/1/Image_20260410_210850.jpg",
]

# ===== 시안 2 · "글로벌 55위" 이미지 3장 =====
SIAN_2_IMAGES = [
    "/assets/image/2/Image_20260410_202519.jpg",
    "/assets/image/2/Image_20260410_202523.jpg",
    "/assets/image/2/Image_20260410_210840.jpg",
]

# ===== 시안 3 · "Room 1201" 이미지 6장 =====
SIAN_3_IMAGES = [
    "/assets/image/3/Image_20260410_203601.jpg",
    "/assets/image/3/Image_20260410_205236.jpg",
    "/assets/image/3/Image_20260410_210136.jpg",
    "/assets/image/3/Image_20260410_210524.jpg",
    "/assets/image/3/Image_20260410_210534.jpg",
    "/assets/image/3/Image_20260410_211835.jpg",
]

# ===== 시안 종합 (THREE PROOFS) -- 모든 이미지 줄별 컴팩트 =====
def _sian_thumb_small(image_path):
    return (
        '<div style="width:200px;height:113px;background:#F5F5F5;border:1px solid #E8E8E8;'
        'border-radius:4px;overflow:hidden;flex-shrink:0">'
        f'<img src="{image_path}" style="width:100%;height:100%;object-fit:cover;display:block">'
        '</div>'
    )

def _sian_row(label, images):
    thumbs = "".join(_sian_thumb_small(p) for p in images)
    return (
        '<div style="display:flex;align-items:center;gap:var(--s-3);padding:var(--s-2) 0">'
        f'<div class="t-caption w-bold is-ink" style="width:120px;flex-shrink:0;letter-spacing:0">{label}</div>'
        f'<div style="display:flex;gap:var(--s-2);flex:1">{thumbs}</div>'
        '</div>'
    )

S_SIAN_SUMMARY_V26 = (
    '<div style="padding:var(--s-2) 0;max-width:1600px;margin:0 auto">'
    + _sian_row("사례 1 · 3.6%", SIAN_1_IMAGES)
    + '<div style="height:1px;background:#E8E8E8;margin:var(--s-1) 0"></div>'
    + _sian_row("사례 2 · 55위", SIAN_2_IMAGES)
    + '<div style="height:1px;background:#E8E8E8;margin:var(--s-1) 0"></div>'
    + _sian_row("사례 3 · Room 1201", SIAN_3_IMAGES)
    + '</div>'
    + script(
        '"지금까지 보신 12개의 시안입니다<br>'
        '세 가지 사실, 세 가지 리프레이밍<br><br>'
        '<strong>영산대는, 이미 증명된 학교였습니다</strong><br>'
        '저희는 그것을, 보이게 만들 뿐입니다"'
    )
)

# ===== 15-A. OUR METHOD · VIDEO (지면 vs 영상 대비 + 선언) =====
S_VIDEO_INTRO = (
    '<div style="padding:var(--s-3) 0;text-align:center">'
    '<div class="t-overline is-accent" style="margin-bottom:var(--s-4)">OUR METHOD &nbsp;·&nbsp; VIDEO</div>'
    # 2칸 대비 박스 (얇은 테두리 + 세로선)
    '<div style="display:flex;justify-content:center;margin-bottom:var(--s-4)">'
    '<div style="display:flex;border:1px solid #E8E8E8;border-radius:6px;max-width:760px">'
    # PRINT 컬럼
    '<div style="flex:1;padding:var(--s-4) var(--s-5);text-align:left">'
    '<div class="t-overline" style="margin-bottom:var(--s-3)">PRINT &nbsp;·&nbsp; 지면</div>'
    '<div class="t-subtitle w-regular" style="line-height:1.6">정제된 한 장면<br>'
    '<span class="is-accent w-bold">리프레이밍</span>으로 증명</div>'
    '</div>'
    # 중앙 세로선
    '<div style="width:1px;background:#E8E8E8"></div>'
    # VIDEO 컬럼
    '<div style="flex:1;padding:var(--s-4) var(--s-5);text-align:left">'
    '<div class="t-overline" style="margin-bottom:var(--s-3)">VIDEO &nbsp;·&nbsp; 영상</div>'
    '<div class="t-subtitle w-regular" style="line-height:1.6;white-space:nowrap">풀어낸 한 편의 이야기<br>'
    '<span class="is-accent w-bold">스토리텔링</span>으로 증명</div>'
    '</div>'
    '</div>'
    '</div>'
    # 화살표
    '<div class="is-muted" style="font-size:32px;line-height:1;margin-bottom:var(--s-4)">↓</div>'
    # short bar
    '<div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-4)"></div>'
    # 헤드라인
    '<div class="t-heading">'
    '같은 컨셉 <span class="is-accent">증명</span>을,<br>'
    '이번엔 <span class="is-accent">이야기</span>로</div>'
    '</div>'
    + script(
        '"지면은, 한 장입니다 정제된 한 순간을 <strong>리프레이밍</strong>으로 증명했습니다<br><br>'
        '영상은, 60초입니다 이야기를 풀어낼 수 있습니다<br>'
        '같은 컨셉 <strong>증명</strong>을, 이번엔 <strong>스토리텔링</strong>으로 풀었습니다"'
    )
)

# ===== 15-B. THE PROTAGONIST -- 3갈래 의미 수렴 =====
S_VIDEO_WHY = (
    '<div style="padding:var(--s-4) 0;text-align:center">'
    '<div class="t-overline is-accent" style="margin-bottom:var(--s-4)">THE PROTAGONIST</div>'
    # 중앙 거대 타이포
    '<div class="t-hero" style="margin-bottom:var(--s-4)">지혜</div>'
    # 주황 short bar
    '<div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div>'
    # 3갈래 의미 리스트 (각 줄: overline 고정폭 + 본문)
    '<div style="display:inline-block;text-align:left;max-width:760px">'
    # 1. 校訓
    '<div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8">'
    '<div class="t-overline" style="width:130px;flex-shrink:0">① 校訓</div>'
    '<div class="t-subtitle w-regular">"지혜가 실력이다" — 영산대학교</div>'
    '</div>'
    # 2. 영상 주인공
    '<div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8">'
    '<div class="t-overline" style="width:130px;flex-shrink:0">② 영상 주인공</div>'
    '<div class="t-subtitle w-regular">누군가 부르면, <span class="is-ink w-bold">돌아보는 사람</span></div>'
    '</div>'
    # 3. 졸업생 공통
    '<div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-2) 0">'
    '<div class="t-overline" style="width:130px;flex-shrink:0">③ 졸업생</div>'
    '<div class="t-subtitle w-regular">항공 · 호텔 · 경찰 · 뷰티 현장, <span class="is-accent w-bold">바로 그 이름</span></div>'
    '</div>'
    '</div>'
    '</div>'
    + script(
        '"왜 <strong>\'지혜\'</strong>인가요? 세 가지 이유가 한 단어에 있습니다<br><br>'
        '<strong>첫째,</strong> 영산대 校訓이 <strong>지혜가 실력이다</strong>입니다<br>'
        '<strong>둘째,</strong> 영상 속 주인공의 이름입니다 -- 누군가 부르면 돌아보는 사람<br>'
        '<strong>셋째,</strong> 각계각층 영산대 졸업생들이 불리는, 바로 그 이름입니다<br><br>'
        '한 이름, 세 갈래의 의미 <strong>하나의 증명</strong>입니다<br><br>'
        '이제, 실제 영상입니다"'
    )
)

# ===== 비디오 파일 경로 (가로형 / 세로형) =====
VIDEO_HORIZONTAL = "/assets/video/KakaoTalk_20260410_151606259.mp4"  # 홍보영상 (가로)
VIDEO_VERTICAL = "/assets/video/KakaoTalk_20260410_151555089.mp4"    # 숏폼 (세로)

# ===== 20 (신규). 실무 확장 대시보드 -- 10장 프레이밍 =====
S_EXPANSION = (
    '<div style="padding:var(--s-4) 0;text-align:center">'
    '<div class="t-overline is-accent" style="margin-bottom:var(--s-4)">EXPANSION</div>'
    '<div class="t-heading" style="margin-bottom:var(--s-3)">'
    '증명을, 이렇게 <span class="is-accent">확장</span>합니다</div>'
    # short bar
    '<div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div>'
    # 6개 매체 리스트 (2열 grid)
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:0 var(--s-6);max-width:980px;margin:0 auto var(--s-5);text-align:left">'
    '<div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8">'
    '<div class="t-overline is-accent" style="width:110px;flex-shrink:0">인플루언서</div>'
    '<div class="t-body is-muted">교육·호텔 업계 유튜버 협업</div>'
    '</div>'
    '<div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8">'
    '<div class="t-overline is-accent" style="width:110px;flex-shrink:0">인쇄 매체</div>'
    '<div class="t-body is-muted">3.6% 중심 배치 (버스·지하철·현수막)</div>'
    '</div>'
    '<div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8">'
    '<div class="t-overline is-accent" style="width:110px;flex-shrink:0">디지털 매체</div>'
    '<div class="t-body is-muted">심사위원석 + Room 1201 A/B 실험</div>'
    '</div>'
    '<div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8">'
    '<div class="t-overline is-accent" style="width:110px;flex-shrink:0">숏폼</div>'
    '<div class="t-body is-muted">졸업선배 9~12월 연 4편</div>'
    '</div>'
    '<div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0">'
    '<div class="t-overline is-accent" style="width:110px;flex-shrink:0">소셜 미디어</div>'
    '<div class="t-body is-muted">3채널 통합 + 월간 캘린더</div>'
    '</div>'
    '<div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0">'
    '<div class="t-overline is-accent" style="width:110px;flex-shrink:0">언론</div>'
    '<div class="t-body is-muted">수시·정시 시기별 매체 집행</div>'
    '</div>'
    '</div>'
    # 하단 한 줄
    '<div class="t-subtitle w-regular is-muted">'
    '— 같은 증명 <span class="is-ink w-bold">다른 채널</span>'
    '</div>'
    '</div>'
    + script(
        '"지면과 영상으로 증명을 보여드렸습니다<br>'
        '이제 이 증명을, <strong>6개 채널</strong>로 확장하겠습니다<br><br>'
        '인플루언서, 인쇄, 디지털, 숏폼, 소셜 미디어, 언론<br><br>'
        '같은 <strong>증명</strong>. 다른 <strong>채널</strong>입니다<br>'
        '지금부터, 하나씩 설명드리겠습니다"'
    )
)

# ===== 17. "지혜" 메인 영상 -- 실제 비디오 재생 =====
S_JIHYE = (
    '<div style="display:flex;justify-content:center;align-items:center;padding:0">'
    '<div style="position:relative;width:1440px;height:810px;background:#000;border-radius:6px;'
    'overflow:hidden;border:1px solid #E8E8E8">'
    '<video style="width:100%;height:100%;object-fit:contain;background:#000;display:block" '
    f'src="{VIDEO_HORIZONTAL}" controls preload="metadata" '
    'poster=""></video>'
    '<div class="t-overline" style="position:absolute;top:16px;left:16px;letter-spacing:1px;'
    'color:#fff;background:#E84E10;padding:4px 12px;border-radius:2px;pointer-events:none">'
    '홍보영상 · 16:9</div>'
    '</div></div>'
    '<div class="t-caption" style="text-align:center;margin-top:var(--s-2)">'
    '<strong class="is-ink">"지혜" 메인 영상 (60초)</strong> &nbsp;·&nbsp; WISE YOU &nbsp;·&nbsp; '
    '<span class="is-accent w-bold">25명의 지혜, 전부 영산대 졸업생입니다</span>'
    '</div>'
    + script(
        '<strong>[씬 구성]</strong><br>'
        '비행기 "지혜야~" → 호텔 "박지혜 지배인님" → 경찰서 "지혜 경위" → 뷰티 "지혜 선생님" → '
        '<strong>"우리는 모두 지혜입니다"</strong><br><br>'
        '"(영상 재생 -- 60초)<br><br>'
        '비행기에서, 호텔에서, 경찰서에서, 뷰티 매장에서<br>'
        '누군가 <strong>\'지혜야\'</strong>를 부르면,<br>'
        '뒤돌아보는 사람은 전부 영산대 졸업생입니다<br><br>'
        '<strong>25명의 지혜 전부 영산대 졸업생입니다</strong><br>'
        '상징이 아닌, 숫자로 증명합니다"'
    )
)

# ===== 추가 영상 2 (2.mp4) =====
S_JIHYE_2 = (
    '<div style="display:flex;justify-content:center;align-items:center;padding:0">'
    '<div style="position:relative;width:1440px;height:810px;background:#000;border-radius:6px;'
    'overflow:hidden;border:1px solid #E8E8E8">'
    '<video style="width:100%;height:100%;object-fit:contain;background:#000;display:block" '
    'src="/assets/video/2.mp4" controls preload="metadata"></video>'
    '<div class="t-overline" style="position:absolute;top:16px;left:16px;letter-spacing:1px;'
    'color:#fff;background:#E84E10;padding:4px 12px;border-radius:2px;pointer-events:none">'
    '홍보영상 · 16:9</div>'
    '</div></div>'
)

# ===== 추가 영상 3 (3.mp4) =====
S_JIHYE_3 = (
    '<div style="display:flex;justify-content:center;align-items:center;padding:0">'
    '<div style="position:relative;width:1440px;height:810px;background:#000;border-radius:6px;'
    'overflow:hidden;border:1px solid #E8E8E8">'
    '<video style="width:100%;height:100%;object-fit:contain;background:#000;display:block" '
    'src="/assets/video/3.mp4" controls preload="metadata"></video>'
    '<div class="t-overline" style="position:absolute;top:16px;left:16px;letter-spacing:1px;'
    'color:#fff;background:#E84E10;padding:4px 12px;border-radius:2px;pointer-events:none">'
    '홍보영상 · 16:9</div>'
    '</div></div>'
)

# ===== 마지막: 빈칸 회수 =====
S_ENDING = (
    '<div style="padding:var(--s-7) 0;text-align:center">'
    '<div class="t-subtitle w-regular is-muted" style="line-height:2.4">'
    '홍익대 = <strong class="is-ink">미대</strong><br>'
    '한양대 에리카 = <strong class="is-ink">공대</strong><br>'
    '동의대 = <strong class="is-ink">한의대</strong>'
    '</div>'
    '<div class="t-heading" style="margin-top:var(--s-6)">'
    '영산대 = <strong class="is-accent">이름을 가려도 보이는 대학</strong>'
    '</div>'
    '</div>'
    + script(
        '"(이 슬라이드에서 천천히)<br><br>'
        '처음에 빈칸이었습니다<br>'
        '이제 채웠습니다<br><br>'
        '<strong>영산대 = 이름을 가려도 보이는 대학</strong><br><br>'
        '감사합니다"<br>'
        '(3초 정지 PT 종료)'
    )
)


def make_sections():
    # section_parent는 메인 로마 섹션만
    P_I = "I. 제안개요"
    P_II = "II 제안업체 일반"
    P_III = "III 세부 과업 수행 계획"
    P_IV = "IV 사업 관리 계획"

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
        # I. 제안개요 (2페이지 분할: EVIDENCE + PROBLEM)
        (2, "", 1, parent(P_I) + S_FACTS),
        (2, "", 2, parent(P_I) + S_PROBLEM),
        # II 제안업체 일반
        (2, "제안업체 일반", 3, parent(P_II) + S_COMPANY),
        # III 세부 과업 수행 계획 (간지)
        (1, "세부 과업 수행 계획", 4, None),

        # III 1 - 소재 발굴 및 콘텐츠 기획 (빌드업 4장 + 컨셉 2장 + 시안 4장 = 10장)
        (2, T_SOURCE, 5, parent(P_III) + tag("인식의 한계") + S_NUMBERS),
        (2, T_SOURCE, 6, parent(P_III) + tag("차별화의 부재") + S_TRANSITION),
        (2, T_SOURCE, 7, parent(P_III) + tag("소음") + S_LOSS),
        (2, T_SOURCE, 8, parent(P_III) + tag("접근법") + S_BRIDGE),
        (2, T_SOURCE, 9, parent(P_III) + tag("컨셉") + S_CONCEPT_ONLY),
        (2, T_SOURCE, 10, parent(P_III) + tag("기법") + S_METHOD_ONLY),
        (2, T_SOURCE, 11, parent(P_III) + tag("프리뷰") + S_REFRAMING_PREVIEW),
        (2, T_SOURCE, 12, parent(P_III) + tag("사례 1-1") + sian_image_fullscreen("1-1", "96.4%", "3.6%", SIAN_1_IMAGES[0], "")),
        (2, T_SOURCE, 13, parent(P_III) + tag("사례 1-2") + sian_image_fullscreen("1-2", "96.4%", "3.6%", SIAN_1_IMAGES[1], "")),
        (2, T_SOURCE, 14, parent(P_III) + tag("사례 1-3") + sian_image_fullscreen("1-3", "96.4%", "3.6%", SIAN_1_IMAGES[2], "")),
        (2, T_SOURCE, 15, parent(P_III) + tag("사례 2-1") + sian_image_fullscreen("2-1", "국내 우수 호스피탈리티", "글로벌 55위 영산대", SIAN_2_IMAGES[0], "")),
        (2, T_SOURCE, 16, parent(P_III) + tag("사례 2-2") + sian_image_fullscreen("2-2", "국내 우수 호스피탈리티", "글로벌 55위 영산대", SIAN_2_IMAGES[1], "")),
        (2, T_SOURCE, 17, parent(P_III) + tag("사례 2-3") + sian_image_fullscreen("2-3", "국내 우수 호스피탈리티", "글로벌 55위 영산대", SIAN_2_IMAGES[2], "")),
        (2, T_SOURCE, 18, parent(P_III) + tag("사례 3-1") + sian_image_fullscreen("3-1", "25명의 총지배인", "25개 호텔 · 하나의 대학", SIAN_3_IMAGES[0], "")),
        (2, T_SOURCE, 19, parent(P_III) + tag("사례 3-2") + sian_image_fullscreen("3-2", "25명의 총지배인", "25개 호텔 · 하나의 대학", SIAN_3_IMAGES[1], "")),
        (2, T_SOURCE, 20, parent(P_III) + tag("사례 3-3") + sian_image_fullscreen("3-3", "25명의 총지배인", "25개 호텔 · 하나의 대학", SIAN_3_IMAGES[2], "")),
        (2, T_SOURCE, 21, parent(P_III) + tag("사례 3-4") + sian_image_fullscreen("3-4", "25명의 총지배인", "25개 호텔 · 하나의 대학", SIAN_3_IMAGES[3], "")),
        (2, T_SOURCE, 22, parent(P_III) + tag("사례 3-5") + sian_image_fullscreen("3-5", "25명의 총지배인", "25개 호텔 · 하나의 대학", SIAN_3_IMAGES[4], "")),
        (2, T_SOURCE, 23, parent(P_III) + tag("사례 3-6") + sian_image_fullscreen("3-6", "25명의 총지배인", "25개 호텔 · 하나의 대학", SIAN_3_IMAGES[5], "")),
        (2, T_SOURCE, 24, parent(P_III) + tag("종합") + S_SIAN_SUMMARY_V26),

        # 대학 공식 홍보영상
        (1, "대학 공식 홍보영상", 25, None),
        (2, T_VIDEO, 26, parent(P_III) + tag("영상 접근법") + S_VIDEO_INTRO),
        (2, T_VIDEO, 27, parent(P_III) + tag("주인공") + S_VIDEO_WHY),
        (2, T_VIDEO, 28, parent(P_III) + tag("본편") + S_JIHYE),
        (2, T_VIDEO, 29, parent(P_III) + tag("영상 2") + S_JIHYE_2),
        (2, T_VIDEO, 30, parent(P_III) + tag("영상 3") + S_JIHYE_3),

        # 실무 확장 대시보드
        (2, T_SOURCE, 31, parent(P_III) + tag("확장 개요") + S_EXPANSION),

        # 매체 전개
        (2, T_YOUTUBE, 32, parent(P_III) + tag("인플루언서") + S_YOUTUBE_V22),
        (2, T_PRINT, 33, parent(P_III) + tag("인쇄 매체") + S_PRINT),
        (2, T_DIGITAL, 34, parent(P_III) + tag("디지털 매체") + S_DIGITAL),
        (2, T_VIDEO, 35, parent(P_III) + tag("숏폼 기획") + S_DOCU_PLAN),
        (2, T_VIDEO, 36, parent(P_III) + tag("숏폼 완성본") + S_DOCU_VIDEOS),
        (2, T_SNS, 37, parent(P_III) + tag("소셜 미디어") + S_SNS),
        (2, T_PRESS, 38, parent(P_III) + tag("언론 매체") + S_PRESS),
        (2, T_MGMT, 39, parent(P_III) + tag("운영 지원") + S_CONSULT),

        # IV
        (2, T_IV_1, 40, parent(P_IV) + tag("예산 배분") + S_GANTT),
        (2, T_IV_2, 41, parent(P_IV) + tag("성과 측정") + S_FEEDBACK),
        (2, T_IV_3, 42, parent(P_IV) + tag("확장 계획") + S_OPERATION),

        # 마무리는 템플릿의 slide-end가 담당 (ANSWER 엔딩)
    ]


if __name__ == "__main__":
    conn = get_conn()
    sections = make_sections()
    cur = conn.execute(
        "INSERT INTO proposals (title,version,status,rfp_json,rfp_summary,raw_text,selected_concept) VALUES (?,?,?,?,?,?,?)",
        ("V27", "V27", "ready", RFP, SUMMARY, SUMMARY, "A"))
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
    print(f"V27: id={pid}")
