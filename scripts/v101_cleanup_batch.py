# -*- coding: utf-8 -*-
"""V101 일괄 정리 — P37 숏폼 재작성, P38 도식화, P39 굵기 완화, 전체 3.6% 제거."""
import sqlite3
import re
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


def main():
    conn = sqlite3.connect(str(DB))

    # =========================================================================
    # 1. 모든 슬라이드에서 레거시 "3.6%" / "36%" / "지혜로운 가치" / 구식 슬로건 정리
    # =========================================================================
    rows = conn.execute(
        "SELECT id, content FROM sections WHERE proposal_id=? AND content IS NOT NULL",
        (PID,)
    ).fetchall()

    legacy_cleanup = [
        (r"3\.6%", "26번째"),           # 3.6% 잘못된 팩트 → 슬로건 키워드
        (r"취업률 96\.4%", "총지배인 25명"),
        (r"96\.4%", "25명"),
        (r"지혜로운 가치를 배우는 대학[\s,·]*지혜로운 당신을 만드는 대학", "산업이 선택한 대학"),
        (r"Room 1201", "산업이 선택한 대학"),
        (r"심사위원석", "글로벌 1위가 될 때까지"),
    ]

    touched = 0
    for rid, c in rows:
        orig = c
        for pat, rep in legacy_cleanup:
            c = re.sub(pat, rep, c)
        if c != orig:
            conn.execute("UPDATE sections SET content=? WHERE id=?", (c, rid))
            touched += 1
    print(f"레거시 카피 정리: {touched}개 섹션")

    # =========================================================================
    # 2. P37 (idx=36) 숏폼 — 3가지 슬로건 매핑으로 재작성
    # =========================================================================
    P37 = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:숏폼 기획-->**졸업선배 숏폼 시리즈 (연 4편)**

9~12월 입시 시즌 · 월 1편 공개 · 60초 세로형 · 인스타 릴스 + 유튜브 쇼츠 + 틱톡 동시 업로드

| 월 | 학과 | 전달 슬로건 | 핵심 장면 |
|---|---|---|---|
| 9월 | 호텔관광 | 산업이 선택한 대학 | 총지배인 아침 라운드 60초 |
| 10월 | 항공서비스 | 산업이 선택한 대학 | 승무원의 하루 60초 |
| 11월 | 조리예술 | 글로벌 1위가 될 때까지 | WACS 셰프의 주방 60초 |
| 12월 | 호텔관광 | 26번째가 당신 | 재학생 인터뷰 60초 |

**운영 방침**
현직 영산대 졸업생 섭외 · 3플랫폼 동시 업로드 · 2주차 성과 리포트 기반 차기 편 기획 반영"""
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=36",
        (P37, PID),
    )
    print("P37 숏폼 재작성: 3가지 슬로건 × 4편 매핑")

    # =========================================================================
    # 3. P38 (idx=37) 공식 홍보영상 — 도식화
    # =========================================================================
    P38 = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:공식 홍보영상--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;padding:var(--s-4) var(--s-5)"><div style="font-size:48px;font-weight:700;color:#1A1A1A;line-height:1.2;margin-bottom:var(--s-2)">대학 공식 홍보영상</div><div style="font-size:18px;color:#6E6E73;margin-bottom:var(--s-5)">TVC 15초 · 디지털 30초 · 풀버전 60초</div><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0;border-top:1px solid #1A1A1A;border-bottom:1px solid #1A1A1A;max-width:1400px;width:100%;margin-bottom:var(--s-4)"><div style="padding:var(--s-4) var(--s-3);border-right:1px solid #E8E8E8"><div style="font-size:13px;color:#E84E10;font-weight:700;letter-spacing:3px;margin-bottom:var(--s-2)">OPENING · 0–15초</div><div style="font-size:22px;font-weight:700;color:#1A1A1A;margin-bottom:var(--s-2);line-height:1.3">산업이 선택한 대학</div><div style="font-size:14px;color:#6E6E73;line-height:1.6">총지배인·셰프·승무원 현장 컷 3초씩 빠른 몽타주</div></div><div style="padding:var(--s-4) var(--s-3);border-right:1px solid #E8E8E8"><div style="font-size:13px;color:#E84E10;font-weight:700;letter-spacing:3px;margin-bottom:var(--s-2)">MIDDLE · 15–45초</div><div style="font-size:22px;font-weight:700;color:#1A1A1A;margin-bottom:var(--s-2);line-height:1.3">글로벌 1위가 될 때까지</div><div style="font-size:14px;color:#6E6E73;line-height:1.6">QS 세계 55위 · 홍콩과기대 AISIC · PATA 가입 세계 무대</div></div><div style="padding:var(--s-4) var(--s-3)"><div style="font-size:13px;color:#E84E10;font-weight:700;letter-spacing:3px;margin-bottom:var(--s-2)">CLOSING · 45–60초</div><div style="font-size:22px;font-weight:700;color:#1A1A1A;margin-bottom:var(--s-2);line-height:1.3">26번째가 당신</div><div style="font-size:14px;color:#6E6E73;line-height:1.6">졸업생 25명 얼굴 클로즈업 → 빈 26번째 자리</div></div></div><div style="display:flex;align-items:center;gap:var(--s-4);max-width:1400px;width:100%;padding-top:var(--s-3);border-top:1px solid #E8E8E8"><div style="font-size:13px;color:#6E6E73;font-weight:700;letter-spacing:3px">STYLE</div><div style="flex:1;height:1px;background:#E8E8E8"></div><div style="font-size:16px;color:#1A1A1A">다큐 톤 · 현장 핸드헬드 · 자연광 · 내레이션 최소화</div></div></div>"""
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=37",
        (P38, PID),
    )
    print("P38 공식 홍보영상 — 3단 타임라인 도식 (Opening/Middle/Closing)")

    # =========================================================================
    # 4. P39 (idx=38) SNS — font-weight:700 완화
    # =========================================================================
    row = conn.execute(
        "SELECT content FROM sections WHERE proposal_id=? AND order_idx=38",
        (PID,)
    ).fetchone()
    c = row[0]
    # 본문 설명 부분의 font-weight:700 대부분 제거
    # 핵심 헤드라인(3채널 통합 운영, 월간 콘텐츠 캘린더, 채널명)만 유지
    # 타이틀 격 ('3채널 통합 운영', '월간 캘린더' 같은 것 외)의 font-weight:700를 400으로
    # 유지 대상: font-size:48px (대형 타이틀), font-size:26px (채널명)
    # 그 외 font-size 15px, 14px, 13px, 12px, 11px의 font-weight:700를 400으로
    c = re.sub(
        r'(font-size:1[1-9]px;[^"]*)font-weight:700',
        r'\1font-weight:400',
        c
    )
    c = re.sub(
        r'font-weight:700;(font-size:1[1-9]px)',
        r'font-weight:400;\1',
        c
    )
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=38",
        (c, PID),
    )
    print("P39 SNS — 본문 font-weight:700 → 400 (핵심 헤드만 볼드 유지)")

    conn.commit()
    conn.close()
    print("\n완료")


if __name__ == "__main__":
    main()
