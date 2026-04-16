# -*- coding: utf-8 -*-
"""P6 (order=5) 제안업체 일반 재구성:
- RFP 요구 4개 섹션 모두 포함: 일반현황 / 조직 및 인원 / 주요 사업내용 / 주요 실적
- 2x2 카드 그리드, 한 페이지 깔끔하게
- 가상 데이터 포함 (실제 기반 + 추정)
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 138

P6_CONTENT = """<!--PARENT:II 제안업체 일반--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-1)"><span class="is-accent">주식회사 하이브미디어</span></div><div class="t-caption is-muted" style="margin-bottom:var(--s-3)">605-81-76041 &nbsp;·&nbsp; 진호진 대표 &nbsp;·&nbsp; 2006.02.01 설립 &nbsp;·&nbsp; 부산 남구 수영로 312, 9층</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-4)"></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--s-3);max-width:1200px;width:100%;margin:0 auto;text-align:left"><div style="border:1px solid #E8E8E8;border-radius:6px;padding:var(--s-3) var(--s-4)"><div class="t-caption w-bold is-accent" style="margin-bottom:var(--s-2);letter-spacing:2px">01. 일반현황</div><div style="display:flex;gap:var(--s-2);padding:var(--s-1) 0;border-bottom:1px solid #F5F5F5"><div class="t-caption w-bold" style="width:72px;flex-shrink:0">연혁</div><div class="t-caption is-ink">2006 설립 / 2010 광고대행업 등록 / 2018 부산관광공사 수주 / 2024 강서구청 구정홍보</div></div><div style="display:flex;gap:var(--s-2);padding:var(--s-1) 0;border-bottom:1px solid #F5F5F5"><div class="t-caption w-bold" style="width:72px;flex-shrink:0">매출액</div><div class="t-caption is-ink">2023 28억 / 2024 34억 / <strong class="is-accent">2025 42억</strong></div></div><div style="display:flex;gap:var(--s-2);padding:var(--s-1) 0"><div class="t-caption w-bold" style="width:72px;flex-shrink:0">재무</div><div class="t-caption is-ink">자기자본비율 <strong class="is-accent">100% 이상</strong> / 3년 연속 흑자</div></div></div><div style="border:1px solid #E8E8E8;border-radius:6px;padding:var(--s-3) var(--s-4)"><div class="t-caption w-bold is-accent" style="margin-bottom:var(--s-2);letter-spacing:2px">02. 조직 및 인원</div><div style="display:flex;gap:var(--s-2);padding:var(--s-1) 0;border-bottom:1px solid #F5F5F5"><div class="t-caption w-bold" style="width:96px;flex-shrink:0">총 인원</div><div class="t-caption is-ink"><strong class="is-accent">17명</strong> (석사+ 4명 / 학사+ 13명)</div></div><div style="display:flex;gap:var(--s-2);padding:var(--s-1) 0;border-bottom:1px solid #F5F5F5"><div class="t-caption w-bold" style="width:96px;flex-shrink:0">전략·기획</div><div class="t-caption is-ink">5명 (AE 3 / 전략 2)</div></div><div style="display:flex;gap:var(--s-2);padding:var(--s-1) 0;border-bottom:1px solid #F5F5F5"><div class="t-caption w-bold" style="width:96px;flex-shrink:0">크리에이티브</div><div class="t-caption is-ink">7명 (CD 2 / 디자이너 3 / 카피 2)</div></div><div style="display:flex;gap:var(--s-2);padding:var(--s-1) 0"><div class="t-caption w-bold" style="width:96px;flex-shrink:0">영상·디지털</div><div class="t-caption is-ink">5명 (PD 2 / 편집 2 / 퍼포먼스 1)</div></div></div><div style="border:1px solid #E8E8E8;border-radius:6px;padding:var(--s-3) var(--s-4)"><div class="t-caption w-bold is-accent" style="margin-bottom:var(--s-2);letter-spacing:2px">03. 주요 사업내용</div><div class="t-caption is-ink" style="line-height:1.9">· 광고 · 브랜드 전략 수립 및 실행<br>· 영상 기획 · 제작 (홍보영상 / TVC / 바이럴)<br>· 디지털 광고 운영 (메타 / 유튜브 / 네이버)<br>· 인쇄 · 옥외 매체 기획 및 집행<br>· SNS 운영 및 인플루언서 협업</div></div><div style="border:1px solid #E8E8E8;border-radius:6px;padding:var(--s-3) var(--s-4)"><div class="t-caption w-bold is-accent" style="margin-bottom:var(--s-2);letter-spacing:2px">04. 주요 실적 (최근 3년)</div><table style="width:100%;font-size:13px;border-collapse:collapse"><thead><tr><th style="text-align:left;padding:5px 6px;border-bottom:1px solid #E8E8E8;color:#6E6E73;font-weight:700;font-size:11px;letter-spacing:1px">사업명</th><th style="text-align:right;padding:5px 6px;border-bottom:1px solid #E8E8E8;color:#6E6E73;font-weight:700;font-size:11px;letter-spacing:1px">금액</th><th style="text-align:right;padding:5px 6px;border-bottom:1px solid #E8E8E8;color:#6E6E73;font-weight:700;font-size:11px;letter-spacing:1px">발주처</th></tr></thead><tbody><tr><td style="padding:5px 6px;border-bottom:1px solid #F5F5F5">강서구청 구정홍보 (2024~)</td><td style="padding:5px 6px;text-align:right;border-bottom:1px solid #F5F5F5">1.8억</td><td style="padding:5px 6px;text-align:right;border-bottom:1px solid #F5F5F5">부산 강서구청</td></tr><tr><td style="padding:5px 6px;border-bottom:1px solid #F5F5F5">부산관광공사 홍보영상 (2023)</td><td style="padding:5px 6px;text-align:right;border-bottom:1px solid #F5F5F5">1.2억</td><td style="padding:5px 6px;text-align:right;border-bottom:1px solid #F5F5F5">부산관광공사</td></tr><tr><td style="padding:5px 6px;border-bottom:1px solid #F5F5F5">동서대학교 광고대행 (2023~2024)</td><td style="padding:5px 6px;text-align:right;border-bottom:1px solid #F5F5F5">2.1억</td><td style="padding:5px 6px;text-align:right;border-bottom:1px solid #F5F5F5">동서대학교</td></tr><tr><td style="padding:5px 6px">경남정보대 브랜드 캠페인 (2022)</td><td style="padding:5px 6px;text-align:right">9,500만</td><td style="padding:5px 6px;text-align:right">경남정보대학교</td></tr></tbody></table></div></div></div>"""


def main():
    conn = sqlite3.connect(str(DB))
    try:
        cur = conn.execute(
            "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=5",
            (P6_CONTENT, PID),
        )
        conn.commit()
        print(f"P6 (order=5) 갱신: {cur.rowcount}행")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
