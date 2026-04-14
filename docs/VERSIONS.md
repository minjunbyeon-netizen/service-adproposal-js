# V30~V50 버전 맵

각 버전은 사이드패널(localhost:8881) 또는 DB `proposals` 테이블에서 접근.
**GitHub Pages에는 V30(기준)**이 배포됨: https://minjunbyeon-netizen.github.io/service-adproposal-js/

## V30 (기준)
전체 대화를 통해 정제된 최종 기준 버전.
- 표지 9645525 코드 (360px)
- P4 4단계 morph
- P5/P6 "들리다" 선언·답
- 본편 "숫자가 들리게 하는 행위" 키워드 체인
- FX v3 (Material easing, bounce 제거)
- 시안 이미지 6장 (airport, hotel, keys, graduate, plane-window, subway-billboard)

---

## V31~V40: 점진적 개선 (각 버전이 이전 버전을 base로)

| 버전 | proposal_id | 개선 포인트 |
|---|---|---|
| V31 | 139 | 표지 기준 snapshot (reference) |
| V32 | 140 | P2 경쟁사 대학명 `<strong>` 처리 — 리듬 |
| V33 | 141 | P5 "들리지 않았을까요?" 하단 오렌지 밑줄 |
| V34 | 142 | P6 "전부" 단어 오렌지 accent로 강조 |
| V35 | 143 | P12 Before/After 카드 폰트 +6px |
| V36 | 144 | P14 "증명" t-hero 140px 초대형 |
| V37 | 145 | P15 PREVIEW 화살표 letter-spacing |
| V38 | 146 | P31 슬로건 88 → 96px 확대 |
| V39 | 147 | P33 퍼널 단계별 전환율 100%·25%·8%·3% |
| V40 | 148 | P46 대시보드 캡션 "측정되지 않는 것은 증명되지 않습니다" |

V40이 V31~V40 누적 최종.

---

## V41~V50: 참신한 방향 실험 (각 버전 V30 독립 base)

| 버전 | proposal_id | 방향성 |
|---|---|---|
| V41 | 149 | **Monochrome** — accent #E84E10 제거, 순수 흑백 |
| V42 | 150 | **Poster-style** — t-title 88px / t-heading 68px 대형 |
| V43 | 151 | **KR/EN Hybrid** — 주요 제목 위 영문 overline 삽입 |
| V44 | 152 | **슬로건 변주** — "지혜로 증명" → "**숫자로 말합니다**" |
| V45 | 153 | **Editorial Serif** — 대형 제목 Noto Serif KR 교체 |
| V46 | 154 | **Asymmetric** — text-align center → left 전체 |
| V47 | 155 | **Dark mode** — 배경 #0A0A0A 반전 |
| V48 | 156 | **Question-driven** — 모든 t-heading 앞 "QUESTION" 태그 |
| V49 | 157 | **Editorial guidebook** — 좌우 여백 확대 (책 느낌) |
| V50 | 158 | **Minimalist manifesto** — 보조 카피 opacity 0.3으로 흐림 |

---

## 사용 방법

1. **로컬**: `localhost:8881` 접속 → 사이드패널에서 V## PT 버튼 클릭
2. **GitHub Pages**: V30만 공개 → https://minjunbyeon-netizen.github.io/service-adproposal-js/
3. 각 버전은 **독립적으로 렌더링** — 원본 V30 훼손 없음

## 개선 방향 체크리스트 (RFP 대응)

- 정량 평가 30점 (실적·인력·재무) → P6 하이브미디어 페이지
- 정성 평가 70점:
  - 홍보 전략·환경·타깃·참신성 20점 → P2-P6 · P8-P14
  - 크리에이티브 창의성 30점 → P15-P27 (시안) · P28-P31 (영상)
  - 매체 전략·예산 20점 → P32-P49 (확장·퍼널·예산·측정·리스크)

## 복원 방법

특정 버전으로 돌아가려면:
1. 사이드패널에서 해당 V## PT 클릭
2. 필요시 해당 버전을 새로운 base로 clone 후 작업 지속
