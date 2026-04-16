# -*- coding: utf-8 -*-
"""V101 P22-P30 9장 최종 - 실제 시안 이미지 + 헤드카피/서브카피 오버레이."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


def build(slogan, img, head, sub, tag):
    # img=None이면 placeholder (B-2)
    img_section = (
        f'<img src="/assets/image/reframing/{img}" alt="{slogan}" '
        f'style="height:100%;width:auto;max-width:100%;object-fit:contain;display:block">'
        if img else
        '<div style="width:60%;height:80%;background:#222;display:flex;align-items:center;'
        'justify-content:center;color:#666;font-size:18px">시안 준비 중 (B-2)</div>'
    )
    return f"""<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:{tag}-->
<style>
.slide-content:has(.showcase-bg) .content-header{{display:none !important}}
.slide-content:has(.showcase-bg) > [style*="HIVE MEDIA"]{{display:none !important}}
.slide-content:has(.showcase-bg) .slide-pagenum{{color:#fff !important;z-index:10}}
.slide-content:has(.showcase-bg){{padding:0 !important;background:#0a0a0a !important}}
</style>
<div class="showcase-bg" style="position:absolute;top:0;left:0;right:0;bottom:0;background:#0a0a0a;display:flex;justify-content:center;align-items:center;overflow:hidden">

<div style="position:absolute;top:16px;left:32px;font-size:13px;font-weight:700;color:#E84E10;z-index:10">{slogan}</div>

{img_section}

<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;z-index:20;padding:var(--s-3);max-width:80%">
<div style="font-size:36px;font-weight:700;color:#FFFFFF;line-height:1.35;text-shadow:0 2px 16px rgba(0,0,0,0.8)">{head}</div>
<div style="font-size:18px;color:#E84E10;font-weight:700;line-height:1.5;margin-top:var(--s-2);text-shadow:0 2px 12px rgba(0,0,0,0.8)">{sub}</div>
</div>

</div>"""


SLIDES = [
    (21, "산업이 먼저 찾아온 대학", "a1.png",
     "호텔이 먼저 고른 대학",
     "대학이 광고하지 않는다 — 호텔이 먼저 증명한 대학", "Industry 01"),
    (22, "산업이 먼저 찾아온 대학", "a2.png",
     "부산을 떠나는 비행기마다,<br>영산이 타고 있습니다",
     "취업률이 아니라 — 하늘이 먼저 선택한 대학", "Industry 02"),
    (23, "산업이 먼저 찾아온 대학", "a3.png",
     "KTX는 서울로 떠나지만,<br>비행기는 부산으로 옵니다",
     "서울로 올라가는 게 아니라 — 산업이 내려오는 대학", "Industry 03"),

    (24, "세계가 증명한 숫자", "b1.png",
     "한국 3위가 아니라,<br>세계 55위",
     "국내 순위가 아니라 — 세계가 먼저 증명한 대학", "Global 01"),
    (25, "세계가 증명한 숫자", None,
     "서울을 기준으로 고르는<br>시대는 끝났다",
     "지방대가 아니라 — 세계 허브와 연결된 대학", "Global 02"),
    (26, "세계가 증명한 숫자", "b3.png",
     "입학 준비물:<br>성적표, 자기소개서, 여권",
     "국내에서 시작하는 게 아니라 — 세계에서 시작하는 대학", "Global 03"),

    (27, "재학 중부터 업계인", "c1.png",
     "학번이 끝나기 전에,<br>사번이 시작됩니다",
     "졸업 후가 아니라 — 재학 중부터 업계인", "Student 01"),
    (28, "재학 중부터 업계인", "c2.png",
     "호텔 총지배인이 되기까지 평균 30년<br>영산대는 25명을 배출했습니다",
     "평균이 아니라 — 예외를 시스템화한 대학", "Student 02"),
    (29, "재학 중부터 업계인", "c3.png",
     "신라가, 롯데가, 하얏트가 —<br>25번 같은 대학을 채용했다",
     "한 번이 아니라 — 25번 반복된 시스템", "Student 03"),
]


def main():
    conn = sqlite3.connect(str(DB))
    for idx, slogan, img, head, sub, tag in SLIDES:
        c = build(slogan, img, head, sub, tag)
        conn.execute(
            "UPDATE sections SET content=?, title=? WHERE proposal_id=? AND order_idx=?",
            (c, f"{slogan} — {tag}", PID, idx),
        )
        print(f"  idx={idx}: {slogan} · {tag} (img={img or 'placeholder'})")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
