# -*- coding: utf-8 -*-
"""P33 매체 전략 -> 퍼널 다이어그램 시각화.
4단계 (인지/관심/검토/전환)를 너비가 점점 좁아지고 색이 진해지는 퍼널로 재구성.
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 138

P33 = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:매체 전략--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-4) 0"><div class="t-heading" style="margin-bottom:var(--s-2)">왜 <span class="is-accent">이 조합</span>인가</div><div class="t-body is-muted" style="margin-bottom:var(--s-3)">타깃 3그룹 × 입시 사이클 = 최소 매체 퍼널</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div style="display:flex;flex-direction:column;align-items:center;gap:10px;width:100%;max-width:1100px;margin:0 auto var(--s-3)"><div style="width:100%;padding:16px 28px;background:#FFF0E6;border-radius:8px;display:flex;align-items:center;justify-content:space-between;gap:16px;text-align:left"><div style="flex:0 0 120px;font-weight:700;color:#1A1A1A;font-size:17px"><span style="color:#E84E10">①</span> 인지</div><div style="flex:1;font-size:14px;color:#1A1A1A">인쇄 매체 + 언론 <span style="color:#A0A0A5">·</span> 학부모 / 교사</div><div style="flex:0 0 280px;font-size:14px;font-weight:700;color:#E84E10;text-align:right">3.6% 시안 · 시각적 충격</div></div><div style="width:85%;padding:16px 28px;background:#FFD9C0;border-radius:8px;display:flex;align-items:center;justify-content:space-between;gap:16px;text-align:left"><div style="flex:0 0 120px;font-weight:700;color:#1A1A1A;font-size:17px"><span style="color:#E84E10">②</span> 관심</div><div style="flex:1;font-size:14px;color:#1A1A1A">유튜브 인플루언서 + 디지털 DA <span style="color:#A0A0A5">·</span> 수험생 + 학부모</div><div style="flex:0 0 280px;font-size:14px;font-weight:700;color:#E84E10;text-align:right">리프레이밍 영상 · 호기심 전환</div></div><div style="width:70%;padding:16px 28px;background:#FAA478;border-radius:8px;display:flex;align-items:center;justify-content:space-between;gap:16px;text-align:left"><div style="flex:0 0 120px;font-weight:700;color:#1A1A1A;font-size:17px"><span style="color:#fff">③</span> 검토</div><div style="flex:1;font-size:14px;color:#1A1A1A">SNS 이벤트 + 숏폼 <span style="color:#6E6E73">·</span> 수험생</div><div style="flex:0 0 260px;font-size:14px;font-weight:700;color:#fff;text-align:right">졸업선배 리얼 · 신뢰 축적</div></div><div style="width:55%;padding:16px 28px;background:#E84E10;border-radius:8px;display:flex;align-items:center;justify-content:space-between;gap:16px;text-align:left;color:#fff"><div style="flex:0 0 120px;font-weight:700;font-size:17px"><span style="color:#fff">④</span> 전환</div><div style="flex:1;font-size:14px">홍보영상 + 입시요강 <span style="opacity:0.7">·</span> 전체</div><div style="flex:0 0 240px;font-size:14px;font-weight:700;text-align:right">"지혜" 메인 · 최종 결정</div></div></div><div class="t-caption is-muted" style="font-style:italic">개별 매체가 아닌, 퍼널 전체를 설계합니다</div></div>"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=32",
        (P33, PID),
    )
    conn.commit()
    conn.close()
    print("P33 (order=32) 퍼널 다이어그램 반영")


if __name__ == "__main__":
    main()
