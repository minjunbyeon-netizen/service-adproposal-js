# -*- coding: utf-8 -*-
"""V30 (id=138) P12/P13 스왑 + P14 강화."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 138

# P12 (order=11): METHOD 리프레이밍
P12 = (
    "기법",
    """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:기법--><div style="padding:var(--s-5) 0;text-align:center"><div class="t-overline is-accent" style="margin-bottom:var(--s-5)">METHOD</div><div class="t-title" style="margin-bottom:var(--s-4)">리프레이밍</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div class="t-subtitle w-regular is-muted" style="line-height:1.8">같은 사실을, <span class="is-ink w-bold">다른 프레임</span>에 놓는 일<br>— 저희는 이 기법으로, 사실을 <span class="is-accent w-bold">각인</span>시키겠습니다</div></div><!--SCRIPT_START-->"앞서 말씀드린 '다른 언어' — 저희는 이것을 <strong>리프레이밍(Re-framing)</strong>이라 부릅니다<br><br>행동경제학에서 검증된 기법으로, 같은 사실을 <strong>다른 프레임</strong>에 놓는 일입니다<br><br>저희는 이 리프레이밍으로, 영산대의 사실을 <strong>각인</strong>시키겠습니다"<!--SCRIPT_END-->""",
)

# P13 (order=12): CONCEPT 증명 + 각인=증명 연결
P13 = (
    "컨셉",
    """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:컨셉--><div style="padding:var(--s-5) 0;text-align:center"><div class="t-overline is-accent" style="margin-bottom:var(--s-4)">CONCEPT</div><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-4);line-height:1.6">각인시키는 행위 — 그것이 곧,</div><div class="t-hero" style="margin-bottom:var(--s-4)">증명</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div class="t-subtitle w-regular" style="line-height:1.7">주장이 아닌, <span class="is-accent w-bold">사실</span>로 설득하는 일<br>— 이 <span class="is-accent w-bold">증명</span>이, 저희의 컨셉입니다</div></div><!--SCRIPT_START-->"리프레이밍으로 사실을 <strong>각인</strong>시키는 행위 — 그것이 곧, 한 단어로 <strong>증명</strong>입니다<br><br>주장이 아닌, <strong>사실로 설득하는 일</strong><br><br>이 <strong>증명</strong>이, 저희의 이번 광고 컨셉입니다"<!--SCRIPT_END-->""",
)

# P14 (order=13): PREVIEW 강화 (각인 쪽 특대)
P14 = (
    "프리뷰",
    """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:프리뷰--><div style="padding:var(--s-4) 0;text-align:center"><div class="t-overline is-accent" style="margin-bottom:var(--s-3)">PREVIEW</div><div class="t-heading" style="margin-bottom:var(--s-2)">3가지 <span class="is-accent">증명</span></div><div class="t-body is-muted" style="margin-bottom:var(--s-4)">— 소음을 <span class="is-ink w-bold">각인</span>으로 바꾸는 일</div><div style="display:grid;grid-template-columns:1fr 80px 1.1fr;align-items:center;max-width:1200px;margin:0 auto;gap:var(--s-2) var(--s-3)"><div style="text-align:right;font-size:13px;letter-spacing:3px;color:#A0A0A5;font-weight:700">소음</div><div></div><div style="text-align:left;font-size:13px;letter-spacing:3px;color:#E84E10;font-weight:700">각인</div><div style="height:1px;background:#E8E8E8"></div><div></div><div style="height:1px;background:#E84E10"></div><div style="text-align:right;padding:var(--s-2) 0;font-size:20px;color:#A0A0A5;font-weight:400;line-height:1.4"><span style="font-size:12px;color:#C5C5C9">01</span>&nbsp;&nbsp;96.4% 취업률</div><div style="font-size:40px;font-weight:700;color:#E84E10;line-height:1">→</div><div style="text-align:left;padding:var(--s-1) 0;line-height:1"><div style="font-size:72px;font-weight:700;color:#E84E10;letter-spacing:-2px;line-height:1">3.6%</div><div style="font-size:22px;font-weight:400;color:#1A1A1A;margin-top:4px">탈락률</div></div><div style="text-align:right;padding:var(--s-2) 0;font-size:20px;color:#A0A0A5;font-weight:400;line-height:1.4"><span style="font-size:12px;color:#C5C5C9">02</span>&nbsp;&nbsp;국내 55위 대학교</div><div style="font-size:40px;font-weight:700;color:#E84E10;line-height:1">→</div><div style="text-align:left;padding:var(--s-1) 0;line-height:1"><div style="font-size:56px;font-weight:700;color:#E84E10;letter-spacing:-1.5px;line-height:1">글로벌 55위</div><div style="font-size:22px;font-weight:400;color:#1A1A1A;margin-top:4px">대학교</div></div><div style="text-align:right;padding:var(--s-2) 0;font-size:20px;color:#A0A0A5;font-weight:400;line-height:1.4"><span style="font-size:12px;color:#C5C5C9">03</span>&nbsp;&nbsp;25명의 총지배인</div><div style="font-size:40px;font-weight:700;color:#E84E10;line-height:1">→</div><div style="text-align:left;padding:var(--s-1) 0;line-height:1"><div style="font-size:56px;font-weight:700;color:#E84E10;letter-spacing:-1.5px;line-height:1">1개의 시스템</div><div style="font-size:22px;font-weight:400;color:#1A1A1A;margin-top:4px">(영산대)</div></div></div></div><!--SCRIPT_START-->"저희가 보여드릴 3가지 <strong>증명</strong>입니다<br><br>첫째, 96.4% 취업률이 아니라 <strong>3.6% 탈락률</strong><br>둘째, 국내 55위가 아니라 <strong>글로벌 55위</strong><br>셋째, 25명의 총지배인이 아니라 <strong>1개의 시스템(영산대)</strong>입니다<br><br>지금부터, 각 시안으로 보여드리겠습니다"<!--SCRIPT_END-->""",
)


def main():
    conn = sqlite3.connect(str(DB))
    try:
        for order_idx, (_tag, content) in zip([11, 12, 13], [P12, P13, P14]):
            cur = conn.execute(
                "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=?",
                (content, PID, order_idx),
            )
            print(f"order={order_idx} 갱신: {cur.rowcount}행")
        conn.commit()
        print("\n완료 -- V30 id=138 P12/P13/P14 반영")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
