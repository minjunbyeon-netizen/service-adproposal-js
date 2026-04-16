# -*- coding: utf-8 -*-
"""P46 측정 체계 -> GA4 스타일 대시보드 레이아웃 (도넛 차트 + 3카드).
CSS conic-gradient로 도넛 차트 구현, 카드마다 지표/도구/주기/트렌드.
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 138


def donut(percent, label_top, label_bottom, accent=True):
    """SVG-free 도넛 차트 via conic-gradient."""
    deg = percent * 3.6
    color = "#E84E10" if accent else "#FAA478"
    return f"""<div style="width:172px;height:172px;border-radius:50%;background:conic-gradient({color} 0 {deg}deg, #F0F0F0 {deg}deg 360deg);display:flex;align-items:center;justify-content:center;position:relative;margin:0 auto"><div style="width:128px;height:128px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center"><div style="text-align:center"><div style="font-size:32px;font-weight:700;color:{color};line-height:1;letter-spacing:-1px">{label_top}</div><div style="font-size:13px;color:#6E6E73;letter-spacing:2px;margin-top:5px;font-weight:700">{label_bottom}</div></div></div></div>"""


def sparkline_bars(values, accent=True):
    """미니 bar chart - 성장 추이 시각화 (7 bars)"""
    color = "#E84E10" if accent else "#FAA478"
    max_v = max(values)
    bars_html = ""
    for v in values:
        h = round(v / max_v * 100)
        bars_html += f'<div style="width:8px;height:{h}%;background:{color};border-radius:1px"></div>'
    return f'<div style="display:flex;align-items:flex-end;gap:4px;height:36px">{bars_html}</div>'


def card(layer_num, layer_name, donut_html, metric_big, metric_sub, tools, cycle, trend_html, highlight=False):
    bg = "background:#FFF5F0;" if highlight else ""
    border_top = "border-top:3px solid #E84E10;" if highlight else "border-top:3px solid #F0F0F0;"
    return f"""<div style="border:1px solid #E8E8E8;{border_top}{bg}border-radius:8px;padding:var(--s-4) var(--s-4);display:flex;flex-direction:column;gap:14px;text-align:center"><div style="display:flex;align-items:center;justify-content:space-between"><div style="font-size:14px;letter-spacing:3px;color:#6E6E73;font-weight:700">{layer_num}</div><div style="font-size:24px;font-weight:700;color:#1A1A1A;letter-spacing:-0.5px">{layer_name}</div><div style="width:24px"></div></div>{donut_html}<div style="display:flex;flex-direction:column;gap:6px"><div style="font-size:17px;font-weight:700;color:#1A1A1A">{metric_big}</div><div style="font-size:14px;color:#6E6E73">{metric_sub}</div></div><div style="display:flex;justify-content:center;margin:6px 0">{trend_html}</div><div style="padding-top:12px;border-top:1px solid #F0F0F0;font-size:13px;color:#6E6E73;letter-spacing:1px"><div style="margin-bottom:3px"><span style="color:#E84E10;font-weight:700">{cycle}</span> · {tools}</div></div></div>"""


P46 = (
    '<!--PARENT:IV 사업 관리 계획--><!--TAG:측정 체계-->'
    '<div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0">'
    '<div class="t-heading" style="margin-bottom:var(--s-2)">광고 결과를, <span class="is-accent">3계층</span>으로 측정합니다</div>'
    '<div class="t-caption is-muted" style="margin-bottom:var(--s-3)">GA4 · YouTube Studio · Meta Ads · Naver GFA · 입학처 DB — 실시간 대시보드 통합</div>'
    '<div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-4)"></div>'
    '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--s-3);max-width:1100px;width:100%;margin:0 auto var(--s-4)">'
    + card(
        "CONVERSION",
        "전환",
        donut(15, "+15%", "YoY"),
        "지원자 수 · 입시 홈 유입",
        "전년 대비 +15% 목표",
        "입학처 DB · GA4",
        "분기",
        sparkline_bars([2, 3, 3, 4, 5, 6, 7], accent=True),
        highlight=True,
    )
    + card(
        "ACTION",
        "행동",
        donut(30, "30%+", "완시청"),
        "영상 완시청률 · SNS 인게이지먼트",
        "완시청 30%+ / 참여 3%+",
        "YouTube Studio · Meta",
        "월간",
        sparkline_bars([4, 5, 4, 6, 5, 7, 8], accent=False),
        highlight=False,
    )
    + card(
        "AWARENESS",
        "인지",
        donut(70, "500만+", "연 노출"),
        "노출 · 도달 · CTR",
        "연 500만+ 노출",
        "GA · Meta Ads · Naver GFA",
        "주간",
        sparkline_bars([3, 4, 5, 4, 6, 7, 9], accent=False),
        highlight=False,
    )
    + '</div>'
    '<div class="t-caption is-muted" style="font-style:italic">인지가 행동을, 행동이 전환을 만듭니다</div>'
    '</div>'
    '<!--SCRIPT_START-->"성과 측정은, 3계층으로 나눕니다<br><br><strong>인지</strong> · 얼마나 많이 봤는지 (주간)<br><strong>행동</strong> · 얼마나 깊이 보고 반응했는지 (월간)<br><strong>전환</strong> · 얼마나 지원으로 이어졌는지 (분기)<br><br>GA4, YouTube Studio, Meta Ads, Naver GFA, 입학처 DB를 통합 대시보드에 연결합니다<br>각 계층의 지표가 실시간으로 누적됩니다"<!--SCRIPT_END-->'
)


def main():
    conn = sqlite3.connect(str(DB))
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=45",
        (P46, PID),
    )
    conn.commit()
    conn.close()
    print("P46 (order=45) 도넛 대시보드 반영")


if __name__ == "__main__":
    main()
