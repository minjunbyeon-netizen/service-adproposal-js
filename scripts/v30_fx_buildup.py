# -*- coding: utf-8 -*-
"""빌드업 FX 적용 (P3·P4·P10·P11·P14·P30).
CSS/JS는 이미 template에 있음. 섹션 content에 fx 클래스/data 속성만 주입.
"""
import re
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 138


def update(conn, order, fn):
    r = conn.execute(
        "SELECT id, content FROM sections WHERE proposal_id=? AND order_idx=?",
        (PID, order),
    ).fetchone()
    if not r:
        print(f"order={order} NOT FOUND")
        return
    new = fn(r[1])
    if new != r[1]:
        conn.execute("UPDATE sections SET content=? WHERE id=?", (new, r[0]))
        print(f"order={order} (P{order+1}) fx applied")
    else:
        print(f"order={order} (P{order+1}) no change")


# --------- P3 (order=2): "?" 커서 깜빡임 ---------
def fx_p3(body):
    return body.replace(
        '<span class="is-accent">?</span>',
        '<span class="is-accent fx-cursor">?</span>',
    )


# --------- P4 (order=3): 숫자 count-up ---------
def fx_p4(body):
    # 96.4%
    body = body.replace(
        '<span class="is-accent w-bold" style="font-size:30px">96.4%</span>',
        '<span class="is-accent w-bold" style="font-size:30px" data-count-to="96.4" data-count-decimals="1" data-count-suffix="%" data-count-delay="200">0.0%</span>',
    )
    # 55위
    body = body.replace(
        '<span class="is-accent w-bold" style="font-size:30px">55위</span>',
        '<span class="is-accent w-bold" style="font-size:30px" data-count-to="55" data-count-suffix="위" data-count-delay="500">0위</span>',
    )
    # 25명
    body = body.replace(
        '<span class="is-accent w-bold" style="font-size:30px">25명</span>',
        '<span class="is-accent w-bold" style="font-size:30px" data-count-to="25" data-count-suffix="명" data-count-delay="800">0명</span>',
    )
    # 校訓 — static (그대로)
    return body


# --------- P10 (order=9): 웨이브폼 bar 애니 ---------
def fx_p10(body):
    # 각 bar div에 fx-wave-bar 클래스 + 순차 delay 적용
    bar_count = [0]

    def repl(m):
        bar_count[0] += 1
        delay = (bar_count[0] % 7) * 0.08  # 0.0 ~ 0.48s
        original_style = m.group(1)
        return (
            f'<div class="fx-wave-bar" style="{original_style};animation-delay:{delay:.2f}s">'
        )

    new_body = re.sub(
        r'<div style="(width:6px;background:#E84E10;height:\d+%;border-radius:2px)">',
        repl,
        body,
    )
    return new_body


# --------- P11 (order=10): Before → After flip ---------
def fx_p11(body):
    # Before 카드 (#F9F9F9 배경)
    body = body.replace(
        '<div style="border:1px solid #E8E8E8;border-radius:8px;padding:24px 36px;text-align:center;min-width:280px;background:#F9F9F9">',
        '<div class="fx-flip-before" style="border:1px solid #E8E8E8;border-radius:8px;padding:24px 36px;text-align:center;min-width:280px;background:#F9F9F9">',
    )
    # 회전 화살표
    body = body.replace(
        '<div style="font-size:56px;color:#E84E10;font-weight:700;line-height:1">↻</div>',
        '<div class="fx-flip-rotor" style="font-size:56px;color:#E84E10;font-weight:700;line-height:1">↻</div>',
    )
    # After 카드 (#FFF5F0 배경)
    body = body.replace(
        '<div style="border:2px solid #E84E10;border-radius:8px;padding:24px 36px;text-align:center;min-width:280px;background:#FFF5F0">',
        '<div class="fx-flip-after" style="border:2px solid #E84E10;border-radius:8px;padding:24px 36px;text-align:center;min-width:280px;background:#FFF5F0">',
    )
    return body


# --------- P14 (order=13): 3행 stagger fade ---------
def fx_p14(body):
    # 각 row의 소음/화살표/각인 3셀 묶음을 stagger. grid 안의 row 1~3만 target.
    # row1: "01" 96.4% 취업률 -> 3.6% 탈락률
    # row2: "02" 국내 55위 -> 글로벌 55위
    # row3: "03" 25명의 총지배인 -> 1개의 시스템
    # 각 row는 3개 cell로 구성. cell마다 class를 붙이면 복잡하므로 grid row를 감싸는 wrapper는 없음 (flat grid).
    # 대안: 각 row의 3개 cell(소음+화살표+각인)에 각각 fx-stagger-N 적용.
    row_marks = [
        ('01', 'fx-stagger-1'),
        ('02', 'fx-stagger-2'),
        ('03', 'fx-stagger-3'),
    ]
    for label, cls in row_marks:
        # 소음 셀
        body = body.replace(
            f'<div style="text-align:right;padding:var(--s-2) 0;font-size:20px;color:#A0A0A5;font-weight:400;line-height:1.4"><span style="font-size:12px;color:#C5C5C9">{label}</span>',
            f'<div class="{cls}" style="text-align:right;padding:var(--s-2) 0;font-size:20px;color:#A0A0A5;font-weight:400;line-height:1.4"><span style="font-size:12px;color:#C5C5C9">{label}</span>',
        )
    # arrow & 각인 cell도 같이 stagger - 각 row의 arrow 3개가 동일하므로 순차 replacement 필요
    # 단순화: 화살표 3개를 sequential replace + 각인 cell 3개도 sequential
    arrow_template = '<div style="font-size:40px;font-weight:700;color:#E84E10;line-height:1">→</div>'
    arrow_replacements = [
        '<div class="fx-stagger-1" style="font-size:40px;font-weight:700;color:#E84E10;line-height:1">→</div>',
        '<div class="fx-stagger-2" style="font-size:40px;font-weight:700;color:#E84E10;line-height:1">→</div>',
        '<div class="fx-stagger-3" style="font-size:40px;font-weight:700;color:#E84E10;line-height:1">→</div>',
    ]
    for replacement in arrow_replacements:
        body = body.replace(arrow_template, replacement, 1)

    # 각인 cell (3.6%, 글로벌 55위, 1개의 시스템)
    kakin_mapping = [
        ('3.6%', 'fx-stagger-1'),
        ('글로벌 55위', 'fx-stagger-2'),
        ('1개의 시스템', 'fx-stagger-3'),
    ]
    for key_text, cls in kakin_mapping:
        # <div style="text-align:left;padding:var(--s-1) 0;line-height:1"><div style="font-size:72px...
        body = re.sub(
            r'<div (style="text-align:left;padding:var\(--s-1\) 0;line-height:1")><div (style="font-size:[0-9]+px;font-weight:700;color:#E84E10;letter-spacing:-[0-9.]+px;line-height:1")>'
            + re.escape(key_text),
            f'<div class="{cls}" \\1><div \\2>{key_text}',
            body,
            count=1,
        )
    return body


# --------- P30 (order=29): 슬로건 slow fade ---------
def fx_p30(body):
    return body.replace(
        '<div class="t-headline" style="line-height:1.2;font-size:88px">',
        '<div class="t-headline fx-slogan" style="line-height:1.2;font-size:88px">',
    )


def main():
    conn = sqlite3.connect(str(DB))
    update(conn, 2, fx_p3)
    update(conn, 3, fx_p4)
    update(conn, 9, fx_p10)
    update(conn, 10, fx_p11)
    update(conn, 13, fx_p14)
    update(conn, 29, fx_p30)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
