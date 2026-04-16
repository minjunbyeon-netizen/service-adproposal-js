# -*- coding: utf-8 -*-
"""P45 비용 효율 -> 업계 평균 vs 우리 비교 그래프."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 138


def row(name, metric, unit, ours, avg, ours_val, avg_val, cut_pct):
    """매체 비교 row (4단 grid: 매체명 · 2개 bar · 절감률)"""
    ours_width = round((ours_val / avg_val) * 100, 1)
    return f"""<div style="display:grid;grid-template-columns:160px 1fr 90px;gap:18px;align-items:center"><div style="font-weight:700;font-size:15px;color:#1A1A1A">{name}<br><span style="font-size:11px;color:#6E6E73;font-weight:400">{metric}</span></div><div style="display:flex;flex-direction:column;gap:6px"><div style="display:flex;align-items:center;gap:10px"><div style="width:64px;font-size:11px;color:#6E6E73;flex-shrink:0;letter-spacing:1px">업계 평균</div><div style="flex:1;height:20px;background:#E8E8E8;border-radius:3px;position:relative;overflow:hidden"><div style="width:100%;height:100%;background:#C5C5C9"></div><div style="position:absolute;right:10px;top:0;height:100%;display:flex;align-items:center;color:#1A1A1A;font-size:11px;font-weight:700">{unit} {avg}</div></div></div><div style="display:flex;align-items:center;gap:10px"><div style="width:64px;font-size:11px;color:#E84E10;flex-shrink:0;font-weight:700;letter-spacing:1px">우리</div><div style="flex:1;height:20px;background:#F5F5F5;border-radius:3px;position:relative;overflow:hidden"><div style="width:{ours_width}%;height:100%;background:#E84E10"></div><div style="position:absolute;left:calc({ours_width}% + 10px);top:0;height:100%;display:flex;align-items:center;color:#E84E10;font-size:11px;font-weight:700">{unit} {ours}</div></div></div></div><div style="text-align:right;font-weight:700;font-size:26px;color:#E84E10;letter-spacing:-1px">-{cut_pct}%</div></div>"""


def row_solo(name, metric, ours, avg_note):
    """비교 없는 단독 row (인쇄 매체 등)"""
    return f"""<div style="display:grid;grid-template-columns:160px 1fr 90px;gap:18px;align-items:center"><div style="font-weight:700;font-size:15px;color:#1A1A1A">{name}<br><span style="font-size:11px;color:#6E6E73;font-weight:400">{metric}</span></div><div style="display:flex;align-items:center;gap:10px"><div style="width:64px;font-size:11px;color:#E84E10;flex-shrink:0;font-weight:700;letter-spacing:1px">우리</div><div style="flex:1;height:20px;background:#F5F5F5;border-radius:3px;position:relative;overflow:hidden"><div style="width:100%;height:100%;background:#E84E10"></div><div style="position:absolute;right:10px;top:0;height:100%;display:flex;align-items:center;color:#fff;font-size:11px;font-weight:700">{ours}</div></div></div><div style="text-align:right;font-size:11px;color:#6E6E73;font-style:italic">{avg_note}</div></div>"""


rows_html = "".join([
    row("디지털 DA", "노출 200만회", "CPM", "1,563원", "2,500원", 1563, 2500, 37),
    row("유튜브 프리롤", "완시청 5만회", "CPCV", "625원", "900원", 625, 900, 31),
    row("숏폼 4편", "합산 조회 4.5만", "편당", "313만", "500만", 313, 500, 37),
    row("SNS 운영", "팔로워 +6,000명", "팔로워당", "208원", "350원", 208, 350, 41),
    row_solo("인쇄 매체", "일 유동 5만 × 180일", "일 10,417원", "업계 비교 없음"),
])

P45 = (
    '<!--PARENT:IV 사업 관리 계획--><!--TAG:비용 효율-->'
    '<div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0">'
    '<div class="t-heading" style="margin-bottom:var(--s-2)">1억 2천 5백만 원의 <span class="is-accent">가치</span></div>'
    '<div class="t-body is-muted" style="margin-bottom:var(--s-3);font-size:16px">업계 평균 대비, 전 매체 <span class="is-ink w-bold">30~40%+</span> 효율</div>'
    '<div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-4)"></div>'
    '<div style="display:flex;flex-direction:column;gap:var(--s-3);max-width:1210px;width:100%;margin:0 auto var(--s-3);text-align:left">'
    + rows_html +
    '</div>'
    '<div class="t-caption is-muted" style="font-style:italic">같은 예산으로, 더 많이 보여드리겠습니다</div>'
    '</div>'
)


def main():
    conn = sqlite3.connect(str(DB))
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=44",
        (P45, PID),
    )
    conn.commit()
    conn.close()
    print("P45 (order=44) 비교 그래프 반영")


if __name__ == "__main__":
    main()
