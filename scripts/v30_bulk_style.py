# -*- coding: utf-8 -*-
"""V30 전체 페이지 일괄 스타일 적용:
1. flex 세로 중앙 정렬 (height:100%;display:flex;flex-direction:column;justify-content:center)
2. inline-block + text-align:left -> text-align:center
3. 본문 영역의 em-dash(—) 장식 제거 (script 내레이션은 보존)

대상: scripts/pt.html 전체 + DB proposal_id=138 모든 섹션
"""
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PT = ROOT / "scripts" / "pt.html"
DB = ROOT / "data" / "adproposal.db"
PID = 138

FLEX_RE = re.compile(r'<div style="padding:var\(--s-(\d+)\) 0;text-align:center">')
FLEX_REPL = r'<div style="height:100%;display:flex;flex-direction:column;justify-content:center;text-align:center;padding:var(--s-\1) 0">'

EM_DASH_DECOR = '<span class="is-muted">—</span>'


def process_body(seg: str) -> str:
    # 1. flex 세로 중앙
    seg = FLEX_RE.sub(FLEX_REPL, seg)
    # 2. inline-block left -> center
    seg = seg.replace("text-align:left;display:inline-block", "text-align:center")
    # 3. em-dash 장식 제거
    seg = seg.replace(f"{EM_DASH_DECOR} ", "")
    seg = seg.replace(f" {EM_DASH_DECOR}", "")
    seg = seg.replace(EM_DASH_DECOR, "")
    # italic 캡션 앞 `— ` 제거
    seg = re.sub(r'(font-style:italic[^>]*>)\s*—\s*', r'\1', seg)
    # `>— ` 패턴 (캡션/부연 시작) 제거 -- 한글 문자 앞에만 한정
    seg = re.sub(r'>—\s+(?=[가-힣])', '>', seg)
    return seg


# --- pt.html 처리 ---
html = PT.read_text(encoding="utf-8")
SCRIPT_HTML_RE = re.compile(r'(<div class="script-side">[\s\S]*?</div>)')
parts = SCRIPT_HTML_RE.split(html)
new_parts = []
for i, p in enumerate(parts):
    if i % 2 == 1:  # script-side 블록 -- 손대지 않음
        new_parts.append(p)
    else:
        new_parts.append(process_body(p))
html_new = "".join(new_parts)
PT.write_text(html_new, encoding="utf-8")
print(f"pt.html 갱신 완료 ({len(html_new)} bytes)")


# --- DB 처리 ---
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
    out = []
    for i, s in enumerate(segs):
        out.append(s if i % 2 == 1 else process_body(s))
    new_content = "".join(out)
    if new_content != r["content"]:
        conn.execute("UPDATE sections SET content=? WHERE id=?", (new_content, r["id"]))
        updated += 1
conn.commit()
conn.close()
print(f"DB 갱신 완료: {updated}개 섹션")
