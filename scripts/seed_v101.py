# -*- coding: utf-8 -*-
"""V101 seed - Railway 시작 시 proposal 179 로딩."""
import json
import sqlite3
import os
from pathlib import Path

SNAPSHOT = Path(__file__).resolve().parent / "v101_snapshot.json"
DB_PATH = os.environ.get("ADPROPOSAL_DB", "/app/data/adproposal.db")


def init_schema(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS proposals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        rfp_text TEXT,
        analysis TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS sections(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proposal_id INTEGER NOT NULL,
        level INTEGER NOT NULL,
        title TEXT,
        order_idx INTEGER NOT NULL,
        content TEXT,
        status TEXT DEFAULT 'empty',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(proposal_id) REFERENCES proposals(id) ON DELETE CASCADE
    )""")


def main():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    init_schema(conn)

    with open(SNAPSHOT, encoding="utf-8") as f:
        data = json.load(f)

    p = data["proposal"]
    # 기존 proposal 179 + sections 싹 지우고 재주입
    conn.execute("DELETE FROM sections WHERE proposal_id=?", (p["id"],))
    conn.execute("DELETE FROM proposals WHERE id=?", (p["id"],))

    conn.execute(
        "INSERT INTO proposals (id, title, rfp_text, analysis) VALUES (?, ?, ?, ?)",
        (p["id"], p.get("title"), p.get("rfp_text"), p.get("analysis")),
    )

    for s in data["sections"]:
        conn.execute(
            """INSERT INTO sections (id, proposal_id, level, title, order_idx, content, status)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (s["id"], s["proposal_id"], s["level"], s.get("title"),
             s["order_idx"], s.get("content"), s.get("status", "empty")),
        )

    conn.commit()
    conn.close()
    print(f"V101 seeded: proposal id={p['id']}, {len(data['sections'])} sections")


if __name__ == "__main__":
    main()
