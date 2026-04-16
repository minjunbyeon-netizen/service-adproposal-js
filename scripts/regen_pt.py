# -*- coding: utf-8 -*-
"""V30 DB 상태로 scripts/pt.html 재생성."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402

PT = ROOT / "scripts" / "pt.html"
PID = 138

app = create_app()
with app.test_client() as client:
    r = client.get(f"/api/proposals/{PID}/export-html")
    if r.status_code != 200:
        raise RuntimeError(f"렌더 실패 status={r.status_code}")
    html = r.get_data(as_text=True)

PT.write_text(html, encoding="utf-8")
print(f"pt.html 재생성 완료: {len(html)} bytes")
