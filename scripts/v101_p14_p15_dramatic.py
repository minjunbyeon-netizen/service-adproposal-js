# -*- coding: utf-8 -*-
"""V101 P14/P15 - 각 광고가 대형 → 제자리로 순차 트랜지션."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


def build(u_list, caption_list, tag_name="Memory Test"):
    u1, u2, u3 = u_list
    c1, c2, c3 = caption_list

    return f"""<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:{tag_name}-->
<style>
.bigstage{{position:absolute;top:100px;left:0;right:0;bottom:80px;pointer-events:none}}
.bigfade{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);max-height:86%;max-width:86%;opacity:0;box-shadow:0 8px 32px rgba(0,0,0,0.25)}}
.bigcap{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;font-size:16px;color:#6E6E73;opacity:0;margin-top:8px}}

.slide.active .bf1{{animation:bfA1 2.6s ease forwards}}
.slide.active .bf2{{animation:bfA2 2.6s ease 2.2s forwards}}
.slide.active .bf3{{animation:bfA3 2.6s ease 4.4s forwards}}
.slide.active .cp1{{animation:cpA1 1s ease 1.8s forwards}}
.slide.active .cp2{{animation:cpA2 1s ease 4.0s forwards}}
.slide.active .cp3{{animation:cpA3 1s ease 6.2s forwards}}

@keyframes bfA1{{
 0%{{opacity:0;top:50%;left:50%;max-height:86%;max-width:86%;z-index:10}}
 8%{{opacity:1;top:50%;left:50%;max-height:86%;max-width:86%;z-index:10}}
 46%{{opacity:1;top:50%;left:50%;max-height:86%;max-width:86%;z-index:10}}
 100%{{opacity:1;top:48%;left:18%;max-height:52%;max-width:28%;z-index:1}}
}}
@keyframes bfA2{{
 0%{{opacity:0;top:50%;left:50%;max-height:86%;max-width:86%;z-index:10}}
 8%{{opacity:1;top:50%;left:50%;max-height:86%;max-width:86%;z-index:10}}
 46%{{opacity:1;top:50%;left:50%;max-height:86%;max-width:86%;z-index:10}}
 100%{{opacity:1;top:48%;left:50%;max-height:52%;max-width:28%;z-index:1}}
}}
@keyframes bfA3{{
 0%{{opacity:0;top:50%;left:50%;max-height:86%;max-width:86%;z-index:10}}
 8%{{opacity:1;top:50%;left:50%;max-height:86%;max-width:86%;z-index:10}}
 46%{{opacity:1;top:50%;left:50%;max-height:86%;max-width:86%;z-index:10}}
 100%{{opacity:1;top:48%;left:82%;max-height:52%;max-width:28%;z-index:1}}
}}

@keyframes cpA1{{0%{{opacity:0;top:82%;left:18%}}100%{{opacity:1;top:82%;left:18%}}}}
@keyframes cpA2{{0%{{opacity:0;top:82%;left:50%}}100%{{opacity:1;top:82%;left:50%}}}}
@keyframes cpA3{{0%{{opacity:0;top:82%;left:82%}}100%{{opacity:1;top:82%;left:82%}}}}
</style>

<div class="bigstage">
<img src="/assets/image/other_univ/{u1}" class="bigfade bf1" alt="{c1}">
<img src="/assets/image/other_univ/{u2}" class="bigfade bf2" alt="{c2}">
<img src="/assets/image/other_univ/{u3}" class="bigfade bf3" alt="{c3}">
<div class="bigcap cp1">{c1}</div>
<div class="bigcap cp2">{c2}</div>
<div class="bigcap cp3">{c3}</div>
</div>"""


def main():
    conn = sqlite3.connect(str(DB))

    # P14 (idx=13): u1 동신대, u2 수원여대, u3 한국기술교육대
    P14 = build(
        ["u1.png", "u2.png", "u3.png"],
        ["동신대 · 취업률 1위", "수원여대 · 취업률 1위 달성", "한국기술교육대 · 4년제 대학 1위"],
    )
    conn.execute("UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=13", (P14, PID))
    print("[P14] 3개 광고 대형→제자리 트랜지션 적용")

    # P15 (idx=14): u5 한양사이버대, u6 대전, u8 대관령
    P15 = build(
        ["u5.png", "u6.png", "u8.png"],
        ["한양사이버대 · 1등 넘어 월등하게", "대전 · 국고 1,295억 확보", "대관령 · 전국 4년제 1위"],
    )
    conn.execute("UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=14", (P15, PID))
    print("[P15] 3개 광고 대형→제자리 트랜지션 적용")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
