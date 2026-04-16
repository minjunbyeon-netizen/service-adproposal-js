# -*- coding: utf-8 -*-
"""V101 P22-P30 - 헤드카피(좌상·대형) / 서브카피(좌·중) / 바디카피(우하·작게)."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


def build(slogan, img, head, sub, body, tag):
    body_html = "<br>".join(body)
    return f"""<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:{tag}-->
<style>
.slide-content:has(.showcase-bg) .content-header{{display:none !important}}
.slide-content:has(.showcase-bg) > [style*="HIVE MEDIA"]{{display:none !important}}
.slide-content:has(.showcase-bg) .slide-pagenum{{color:#fff !important;z-index:10}}
.slide-content:has(.showcase-bg){{padding:0 !important;background:#0a0a0a !important}}
</style>
<div class="showcase-bg" style="position:absolute;top:0;left:0;right:0;bottom:0;background:#0a0a0a;display:flex;justify-content:center;align-items:center;overflow:hidden">

<div style="position:absolute;top:16px;left:32px;font-size:13px;font-weight:700;color:#E84E10;z-index:10">{slogan}</div>

<img src="/assets/image/reframing/{img}" alt="{slogan}" style="height:100%;width:auto;max-width:100%;object-fit:contain;display:block">

<div style="position:absolute;top:40%;left:5%;max-width:55%;z-index:20;text-shadow:0 2px 16px rgba(0,0,0,0.85)">
<div style="font-size:52px;font-weight:700;color:#FFFFFF;line-height:1.25">{head}</div>
<div style="font-size:18px;color:#E84E10;font-weight:700;line-height:1.5;margin-top:16px">{sub}</div>
</div>

<div style="position:absolute;bottom:40px;right:40px;max-width:40%;text-align:right;z-index:20;text-shadow:0 2px 12px rgba(0,0,0,0.85)">
<div style="font-size:13px;color:#DDD;line-height:1.8;font-weight:400">{body_html}</div>
</div>

</div>"""


SLIDES = [
    (21, "산업이 먼저 찾아온 대학", "a1.png",
     "호텔이 먼저 고른 대학",
     "대학이 광고하지 않는다 — 호텔이 먼저 증명한 대학",
     ["신라, 롯데, 하얏트, 그랜드하얏트, 포시즌스.",
      "25개 호텔의 총지배인이 같은 강의실에서 시작했습니다.",
      "대학 광고는 이미 있습니다. 대학이 만들지 않았을 뿐입니다."],
     "Industry 01"),

    (22, "산업이 먼저 찾아온 대학", "a2.png",
     "부산을 떠나는 비행기마다,<br>영산이 타고 있습니다",
     "취업률이 아니라 — 하늘이 먼저 선택한 대학",
     ["대한항공, 아시아나, 제주항공, 진에어, 에어부산.",
      "동남권에서 가장 많은 승무원이 같은 대학에서 출발했습니다.",
      "김해공항의 유니폼은, 영산에서 시작됩니다."],
     "Industry 02"),

    (23, "산업이 먼저 찾아온 대학", "a3.png",
     "KTX는 서울로 떠나지만,<br>비행기는 부산으로 옵니다",
     "서울로 올라가는 게 아니라 — 산업이 내려오는 대학",
     ["매년 27개 호텔·항공·외식 기업의 채용팀이 영산대로 향합니다.",
      "당신이 올라갈 필요가 없습니다.",
      "산업이 먼저 내려옵니다."],
     "Industry 03"),

    (24, "세계가 증명한 숫자", "b1.png",
     "한국 3위가 아니라,<br>세계 55위",
     "국내 순위가 아니라 — 세계가 먼저 증명한 대학",
     ["QS 세계대학평가 호스피탈리티 부문 Top 55.",
      "국내 3위, 세계 55위.",
      "당신이 고르고 있던 축이, 전부였습니까."],
     "Global 01"),

    (25, "세계가 증명한 숫자", "b2.png",
     "서울을 기준으로 고르는<br>시대는 끝났다",
     "지방대가 아니라 — 세계 허브와 연결된 대학",
     ["홍콩과기대와 공동 국제학술대회 AISIC.",
      "수도권 대학 중 유일한 PATA 정회원.",
      "세계와 가장 직접 연결된 부산의 대학."],
     "Global 02"),

    (26, "세계가 증명한 숫자", "b3.png",
     "입학 준비물:<br>성적표, 자기소개서, 여권",
     "국내에서 시작하는 게 아니라 — 세계에서 시작하는 대학",
     ["이 대학은 여기서 시작하지 않습니다.",
      "홍콩에서, 방콕에서, 두바이에서 시작합니다.",
      "합격 통지서와 함께, 여권을 갱신하세요."],
     "Global 03"),

    (27, "재학 중부터 업계인", "c1.png",
     "학번이 끝나기 전에,<br>사번이 시작됩니다",
     "졸업 후가 아니라 — 재학 중부터 업계인",
     ["졸업을 기다리지 않습니다.",
      "영산대 호스피탈리티 재학생이 재학 중 현장에 나갑니다.",
      "대학의 안과 밖이 구분되지 않는 4년."],
     "Student 01"),

    (28, "재학 중부터 업계인", "c2.png",
     "호텔 총지배인이 되기까지 평균 30년<br>영산대는 25명을 배출했습니다",
     "평균이 아니라 — 예외를 시스템화한 대학",
     ["시간은 줄어들지 않습니다.",
      "다만, 어느 대학에서 시작하느냐가 결정합니다.",
      "25명의 총지배인이 같은 곳에서 출발했습니다."],
     "Student 02"),

    (29, "재학 중부터 업계인", "c3.png",
     "신라가, 롯데가, 하얏트가 —<br>25번 같은 대학을 채용했다",
     "한 번이 아니라 — 25번 반복된 시스템",
     ["같은 주소, 같은 강의실.",
      "우연이라 부르기엔 너무 자주 반복됐습니다.",
      "이 숫자는 지금도 늘어나는 중입니다."],
     "Student 03"),
]


def main():
    conn = sqlite3.connect(str(DB))
    for idx, slogan, img, head, sub, body, tag in SLIDES:
        c = build(slogan, img, head, sub, body, tag)
        conn.execute(
            "UPDATE sections SET content=?, title=? WHERE proposal_id=? AND order_idx=?",
            (c, f"{slogan} — {tag}", PID, idx),
        )
        print(f"  idx={idx}: {tag}")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
