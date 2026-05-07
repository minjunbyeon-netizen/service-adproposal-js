"""V101 PT를 GitHub Pages용 정적 HTML로 export.

localhost에서 PT를 fetch한 뒤 /assets/ 절대경로 → assets/ 상대경로로 치환.
docs/index.html 에 저장 (GitHub Pages = master:/docs).
"""
import re, urllib.request, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

URL = 'http://localhost:8881/api/proposals/179/export-html'
OUT = 'docs/index.html'

with urllib.request.urlopen(URL, timeout=30) as r:
    src = r.read().decode('utf-8')

# /assets/ 절대경로 → 상대경로 ("/assets/ 또는 '/assets/")
out = re.sub(r'''(["'])/(assets/)''', r'\1\2', src)

with open(OUT, 'w', encoding='utf-8', newline='') as f:
    f.write(out)

print(f'OUT: {OUT} ({len(out):,} bytes)')
print(f'잔존 절대 /assets: {out.count(chr(34) + "/assets")}')
print(f'상대 assets: {out.count(chr(34) + "assets/")}')
