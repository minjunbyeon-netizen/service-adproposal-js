# -*- coding: utf-8 -*-
"""V101 P14 (idx=13) - TEXT 상단 이동 + 하단에 타대학 시안 4장 배치."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


# P14 재구성 - TEXT 상단으로 + 하단 4장 시안
# 의도: "모두가 같은 말을 한다"는 메시지를 시각적으로 증명
P14 = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><div style="height:100%;display:flex;flex-direction:column;justify-content:flex-start;padding:var(--s-5) var(--s-4) var(--s-4)">

<div style="text-align:center;margin-bottom:var(--s-4)">
<div class="t-headline">왜 <span class="is-accent">기억되지 않을까요?</span></div>
<div class="t-headline" style="margin-top:var(--s-3)">모두가, <span class="is-accent">같은 말</span>을 하기 때문입니다</div>
</div>

<div style="flex:1;display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:var(--s-3);align-items:center;max-width:1400px;width:100%;margin:0 auto;padding-top:var(--s-2)">
<div style="display:flex;flex-direction:column;align-items:center;gap:var(--s-2)">
<img src="/assets/image/other_univ/u1.png" alt="동신대학교" style="width:100%;height:auto;max-height:360px;object-fit:contain;box-shadow:0 4px 16px rgba(0,0,0,0.12)">
<div style="font-size:13px;color:#6E6E73;letter-spacing:1px">동신대학교 · 취업률 1위</div>
</div>
<div style="display:flex;flex-direction:column;align-items:center;gap:var(--s-2)">
<img src="/assets/image/other_univ/u2.png" alt="수원여대" style="width:100%;height:auto;max-height:360px;object-fit:contain;box-shadow:0 4px 16px rgba(0,0,0,0.12)">
<div style="font-size:13px;color:#6E6E73;letter-spacing:1px">수원여대 · 취업률 1위 달성</div>
</div>
<div style="display:flex;flex-direction:column;align-items:center;gap:var(--s-2)">
<img src="/assets/image/other_univ/u3.png" alt="한국기술교육대" style="width:100%;height:auto;max-height:360px;object-fit:contain;box-shadow:0 4px 16px rgba(0,0,0,0.12)">
<div style="font-size:13px;color:#6E6E73;letter-spacing:1px">한국기술교육대 · 4년제 대학 1위</div>
</div>
<div style="display:flex;flex-direction:column;align-items:center;gap:var(--s-2)">
<img src="/assets/image/other_univ/u4.png" alt="동명대학교" style="width:100%;height:auto;max-height:360px;object-fit:contain;box-shadow:0 4px 16px rgba(0,0,0,0.12)">
<div style="font-size:13px;color:#6E6E73;letter-spacing:1px">동명대학교 · 도전해 보는거야</div>
</div>
</div>

</div>"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=13",
        (P14, PID),
    )
    conn.commit()
    conn.close()
    print("[P14] TEXT 상단 + 타대학 4장 시안 배치 완료")


if __name__ == "__main__":
    main()
