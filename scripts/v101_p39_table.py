# -*- coding: utf-8 -*-
"""V101 P39 (idx=38) - ROW 표 형태 중앙정렬."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


# 표 형태 + 중앙정렬 (P11 ROW 스타일과 대구)
P39 = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:소셜 미디어--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;padding:var(--s-5) var(--s-5)">

<div style="text-align:center;margin-bottom:var(--s-5)">
<div style="font-size:20px;color:#6E6E73;letter-spacing:3px;font-weight:400;margin-bottom:var(--s-2)">Ⅲ. 세부 과업 수행 계획</div>
<div style="font-size:64px;font-weight:700;color:#1A1A1A;line-height:1.2;letter-spacing:-1px">3채널 통합 운영</div>
<div style="font-size:18px;color:#6E6E73;margin-top:var(--s-2)">수시 집중기 5~7월 예산 70% 집중</div>
</div>

<table style="border-collapse:collapse;max-width:1100px;width:100%;margin:0 auto;text-align:center">

<thead>
<tr style="border-top:2px solid #1A1A1A;border-bottom:1px solid #1A1A1A">
<th style="padding:var(--s-3) var(--s-2);font-size:13px;font-weight:700;color:#6E6E73;letter-spacing:3px;width:60px">NO</th>
<th style="padding:var(--s-3) var(--s-2);font-size:13px;font-weight:700;color:#6E6E73;letter-spacing:3px">채널</th>
<th style="padding:var(--s-3) var(--s-2);font-size:13px;font-weight:700;color:#6E6E73;letter-spacing:3px">주 콘텐츠</th>
<th style="padding:var(--s-3) var(--s-2);font-size:13px;font-weight:700;color:#6E6E73;letter-spacing:3px">주기</th>
<th style="padding:var(--s-3) var(--s-2);font-size:13px;font-weight:700;color:#6E6E73;letter-spacing:3px">목표</th>
</tr>
</thead>

<tbody>

<tr style="border-bottom:1px solid #E8E8E8">
<td style="padding:var(--s-4) var(--s-2);font-size:18px;color:#6E6E73;font-weight:400">01</td>
<td style="padding:var(--s-4) var(--s-2);font-size:24px;font-weight:700;color:#1A1A1A">인스타그램</td>
<td style="padding:var(--s-4) var(--s-2);font-size:16px;color:#6E6E73">시안 이미지 · 릴스 · 스토리</td>
<td style="padding:var(--s-4) var(--s-2);font-size:16px;color:#1A1A1A">주 3회</td>
<td style="padding:var(--s-4) var(--s-2);font-size:16px;color:#E84E10;font-weight:700">팔로워 +500/월</td>
</tr>

<tr style="border-bottom:1px solid #E8E8E8">
<td style="padding:var(--s-4) var(--s-2);font-size:18px;color:#6E6E73;font-weight:400">02</td>
<td style="padding:var(--s-4) var(--s-2);font-size:24px;font-weight:700;color:#1A1A1A">유튜브 쇼츠</td>
<td style="padding:var(--s-4) var(--s-2);font-size:16px;color:#6E6E73">숏폼 · 졸업생 인터뷰</td>
<td style="padding:var(--s-4) var(--s-2);font-size:16px;color:#1A1A1A">주 2회</td>
<td style="padding:var(--s-4) var(--s-2);font-size:16px;color:#E84E10;font-weight:700">조회수 3,000+/편</td>
</tr>

<tr style="border-bottom:2px solid #1A1A1A">
<td style="padding:var(--s-4) var(--s-2);font-size:18px;color:#6E6E73;font-weight:400">03</td>
<td style="padding:var(--s-4) var(--s-2);font-size:24px;font-weight:700;color:#1A1A1A">네이버 블로그</td>
<td style="padding:var(--s-4) var(--s-2);font-size:16px;color:#6E6E73">팩트 카드뉴스 · 입시 가이드</td>
<td style="padding:var(--s-4) var(--s-2);font-size:16px;color:#1A1A1A">주 2회</td>
<td style="padding:var(--s-4) var(--s-2);font-size:16px;color:#E84E10;font-weight:700">검색 상위 노출</td>
</tr>

</tbody>

</table>

<div style="display:flex;align-items:center;justify-content:center;gap:var(--s-3);max-width:1100px;width:100%;padding-top:var(--s-4);font-size:13px;color:#6E6E73;letter-spacing:2px">
<span>3 CHANNELS</span>
<span>·</span>
<span>참여형 해시태그</span>
<span>·</span>
<span>학과 로테이션</span>
<span>·</span>
<span>월간 리포트 제공</span>
</div>

</div>"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=38",
        (P39, PID),
    )
    conn.commit()
    conn.close()
    print("[P39] 표 형태 중앙정렬 ROW 레이아웃 완료")


if __name__ == "__main__":
    main()
