# -*- coding: utf-8 -*-
"""V101 빌드업 재구성 (11장 빌드업 + 이후).

변경:
  P3  시장 현황 (생존 톤 추가)
  P4~P7  광고 시안 4장 (각 대학 1개씩) — 신규 3장 + 기존 idx=3 교체
  P8  '똑같이' 기억 안됨 + PIVOT 질문
  P9  morph (이동)
  P10 '똑같이' 외치지 않는 것 (신규, 각인 선언 분리)
  P11 기억을 넘어 각인 = 전부 (기존 각인 선언 재작성)
  P12 제안업체 (+4 시프트)
  ... 이후 +4 시프트
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

# =============================================================================
# P3 시장 현황 — 생존 톤 강화
# =============================================================================
P3_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-4) 0"><div class="t-headline" style="margin-bottom:var(--s-3);line-height:1.35">대학은 지금, <span class="is-accent">생존의 시간</span>입니다</div><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-5);font-style:italic">모두가, 이 문제로 분투하고 있습니다</div><div style="display:flex;flex-direction:column;gap:0;max-width:880px;width:100%;margin:0 auto var(--s-4)"><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:42px;font-weight:700;color:#E84E10;line-height:1;min-width:140px;text-align:left;letter-spacing:-1px">-18%</div><div style="font-size:20px;color:#1A1A1A;text-align:left;flex:1">부울경 수험생 (2018→2025)</div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:42px;font-weight:700;color:#E84E10;line-height:1;min-width:140px;text-align:left;letter-spacing:-1px">2.3배</div><div style="font-size:20px;color:#1A1A1A;text-align:left;flex:1">지방 사립대 광고 경쟁 격화</div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:42px;font-weight:700;color:#E84E10;line-height:1;min-width:140px;text-align:left;letter-spacing:-1px">38%</div><div style="font-size:20px;color:#1A1A1A;text-align:left;flex:1">2030 폐교 위기 예측</div></div></div><div class="t-caption is-muted" style="font-style:italic">다들 아시는 이야기입니다. 짚고 넘어갑니다.</div></div><!--SCRIPT_START-->"대학은 지금, <strong>생존의 시간</strong>입니다.<br>모두가, 이 문제로 분투하고 있습니다.<br><br>부울경 수험생 18% 감소, 광고 경쟁 2.3배, 2030년 38% 폐교 위기.<br>다들 아시는 이야기입니다. 짚고 넘어가겠습니다."<!--SCRIPT_END-->"""


# =============================================================================
# 광고 시안 4장 — 각 대학 1개, 동일 레이아웃
# =============================================================================
def ad_slide(label: str, copy: str) -> str:
    return (
        '<!--PARENT:I 제안개요--><!--TAG:다른 대학 광고-->'
        '<div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0">'
        f'<div class="t-caption is-muted" style="letter-spacing:3px;margin-bottom:var(--s-3)">{label}</div>'
        '<div style="width:88%;max-width:960px;aspect-ratio:16/9;background:#F5F5F5;border:1px solid #E0E0E0;display:flex;align-items:center;justify-content:center;color:#A0A0A5;font-size:13px;letter-spacing:3px;font-weight:700;margin-bottom:var(--s-4)">AD PLACEHOLDER</div>'
        f'<div style="font-size:32px;font-weight:700;color:#1A1A1A;line-height:1.3;letter-spacing:-0.5px">"{copy}"</div>'
        '</div>'
        f'<!--SCRIPT_START-->"{label} — <strong>\'{copy}\'</strong>"<!--SCRIPT_END-->'
    )


AD1 = ad_slide("A 대학교", "글로벌 경쟁력 1위")
AD2 = ad_slide("B 대학교", "국내 최고의 교수진")
AD3 = ad_slide("C 대학교", "미래형 인재를 키웁니다")
AD4 = ad_slide("D 대학교", "4차 산업혁명을 선도합니다")


# =============================================================================
# P8 PIVOT (소음 리스트 제거 — 광고 4장으로 이미 체감)
# =============================================================================
P8_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-headline" style="margin-bottom:var(--s-3);line-height:1.35;max-width:1100px">'<span class="is-accent">똑같이</span>'만 말하는 대학은,<br>더 이상 기억되지 않습니다</div><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-6);font-style:italic">이제 사람들은 — 다음에 집중합니다</div><div style="width:60px;height:1px;background:#E0E0E0;margin:0 auto var(--s-6)"></div><div style="font-size:68px;font-weight:700;color:#1A1A1A;line-height:1.4;letter-spacing:-2px;max-width:1100px">"그래서 —<br><span class="is-accent">지금 뭘 하고 있지?"</span></div></div><!--SCRIPT_START-->"(광고 4장을 본 직후)<br><br>'<strong>똑같이</strong>'만 말하는 대학은, 더 이상 기억되지 않습니다.<br>이제 사람들은 — 다음에 집중합니다.<br><br><strong>'그래서 — 지금 뭘 하고 있지?'</strong><br><br>(5초 침묵)"<!--SCRIPT_END-->"""


# =============================================================================
# P10 '똑같이' 외치지 않는 것 (신규, 각인 선언 분리 1/2)
# =============================================================================
P10_NOT_SAME = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-4)">앞서 보신 영산대의 이 움직임을 —</div><div class="t-hero" style="line-height:1.3;max-width:1100px">'<span class="is-accent">똑같이</span>' 외치지 않는 것</div></div><!--SCRIPT_START-->"앞서 보신 영산대의 이 움직임을 —<br><br><strong>'똑같이' 외치지 않는 것.</strong>"<!--SCRIPT_END-->"""


# =============================================================================
# P11 기억을 넘어 각인 = 전부 (기존 각인 선언 재작성)
# =============================================================================
P11_IMPRINT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-3)">영산대를 —</div><div class="t-title" style="line-height:1.4;margin-bottom:var(--s-5);max-width:1100px">기억시키는 것을 넘어,<br>'<span class="is-accent">각인</span>'시키는 것</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div class="t-subtitle w-regular is-muted">이것이, 이번 제안의 <span class="is-accent w-bold">전부</span>입니다</div></div><!--SCRIPT_START-->"영산대를 —<br><br>기억시키는 것을 넘어, <strong>'각인'시키는 것.</strong><br><br>이것이, 이번 제안의 <strong>전부</strong>입니다."<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    try:
        # 레퍼런스 (level, status)
        sample = conn.execute(
            "SELECT level, status FROM sections WHERE proposal_id=? AND order_idx=3",
            (PID,),
        ).fetchone()
        lvl = sample["level"]
        st = sample["status"]

        # STEP 1: idx 6 이상 모두 +4 시프트 (음수 경유)
        conn.execute(
            "UPDATE sections SET order_idx = -(order_idx + 4) "
            "WHERE proposal_id=? AND order_idx >= 6",
            (PID,),
        )
        conn.execute(
            "UPDATE sections SET order_idx = -order_idx "
            "WHERE proposal_id=? AND order_idx < 0",
            (PID,),
        )
        print("STEP 1: idx 6~ 모두 +4 시프트")

        # STEP 2: idx 4, 5 → idx 7, 8로 이동 (+3)
        conn.execute(
            "UPDATE sections SET order_idx=7 WHERE proposal_id=? AND order_idx=4",
            (PID,),
        )
        conn.execute(
            "UPDATE sections SET order_idx=8 WHERE proposal_id=? AND order_idx=5",
            (PID,),
        )
        print("STEP 2: idx 4 (PIVOT) → 7, idx 5 (morph) → 8")

        # STEP 3: idx 3 (기존 소음 4분할) → 광고 시안 1로 내용 교체
        conn.execute(
            "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=3",
            ("광고 시안 1 — A대학", AD1, PID),
        )
        print("STEP 3: idx 3 → 광고 시안 1 (A대학)")

        # STEP 4: idx 2 시장 현황 생존 톤 강화
        conn.execute(
            "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=2",
            ("시장 현황 — 생존", P3_CONTENT, PID),
        )
        print("STEP 4: idx 2 시장 현황 생존 톤 강화")

        # STEP 5: idx 4, 5, 6 신규 INSERT (광고 시안 2, 3, 4)
        inserts = [
            (4, "광고 시안 2 — B대학", AD2),
            (5, "광고 시안 3 — C대학", AD3),
            (6, "광고 시안 4 — D대학", AD4),
        ]
        for idx, title, content in inserts:
            conn.execute(
                """INSERT INTO sections (proposal_id, level, title, order_idx, content, status)
                   VALUES (?,?,?,?,?,?)""",
                (PID, lvl, title, idx, content, st),
            )
        print("STEP 5: idx 4, 5, 6 광고 시안 2~4 INSERT")

        # STEP 6: idx 7 (이동된 PIVOT)을 새 P8 내용으로 재작성 (소음 리스트 제거)
        conn.execute(
            "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=7",
            ("PIVOT 질문", P8_CONTENT, PID),
        )
        print("STEP 6: idx 7 PIVOT 재작성 (소음 리스트 제거)")

        # STEP 7: idx 10 (이동된 기존 각인 선언) → '똑같이' 외치지 않음으로
        #         idx 11 신규 INSERT → 각인 = 전부
        # 현재 idx 10 자리엔 기존 각인 선언이 있음 (+4 시프트된 것)
        # 이걸 '똑같이 외치지 않음'으로 교체하고, idx 11에 각인=전부 삽입
        # 그러나 현재 idx 11에는 기존 제안업체 일반 (+4 시프트)이 있음
        # → 순서: idx 11~ 모두 +1 시프트 먼저, 그다음 idx 10 재작성 + idx 11 INSERT

        # 7-a. idx 11~ 모두 +1 시프트 (음수 경유)
        conn.execute(
            "UPDATE sections SET order_idx = -(order_idx + 1) "
            "WHERE proposal_id=? AND order_idx >= 11",
            (PID,),
        )
        conn.execute(
            "UPDATE sections SET order_idx = -order_idx "
            "WHERE proposal_id=? AND order_idx < 0",
            (PID,),
        )

        # 7-b. idx 10 내용을 '똑같이 외치지 않음'으로 교체
        conn.execute(
            "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=10",
            ("똑같이 외치지 않음", P10_NOT_SAME, PID),
        )

        # 7-c. idx 11에 '각인 = 전부' INSERT
        conn.execute(
            """INSERT INTO sections (proposal_id, level, title, order_idx, content, status)
               VALUES (?,?,?,?,?,?)""",
            (PID, lvl, "각인 선언 — 전부", 11, P11_IMPRINT, st),
        )
        print("STEP 7: idx 10 '똑같이 외치지 않음' + idx 11 '각인=전부'")

        conn.commit()

        # 결과
        rows = conn.execute(
            "SELECT order_idx, title FROM sections WHERE proposal_id=? ORDER BY order_idx LIMIT 20",
            (PID,),
        ).fetchall()
        print(f"\n=== V101 빌드업 재구성 후 (11장 빌드업) ===")
        for r in rows:
            print(f"  idx={r['order_idx']:2d} | {r['title']}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
