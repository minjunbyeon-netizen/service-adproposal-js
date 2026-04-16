# -*- coding: utf-8 -*-
"""P30 간결화 + P32 확장 시각화 추가.
- P30 (order=29): 슬로건만 남기고 3가지 이유 블록 제거
- P32 (order=31): 제목 아래에 '1 증명 -> 6 채널 -> N 접점' 확장 시각 블록 추가, 채널 라벨 복구
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 138

# ========== P30: 슬로건만 ==========
P30 = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:슬로건--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-headline" style="line-height:1.2;font-size:88px">영산대학교는,<br><span class="is-accent">지혜</span>로 증명합니다</div></div><!--SCRIPT_START-->"이번 영상의 슬로건은 한 문장입니다<br><br><strong>영산대학교는, 지혜로 증명합니다</strong><br><br>(3초 멈춤)<br><br>이제, 실제 영상입니다"<!--SCRIPT_END-->"""

# ========== P32: 확장 시각화 + 채널 라벨 복구 ==========
P32 = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:확장 개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-3)">증명을, 이렇게 <span class="is-accent">확장</span>합니다</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-4)"></div><div style="display:flex;align-items:flex-end;justify-content:center;gap:var(--s-3);margin-bottom:var(--s-5)"><div style="display:flex;flex-direction:column;align-items:center"><div style="width:64px;height:64px;border-radius:8px;background:#E84E10;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:22px;letter-spacing:-1px">1</div><div class="t-caption w-bold" style="margin-top:8px;color:#1A1A1A">증명</div></div><div style="font-size:40px;color:#E84E10;font-weight:700;padding-bottom:28px">→</div><div style="display:flex;flex-direction:column;align-items:center"><div style="width:92px;height:92px;border-radius:8px;background:#E84E10;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:34px;letter-spacing:-1px">6</div><div class="t-caption w-bold" style="margin-top:8px;color:#1A1A1A">채널</div></div><div style="font-size:40px;color:#E84E10;font-weight:700;padding-bottom:44px">→</div><div style="display:flex;flex-direction:column;align-items:center"><div style="width:132px;height:132px;border-radius:8px;background:#E84E10;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:52px;letter-spacing:-2px">N</div><div class="t-caption w-bold" style="margin-top:8px;color:#1A1A1A">접점</div></div></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:0 var(--s-6);max-width:1000px;margin:0 auto var(--s-4);text-align:left"><div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8"><div class="t-caption w-bold is-accent" style="width:110px;flex-shrink:0;letter-spacing:1px">인플루언서</div><div class="t-caption is-ink">교육·호텔 업계 유튜버 협업</div></div><div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8"><div class="t-caption w-bold is-accent" style="width:110px;flex-shrink:0;letter-spacing:1px">인쇄 매체</div><div class="t-caption is-ink">3.6% 중심 배치 (버스·지하철·현수막)</div></div><div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8"><div class="t-caption w-bold is-accent" style="width:110px;flex-shrink:0;letter-spacing:1px">디지털 매체</div><div class="t-caption is-ink">심사위원석 + Room 1201 A/B 실험</div></div><div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8"><div class="t-caption w-bold is-accent" style="width:110px;flex-shrink:0;letter-spacing:1px">숏폼</div><div class="t-caption is-ink">졸업선배 9~12월 연 4편</div></div><div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0"><div class="t-caption w-bold is-accent" style="width:110px;flex-shrink:0;letter-spacing:1px">소셜 미디어</div><div class="t-caption is-ink">3채널 통합 + 월간 캘린더</div></div><div style="display:flex;align-items:baseline;gap:var(--s-3);padding:var(--s-2) 0"><div class="t-caption w-bold is-accent" style="width:110px;flex-shrink:0;letter-spacing:1px">언론</div><div class="t-caption is-ink">수시·정시 시기별 매체 집행</div></div></div><div class="t-subtitle w-regular is-muted">같은 증명 <span class="is-ink w-bold">다른 채널</span></div></div><!--SCRIPT_START-->"지면과 영상으로 <strong>하나의 증명</strong>을 보여드렸습니다<br><br>이제 이 증명을, <strong>6개 채널</strong>로 확장합니다<br>6개 채널은, <strong>수많은 접점</strong>으로 확산됩니다<br><br>인플루언서, 인쇄, 디지털, 숏폼, 소셜 미디어, 언론<br>같은 <strong>증명</strong>, 다른 <strong>채널</strong>입니다"<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    try:
        conn.execute(
            "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=29",
            (P30, PID),
        )
        print("P30 (order=29) 슬로건만 남김")
        conn.execute(
            "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=31",
            (P32, PID),
        )
        print("P32 (order=31) 확장 시각화 추가 + 채널 라벨 복구")
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
