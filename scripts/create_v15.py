"""V15-1/V15-2/V15-3: V14 콘텐츠 + 트랜지션 쇼케이스 템플릿."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.db import get_conn, init_db, migrate_db

# V14 스크립트에서 콘텐츠 함수 재사용
from create_v8_to_v14 import (
    RFP, SUMMARY, CONCEPTS, v14_sections,
    concept_A, concept_B, concept_C,
)

init_db()
migrate_db()

def create(conn, title, version, label, sections):
    cur = conn.execute(
        "INSERT INTO proposals (title,version,status,rfp_json,rfp_summary,raw_text,selected_concept) VALUES (?,?,?,?,?,?,?)",
        (title, version, "ready", RFP, SUMMARY, SUMMARY, label))
    pid = cur.lastrowid
    for lv, t, idx, content in sections:
        conn.execute("INSERT INTO sections (proposal_id,level,title,order_idx,content,status) VALUES (?,?,?,?,?,?)",
            (pid, lv, t, idx, content, "done" if content else "pending"))
    for lb, ct, bd in CONCEPTS:
        conn.execute("INSERT OR REPLACE INTO concepts (proposal_id,label,title,body) VALUES (?,?,?,?)",
            (pid, lb, ct, bd))
    return pid

conn = get_conn()

specs = [
    ("V15-1: 이름을 가려봐", "V15-1", "A", "이름을 가려봐.", "이름을 가려도 보이는 대학.", concept_A),
    ("V15-2: 같은 학교", "V15-2", "B", "같은 학교.", "같은 학교. 영산대학교.", concept_B),
    ("V15-3: 이 사람은 배우가 아닙니다", "V15-3", "C", "이 사람은 배우가 아닙니다.", "이 사람은 배우가 아닙니다.", concept_C),
]

for title, ver, label, cc, tl, cfn in specs:
    cb, sb = cfn()
    secs = v14_sections(cc, tl, cb, sb)
    pid = create(conn, title, ver, label, secs)
    print(f"{ver}: id={pid}")

conn.commit()
conn.close()
print("Done.")
