"""V101 (proposal_id=179) 텍스트 일괄 수정.

1. "재학 중부터 업계인" → "강의실이 곧 현장" (title/body/alt/주석 전부)
2. order=33 (Slide 34): "철학</span>를" → "철학</span>을"
3. order=38 (Slide 38):
   - "신뢰 매체로 안정감 형성" → "특정 지역의 다양한 타겟에게 지속적으로 노출"
   - "제3자 검증으로 권위 확보" → "공신력 있는 매체를 통한 신뢰성 확보"
"""
import sqlite3, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROPOSAL_ID = 179
conn = sqlite3.connect('data/adproposal.db')
conn.row_factory = sqlite3.Row

rows = conn.execute(
    'SELECT id, order_idx, title, content FROM sections WHERE proposal_id=? ORDER BY order_idx',
    (PROPOSAL_ID,),
).fetchall()

OLD_PHRASE = '재학 중부터 업계인'
NEW_PHRASE = '강의실이 곧 현장'

total_title = 0
total_body = 0
total_slide34 = 0
total_slide38 = 0

for r in rows:
    new_title = r['title']
    new_content = r['content'] or ''
    title_changes = 0
    body_changes = 0

    # 1. 재학 중부터 업계인 전체 치환
    if OLD_PHRASE in (new_title or ''):
        cnt = new_title.count(OLD_PHRASE)
        new_title = new_title.replace(OLD_PHRASE, NEW_PHRASE)
        title_changes += cnt
    if OLD_PHRASE in new_content:
        cnt = new_content.count(OLD_PHRASE)
        new_content = new_content.replace(OLD_PHRASE, NEW_PHRASE)
        body_changes += cnt

    # 2. Slide 34 (order=33): 철학</span>를 → 철학</span>을
    if r['order_idx'] == 33:
        before = new_content
        new_content = new_content.replace('철학</span>를', '철학</span>을')
        if new_content != before:
            total_slide34 += 1

    # 3. Slide 38 (order=38)
    if r['order_idx'] == 38:
        before = new_content
        new_content = new_content.replace(
            '신뢰 매체로 안정감 형성',
            '특정 지역의 다양한 타겟에게 지속적으로 노출',
        )
        new_content = new_content.replace(
            '제3자 검증으로 권위 확보',
            '공신력 있는 매체를 통한 신뢰성 확보',
        )
        if new_content != before:
            total_slide38 += 1

    if title_changes or body_changes or new_title != r['title'] or new_content != (r['content'] or ''):
        conn.execute(
            'UPDATE sections SET title=?, content=?, updated_at=CURRENT_TIMESTAMP WHERE id=?',
            (new_title, new_content, r['id']),
        )
        total_title += title_changes
        total_body += body_changes
        print(f"id={r['id']} order={r['order_idx']} title_hits={title_changes} body_hits={body_changes}")

conn.commit()
conn.close()

print(f"\n=== 요약 ===")
print(f"강의실이 곧 현장 — title 치환: {total_title}건")
print(f"강의실이 곧 현장 — body 치환:  {total_body}건")
print(f"Slide 34 철학을 수정 적용:     {total_slide34}건")
print(f"Slide 38 신뢰/제3자 수정 적용: {total_slide38}건")
