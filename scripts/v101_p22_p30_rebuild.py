# -*- coding: utf-8 -*-
"""V101 P22-P30 재구축: 9장 시안, 각 1장씩, 좌상단 slogan / 우상단 placeholder / 중앙 꽉찬 시안."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


def build(slogan, right_label, ad_img, tag):
    return f"""<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:{tag}--><div style="position:absolute;top:0;left:0;right:0;bottom:0;display:flex;justify-content:center;align-items:center;padding:var(--s-3) 0;background:#FFFFFF">

<div style="position:absolute;top:120px;left:120px;font-size:26px;font-weight:700;color:#E84E10;letter-spacing:-0.5px;z-index:10">{slogan}</div>

<div style="position:absolute;top:120px;right:120px;font-size:14px;font-weight:700;color:#6E6E73;letter-spacing:3px;z-index:10">{right_label}</div>

<img src="/assets/image/{ad_img}" alt="{slogan}" style="max-height:84%;max-width:70%;height:auto;width:auto;box-shadow:0 8px 32px rgba(0,0,0,0.2)">

</div>"""


SLIDES = [
    # (idx, slogan, right_label, ad_img_filename, tag)
    (21, "산업이 먼저 찾아온 대학", "CASE 01", "ysu_ad_left.png", "Industry Choice 01"),
    (22, "산업이 먼저 찾아온 대학", "CASE 02", "ysu_ad_right.png", "Industry Choice 02"),
    (23, "산업이 먼저 찾아온 대학", "CASE 03", "ysu_ad_poster.png", "Industry Choice 03"),

    (24, "세계가 증명한 숫자", "CASE 01", "ysu_ad_poster.png", "Global Proof 01"),
    (25, "세계가 증명한 숫자", "CASE 02", "ysu_ad_left.png", "Global Proof 02"),
    (26, "세계가 증명한 숫자", "CASE 03", "ysu_ad_right.png", "Global Proof 03"),

    (27, "재학 중부터 업계인", "CASE 01", "ysu_ad_left.png", "Industry Student 01"),
    (28, "재학 중부터 업계인", "CASE 02", "ysu_ad_poster.png", "Industry Student 02"),
    (29, "재학 중부터 업계인", "CASE 03", "ysu_ad_right.png", "Industry Student 03"),
]


def main():
    conn = sqlite3.connect(str(DB))

    for idx, slogan, right, img, tag in SLIDES:
        content = build(slogan, right, img, tag)
        # 기존 있으면 UPDATE, 없으면 INSERT
        existing = conn.execute(
            "SELECT id FROM sections WHERE proposal_id=? AND order_idx=?",
            (PID, idx),
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE sections SET content=?, title=? WHERE id=?",
                (content, f"{slogan} — {right}", existing[0]),
            )
            print(f"  UPDATE idx={idx}: {slogan} · {right}")
        else:
            conn.execute(
                """INSERT INTO sections (proposal_id, order_idx, level, title, content)
                   VALUES (?, ?, 2, ?, ?)""",
                (PID, idx, f"{slogan} — {right}", content),
            )
            print(f"  INSERT idx={idx}: {slogan} · {right}")

    conn.commit()

    rows = conn.execute(
        "SELECT order_idx, title FROM sections WHERE proposal_id=? AND order_idx BETWEEN 21 AND 31 ORDER BY order_idx",
        (PID,),
    ).fetchall()
    print("\n== 결과 ==")
    for r in rows:
        print(f"  idx={r[0]}: {r[1]}")
    conn.close()


if __name__ == "__main__":
    main()
