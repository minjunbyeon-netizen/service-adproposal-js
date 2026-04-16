# -*- coding: utf-8 -*-
"""V101 - P37 VOGUE/Swiss + P39 ROW + 마지막장(idx=48) 삭제."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


# =============================================================================
# P37 (idx=36) - VOGUE/Swiss Executive Summary 레이아웃
# 참조: 2026-04-15 22 56 42.png
#   좌상단 라벨 + 오렌지 언더라인
#   대형 헤드라인 좌측정렬
#   3단 그리드 (01/02/03 번호 + 라벨 + 키워드 + 설명)
#   하단 얇은 라인 + 메타
# =============================================================================
P37 = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:숏폼 기획--><div style="height:100%;display:flex;flex-direction:column;justify-content:space-between;padding:var(--s-5) var(--s-5)">

<div>
<div style="font-size:14px;color:#6E6E73;letter-spacing:4px;font-weight:400;margin-bottom:var(--s-1)">Ⅲ. 세부 과업 수행 계획 / Short Form Series</div>
<div style="width:64px;height:3px;background:#E84E10;margin-bottom:var(--s-5)"></div>
<div style="font-size:72px;font-weight:700;color:#1A1A1A;line-height:1.1;letter-spacing:-2px;margin-bottom:var(--s-5)">졸업선배가<br>영산대를 증명합니다</div>
</div>

<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0;border-top:1px solid #1A1A1A;border-bottom:1px solid #1A1A1A;background:#FFFFFF">

<div style="padding:var(--s-4) var(--s-3);border-right:1px solid #E8E8E8;background:#FFFFFF">
<div style="font-size:13px;color:#6E6E73;letter-spacing:3px;font-weight:400;margin-bottom:var(--s-2)">01 — 산업</div>
<div style="font-size:32px;font-weight:700;color:#1A1A1A;line-height:1.2;margin-bottom:var(--s-2)">총지배인<br>아침 라운드</div>
<div style="font-size:14px;color:#6E6E73;line-height:1.6;margin-bottom:var(--s-3)">9월 · 호텔관광 · 60초</div>
<div style="font-size:16px;color:#E84E10;font-weight:700;line-height:1.4">산업이 선택한 대학</div>
</div>

<div style="padding:var(--s-4) var(--s-3);border-right:1px solid #E8E8E8;background:#FAFAFA">
<div style="font-size:13px;color:#6E6E73;letter-spacing:3px;font-weight:400;margin-bottom:var(--s-2)">02 — 세계</div>
<div style="font-size:32px;font-weight:700;color:#1A1A1A;line-height:1.2;margin-bottom:var(--s-2)">WACS 셰프의<br>주방 60초</div>
<div style="font-size:14px;color:#6E6E73;line-height:1.6;margin-bottom:var(--s-3)">11월 · 조리예술 · 60초</div>
<div style="font-size:16px;color:#E84E10;font-weight:700;line-height:1.4">글로벌 1위가 될 때까지</div>
</div>

<div style="padding:var(--s-4) var(--s-3);background:#FFF8F3;border-left:3px solid #E84E10">
<div style="font-size:13px;color:#E84E10;letter-spacing:3px;font-weight:700;margin-bottom:var(--s-2)">03 — 지원자</div>
<div style="font-size:32px;font-weight:700;color:#1A1A1A;line-height:1.2;margin-bottom:var(--s-2)">재학생<br>인터뷰 릴레이</div>
<div style="font-size:14px;color:#6E6E73;line-height:1.6;margin-bottom:var(--s-3)">12월 · 호텔관광 · 60초</div>
<div style="font-size:16px;color:#E84E10;font-weight:700;line-height:1.4">26번째가 당신</div>
</div>

</div>

<div style="display:flex;align-items:center;gap:var(--s-4);padding-top:var(--s-3)">
<div style="font-size:12px;color:#6E6E73;letter-spacing:3px;font-weight:400">4 EPISODES</div>
<div style="flex:1;height:1px;background:#E8E8E8"></div>
<div style="font-size:12px;color:#6E6E73;letter-spacing:2px;font-weight:400">인스타 릴스 + 유튜브 쇼츠 + 틱톡 동시 업로드 · 월 1편 공개</div>
</div>

</div>"""


# =============================================================================
# P39 (idx=38) - ROW 엄청나게 깔끔
# 채널·주기·목표를 ROW로 한 줄씩 시원하게
# =============================================================================
P39 = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:소셜 미디어--><div style="height:100%;display:flex;flex-direction:column;justify-content:space-between;padding:var(--s-5) var(--s-5)">

<div>
<div style="font-size:14px;color:#6E6E73;letter-spacing:4px;font-weight:400;margin-bottom:var(--s-1)">Ⅲ. 세부 과업 수행 계획 / SNS Operation</div>
<div style="width:64px;height:3px;background:#E84E10;margin-bottom:var(--s-5)"></div>
<div style="font-size:72px;font-weight:700;color:#1A1A1A;line-height:1.1;letter-spacing:-2px">3채널 통합 운영</div>
<div style="font-size:20px;color:#6E6E73;margin-top:var(--s-2)">수시 집중기 5~7월 예산 70% 집중</div>
</div>

<div style="display:flex;flex-direction:column;gap:0">

<div style="display:grid;grid-template-columns:60px 1fr 200px 200px 160px;gap:var(--s-3);align-items:center;padding:var(--s-3) 0;border-top:1px solid #1A1A1A">
<div style="font-size:13px;color:#6E6E73;letter-spacing:3px;font-weight:400">01</div>
<div style="font-size:28px;font-weight:700;color:#1A1A1A">인스타그램</div>
<div style="font-size:16px;color:#6E6E73">시안 이미지 · 릴스 · 스토리</div>
<div style="font-size:16px;color:#1A1A1A">주 3회 업로드</div>
<div style="font-size:16px;color:#E84E10;font-weight:700;text-align:right">팔로워 +500/월</div>
</div>

<div style="display:grid;grid-template-columns:60px 1fr 200px 200px 160px;gap:var(--s-3);align-items:center;padding:var(--s-3) 0;border-top:1px solid #E8E8E8">
<div style="font-size:13px;color:#6E6E73;letter-spacing:3px;font-weight:400">02</div>
<div style="font-size:28px;font-weight:700;color:#1A1A1A">유튜브 쇼츠</div>
<div style="font-size:16px;color:#6E6E73">숏폼 · 졸업생 인터뷰</div>
<div style="font-size:16px;color:#1A1A1A">주 2회 업로드</div>
<div style="font-size:16px;color:#E84E10;font-weight:700;text-align:right">조회수 3,000+/편</div>
</div>

<div style="display:grid;grid-template-columns:60px 1fr 200px 200px 160px;gap:var(--s-3);align-items:center;padding:var(--s-3) 0;border-top:1px solid #E8E8E8;border-bottom:1px solid #1A1A1A">
<div style="font-size:13px;color:#6E6E73;letter-spacing:3px;font-weight:400">03</div>
<div style="font-size:28px;font-weight:700;color:#1A1A1A">네이버 블로그</div>
<div style="font-size:16px;color:#6E6E73">팩트 카드뉴스 · 입시 가이드</div>
<div style="font-size:16px;color:#1A1A1A">주 2회 업로드</div>
<div style="font-size:16px;color:#E84E10;font-weight:700;text-align:right">검색 상위 노출</div>
</div>

</div>

<div style="display:flex;align-items:center;gap:var(--s-4);padding-top:var(--s-3)">
<div style="font-size:12px;color:#6E6E73;letter-spacing:3px;font-weight:400">3 CHANNELS</div>
<div style="flex:1;height:1px;background:#E8E8E8"></div>
<div style="font-size:12px;color:#6E6E73;letter-spacing:2px;font-weight:400">참여형 해시태그 · 학과 로테이션 · 월간 리포트 제공</div>
</div>

</div>"""


def main():
    conn = sqlite3.connect(str(DB))

    # 1) P37 교체
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=36",
        (P37, PID),
    )
    print("[1] P37 (idx=36) - VOGUE/Swiss Executive Summary 레이아웃 적용")

    # 2) P39 교체
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=38",
        (P39, PID),
    )
    print("[2] P39 (idx=38) - ROW 3채널 깔끔 레이아웃 적용")

    # 3) 마지막장(idx=48) 삭제
    conn.execute(
        "DELETE FROM sections WHERE proposal_id=? AND order_idx=48",
        (PID,),
    )
    print("[3] 마지막장(idx=48 '2026 각인 · 2027 많이 팔다') 삭제")

    conn.commit()

    # 4) 결과 확인
    rows = conn.execute(
        "SELECT order_idx, title FROM sections WHERE proposal_id=? AND order_idx >= 45 ORDER BY order_idx",
        (PID,),
    ).fetchall()
    print("\n== 뒤쪽 슬라이드 확인 ==")
    for r in rows:
        print(f"  idx={r[0]}: {r[1]}")

    conn.close()
    print("\n완료")


if __name__ == "__main__":
    main()
