# -*- coding: utf-8 -*-
"""V101 P27 (idx=28) - Executive Summary를 실행 요약으로 전환.
P17은 '무엇을' 결론 (증명/리프레이밍/3슬로건),
P27은 '어떻게' 도입 (3타겟·6채널·연간 시스템)."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


P27 = """<!--PARENT:Ⅳ. 사업 관리 계획--><!--TAG:실행 요약--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;padding:var(--s-5) var(--s-6)">

<div style="font-size:14px;color:#E84E10;font-weight:700;letter-spacing:4px;margin-bottom:var(--s-3)">EXECUTION PLAN</div>

<div style="font-size:96px;font-weight:700;color:#1A1A1A;line-height:1;margin-bottom:var(--s-5);letter-spacing:-3px">이렇게<br>많이 팔겠습니다</div>

<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0;border-top:1px solid #1A1A1A;border-bottom:1px solid #1A1A1A;max-width:1400px;width:100%">

<div style="padding:var(--s-4) var(--s-3);border-right:1px solid #E8E8E8">
<div style="font-size:13px;color:#6E6E73;font-weight:700;letter-spacing:3px;margin-bottom:var(--s-2)">01 — 타겟</div>
<div style="font-size:28px;font-weight:700;color:#1A1A1A;margin-bottom:var(--s-2);line-height:1.2">3그룹</div>
<div style="font-size:15px;color:#6E6E73;line-height:1.6">수험생 · 학부모 · 관계자<br>각자에게 맞는 메시지<br>각자에게 맞는 채널</div>
</div>

<div style="padding:var(--s-4) var(--s-3);border-right:1px solid #E8E8E8;background:#FAFAFA">
<div style="font-size:13px;color:#E84E10;font-weight:700;letter-spacing:3px;margin-bottom:var(--s-2)">02 — 채널</div>
<div style="font-size:28px;font-weight:700;color:#E84E10;margin-bottom:var(--s-2);line-height:1.2">6매체</div>
<div style="font-size:15px;color:#6E6E73;line-height:1.6">인쇄 · 디지털 DA<br>유튜브 · SNS<br>언론 · 옥외</div>
</div>

<div style="padding:var(--s-4) var(--s-3);background:#FFF8F3;border-left:3px solid #E84E10">
<div style="font-size:13px;color:#E84E10;font-weight:700;letter-spacing:3px;margin-bottom:var(--s-2)">03 — 시스템</div>
<div style="font-size:28px;font-weight:700;color:#E84E10;margin-bottom:var(--s-2);line-height:1.2">1사이클</div>
<div style="font-size:15px;color:#6E6E73;line-height:1.6">수시 80% · 정시 20%<br>2주 단위 A/B 테스트<br>월간 리포트 피드백</div>
</div>

</div>

<div style="display:flex;align-items:center;gap:var(--s-4);margin-top:var(--s-4);padding-top:var(--s-3);max-width:1400px;width:100%">
<div style="font-size:13px;color:#6E6E73;font-weight:700;letter-spacing:3px">3 TARGET · 6 CHANNEL · 1 SYSTEM</div>
<div style="flex:1;height:1px;background:#E8E8E8"></div>
<div style="font-size:16px;color:#1A1A1A">연 1.25억 · 수시 집중 · 성과 기반 재배분</div>
</div>

</div>"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.execute(
        "UPDATE sections SET content=?, title=? WHERE proposal_id=? AND order_idx=28",
        (P27, "실행 요약 — 3타겟 6채널 1시스템", PID),
    )
    conn.commit()
    conn.close()
    print("[P27] EXECUTION PLAN: 이렇게 많이 팔겠습니다 + 3타겟/6채널/1시스템")


if __name__ == "__main__":
    main()
