# -*- coding: utf-8 -*-
"""V30 정렬 보강:
1. 모든 flex container에 align-items:center 추가 (자식이 inline-block일 때 좌측 쏠림 방지)
2. 모든 <th> 태그의 text-align:left -> center (헤더 행 중앙정렬)
대상: scripts/pt.html + DB proposal_id=138
"""
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PT = ROOT / "scripts" / "pt.html"
DB = ROOT / "data" / "adproposal.db"
PID = 138

# 1) flex 컨테이너에 align-items:center 추가 (이미 있으면 건너뜀)
FLEX_JC_RE = re.compile(
    r"(display:flex;flex-direction:column;justify-content:center;)(?!align-items)"
)
FLEX_JC_REPL = r"\1align-items:center;"

# 2) <th ... text-align:left ...> -> <th ... text-align:center ...>
TH_ALIGN_RE = re.compile(r"(<th[^>]*?text-align:)left")


def process(s: str) -> str:
    s = FLEX_JC_RE.sub(FLEX_JC_REPL, s)
    s = TH_ALIGN_RE.sub(r"\1center", s)
    return s


# --- pt.html ---
html = PT.read_text(encoding="utf-8")
# script-side 제외
SCRIPT_HTML_RE = re.compile(r'(<div class="script-side">[\s\S]*?</div>)')
parts = SCRIPT_HTML_RE.split(html)
parts = [p if i % 2 == 1 else process(p) for i, p in enumerate(parts)]
new_html = "".join(parts)
PT.write_text(new_html, encoding="utf-8")
print(f"pt.html 갱신: {len(new_html)} bytes")

# --- DB ---
conn = sqlite3.connect(str(DB))
conn.row_factory = sqlite3.Row
DB_SCRIPT_RE = re.compile(r"(<!--SCRIPT_START-->[\s\S]*?<!--SCRIPT_END-->)")
rows = conn.execute(
    "SELECT id, content FROM sections WHERE proposal_id=?", (PID,)
).fetchall()
updated = 0
for r in rows:
    if not r["content"]:
        continue
    segs = DB_SCRIPT_RE.split(r["content"])
    segs = [s if i % 2 == 1 else process(s) for i, s in enumerate(segs)]
    new = "".join(segs)
    if new != r["content"]:
        conn.execute("UPDATE sections SET content=? WHERE id=?", (new, r["id"]))
        updated += 1
conn.commit()
conn.close()
print(f"DB 갱신: {updated}개 섹션")
