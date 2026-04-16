# -*- coding: utf-8 -*-
"""V101 빌드업 영어 캡션 제거 (P2~P7).

제거 대상:
  P2  THE ESSENCE
  P3  MARKET CONTEXT · COLD FACTS · THE NOISE
  P4  BROKEN PLAYBOOK
  P5  THE ONLY QUESTION · 5 SECONDS OF SILENCE
  P7  THE ENTIRE PROPOSAL
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

# (order_idx, [old_snippet, ...])  — 각 snippet을 빈 문자열로 치환
STRIPS = {
    1: [  # P2
        '<div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-5)">THE ESSENCE</div>',
    ],
    2: [  # P3
        '<div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-3)">MARKET CONTEXT</div>',
        '<div class="t-caption w-bold" style="color:#6E6E73;letter-spacing:3px;margin-bottom:var(--s-3)">COLD FACTS</div>',
        '<div class="t-caption w-bold" style="color:#6E6E73;letter-spacing:3px;margin-bottom:var(--s-3)">THE NOISE</div>',
    ],
    3: [  # P4
        '<div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-3)">BROKEN PLAYBOOK</div>',
    ],
    4: [  # P5
        '<div class="t-caption is-muted" style="letter-spacing:4px;position:absolute;top:var(--s-5)">THE ONLY QUESTION</div>',
        '<div class="t-caption is-muted" style="letter-spacing:3px;font-style:italic;position:absolute;bottom:var(--s-4)">5 SECONDS OF SILENCE</div>',
    ],
    6: [  # P7
        '<div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-5)">THE ENTIRE PROPOSAL</div>',
    ],
}


def main():
    conn = sqlite3.connect(str(DB))
    try:
        for idx, snippets in STRIPS.items():
            row = conn.execute(
                "SELECT content FROM sections WHERE proposal_id=? AND order_idx=?",
                (PID, idx),
            ).fetchone()
            if not row:
                print(f"idx={idx}: 섹션 없음, skip")
                continue
            content = row[0]
            removed = 0
            for s in snippets:
                if s in content:
                    content = content.replace(s, "")
                    removed += 1
            conn.execute(
                "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=?",
                (content, PID, idx),
            )
            print(f"idx={idx}: {removed}/{len(snippets)} snippet 제거")

        conn.commit()
        print("\n영어 캡션 제거 완료")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
