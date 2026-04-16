# -*- coding: utf-8 -*-
"""V30 정리:
1. pt.html에서 P32(영상 2), P33(영상 3) 슬라이드 블록 삭제
2. P34~P49 slide-pagenum 값을 -2 (P32~P47)
3. 모든 페이지에서 `<div class="t-overline is-accent" ...>...</div>` 제거
4. DB(V30 id=138) 동일 반영: order 31/32 삭제, order 33+ order_idx -2, 모든 섹션 content에서 t-overline is-accent 제거
"""
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PT = ROOT / "scripts" / "pt.html"
DB = ROOT / "data" / "adproposal.db"
PID = 138

# =========================================================
# 1) pt.html 처리
# =========================================================
html = PT.read_text(encoding="utf-8")

# (a) P32(영상 2), P33(영상 3) 슬라이드 블록 삭제
# 각 블록은 '<div class="slide slide-content...> ... slide-pagenum">32</div> ... </div>' 구조
def remove_slide_block(html: str, pagenum: str) -> str:
    pattern = re.compile(
        r'<div class="slide slide-content[^"]*">[\s\S]*?<div class="slide-pagenum">'
        + re.escape(pagenum)
        + r"</div>[\s\S]*?\n</div>\n",
        re.MULTILINE,
    )
    m = pattern.search(html)
    if not m:
        raise RuntimeError(f"P{pagenum} 슬라이드 블록 못 찾음")
    return html[: m.start()] + html[m.end():]

html = remove_slide_block(html, "32")
html = remove_slide_block(html, "33")
print("P32, P33 슬라이드 블록 삭제 완료")

# (b) slide-pagenum 값 P34~P49 -> -2 (P32~P47)
# 주의: 낮은 번호부터 순차 치환 (34->32, 35->33, ... 49->47)
# 각 pagenum 문자열은 파일 내 유일
for old in range(34, 50):
    new = old - 2
    old_tag = f'<div class="slide-pagenum">{old:02d}</div>'
    new_tag = f'<div class="slide-pagenum">{new:02d}</div>'
    if old_tag in html:
        html = html.replace(old_tag, new_tag, 1)
    else:
        # 두 자리 없이 쓰여있을 가능성 (ex. "34" without zero-pad)
        alt_old = f'<div class="slide-pagenum">{old}</div>'
        alt_new = f'<div class="slide-pagenum">{new}</div>'
        if alt_old in html:
            html = html.replace(alt_old, alt_new, 1)
        else:
            print(f"  경고: P{old} pagenum 태그 못 찾음 (스킵)")
print("P34~P49 -> P32~P47 번호 조정 완료")

# (c) t-overline is-accent div 제거
# 매치 대상: <div class="t-overline is-accent"...>...</div>
overline_pattern = re.compile(
    r'<div class="t-overline is-accent"[^>]*>[^<]*</div>',
    re.DOTALL,
)
removed = len(overline_pattern.findall(html))
html = overline_pattern.sub("", html)
print(f"t-overline is-accent 제거: {removed}곳")

PT.write_text(html, encoding="utf-8")
print("pt.html 저장 완료\n")

# =========================================================
# 2) DB 처리 (V30 id=138)
# =========================================================
conn = sqlite3.connect(str(DB))
conn.row_factory = sqlite3.Row

# (a) order 31, 32 섹션 삭제 (P32, P33)
cur = conn.execute("DELETE FROM sections WHERE proposal_id=? AND order_idx IN (31,32)", (PID,))
print(f"DB 섹션 삭제: order 31/32 총 {cur.rowcount}개")

# (b) order 33+ -> order-2
rows = conn.execute(
    "SELECT id, order_idx FROM sections WHERE proposal_id=? AND order_idx>=33 ORDER BY order_idx",
    (PID,),
).fetchall()
for r in rows:
    conn.execute("UPDATE sections SET order_idx=? WHERE id=?", (r["order_idx"] - 2, r["id"]))
print(f"DB 섹션 재정렬: {len(rows)}개 -> order-2")

# (c) 모든 섹션 content에서 t-overline is-accent div 제거
all_rows = conn.execute(
    "SELECT id, content FROM sections WHERE proposal_id=?", (PID,)
).fetchall()
db_removed_total = 0
for r in all_rows:
    if not r["content"]:
        continue
    new_content, n = overline_pattern.subn("", r["content"])
    if n > 0:
        conn.execute("UPDATE sections SET content=? WHERE id=?", (new_content, r["id"]))
        db_removed_total += n
print(f"DB content t-overline is-accent 제거: {db_removed_total}곳")

# (d) P29, P30, P31 content도 pt.html과 맞추기 위해 업데이트
# 이 3개는 구조가 크게 바뀌었으므로 수동 sync
P29_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:영상 접근법--><div style="padding:var(--s-3) 0;text-align:center"><div style="display:flex;justify-content:center;margin-bottom:var(--s-4)"><div style="display:flex;border:1px solid #E8E8E8;border-radius:6px;max-width:760px"><div style="flex:1;padding:var(--s-4) var(--s-5);text-align:left"><div class="t-overline" style="margin-bottom:var(--s-3)">PRINT &nbsp;·&nbsp; 지면</div><div class="t-subtitle w-regular" style="line-height:1.6">정제된 한 장면<br><span class="is-accent w-bold">리프레이밍</span>으로 증명</div></div><div style="width:1px;background:#E8E8E8"></div><div style="flex:1;padding:var(--s-4) var(--s-5);text-align:left"><div class="t-overline" style="margin-bottom:var(--s-3)">VIDEO &nbsp;·&nbsp; 영상</div><div class="t-subtitle w-regular" style="line-height:1.6;white-space:nowrap">풀어낸 한 편의 이야기<br><span class="is-accent w-bold">스토리텔링</span>으로 증명</div></div></div></div><div class="is-muted" style="font-size:32px;line-height:1;margin-bottom:var(--s-4)">↓</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-4)"></div><div class="t-heading" style="margin-bottom:var(--s-4)">같은 컨셉 <span class="is-accent">증명</span>을,<br>이번엔 <span class="is-accent">이야기</span>로</div><div style="width:60px;height:1px;background:#E8E8E8;margin:0 auto var(--s-3)"></div><div class="t-subtitle w-regular is-muted" style="font-style:italic">— 그렇다면, 어떤 이야기로?</div></div><!--SCRIPT_START-->"지면은, 한 장입니다 정제된 한 순간을 <strong>리프레이밍</strong>으로 증명했습니다<br><br>영상은, 60초입니다 이야기를 풀어낼 수 있습니다<br>같은 컨셉 <strong>증명</strong>을, 이번엔 <strong>스토리텔링</strong>으로 풀었습니다<br><br><strong>그렇다면 — 어떤 이야기로?</strong>"<!--SCRIPT_END-->"""

P30_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:슬로건--><div style="padding:var(--s-4) 0;text-align:center"><div class="t-headline" style="margin-bottom:var(--s-5);line-height:1.2;font-size:72px">영산대학교는,<br><span class="is-accent">지혜</span>로 증명합니다</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div class="t-caption is-muted" style="margin-bottom:var(--s-4);letter-spacing:2px">왜 '지혜'인가</div><div style="display:inline-block;text-align:left;max-width:820px"><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8"><div class="t-overline" style="width:130px;flex-shrink:0">① 校訓</div><div class="t-subtitle w-regular">"지혜로운 가치를 배우는 대학, 지혜로운 당신을 만드는 대학"</div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-2) 0;border-bottom:1px solid #E8E8E8"><div class="t-overline" style="width:130px;flex-shrink:0">② 영상 주인공</div><div class="t-subtitle w-regular">누군가 부르면, <span class="is-ink w-bold">돌아보는 사람</span></div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-2) 0"><div class="t-overline" style="width:130px;flex-shrink:0">③ 졸업생</div><div class="t-subtitle w-regular">항공·호텔·경찰·뷰티 현장, <span class="is-accent w-bold">바로 그 이름</span></div></div></div></div><!--SCRIPT_START-->"이번 영상의 슬로건은 한 문장입니다<br><br><strong>영산대학교는, 지혜로 증명합니다</strong><br><br>왜 <strong>'지혜'</strong>인가 — 세 가지 이유가 한 단어에 있습니다<br><br><strong>첫째,</strong> 영산대 校訓이 <strong>지혜로운 가치를 배우는 대학, 지혜로운 당신을 만드는 대학</strong>입니다<br><strong>둘째,</strong> 영상 속 주인공의 이름입니다 — 누군가 부르면 돌아보는 사람<br><strong>셋째,</strong> 각계각층 영산대 졸업생이 불리는, 바로 그 이름입니다<br><br>한 이름, 세 갈래의 의미 — 하나의 <strong>증명</strong>입니다<br><br>이제, 실제 영상입니다"<!--SCRIPT_END-->"""

# P31은 기존 구조 유지 + 하단 캡션만 슬로건으로 교체. DB의 P31 content를 조회해서 하단 캡션 부분만 치환.
row31 = conn.execute(
    "SELECT id, content FROM sections WHERE proposal_id=? AND order_idx=30", (PID,)
).fetchone()
if row31 and row31["content"]:
    body = row31["content"]
    # 기존 캡션 블록 찾아 슬로건으로 교체
    old_caption_re = re.compile(
        r'<div class="t-caption"[^>]*margin-top[^>]*>.*?</div>',
        re.DOTALL,
    )
    new_caption = '<div style="text-align:center;margin-top:var(--s-3);font-size:36px;font-weight:700;line-height:1.2;letter-spacing:-1px;color:#1A1A1A">영산대학교는, <span style="color:#E84E10">지혜</span>로 증명합니다</div>'
    new_body, n = old_caption_re.subn(new_caption, body)
    if n > 0:
        conn.execute("UPDATE sections SET content=? WHERE id=?", (new_body, row31["id"]))
        print(f"DB P31(order=30) 하단 캡션 슬로건 교체")
    else:
        print("경고: P31 기존 캡션 패턴 못 찾음")

conn.execute(
    "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=28",
    (P29_CONTENT, PID),
)
print("DB P29(order=28) content 갱신")
conn.execute(
    "UPDATE sections SET content=?, title=? WHERE proposal_id=? AND order_idx=29",
    (P30_CONTENT, "대학 공식 홍보영상 기획 및 제작", PID),
)
print("DB P30(order=29) content 갱신")

conn.commit()
conn.close()
print("\nDB 갱신 완료")
