# -*- coding: utf-8 -*-
"""P43/P44/P45 수정:
- P43: 매체 td 좌측정렬 + 괄호 영역 줄바꿈
- P44: 헤더가 center인 컬럼(월/핵심 활동) td들도 center 정렬
- P45: 테이블 max-width 1100 -> 1210 (좌우 10% 넓게)
대상: scripts/pt.html + DB proposal_id=138 (order 42, 43, 44)
"""
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PT = ROOT / "scripts" / "pt.html"
DB = ROOT / "data" / "adproposal.db"
PID = 138


def fix_p43(s: str) -> str:
    # 괄호 영역 줄바꿈 (3곳)
    s = s.replace(
        "<strong>디지털 광고</strong> (유튜브/인스타/페이스북 DA)",
        "<strong>디지털 광고</strong><br>(유튜브/인스타/페이스북 DA)",
    )
    s = s.replace(
        "<strong>인쇄 매체</strong> (버스/지하철/현수막/리플렛)",
        "<strong>인쇄 매체</strong><br>(버스/지하철/현수막/리플렛)",
    )
    s = s.replace(
        "<strong>숏폼 시리즈</strong> (4편)",
        "<strong>숏폼 시리즈</strong><br>(4편)",
    )
    # 매체 td에 text-align:left 명시
    # 패턴: td 안에 <strong>매체명</strong>으로 시작하는 셀 (첫 컬럼)
    labels = [
        "디지털 광고", "홍보영상 제작", "크리에이티브 시안 제작",
        "인쇄 매체", "숏폼 시리즈", "SNS 운영 + 인플루언서", "언론 매체",
    ]
    for label in labels:
        # text-align 없는 td만 매치 (;border-bottom 또는 마지막 td ")
        s = re.sub(
            r'(<td style="padding:var\(--s-1\) var\(--s-2\);border-bottom:1px solid #E8E8E8)"(><strong>'
            + re.escape(label) + r")",
            r'\1;text-align:left"\2',
            s,
        )
        s = re.sub(
            r'(<td style="padding:var\(--s-1\) var\(--s-2\))"(><strong>'
            + re.escape(label) + r")",
            r'\1;text-align:left"\2',
            s,
        )
    return s


def fix_p44(s: str) -> str:
    # "월" 컬럼 td와 "핵심 활동" 컬럼 td에 text-align:center 추가
    # 월 컬럼: td 안에 <strong>N월</strong> 또는 그냥 텍스트 N월/4월/8~9월 등
    # 핵심 활동 컬럼: td 안에 일반 텍스트 (수시 시작 -- ...)
    # 가장 쉬운 방법: tr 전체를 찾아서 그 안의 첫번째 td와 네번째 td를 수정

    # 각 <tr> 블록 처리
    def process_tr(match):
        tr_html = match.group(0)
        # 첫번째 td와 네번째 td에 text-align:center 추가
        # td들을 순서대로 찾아서 1번째와 4번째만 수정
        tds = list(re.finditer(r'<td style="([^"]*)"([^>]*)>', tr_html))
        if len(tds) < 4:
            return tr_html
        # 4번째 td부터 수정 (뒤에서 수정하면 offset 안 밀림)
        for idx in [3, 0]:
            td = tds[idx]
            style = td.group(1)
            if "text-align" in style:
                continue  # 이미 있으면 skip
            new_style = style + ";text-align:center"
            tr_html = tr_html[: td.start()] + f'<td style="{new_style}"{td.group(2)}>' + tr_html[td.end():]
            # re-index for subsequent edits (already done in reverse)
        return tr_html

    # tbody 내의 tr만 처리 (thead 제외)
    def process_tbody(m):
        tbody = m.group(0)
        tbody = re.sub(r'<tr[^>]*>.*?</tr>', process_tr, tbody, flags=re.DOTALL)
        return tbody

    s = re.sub(r'<tbody>.*?</tbody>', process_tbody, s, flags=re.DOTALL)
    return s


def fix_p45(s: str) -> str:
    # table max-width 1100px -> 1210px (10% 증가)
    s = s.replace("max-width:1100px", "max-width:1210px")
    return s


# --- pt.html ---
html = PT.read_text(encoding="utf-8")

# P43 블록: slide-pagenum">43 포함
def replace_slide(html, pagenum: str, fixer):
    # 해당 pagenum을 가진 slide-content 블록 찾기 — 이전/다음 <div class="slide 기준
    marker = f'<div class="slide-pagenum">{pagenum}</div>'
    idx = html.find(marker)
    if idx < 0:
        raise RuntimeError(f"P{pagenum} 마커 없음")
    # 이 슬라이드 블록의 시작 (<div class="slide slide-content...) — 이전 <div class="slide 역검색
    start = html.rfind('<div class="slide slide-content', 0, idx)
    # 끝: 다음 <div class="slide 또는 </div><!-- end deck -->
    next_start = html.find('<div class="slide', idx + len(marker))
    end = next_start if next_start > 0 else len(html)
    block = html[start:end]
    new_block = fixer(block)
    return html[:start] + new_block + html[end:]

html = replace_slide(html, "43", fix_p43)
html = replace_slide(html, "44", fix_p44)
html = replace_slide(html, "45", fix_p45)
PT.write_text(html, encoding="utf-8")
print("pt.html 갱신 완료")


# --- DB ---
conn = sqlite3.connect(str(DB))
for order_idx, fixer in [(42, fix_p43), (43, fix_p44), (44, fix_p45)]:
    r = conn.execute(
        "SELECT id, content FROM sections WHERE proposal_id=? AND order_idx=?",
        (PID, order_idx),
    ).fetchone()
    if not r:
        print(f"order={order_idx} 없음")
        continue
    sid, body = r
    new_body = fixer(body)
    conn.execute("UPDATE sections SET content=? WHERE id=?", (new_body, sid))
    changed = new_body != body
    print(f"order={order_idx}: {'수정됨' if changed else '변경없음'}")
conn.commit()
conn.close()
print("DB 갱신 완료")
