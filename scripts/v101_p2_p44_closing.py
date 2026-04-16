# -*- coding: utf-8 -*-
"""V101 - P2 순서 변경 + P44 3계층 도식 + 하드코딩 closing slide 제거."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


# =============================================================================
# P2 (idx=1) - 순서 변경: 기억시킬 것이냐 -> 많이 팔 것이냐
# =============================================================================
P2 = """<!--PARENT:Ⅰ. 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div style="display:flex;flex-direction:column;gap:var(--s-3);max-width:780px;width:100%;margin-bottom:var(--s-6)"><div style="display:flex;align-items:center;justify-items:center;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:24px;font-weight:700;color:#1A1A1A;line-height:1.2;text-align:center;flex:1">얼마나 <span style="">기억시킬 것이냐</span></div></div><div style="display:flex;align-items:center;justify-items:center;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:24px;font-weight:700;color:#1A1A1A;line-height:1.2;text-align:center;flex:1">얼마나 <span style="">많이 팔 것이냐</span></div></div></div><div class="t-caption is-muted" style=";">나머지는 모두 수단입니다</div></div><!--SCRIPT_START-->광고대행사 선정은 단 두 가지로 결정됩니다<br><br><strong>하나 얼마나 기억시킬 것이냐</strong><br><strong>둘 얼마나 많이 팔 것이냐</strong><br><br>나머지는 모두 수단입니다 이 2개로만 평가받습니다<!--SCRIPT_END-->"""


# =============================================================================
# P44 (idx=45) - 3계층 측정 시각화 도식 (깔대기/피라미드 형태)
# AWARENESS 인지 -> ENGAGEMENT 관여 -> CONVERSION 전환
# =============================================================================
P44 = """<!--PARENT:Ⅳ. 사업 관리 계획--><!--TAG:3계층 측정--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;padding:var(--s-5) var(--s-5)">

<div style="text-align:center;margin-bottom:var(--s-5)">
<div style="font-size:20px;color:#6E6E73;letter-spacing:3px;font-weight:400;margin-bottom:var(--s-2)">Ⅳ. 사업 관리 계획</div>
<div style="font-size:56px;font-weight:700;color:#1A1A1A;line-height:1.2;letter-spacing:-1px">광고 결과를 <span style="color:#E84E10">3계층</span>으로 측정합니다</div>
<div style="font-size:18px;color:#6E6E73;margin-top:var(--s-2)">넓게 보고 좁게 파고 깊게 남깁니다</div>
</div>

<div style="display:flex;flex-direction:column;gap:0;max-width:1200px;width:100%;margin:0 auto">

<div style="display:grid;grid-template-columns:100px 1fr 280px;gap:0;align-items:stretch;background:#FFFFFF">
<div style="display:flex;align-items:center;justify-content:center;background:#FFF8F3;border-top:1px solid #E84E10;border-left:1px solid #E84E10;border-bottom:1px solid #E84E10">
<div style="font-size:48px;font-weight:700;color:#E84E10;line-height:1">01</div>
</div>
<div style="padding:var(--s-4) var(--s-4);border-top:1px solid #1A1A1A;border-bottom:1px solid #E8E8E8">
<div style="font-size:13px;color:#E84E10;letter-spacing:3px;font-weight:700;margin-bottom:var(--s-1)">AWARENESS · 넓게 보다</div>
<div style="font-size:28px;font-weight:700;color:#1A1A1A;line-height:1.3;margin-bottom:var(--s-1)">누가 영산대를 봤는가</div>
<div style="font-size:15px;color:#6E6E73;line-height:1.5">인쇄 · 디지털 DA · 언론 지면 노출 집계</div>
</div>
<div style="padding:var(--s-4) var(--s-3);border-top:1px solid #1A1A1A;border-bottom:1px solid #E8E8E8;background:#FAFAFA;display:flex;flex-direction:column;justify-content:center;align-items:flex-end">
<div style="font-size:48px;font-weight:700;color:#1A1A1A;line-height:1">500만+</div>
<div style="font-size:13px;color:#6E6E73;letter-spacing:2px;margin-top:var(--s-1)">총 노출 목표</div>
</div>
</div>

<div style="display:grid;grid-template-columns:100px 1fr 280px;gap:0;align-items:stretch;background:#FFFFFF">
<div style="display:flex;align-items:center;justify-content:center;background:#FFF8F3;border-left:1px solid #E84E10;border-bottom:1px solid #E84E10">
<div style="font-size:48px;font-weight:700;color:#E84E10;line-height:1">02</div>
</div>
<div style="padding:var(--s-4) var(--s-4);border-bottom:1px solid #E8E8E8">
<div style="font-size:13px;color:#E84E10;letter-spacing:3px;font-weight:700;margin-bottom:var(--s-1)">ENGAGEMENT · 좁게 파다</div>
<div style="font-size:28px;font-weight:700;color:#1A1A1A;line-height:1.3;margin-bottom:var(--s-1)">누가 반응했는가</div>
<div style="font-size:15px;color:#6E6E73;line-height:1.5">CTR · 영상 시청 완료 · SNS 저장 · 댓글 · 해시태그</div>
</div>
<div style="padding:var(--s-4) var(--s-3);border-bottom:1px solid #E8E8E8;background:#FAFAFA;display:flex;flex-direction:column;justify-content:center;align-items:flex-end">
<div style="font-size:48px;font-weight:700;color:#1A1A1A;line-height:1">25만+</div>
<div style="font-size:13px;color:#6E6E73;letter-spacing:2px;margin-top:var(--s-1)">반응 건수 목표</div>
</div>
</div>

<div style="display:grid;grid-template-columns:100px 1fr 280px;gap:0;align-items:stretch;background:#FFFFFF">
<div style="display:flex;align-items:center;justify-content:center;background:#E84E10">
<div style="font-size:48px;font-weight:700;color:#FFFFFF;line-height:1">03</div>
</div>
<div style="padding:var(--s-4) var(--s-4);border-bottom:2px solid #1A1A1A;background:#FFF8F3">
<div style="font-size:13px;color:#E84E10;letter-spacing:3px;font-weight:700;margin-bottom:var(--s-1)">CONVERSION · 깊게 남다</div>
<div style="font-size:28px;font-weight:700;color:#1A1A1A;line-height:1.3;margin-bottom:var(--s-1)">누가 지원했는가</div>
<div style="font-size:15px;color:#6E6E73;line-height:1.5">원서 접수 · 입학 상담 · 오픈캠퍼스 참여 · 합격 기여</div>
</div>
<div style="padding:var(--s-4) var(--s-3);border-bottom:2px solid #1A1A1A;background:#FFF0E5;display:flex;flex-direction:column;justify-content:center;align-items:flex-end">
<div style="font-size:48px;font-weight:700;color:#E84E10;line-height:1">+8%</div>
<div style="font-size:13px;color:#6E6E73;letter-spacing:2px;margin-top:var(--s-1)">수시 지원 증가</div>
</div>
</div>

</div>

<div style="display:flex;align-items:center;justify-content:center;gap:var(--s-3);padding-top:var(--s-4);font-size:13px;color:#6E6E73;letter-spacing:2px">
<span>넓게</span><span>→</span><span>좁게</span><span>→</span><span>깊게</span>
</div>

</div>"""


# =============================================================================
# P47 (idx=48) - 2페이지와 동일 포맷으로 수미상관 (2026년 기억시키고 / 2027년 많이 팔겠습니다)
# =============================================================================
P47 = """<!--PARENT:Epilogue--><!--TAG:클로징--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div style="display:flex;flex-direction:column;gap:var(--s-3);max-width:780px;width:100%;margin-bottom:var(--s-6)"><div style="display:flex;align-items:center;justify-items:center;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:24px;font-weight:700;color:#1A1A1A;line-height:1.2;text-align:center;flex:1">2026년 <span style="color:#E84E10">기억</span>시키고</div></div><div style="display:flex;align-items:center;justify-items:center;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:24px;font-weight:700;color:#1A1A1A;line-height:1.2;text-align:center;flex:1">2027년 <span style="color:#E84E10">많이</span> 팔겠습니다</div></div></div><div class="t-caption is-muted" style=";">나머지는 모두 수단입니다</div></div>"""


def main():
    conn = sqlite3.connect(str(DB))

    # 1) P2 순서 변경
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=1",
        (P2, PID),
    )
    print("[1] P2 (idx=1) - 기억시킬 것이냐 / 많이 팔 것이냐 순서 변경")

    # 2) P44 3계층 도식 시각화
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=45",
        (P44, PID),
    )
    print("[2] P44 (idx=45) - 3계층 측정 도식 (01/02/03 + 목표치) 적용")

    # 3) P47 (idx=48) 수미상관 - P2 동일 포맷
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=48",
        (P47, PID),
    )
    print("[3] P47 (idx=48) - P2와 수미상관 (2026 기억 / 2027 많이)")

    conn.commit()
    conn.close()
    print("\n완료")


if __name__ == "__main__":
    main()
