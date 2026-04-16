# -*- coding: utf-8 -*-
"""V101 디자인 시스템 리팩토링 — 7 토큰 체계 + HIGH/MID/팀장지적 일괄 수정.

## 토큰 시스템

| 토큰      | 크기    | 용도                      |
|-----------|--------|--------------------------|
| display   | 120px  | divider, 최종 수미 슬로건  |
| hero      | 72px   | 표지, 각인 선언           |
| kpi       | 56px   | 수치 강조 전용            |
| headline  | 48px   | 슬라이드 타이틀           |
| body      | 24px   | 본문                     |
| table     | 20px   | 표·차트                  |
| caption   | 16px   | 캡션·라벨·출처            |

## 매핑 방식

1. Template CSS: :root 변수 선언 + 기존 .t-* 클래스 토큰 참조
2. DB: 인라인 font-size:Npx 교체 (구간 기반 매핑)
3. 특정 슬라이드 인라인 개별 수정 (HIGH/MID 건)
"""
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "adproposal.db"
TEMPLATE = ROOT / "templates" / "presentation_clean.html"
PID = 179

# =============================================================================
# PHASE 1: Template CSS 토큰 시스템 재작성
# =============================================================================

def refactor_template_css():
    """Template CSS를 7토큰 체계로 재작성."""
    tpl = TEMPLATE.read_text(encoding="utf-8")

    # 1. :root에 토큰 선언 삽입 (기존 --s-* 다음에 추가)
    old_root = """:root{
  --s-1:8px; --s-2:16px; --s-3:24px; --s-4:32px;
  --s-5:48px; --s-6:64px; --s-7:96px;
}"""
    new_root = """:root{
  --s-1:8px; --s-2:16px; --s-3:24px; --s-4:32px;
  --s-5:48px; --s-6:64px; --s-7:96px;
  /* ===== 7 토큰 디자인 시스템 ===== */
  --fs-display:120px;
  --fs-hero:72px;
  --fs-kpi:56px;
  --fs-headline:48px;
  --fs-body:24px;
  --fs-table:20px;
  --fs-caption:16px;
}"""
    tpl = tpl.replace(old_root, new_root)

    # 2. 타이포 유틸리티 클래스 재정의 (토큰 참조)
    old_typo = """.content-body .t-display  {font-size:96px;font-weight:700;line-height:1;letter-spacing:-6px;color:#1A1A1A;font-family:'Noto Sans KR',sans-serif}
.content-body .t-hero     {font-size:96px;font-weight:700;line-height:1;letter-spacing:-4px;color:#1A1A1A}
.content-body .t-headline {font-size:96px;font-weight:700;line-height:1.1;letter-spacing:-3px;color:#1A1A1A}
.content-body .t-title    {font-size:48px;font-weight:700;line-height:1.15;letter-spacing:-1.5px;color:#1A1A1A}
.content-body .t-heading  {font-size:24px;font-weight:700;line-height:1.3;letter-spacing:-1px;color:#1A1A1A}
.content-body .t-subtitle {font-size:24px;font-weight:700;line-height:1.5;color:#1A1A1A}
.content-body .t-body     {font-size:24px;font-weight:400;line-height:1.6;color:#1A1A1A}
.content-body .t-caption  {font-size:24px;font-weight:400;line-height:1.5;color:#6E6E73}
.content-body .t-overline {font-size:14px;font-weight:700;line-height:1.4;letter-spacing:3px;color:#6E6E73}"""

    new_typo = """.content-body .t-display  {font-size:var(--fs-display);font-weight:700;line-height:1;letter-spacing:-4px;color:#1A1A1A}
.content-body .t-hero     {font-size:var(--fs-hero);font-weight:700;line-height:1.1;letter-spacing:-2px;color:#1A1A1A}
.content-body .t-kpi      {font-size:var(--fs-kpi);font-weight:700;line-height:1;letter-spacing:-1.5px;color:#1A1A1A}
.content-body .t-headline {font-size:var(--fs-headline);font-weight:700;line-height:1.2;letter-spacing:-1.5px;color:#1A1A1A}
.content-body .t-title    {font-size:var(--fs-headline);font-weight:700;line-height:1.25;letter-spacing:-1px;color:#1A1A1A}
.content-body .t-heading  {font-size:var(--fs-headline);font-weight:700;line-height:1.3;letter-spacing:-0.8px;color:#1A1A1A}
.content-body .t-subtitle {font-size:var(--fs-body);font-weight:700;line-height:1.5;color:#1A1A1A}
.content-body .t-body     {font-size:var(--fs-body);font-weight:400;line-height:1.6;color:#1A1A1A}
.content-body .t-caption  {font-size:var(--fs-caption);font-weight:400;line-height:1.5;color:#6E6E73}
.content-body .t-overline {font-size:var(--fs-caption);font-weight:700;line-height:1.4;letter-spacing:3px;color:#6E6E73}"""

    tpl = tpl.replace(old_typo, new_typo)

    # 3. 그리드 내부 폰트 오버라이드도 caption 토큰으로
    old_grid = """.content-body [style*="grid-template-columns"] .t-body{font-size:14px;line-height:1.8}
.content-body [style*="grid-template-columns"] .t-caption{font-size:14px;line-height:1.7}
.content-body [style*="grid-template-columns"] .t-overline{font-size:14px}
.content-body [style*="border:1px"] .t-body{font-size:14px;line-height:1.8}"""
    new_grid = """.content-body [style*="grid-template-columns"] .t-body{font-size:var(--fs-caption);line-height:1.8}
.content-body [style*="grid-template-columns"] .t-caption{font-size:var(--fs-caption);line-height:1.7}
.content-body [style*="grid-template-columns"] .t-overline{font-size:var(--fs-caption)}
.content-body [style*="border:1px"] .t-body{font-size:var(--fs-caption);line-height:1.8}"""
    tpl = tpl.replace(old_grid, new_grid)

    # 4. divider-title 120px로
    tpl = tpl.replace(
        ".divider-title{font-size:96px;font-weight:700;line-height:1.1;color:#fff;word-break:keep-all;letter-spacing:-2px}",
        ".divider-title{font-size:var(--fs-display);font-weight:700;line-height:1.1;color:#fff;word-break:keep-all;letter-spacing:-4px}"
    )

    # 5. cover-title 96px로 (표지, 수미상관 대응)
    tpl = re.sub(
        r"\.cover-title\{[^}]+\}",
        ".cover-title{font-size:var(--fs-display);font-weight:700;line-height:0.9;color:#1A1A1A;letter-spacing:-4px;font-family:'Noto Sans KR',sans-serif;font-variant-numeric:tabular-nums;text-align:center}",
        tpl
    )

    # 6. content-header h3 토큰
    tpl = re.sub(
        r"content-header h3\{[^}]+\}",
        "content-header h3{font-size:var(--fs-headline);font-weight:700;color:#1A1A1A;letter-spacing:-0.8px}",
        tpl
    )

    # 7. content-body 기본 사이즈
    tpl = re.sub(
        r"\.content-body\{font-size:16px;line-height:1\.7",
        ".content-body{font-size:var(--fs-body);line-height:1.6",
        tpl
    )

    # 8. slide-pagenum
    tpl = re.sub(
        r"\.slide-pagenum\{[^}]+\}",
        ".slide-pagenum{position:absolute;top:50px;right:80px;font-size:var(--fs-caption);font-weight:700;color:#6E6E73;line-height:1;font-family:'Noto Sans KR',sans-serif;letter-spacing:2px;font-variant-numeric:tabular-nums}",
        tpl
    )

    # 9. section-parent
    tpl = re.sub(
        r"\.section-parent\{[^}]+\}",
        ".section-parent{font-size:var(--fs-caption);color:#E84E10;font-weight:700;letter-spacing:3px;display:block;margin-bottom:12px}",
        tpl
    )

    # 10. slide-tag
    tpl = re.sub(
        r"\.slide-tag\{[^}]+\}",
        ".slide-tag{font-size:var(--fs-caption);color:#1A1A1A;font-weight:400;display:inline-block;margin-top:6px;letter-spacing:0}",
        tpl
    )

    TEMPLATE.write_text(tpl, encoding="utf-8")
    print("[Phase 1] Template CSS 7토큰 재작성 완료")


# =============================================================================
# PHASE 2: DB 인라인 font-size 재매핑 (구간 기반)
# =============================================================================

def map_inline_size(px: int) -> int:
    """기존 14/24/48/96 4단계 → 의미 단위 7토큰 매핑.

    대규모 컨텐츠는 기존 값 그대로 두고, 명백히 작은 것만 보정.
    """
    # 4단계 → 7토큰 대체
    if px <= 15:
        return 16  # caption
    if px <= 22:
        return 20  # table (18-22 사이는 표 가능성)
    if px <= 28:
        return 24  # body
    if px <= 44:
        return 40  # 중간 (headline 조금 작게)
    if px <= 60:
        return 56  # kpi or headline large
    if px <= 80:
        return 72  # hero
    return 120  # display


def refactor_db_inline():
    """DB sections.content의 font-size 재매핑."""
    conn = sqlite3.connect(str(DB))
    rows = conn.execute(
        "SELECT id, content FROM sections WHERE proposal_id=? AND content IS NOT NULL",
        (PID,)
    ).fetchall()

    total = 0
    for sid, content in rows:
        def replacer(m):
            old = int(m.group(1))
            new = map_inline_size(old)
            return f"font-size:{new}px"

        new_content = re.sub(r"font-size\s*:\s*(\d+)px", replacer, content)
        if new_content != content:
            conn.execute(
                "UPDATE sections SET content=? WHERE id=?", (new_content, sid)
            )
            total += 1
    conn.commit()
    conn.close()
    print(f"[Phase 2] DB 인라인 font-size 재매핑 — {total}개 섹션 업데이트")


# =============================================================================
# PHASE 3: 특정 HIGH/MID 슬라이드 개별 수정
# =============================================================================

def fix_p3_kpi():
    """P3 시장 현황 — 수치 3개 KPI 통일 (56px bold)."""
    conn = sqlite3.connect(str(DB))
    row = conn.execute(
        "SELECT content FROM sections WHERE proposal_id=? AND order_idx=2",
        (PID,)
    ).fetchone()
    c = row[0]
    # -18%, 2.3배, 38% 각각 56px로
    # 이미 reMapping으로 40~56로 조정되어있을 수 있지만 통일
    c = re.sub(
        r'(font-size:\d+px;font-weight:700;color:#E84E10;line-height:1;min-width:140px)',
        'font-size:56px;font-weight:700;color:#E84E10;line-height:1;min-width:180px',
        c
    )
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=2",
        (c, PID)
    )
    conn.commit()
    conn.close()
    print("[Phase 3] P3 KPI 수치 56px 통일")


def fix_p16_before_contrast():
    """P16 BEFORE 컬럼 색상 #A0A0A5 → #585858 (대조 강화)."""
    conn = sqlite3.connect(str(DB))
    row = conn.execute(
        "SELECT content FROM sections WHERE proposal_id=? AND order_idx=15",
        (PID,)
    ).fetchone()
    c = row[0]
    # BEFORE 블록의 색상 #A0A0A5 → #585858
    # 단, 해당 블록만 (BEFORE grid column)
    c = c.replace("color:#A0A0A5;line-height:1.6", "color:#585858;line-height:1.6")
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=15",
        (c, PID)
    )
    conn.commit()
    conn.close()
    print("[Phase 3] P16 BEFORE 컬럼 색상 #585858로 대조 강화")


def fix_p26_shift():
    """P26 SHIFT 전환 — 텍스트 크기 48→72px 승격."""
    conn = sqlite3.connect(str(DB))
    # P26은 idx=26 (SHIFT 전환 슬라이드)
    row = conn.execute(
        "SELECT order_idx, content FROM sections WHERE proposal_id=? AND title LIKE '%전환%지면%영상%'",
        (PID,)
    ).fetchone()
    if not row:
        print("[Phase 3] P26 SHIFT 슬라이드 찾을 수 없음 — skip")
        return
    idx = row[0]
    c = row[1]
    # '지면으로 임팩트' / '영상으로는 스토리' 텍스트 크기 확대
    # 현재 48 또는 60으로 되어있을 것
    c = re.sub(
        r"font-size:48px;font-weight:700;color:#1A1A1A;line-height:1\.4",
        "font-size:72px;font-weight:700;color:#1A1A1A;line-height:1.35",
        c
    )
    c = re.sub(
        r"font-size:60px;font-weight:700",
        "font-size:72px;font-weight:700",
        c
    )
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=?",
        (c, PID, idx)
    )
    conn.commit()
    conn.close()
    print(f"[Phase 3] P26 SHIFT(idx={idx}) 텍스트 72px로 승격")


def fix_table_slides_p42_p46():
    """P42~P46 운영/예산/결과 표 슬라이드 — 표 내부 폰트 20px 보장."""
    conn = sqlite3.connect(str(DB))
    # 광고 운영 및 광고 예산 집행 관련 슬라이드 찾기
    rows = conn.execute(
        "SELECT id, order_idx, title FROM sections WHERE proposal_id=? AND (title LIKE '%예산%집행%' OR title LIKE '%결과 분석%' OR title LIKE '%광고 운영%') ORDER BY order_idx",
        (PID,)
    ).fetchall()
    for rid, idx, title in rows:
        content_row = conn.execute("SELECT content FROM sections WHERE id=?", (rid,)).fetchone()
        c = content_row[0]
        if not c:
            continue
        # 16px / 14px 표 관련 → 20px로 승격
        # 이미 caption 매핑으로 16이 됐을 것이지만, 표 안에선 20으로 강제
        new_c = re.sub(r'(<table[^>]*)(style="[^"]*)(font-size:16px)',
                        lambda m: m.group(1) + m.group(2) + 'font-size:20px', c)
        # table 안 td/th의 font-size도 처리
        new_c = re.sub(r'(<(?:td|th)[^>]*)(style="[^"]*)(font-size:16px)',
                        lambda m: m.group(1) + m.group(2) + 'font-size:20px', new_c)
        if new_c != c:
            conn.execute("UPDATE sections SET content=? WHERE id=?", (new_c, rid))
            print(f"[Phase 3] P{idx+1} ({title[:30]}) 표 폰트 20px 승격")
    conn.commit()
    conn.close()


def fix_p1_p51_sumi_sangwan():
    """팀장 지적: P1 ↔ P51 수미상관 시각 동조. 에필로그 0825503 display(120px)로."""
    conn = sqlite3.connect(str(DB))
    row = conn.execute(
        "SELECT content FROM sections WHERE proposal_id=? AND title LIKE '%에필로그%'",
        (PID,)
    ).fetchone()
    if not row:
        print("[Phase 4] 에필로그 못 찾음")
        return
    c = row[0]
    # 0825503 에필로그 폰트 크기 120px 통일
    c = re.sub(
        r'font-size:(96|120|160)px;font-weight:700;color:#1A1A1A;letter-spacing:-6px;font-family',
        'font-size:120px;font-weight:700;color:#1A1A1A;letter-spacing:-4px;font-family',
        c
    )
    c = re.sub(
        r'font-size:(96|120|160)px;font-weight:700;color:#1A1A1A;letter-spacing:-[0-9]+px',
        'font-size:120px;font-weight:700;color:#1A1A1A;letter-spacing:-4px',
        c
    )
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND title LIKE '%에필로그%'",
        (c, PID)
    )
    conn.commit()
    conn.close()
    print("[Phase 4] 에필로그 0825503 display 120px로 P1과 수미동조")


# =============================================================================
# 실행
# =============================================================================

def main():
    print("=" * 60)
    print("V101 디자인 시스템 리팩토링 시작")
    print("=" * 60)

    refactor_template_css()
    refactor_db_inline()
    fix_p3_kpi()
    fix_p16_before_contrast()
    fix_p26_shift()
    fix_table_slides_p42_p46()
    fix_p1_p51_sumi_sangwan()

    print("=" * 60)
    print("리팩토링 완료 — 검증 단계로 진행")
    print("=" * 60)


if __name__ == "__main__":
    main()
