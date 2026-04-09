"""V16-1/V16-2/V16-3: V14 콘텐츠 + V15 트랜지션 + 이미지 편집 기능."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.db import get_conn, init_db, migrate_db
from scripts.create_v8_to_v14 import (
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
for title, ver, label, cc, tl, cfn in [
    ("V16-1: 이름을 가려봐", "V16-1", "A", "이름을 가려봐.", "이름을 가려도 보이는 대학.", concept_A),
    ("V16-2: 같은 학교", "V16-2", "B", "같은 학교.", "같은 학교. 영산대학교.", concept_B),
    ("V16-3: 이 사람은 배우가 아닙니다", "V16-3", "C", "이 사람은 배우가 아닙니다.", "이 사람은 배우가 아닙니다.", concept_C),
]:
    cb, sb = cfn()
    pid = create(conn, title, ver, label, v14_sections(cc, tl, cb, sb))
    print(f"{ver}: id={pid}")
conn.commit()
conn.close()
print("Done.")
