# -*- coding: utf-8 -*-
"""V101 P7 (idx=6) - 표지(cover)와 동일한 디자인으로 재작성."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


# 표지 CSS를 인라인으로 재현:
#   - 흰 배경 / 우상단 agency / 중앙 serial label + 대형 display / 하단 오렌지 bar
# 내용 완전 변경: 0825503 -> 새 코드 "증명" (campaign concept)
P7 = """<!--PARENT:Ⅰ. 제안개요--><div style="position:absolute;top:0;left:0;right:0;bottom:0;background:#fff;display:flex;justify-content:center;align-items:center;overflow:hidden;z-index:5">

<div style="position:absolute;top:80px;right:120px;font-size:14px;color:#1A1A1A;font-weight:700;letter-spacing:2px">FOR YOUNGSAN UNIV.</div>

<div style="position:relative;text-align:center">
<div style="position:absolute;top:-68px;left:50%;transform:translateX(-50%);font-size:14px;color:#A0A0A5;font-weight:700;white-space:nowrap;letter-spacing:4px">THE CORE CONCEPT</div>
<div style="font-size:var(--fs-display);font-weight:700;line-height:0.9;color:#1A1A1A;font-variant-numeric:tabular-nums;text-align:center">증명</div>
</div>

<div style="position:absolute;bottom:0;left:0;right:0;height:8px;background:#E84E10"></div>
<div style="position:absolute;bottom:28px;right:40px;font-size:14px;font-weight:700;color:#6E6E73">07</div>

</div>"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.execute(
        "UPDATE sections SET content=?, title=? WHERE proposal_id=? AND order_idx=6",
        (P7, "표지 스타일 - 증명", PID),
    )
    conn.commit()
    conn.close()
    print("[P7] 표지 스타일 재디자인 완료 — 대형 '증명'")


if __name__ == "__main__":
    main()
