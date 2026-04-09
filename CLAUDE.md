# adproposal-js -- 광고제안서 디벨롭

> 입찰공고문(PDF/DOCX)을 업로드하면 AI가 교차분석하여 과업요구사항 기반 목차를 추출하고,
> 대화형으로 섹션별 제안서를 생성/수정하는 로컬 웹 앱.

## 기술 스택
- 서버: Flask (Python)
- DB: SQLite (WAL)
- AI: claude CLI subprocess
- 프론트: 바닐라 HTML/CSS/JS
- 로컬 전용 (배포 대상 아님)

## 실행
```bash
cd C:\dev\services\adproposal-js
pip install -r requirements.txt
python app.py
# http://localhost:5060
```

## 구조
```
app.py               -- Flask 메인
api/
  db.py              -- SQLite 연결/초기화
  proposals.py       -- 제안서 CRUD, 파일 업로드, 분석, 내보내기
  chat.py            -- 섹션 생성, 대화형 수정
services/
  claude_client.py   -- claude CLI 래퍼
  parser.py          -- PDF/DOCX 텍스트 추출
  rfp_analyzer.py    -- RFP 교차분석
  section_writer.py  -- 섹션 생성/수정
templates/
  index.html         -- 3패널 SPA
static/
  style.css
  app.js
```

## 핵심 워크플로우
1. 파일 업로드 (PDF/DOCX) + 텍스트 직접 입력
2. RFP 교차분석 -> 과업요구사항 추출 + 목차 자동 생성
3. 섹션별 초안 생성 (개별 또는 전체 자동)
4. 대화형 피드백 -> 섹션 수정
5. 마크다운 내보내기
