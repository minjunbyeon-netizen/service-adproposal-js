import sqlite3, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
conn = sqlite3.connect('data/adproposal.db')
conn.row_factory = sqlite3.Row
rows = conn.execute(
    'SELECT id, order_idx, level, title, content FROM sections WHERE proposal_id=179 ORDER BY order_idx'
).fetchall()

# order=38 본문 일부에서 안정감/제3자 주변 컨텍스트 확인
print('=== order=38 본문 안정감/제3자/신뢰 컨텍스트 ===')
for r in rows:
    if r['order_idx'] == 38:
        c = r['content'] or ''
        for kw in ['신뢰', '안정감', '제3자', '권위', '검증']:
            for m in re.finditer(re.escape(kw), c):
                i = m.start()
                print(f"  [{kw}] ...{c[max(0,i-60):i+100]}...")
                print('  ---')

# order=33 (Slide 34) 본문 전체
print('\n=== order=33 (Slide 34) 본문 ===')
for r in rows:
    if r['order_idx'] == 33:
        print(r['content'])

# 재학 중부터 업계인 본문 매치 모든 곳 컨텍스트
print('\n=== "재학 중부터 업계인" 전체 컨텍스트 ===')
for r in rows:
    c = r['content'] or ''
    t = r['title'] or ''
    if '재학 중부터 업계인' in t:
        print(f"\n[TITLE] order={r['order_idx']} → {t!r}")
    for m in re.finditer('재학 중부터 업계인', c):
        i = m.start()
        print(f"  [BODY] order={r['order_idx']} ...{c[max(0,i-50):i+80]}...")
