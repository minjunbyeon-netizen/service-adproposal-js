# -*- coding: utf-8 -*-
"""V30 PT 요약본 → PDF (대표님 공유용).
보고서 형식, 그리드 없음, 깔끔한 타이포그래피.
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

OUT_HTML = Path(__file__).resolve().parent.parent / "uploads" / "v30_pt_brief.html"
OUT_PDF = Path(__file__).resolve().parent.parent / "uploads" / "v30_pt_brief.pdf"

ROWS = [
    ("P1", "표지 — V30 / 영산대학교 광고대행사 선정",
     "(표지 30초 정적, 평가위원 착석)\n\n\"광고대행사 선정의 본질은 두 가지입니다. 더 많이 팔 것이냐, 더 오래 기억될 것이냐.\""),
    ("P2", "경쟁사 4개 이미지 (동의·동서·부경·신라)",
     "\"대학은 이미지로 기억됩니다. 동의대 한의대의 전통, 동서대 영상·IT의 젊음, 부경대 국립의 규모, 신라대 종합대학의 안정 — 모두 '느낌'입니다.\""),
    ("P3", "빈 화면 질문 — \"영산대학교는?\"",
     "\"그렇다면 — 영산대학교는?\"  (3초 침묵)"),
    ("P4", "영산대 = 숫자 (96.4% / 55위 / 25명 / 校訓)",
     "\"이미지가 아닙니다. 숫자입니다. 96.4%, 55위, 25명, 校訓.\"  (숫자 카운트업)"),
    ("P5", "사실은 이미지보다 강합니다 → 증명으로",
     "\"남은 질문은 하나 — 이 사실을, 어떻게 증명으로 바꿀 것인가.\""),
    ("P6", "하이브미디어 일반 (4사분면: 일반/조직/사업/실적)",
     "\"하이브미디어입니다. 17명, 20년. 세부는 생략합니다 — 제안이 회사보다 중요하니까요.\""),
    ("P7", "(디바이더) Ⅲ. 세부 과업 수행 계획",
     "(무발화, 2초 표시)"),
    ("P8", "기억 테스트 — 2분 전 몇 개 기억나십니까?",
     "\"2분 전 네 개 사실을 보여드렸습니다. 지금, 몇 개가 기억나십니까?\"  (3초 침묵)"),
    ("P9", "대학 클리셰 5개 (글로벌 1위·최고 교수진·미래 인재…)",
     "\"잊으신 건 당신 탓이 아닙니다. 모든 대학이 똑같이 말하기 때문입니다.\""),
    ("P10", "소음 — 웨이브폼 + \"소음\" 대형 텍스트",
     "\"이것이, 소음입니다.\""),
    ("P11", "뒤집기 — Before(96.4%) ↻ After(3.6%)",
     "\"그래서 저희는 — 뒤집었습니다. 취업률 96.4%가 아니라, 탈락률 3.6%.\""),
    ("P12", "리프레이밍 (기법 명명)",
     "\"이 기법에는 이름이 있습니다. 리프레이밍.\""),
    ("P13", "증명 (컨셉 명명)",
     "\"리프레이밍으로 각인시키는 행위 — 한 단어로, 증명.\""),
    ("P14", "3가지 증명 프리뷰 (소음 → 각인 표)",
     "\"3.6%, 글로벌 55위, 1개의 시스템. 세 개의 증명 — 지금 보여드리겠습니다.\""),
    ("P15", "시안 ①-1 — 3.6% 탈락률 (메인 비주얼)",
     "\"시안 1, 3.6% 탈락률입니다.\"  (10초 정적)"),
    ("P16", "시안 ①-2 — 3.6% 응용", "(무발화, 시안에 시선 맡김)"),
    ("P17", "시안 ①-3 — 3.6% 응용", "(무발화)"),
    ("P18", "시안 ②-1 — 글로벌 55위 (메인 비주얼)",
     "\"시안 2, 글로벌 55위입니다.\"  (10초 정적)"),
    ("P19", "시안 ②-2 — 글로벌 55위 응용", "(무발화)"),
    ("P20", "시안 ②-3 — 글로벌 55위 응용", "(무발화)"),
    ("P21", "시안 ③-1 — 1개의 시스템 (메인 비주얼)",
     "\"시안 3, 1개의 시스템입니다.\"  (10초 정적)"),
    ("P22~26", "시안 ③ 응용 5컷", "(각 컷 3초씩, 무발화)"),
    ("P27", "시안 1·2·3 총정리 (한 화면 모아보기)",
     "\"세 개의 증명, 한 화면으로 정리한 것입니다.\"  (평가위원이 비교)"),
    ("P28", "(디바이더) 대학 공식 홍보영상",
     "\"지면이 정지된 증명이라면 — 영상은 흐르는 증명입니다.\""),
    ("P29", "영상 접근법 (PRINT vs VIDEO) + 브릿지 질문",
     "\"같은 컨셉, 이번엔 이야기로. 그렇다면 — 어떤 이야기로?\""),
    ("P30", "슬로건 — \"영산대학교는, 지혜로 증명합니다\"",
     "\"이번 영상의 슬로건은 한 문장입니다 — 영산대학교는, 지혜로 증명합니다.\"  (2초 정적)"),
    ("P31", "본편 영상 60초 (지혜야~ 시리즈)",
     "(영상 재생 60초, 발표자 정지) → 끝난 뒤: \"이것이, '지혜'입니다.\""),
]

ACTS = [
    ("Act 1", "충격 도입 (P1~P5)", "표지 → 경쟁사 → 질문 → 숫자 반전 → 증명 선언"),
    ("Act 2", "진단 (P8~P11)", "기억 테스트 → 클리셰 노출 → 소음 → 뒤집기"),
    ("Act 3", "컨셉 (P12~P14)", "리프레이밍 → 증명 → 3가지 증명 프리뷰"),
    ("Act 4", "증거 퍼레이드 (P15~P27)", "시안 1·2·3 + 변형 컷 → 총정리"),
    ("Act 5", "영상 (P28~P31)", "브릿지 → 슬로건 → 본편 60초 → \"이것이 지혜\""),
]


def build_html() -> str:
    rows_html = "".join(
        f'<tr><td class="p">{p}</td><td class="title">{t}</td><td class="script">{s.replace(chr(10), "<br>")}</td></tr>'
        for p, t, s in ROWS
    )
    acts_html = "".join(
        f'<tr><td class="act-num">{n}</td><td class="act-title">{t}</td><td class="act-flow">{f}</td></tr>'
        for n, t, f in ACTS
    )

    return f"""<!DOCTYPE html>
<html lang="ko"><head>
<meta charset="UTF-8">
<title>영산대 광고제안서 PT — 발표 요약본</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box }}
  @page {{ size: A4; margin: 22mm 18mm }}
  body {{
    font-family: 'Roboto', 'Noto Sans KR', sans-serif;
    color: #1A1A1A;
    font-size: 10.5pt;
    line-height: 1.6;
    background: #fff;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .header {{
    border-bottom: 1px solid #1A1A1A;
    padding-bottom: 14px;
    margin-bottom: 22px;
  }}
  .h-eyebrow {{
    font-size: 9pt;
    letter-spacing: 4px;
    color: #6E6E73;
    font-weight: 700;
    margin-bottom: 6px;
  }}
  .h-title {{
    font-size: 22pt;
    font-weight: 700;
    line-height: 1.2;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
  }}
  .h-sub {{
    font-size: 11pt;
    color: #6E6E73;
    font-weight: 400;
  }}

  h2 {{
    font-size: 12pt;
    font-weight: 700;
    letter-spacing: 2px;
    color: #6E6E73;
    margin: 28px 0 12px 0;
    text-transform: uppercase;
    border-bottom: 1px solid #E8E8E8;
    padding-bottom: 6px;
  }}

  /* 표 — row 강조 + 헤더 + 컬럼 구분 */
  table {{
    width: 100%;
    border-collapse: collapse;
    border-top: 2px solid #1A1A1A;
    border-bottom: 2px solid #1A1A1A;
  }}
  thead th {{
    padding: 10px 10px;
    background: #F5F5F5;
    border-bottom: 1.5px solid #1A1A1A;
    font-size: 9pt;
    font-weight: 700;
    color: #1A1A1A;
    letter-spacing: 2px;
    text-align: left;
    text-transform: uppercase;
  }}
  tbody td {{
    padding: 11px 10px;
    border-bottom: 1px solid #E0E0E0;
    border-right: 1px solid #F0F0F0;
    vertical-align: top;
  }}
  tbody td:last-child {{ border-right: none }}
  tbody tr:nth-child(even) td {{ background: #FAFAFA }}
  tbody tr:last-child td {{ border-bottom: none }}

  td.p {{
    width: 9%;
    font-weight: 700;
    color: #E84E10;
    font-family: 'Roboto', sans-serif;
    letter-spacing: 0.5px;
    white-space: nowrap;
    text-align: center;
  }}
  td.title {{
    width: 33%;
    font-weight: 700;
    color: #1A1A1A;
  }}
  td.script {{
    color: #1A1A1A;
    line-height: 1.65;
  }}

  /* Act 요약 — 표 형태 */
  table.acts-table {{
    margin-top: 16px;
  }}
  table.acts-table td.act-num {{
    width: 12%;
    font-weight: 700;
    color: #E84E10;
    font-size: 10.5pt;
    letter-spacing: 1px;
    text-align: center;
    white-space: nowrap;
  }}
  table.acts-table td.act-title {{
    width: 35%;
    font-weight: 700;
    color: #1A1A1A;
  }}
  table.acts-table td.act-flow {{
    color: #6E6E73;
  }}

  .footer {{
    margin-top: 30px;
    padding-top: 14px;
    border-top: 1px solid #E8E8E8;
    font-size: 8.5pt;
    color: #6E6E73;
    line-height: 1.6;
  }}
  .footer a {{ color: #E84E10; text-decoration: none }}
</style></head>
<body>
  <div class="header">
    <div class="h-eyebrow">PRESENTATION BRIEF</div>
    <div class="h-title">영산대학교 광고제안서 — 발표 요약본</div>
    <div class="h-sub">2026~2027학년도 와이즈유 광고대행사 선정 / V30 / 하이브미디어</div>
  </div>

  <h2>발표 흐름 (Build-up)</h2>
  <table class="acts-table">
    <thead><tr><th style="width:12%">Act</th><th style="width:35%">단계</th><th>흐름</th></tr></thead>
    <tbody>{acts_html}</tbody>
  </table>

  <h2>슬라이드별 한 줄 요약 + 핵심 대본</h2>
  <table>
    <thead><tr><th style="width:9%;text-align:center">P</th><th style="width:33%">슬라이드</th><th>핵심 대본</th></tr></thead>
    <tbody>{rows_html}</tbody>
  </table>

  <div class="footer">
    PT 풀버전 (인터랙티브 + 영상): <a href="https://minjunbyeon-netizen.github.io/service-adproposal-js/">minjunbyeon-netizen.github.io/service-adproposal-js</a><br>
    이 요약본은 P1~P31 (오프닝~영상 본편)까지 빌드업 핵심만 발췌. P32 이후 운영·예산·측정 파트는 PT 풀버전 참조.
  </div>
</body></html>"""


async def main():
    OUT_HTML.write_text(build_html(), encoding="utf-8")
    print(f"HTML: {OUT_HTML}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(OUT_HTML.as_uri())
        await page.emulate_media(media="print")
        await page.pdf(
            path=str(OUT_PDF),
            format="A4",
            print_background=True,
            margin={"top": "22mm", "bottom": "22mm", "left": "18mm", "right": "18mm"},
        )
        await browser.close()
    print(f"PDF: {OUT_PDF}")


if __name__ == "__main__":
    asyncio.run(main())
