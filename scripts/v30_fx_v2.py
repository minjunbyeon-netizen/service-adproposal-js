# -*- coding: utf-8 -*-
"""FX v2: 임팩트 강화 (pre-pause + scale punch + sequential)."""
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
        print(f"order={order} (P{order+1}) v2 applied")
    else:
        print(f"order={order} (P{order+1}) no change")


# ---------- P4: 숫자 완료 후 punch, 간격 확대 ----------
def fx_p4(body):
    # 기존 데이터 속성 → 새 delay + punch class wrapper
    # 96.4% (delay 600ms, duration 1200ms → ends 1800ms, punch 1800ms)
    body = body.replace(
        '<span class="is-accent w-bold" style="font-size:30px" data-count-to="96.4" data-count-decimals="1" data-count-suffix="%" data-count-delay="200">0.0%</span>',
        '<span class="is-accent w-bold fx-num-1" style="font-size:30px" data-count-to="96.4" data-count-decimals="1" data-count-suffix="%" data-count-delay="600" data-count-duration="1200">0.0%</span>',
    )
    # 55위 (delay 1900ms → ends 3100ms, punch 3100ms)
    body = body.replace(
        '<span class="is-accent w-bold" style="font-size:30px" data-count-to="55" data-count-suffix="위" data-count-delay="500">0위</span>',
        '<span class="is-accent w-bold fx-num-2" style="font-size:30px" data-count-to="55" data-count-suffix="위" data-count-delay="1900" data-count-duration="1200">0위</span>',
    )
    # 25명 (delay 3200ms → ends 4400ms, punch 4400ms)
    body = body.replace(
        '<span class="is-accent w-bold" style="font-size:30px" data-count-to="25" data-count-suffix="명" data-count-delay="800">0명</span>',
        '<span class="is-accent w-bold fx-num-3" style="font-size:30px" data-count-to="25" data-count-suffix="명" data-count-delay="3200" data-count-duration="1200">0명</span>',
    )
    return body


# ---------- P10: 웨이브 컨테이너 + 소음 단어 pop ----------
def fx_p10(body):
    # 웨이브폼 container (fx-wave-bar들을 감싸는 flex div)
    body = body.replace(
        '<div style="display:flex;align-items:flex-end;justify-content:center;gap:4px;height:96px;margin-bottom:var(--s-4);width:420px">',
        '<div class="fx-wave-container" style="display:flex;align-items:flex-end;justify-content:center;gap:4px;height:96px;margin-bottom:var(--s-4);width:420px">',
    )
    # "소음" 단어에 fx-noise-word
    body = body.replace(
        '<div class="t-display" style="color:#E84E10;margin-bottom:var(--s-5)">소음</div>',
        '<div class="t-display fx-noise-word" style="color:#E84E10;margin-bottom:var(--s-5)">소음</div>',
    )
    return body


# ---------- P11: 화살표는 이미 fx-flip-rotor, before는 fx-flip-before 유지 ----------
# (CSS만 업그레이드, HTML 변경 불필요 — 이미 클래스 있음)
def fx_p11(body):
    return body  # no-op


# ---------- P14: 각인 숫자 div에 fx-pop-N 추가 ----------
def fx_p14(body):
    # 3.6%, 글로벌 55위, 1개의 시스템 wrapper div
    mapping = [
        ('font-size:72px;font-weight:700;color:#E84E10;letter-spacing:-2px;line-height:1">3.6%',
         'font-size:72px;font-weight:700;color:#E84E10;letter-spacing:-2px;line-height:1" class="fx-pop-1-wrap">3.6%'),
        ('font-size:56px;font-weight:700;color:#E84E10;letter-spacing:-1.5px;line-height:1">글로벌 55위',
         'font-size:56px;font-weight:700;color:#E84E10;letter-spacing:-1.5px;line-height:1" class="fx-pop-2-wrap">글로벌 55위'),
        ('font-size:56px;font-weight:700;color:#E84E10;letter-spacing:-1.5px;line-height:1">1개의 시스템',
         'font-size:56px;font-weight:700;color:#E84E10;letter-spacing:-1.5px;line-height:1" class="fx-pop-3-wrap">1개의 시스템'),
    ]
    # 실제로는 class를 div에 추가하는 형태 — 기존 패턴 활용
    # HTML 속성 순서 문제로 class 속성을 inline style 뒤에 추가하는 대신,
    # div 자체를 찾아 class를 주입.
    # 더 안전한 방법: 숫자를 감싸는 inner div에 fx-pop-N을 별도 span wrap
    # 3.6% 텍스트를 <span class="fx-pop-1">3.6%</span>로
    body = body.replace(
        '<div style="font-size:72px;font-weight:700;color:#E84E10;letter-spacing:-2px;line-height:1">3.6%</div>',
        '<div style="font-size:72px;font-weight:700;color:#E84E10;letter-spacing:-2px;line-height:1"><span class="fx-pop-1">3.6%</span></div>',
    )
    body = body.replace(
        '<div style="font-size:56px;font-weight:700;color:#E84E10;letter-spacing:-1.5px;line-height:1">글로벌 55위</div>',
        '<div style="font-size:56px;font-weight:700;color:#E84E10;letter-spacing:-1.5px;line-height:1"><span class="fx-pop-2">글로벌 55위</span></div>',
    )
    body = body.replace(
        '<div style="font-size:56px;font-weight:700;color:#E84E10;letter-spacing:-1.5px;line-height:1">1개의 시스템</div>',
        '<div style="font-size:56px;font-weight:700;color:#E84E10;letter-spacing:-1.5px;line-height:1"><span class="fx-pop-3">1개의 시스템</span></div>',
    )
    return body


# ---------- P30: 슬로건 3단계 분리 ----------
def fx_p30(body):
    # 기존: <div class="t-headline fx-slogan" style="...">영산대학교는,<br><span class="is-accent">지혜</span>로 증명합니다</div>
    # 신규: <div class="t-headline" style="..."><span class="fx-slogan-1">영산대학교는,</span><br><span class="fx-slogan-2"><span class="is-accent fx-zihye-punch">지혜</span>로 증명합니다</span></div>
    body = body.replace(
        '<div class="t-headline fx-slogan" style="line-height:1.2;font-size:88px">영산대학교는,<br><span class="is-accent">지혜</span>로 증명합니다</div>',
        '<div class="t-headline" style="line-height:1.2;font-size:88px"><span class="fx-slogan-1">영산대학교는,</span><br><span class="fx-slogan-2"><span class="is-accent fx-zihye-punch">지혜</span>로 증명합니다</span></div>',
    )
    return body


def main():
    conn = sqlite3.connect(str(DB))
    update(conn, 3, fx_p4)
    update(conn, 9, fx_p10)
    update(conn, 10, fx_p11)
    update(conn, 13, fx_p14)
    update(conn, 29, fx_p30)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
