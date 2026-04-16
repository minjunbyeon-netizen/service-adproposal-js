# -*- coding: utf-8 -*-
"""모든 font-size를 4단계로 압축.

14px  — 캡션·라벨·잔글씨
24px  — 본문·소제목
48px  — 헤드·키워드
96px  — 히어로·디스플레이

대상:
  1) templates/presentation_clean.html
  2) DB sections.content (proposal_id=179, V101)
"""
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "adproposal.db"
TEMPLATE = ROOT / "templates" / "presentation_clean.html"
PID = 179

BUCKETS = [14, 24, 48, 96]


def map_size(size_px: int) -> int:
    """가장 가까운 버킷으로 매핑."""
    return min(BUCKETS, key=lambda b: abs(b - size_px))


def compress_content(text: str):
    """font-size:Xpx 및 font-size: Xpx 등 모든 패턴 교체."""
    count = 0
    before_counts = {}
    after_counts = {}

    def replacer(m):
        nonlocal count
        orig_val = int(m.group(1))
        new_val = map_size(orig_val)
        before_counts[orig_val] = before_counts.get(orig_val, 0) + 1
        after_counts[new_val] = after_counts.get(new_val, 0) + 1
        count += 1
        return f"font-size:{new_val}px"

    # font-size:Xpx (공백 있어도 허용)
    new_text = re.sub(r"font-size\s*:\s*(\d+)px", replacer, text)
    return new_text, count, before_counts, after_counts


def main():
    total = 0

    # 1) 템플릿
    print("=== Template: presentation_clean.html ===")
    tpl_text = TEMPLATE.read_text(encoding="utf-8")
    new_tpl, cnt, before, after = compress_content(tpl_text)
    TEMPLATE.write_text(new_tpl, encoding="utf-8")
    print(f"  {cnt}개 font-size 교체")
    print(f"  → {dict(sorted(after.items()))}")
    total += cnt

    # 2) DB
    print("\n=== DB sections (proposal_id=179) ===")
    conn = sqlite3.connect(str(DB))
    rows = conn.execute(
        "SELECT id, content FROM sections WHERE proposal_id=? AND content IS NOT NULL",
        (PID,),
    ).fetchall()
    db_count = 0
    for sid, content in rows:
        new_content, cnt, _, _ = compress_content(content)
        if cnt > 0:
            conn.execute(
                "UPDATE sections SET content=? WHERE id=?", (new_content, sid)
            )
            db_count += cnt
    conn.commit()
    print(f"  {db_count}개 font-size 교체")
    total += db_count
    conn.close()

    print(f"\n=== 총 {total}개 교체 완료 ===")
    print(f"사용 중 폰트 크기: {BUCKETS} (4단계)")


if __name__ == "__main__":
    main()
