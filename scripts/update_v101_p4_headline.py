# -*- coding: utf-8 -*-
"""V101 P4 헤드라인 변경.

"'대단한 대학'은, 이제 통하지 않습니다"
  → "'대단한 대학'은 이제 각인되지 않습니다"
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

OLD_HEADLINE = "'<span class=\"is-muted\">대단한 대학</span>'은, 이제 통하지 않습니다"
NEW_HEADLINE = "'<span class=\"is-muted\">대단한 대학</span>'은 이제 각인되지 않습니다"

OLD_SCRIPT = "\"그래서 '대단한 대학'은, 이제 통하지 않습니다."
NEW_SCRIPT = "\"그래서 '대단한 대학'은 이제 각인되지 않습니다."


def main():
    conn = sqlite3.connect(str(DB))
    try:
        row = conn.execute(
            "SELECT content FROM sections WHERE proposal_id=? AND order_idx=3",
            (PID,),
        ).fetchone()
        if not row:
            raise RuntimeError("P4 섹션 없음")
        content = row[0]

        if OLD_HEADLINE not in content:
            raise RuntimeError("헤드라인 매칭 실패 — 수동 확인 필요")
        content = content.replace(OLD_HEADLINE, NEW_HEADLINE)

        if OLD_SCRIPT in content:
            content = content.replace(OLD_SCRIPT, NEW_SCRIPT)
            print("스크립트도 함께 교체")
        else:
            print("스크립트 매칭 실패")

        conn.execute(
            "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=3",
            (content, PID),
        )
        conn.commit()
        print("P4 헤드라인 변경 완료: '대단한 대학은 이제 각인되지 않습니다'")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
