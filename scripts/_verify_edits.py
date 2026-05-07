import sqlite3, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
conn = sqlite3.connect('data/adproposal.db')
conn.row_factory = sqlite3.Row
rows = conn.execute(
    'SELECT id, order_idx, title, content FROM sections WHERE proposal_id=179 ORDER BY order_idx'
).fetchall()

# 1. 잔존 검사
remain = []
for r in rows:
    c = (r['content'] or '') + '\n' + (r['title'] or '')
    if '재학 중부터 업계인' in c:
        remain.append(('재학 중부터 업계인', r['order_idx'], r['title']))
    if '철학</span>를' in c:
        remain.append(('철학</span>를', r['order_idx'], r['title']))
    if '신뢰 매체로 안정감 형성' in c:
        remain.append(('신뢰 매체로 안정감 형성', r['order_idx'], r['title']))
    if '제3자 검증으로 권위 확보' in c:
        remain.append(('제3자 검증으로 권위 확보', r['order_idx'], r['title']))

print('=== 잔존 매치 ===')
if remain:
    for x in remain:
        print(x)
else:
    print('없음 (모두 치환 완료)')

# 2. 새 텍스트 확인
print('\n=== 새 텍스트 확인 ===')
for r in rows:
    c = r['content'] or ''
    t = r['title'] or ''
    new_in_t = '강의실이 곧 현장' in t
    cnt_c = c.count('강의실이 곧 현장')
    if new_in_t or cnt_c:
        print(f"order={r['order_idx']:>3} title_hit={new_in_t} body_count={cnt_c} title={t!r}")
    if r['order_idx'] == 33 and '철학</span>을' in c:
        print(f"order=33 ✓ 철학</span>을 적용됨")
    if r['order_idx'] == 38:
        if '특정 지역의 다양한 타겟에게 지속적으로 노출' in c:
            print(f"order=38 ✓ '특정 지역의 다양한 타겟...' 적용됨")
        if '공신력 있는 매체를 통한 신뢰성 확보' in c:
            print(f"order=38 ✓ '공신력 있는 매체...' 적용됨")
