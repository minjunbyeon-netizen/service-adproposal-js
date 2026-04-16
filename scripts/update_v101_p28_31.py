# -*- coding: utf-8 -*-
"""V101 P28~P31 재구성.

P28 (idx=27)  전환 — "지면 임팩트 → 영상 스토리"
P29 (idx=28)  슬로건 — "호텔관광은, 영산으로 각인됩니다"
P30 (idx=29)  써머리 — 전체 제안 요약
P31 (idx=30)  영상 — 실제 영상 재생 영역
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

# =============================================================================
# P28 전환 — 지면 → 영상
# =============================================================================
P28_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:섹션 전환--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-5);font-style:italic;letter-spacing:2px">— SHIFT —</div><div style="font-size:44px;font-weight:400;color:#6E6E73;line-height:1.45;margin-bottom:var(--s-4);letter-spacing:-0.5px">지면광고로 <span class="is-ink w-bold">임팩트</span>를 주었다면,</div><div style="width:60px;height:1px;background:#E0E0E0;margin:0 auto var(--s-4)"></div><div style="font-size:56px;font-weight:700;color:#1A1A1A;line-height:1.35;letter-spacing:-1.5px">영상광고로는<br><span class="is-accent">스토리</span>를 풀어냅니다</div></div><!--SCRIPT_START-->"지금까지, 저희는 지면광고로 <strong>임팩트</strong>를 보여드렸습니다.<br><br>이제부터는, 영상광고로 <strong>스토리</strong>를 풀어내겠습니다."<!--SCRIPT_END-->"""

# =============================================================================
# P29 슬로건 — "호텔관광은 영산으로 각인됩니다"
# =============================================================================
P29_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:슬로건--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div style="font-size:72px;font-weight:400;color:#6E6E73;line-height:1.25;margin-bottom:var(--s-3);letter-spacing:-1px">호텔관광은,</div><div style="font-size:120px;font-weight:700;color:#1A1A1A;line-height:1.1;letter-spacing:-4px;margin-bottom:var(--s-3)"><span class="is-accent">영산</span>으로</div><div style="font-size:72px;font-weight:700;color:#1A1A1A;line-height:1.2;letter-spacing:-1.5px">각인됩니다</div></div><!--SCRIPT_START-->"저희 제안의 한 문장 결론입니다.<br><br><strong>호텔관광은, 영산으로 각인됩니다.</strong><br><br>(잠깐 침묵 — 문장이 각인되도록)"<!--SCRIPT_END-->"""

# =============================================================================
# P30 써머리 — 전체 제안 정리
# =============================================================================
P30_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:전체 요약--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-5)">전체 제안, 한 눈에</div><div style="display:flex;flex-direction:column;gap:0;max-width:920px;width:94%;margin:0 auto"><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:13px;font-weight:700;color:#E84E10;letter-spacing:3px;min-width:120px;text-align:left">컨셉</div><div style="font-size:22px;font-weight:700;color:#1A1A1A;text-align:left;flex:1">증명 <span style="font-size:14px;color:#6E6E73;font-weight:400;margin-left:var(--s-2)">— 주장이 아닌, 숫자가 박히는 일</span></div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:13px;font-weight:700;color:#E84E10;letter-spacing:3px;min-width:120px;text-align:left">기법</div><div style="font-size:22px;font-weight:700;color:#1A1A1A;text-align:left;flex:1">리프레이밍 <span style="font-size:14px;color:#6E6E73;font-weight:400;margin-left:var(--s-2)">— 같은 숫자, 다른 프레임으로</span></div></div><div style="display:flex;align-items:flex-start;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:13px;font-weight:700;color:#E84E10;letter-spacing:3px;min-width:120px;text-align:left;padding-top:4px">시안 3가지</div><div style="font-size:16px;color:#1A1A1A;text-align:left;flex:1;line-height:1.9">· 대학이 아니라, <strong>산업이 선택한 대학</strong><br>· 세계 55위? 국내 3위. <strong>글로벌 1위가 될 때까지</strong><br>· 25명이 끝이 아닙니다. <strong>26번째가 당신이 될 때까지</strong></div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:13px;font-weight:700;color:#E84E10;letter-spacing:3px;min-width:120px;text-align:left">영상 스토리</div><div style="font-size:18px;color:#1A1A1A;text-align:left;flex:1">호텔관광 특성화의 생생한 현장 — 취업과 글로벌 무대로 가는 길</div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0"><div style="font-size:13px;font-weight:700;color:#E84E10;letter-spacing:3px;min-width:120px;text-align:left">기대 효과</div><div style="font-size:18px;color:#1A1A1A;text-align:left;flex:1">수험생·학부모의 기억 <span style="font-size:22px;color:#E84E10">→</span> <strong>각인</strong> <span style="font-size:22px;color:#E84E10">→</span> <strong>지원</strong></div></div></div></div><!--SCRIPT_START-->"전체 제안을 한 눈에 정리하면 —<br><br><strong>컨셉</strong>은 증명, <strong>기법</strong>은 리프레이밍.<br>3가지 시안으로 영산대의 자랑을 각인시키고,<br>영상으로 호텔관광 특성화의 스토리를 풀어냅니다.<br><br>그 결과 — 기억이 <strong>각인</strong>으로, 각인이 <strong>지원</strong>으로 전환됩니다."<!--SCRIPT_END-->"""

# =============================================================================
# P31 영상 — 실제 재생 영역
# =============================================================================
P31_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:영상 재생--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-caption is-muted" style="letter-spacing:3px;margin-bottom:var(--s-3)">— 영상 재생 —</div><div style="width:82%;max-width:1100px;aspect-ratio:16/9;background:#1A1A1A;display:flex;flex-direction:column;align-items:center;justify-content:center;margin:0 auto var(--s-4);border-radius:4px"><div style="width:90px;height:90px;border-radius:50%;background:rgba(255,255,255,0.12);display:flex;align-items:center;justify-content:center;margin-bottom:var(--s-3)"><div style="width:0;height:0;border-left:26px solid #FFFFFF;border-top:18px solid transparent;border-bottom:18px solid transparent;margin-left:6px"></div></div><div style="color:#FFFFFF;font-size:20px;font-weight:700;letter-spacing:-0.5px;margin-bottom:var(--s-1)">대학 공식 홍보영상</div><div style="color:#A0A0A5;font-size:13px;letter-spacing:2px">TVC 15" · 디지털 30"</div></div><div class="t-subtitle w-regular is-muted" style="font-style:italic">"호텔관광은, 영산으로 각인됩니다"</div></div><!--SCRIPT_START-->"(영상 재생 시작)<br><br>직접 보여드리겠습니다 — <strong>호텔관광은, 영산으로 각인됩니다.</strong><br><br>(영상 15초 또는 30초)<br><br>(영상 종료 후 잠깐 침묵)"<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    updates = [
        (27, "전환 — 지면 → 영상", P28_CONTENT),
        (28, "슬로건 — 영산으로 각인", P29_CONTENT),
        (29, "전체 제안 요약", P30_CONTENT),
        (30, "영상 재생 — 공식 홍보영상", P31_CONTENT),
    ]
    for idx, title, content in updates:
        conn.execute(
            "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=?",
            (title, content, PID, idx),
        )
        print(f"idx={idx} (P{idx+1}): {title}")
    conn.commit()
    print("\nP28~P31 재구성 완료")
    conn.close()


if __name__ == "__main__":
    main()
