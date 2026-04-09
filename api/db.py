import sqlite3
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DB_PATH = os.environ.get("ADPROPOSAL_DB", str(Path(__file__).resolve().parent.parent / "data" / "adproposal.db"))


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def init_db():
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    conn = get_conn()
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS proposals (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                title        TEXT    NOT NULL,
                status       TEXT    NOT NULL DEFAULT 'draft',
                raw_text     TEXT,
                rfp_summary  TEXT,
                rfp_json     TEXT,
                toc_json     TEXT,
                created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS sections (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                proposal_id  INTEGER NOT NULL REFERENCES proposals(id) ON DELETE CASCADE,
                level        INTEGER NOT NULL,
                title        TEXT    NOT NULL,
                order_idx    INTEGER NOT NULL,
                content      TEXT,
                status       TEXT    NOT NULL DEFAULT 'pending',
                created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS messages (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                section_id   INTEGER NOT NULL REFERENCES sections(id) ON DELETE CASCADE,
                role         TEXT    NOT NULL,
                content      TEXT    NOT NULL,
                created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS concepts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                proposal_id INTEGER NOT NULL REFERENCES proposals(id) ON DELETE CASCADE,
                label       TEXT    NOT NULL CHECK(label IN ('A','B','C')),
                title       TEXT    NOT NULL,
                body        TEXT    NOT NULL DEFAULT '',
                created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
                UNIQUE(proposal_id, label)
            );

            CREATE INDEX IF NOT EXISTS idx_sections_proposal ON sections(proposal_id);
            CREATE INDEX IF NOT EXISTS idx_messages_section ON messages(section_id);
            CREATE INDEX IF NOT EXISTS idx_concepts_proposal ON concepts(proposal_id);
        """)
        conn.commit()
        logger.info("DB initialized: %s", DB_PATH)
    finally:
        conn.close()


def migrate_db():
    """idempotent 마이그레이션."""
    conn = get_conn()
    try:
        cols = [r["name"] for r in conn.execute("PRAGMA table_info(proposals)").fetchall()]
        if "selected_concept" not in cols:
            conn.execute("ALTER TABLE proposals ADD COLUMN selected_concept TEXT DEFAULT NULL")
            conn.commit()
            logger.info("migrate: added proposals.selected_concept")
    finally:
        conn.close()


def get_concepts(proposal_id: int) -> list[dict]:
    conn = get_conn()
    try:
        rows = conn.execute(
            "SELECT id, proposal_id, label, title, body, created_at "
            "FROM concepts WHERE proposal_id=? ORDER BY label",
            (proposal_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def upsert_concepts(proposal_id: int, concepts: list[dict]) -> None:
    conn = get_conn()
    try:
        for c in concepts:
            conn.execute(
                "INSERT OR REPLACE INTO concepts (proposal_id, label, title, body) "
                "VALUES (?, ?, ?, ?)",
                (proposal_id, c["label"], c["title"], c.get("body", "")),
            )
        conn.commit()
    finally:
        conn.close()


def update_concept(concept_id: int, title: str, body: str) -> dict | None:
    conn = get_conn()
    try:
        conn.execute(
            "UPDATE concepts SET title=?, body=? WHERE id=?",
            (title, body, concept_id),
        )
        conn.commit()
        row = conn.execute(
            "SELECT id, proposal_id, label, title, body, created_at "
            "FROM concepts WHERE id=?",
            (concept_id,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def select_concept(proposal_id: int, label: str) -> None:
    conn = get_conn()
    try:
        conn.execute(
            "UPDATE proposals SET selected_concept=? WHERE id=?",
            (label, proposal_id),
        )
        conn.commit()
    finally:
        conn.close()


def get_proposal_with_concepts(proposal_id: int) -> dict | None:
    conn = get_conn()
    try:
        row = conn.execute(
            "SELECT id, title, rfp_json, toc_json, selected_concept "
            "FROM proposals WHERE id=?",
            (proposal_id,),
        ).fetchone()
        if not row:
            return None
        data = dict(row)
        sections = conn.execute(
            "SELECT level, title, content FROM sections "
            "WHERE proposal_id=? ORDER BY order_idx",
            (proposal_id,),
        ).fetchall()
        data["sections"] = [dict(s) for s in sections]
        concepts = conn.execute(
            "SELECT id, label, title, body FROM concepts "
            "WHERE proposal_id=? ORDER BY label",
            (proposal_id,),
        ).fetchall()
        data["concepts"] = [dict(c) for c in concepts]
        return data
    finally:
        conn.close()
