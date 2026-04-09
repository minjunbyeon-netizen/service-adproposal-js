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

            CREATE INDEX IF NOT EXISTS idx_sections_proposal ON sections(proposal_id);
            CREATE INDEX IF NOT EXISTS idx_messages_section ON messages(section_id);
        """)
        conn.commit()
        logger.info("DB initialized: %s", DB_PATH)
    finally:
        conn.close()


def migrate_db():
    """idempotent 마이그레이션."""
    pass
