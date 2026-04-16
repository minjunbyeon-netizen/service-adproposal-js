# -*- coding: utf-8 -*-
"""V101 P6 morph 결론 멘트 변경.

"세계가 주목하는 호텔관광, 그 중심 — 부산 영산대학교"
  → "영산대는, 이렇게 움직이고 있습니다"
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

OLD_CONCLUSION = '<div class="t-heading">세계가 주목하는 호텔관광,<br>그 중심 — <span class="is-accent">부산 영산대학교</span></div>'
NEW_CONCLUSION = '<div class="t-heading"><span class="is-accent">영산대</span>는, 이렇게 움직이고 있습니다</div>'

OLD_SCRIPT_TAIL = '(결론 등장 시)<br>"세계가 주목하는 호텔관광 — 그 중심은, <strong>부산 영산대학교</strong>입니다."'
NEW_SCRIPT_TAIL = '(결론 등장 시)<br>"<strong>영산대는, 이렇게 움직이고 있습니다.</strong>"'


def main():
    conn = sqlite3.connect(str(DB))
    try:
        row = conn.execute(
            "SELECT content FROM sections WHERE proposal_id=? AND order_idx=5",
            (PID,),
        ).fetchone()
        if not row:
            raise RuntimeError("P6 morph 섹션 없음")
        content = row[0]

        if OLD_CONCLUSION not in content:
            raise RuntimeError("결론 HTML 매칭 실패 — 수동 확인 필요")
        content = content.replace(OLD_CONCLUSION, NEW_CONCLUSION)

        if OLD_SCRIPT_TAIL in content:
            content = content.replace(OLD_SCRIPT_TAIL, NEW_SCRIPT_TAIL)
            print("스크립트 결론부도 함께 교체")
        else:
            print("스크립트 결론부 매칭 실패 — 수동 확인 필요")

        conn.execute(
            "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=5",
            (content, PID),
        )
        conn.commit()
        print("P6 결론 멘트 변경 완료: '영산대는, 이렇게 움직이고 있습니다'")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
