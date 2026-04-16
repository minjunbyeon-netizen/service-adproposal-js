# -*- coding: utf-8 -*-
"""V101 P3 위아래 변경 + P7 2장 분리.

P3  위아래 뒤집기 (수치 위, 헤드라인 아래) + "다들 아시는" 캡션 삭제
P7  PIVOT 2장 분리:
    P7 — "'똑같이' 기억 안됨 + 다음에 집중"
    P8 — "그래서 — 지금 뭘 하고 있지?" (단독)
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

# =============================================================================
# P3 — 위아래 뒤집기, 캡션 삭제
# =============================================================================
P3_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-4) 0"><div style="display:flex;flex-direction:column;gap:0;max-width:880px;width:100%;margin:0 auto var(--s-6)"><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:42px;font-weight:700;color:#E84E10;line-height:1;min-width:140px;text-align:left;letter-spacing:-1px">-18%</div><div style="font-size:20px;color:#1A1A1A;text-align:left;flex:1">부울경 수험생 (2018→2025)</div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:42px;font-weight:700;color:#E84E10;line-height:1;min-width:140px;text-align:left;letter-spacing:-1px">2.3배</div><div style="font-size:20px;color:#1A1A1A;text-align:left;flex:1">지방 사립대 광고 경쟁 격화</div></div><div style="display:flex;align-items:baseline;gap:var(--s-4);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8"><div style="font-size:42px;font-weight:700;color:#E84E10;line-height:1;min-width:140px;text-align:left;letter-spacing:-1px">38%</div><div style="font-size:20px;color:#1A1A1A;text-align:left;flex:1">2030 폐교 위기 예측</div></div></div><div style="width:60px;height:1px;background:#E0E0E0;margin:0 auto var(--s-4)"></div><div class="t-headline" style="margin-bottom:var(--s-2);line-height:1.35">대학은 지금, <span class="is-accent">생존의 시간</span>입니다</div><div class="t-subtitle w-regular is-muted" style="font-style:italic">모두가, 이 문제로 분투하고 있습니다</div></div><!--SCRIPT_START-->"부울경 수험생 18% 감소, 광고 경쟁 2.3배, 2030년 38% 폐교 위기.<br><br>대학은 지금, <strong>생존의 시간</strong>입니다.<br>모두가, 이 문제로 분투하고 있습니다."<!--SCRIPT_END-->"""

# =============================================================================
# P7 — '똑같이' 기억 안됨 (질문 분리)
# =============================================================================
P7_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-headline" style="margin-bottom:var(--s-4);line-height:1.35;max-width:1100px">'<span class="is-accent">똑같이</span>'만 말하는 대학은,<br>더 이상 기억되지 않습니다</div><div style="width:60px;height:1px;background:#E0E0E0;margin:0 auto var(--s-4)"></div><div class="t-subtitle w-regular is-muted" style="font-style:italic">이제 사람들은 — 다음에 집중합니다</div></div><!--SCRIPT_START-->"(광고 3장을 본 직후)<br><br>'<strong>똑같이</strong>'만 말하는 대학은, 더 이상 기억되지 않습니다.<br><br>이제 사람들은 — 다음에 집중합니다."<!--SCRIPT_END-->"""

# =============================================================================
# P8 — PIVOT 질문 단독
# =============================================================================
P8_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div style="font-size:84px;font-weight:700;color:#1A1A1A;line-height:1.4;letter-spacing:-2.5px;max-width:1200px">"그래서 —<br><span class="is-accent">지금 뭘 하고 있지?"</span></div></div><!--SCRIPT_START-->"<strong>'그래서 — 지금 뭘 하고 있지?'</strong><br><br>(5초 침묵 — 평가위원이 스스로 답을 찾게 둡니다)"<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    try:
        # 1. P3 수정 (위아래 뒤집기)
        conn.execute(
            "UPDATE sections SET title=?, content=? WHERE proposal_id=? AND order_idx=2",
            ("시장 현황 — 생존", P3_CONTENT, PID),
        )
        print("P3 (idx=2): 위아래 뒤집기 + 캡션 삭제")

        # 2. idx 7 이후 +1 시프트 (P8 삽입 위한 빈자리)
        conn.execute(
            "UPDATE sections SET order_idx = -(order_idx + 1) "
            "WHERE proposal_id=? AND order_idx >= 7",
            (PID,),
        )
        conn.execute(
            "UPDATE sections SET order_idx = -order_idx "
            "WHERE proposal_id=? AND order_idx < 0",
            (PID,),
        )
        print("idx 7+ 모두 +1 시프트")

        # idx 7 이제 비어있음 — 기존 PIVOT은 idx 8로 이동됨
        # 3. idx 8 (이동된 기존 PIVOT) content를 P7 내용으로 교체 후 idx 7로 되돌림
        # 더 간단하게: idx 8 (이동된 PIVOT)을 idx 7로 되돌리고 내용 교체
        conn.execute(
            "UPDATE sections SET order_idx=7, title=?, content=? "
            "WHERE proposal_id=? AND order_idx=8",
            ("똑같이 기억 안됨", P7_CONTENT, PID),
        )
        print("idx 8 (이동된 PIVOT) → idx 7로 복귀 + 내용 교체")

        # 4. idx 8에 질문 단독 INSERT
        sample = conn.execute(
            "SELECT level, status FROM sections WHERE proposal_id=? AND order_idx=7",
            (PID,),
        ).fetchone()
        conn.execute(
            """INSERT INTO sections (proposal_id, level, title, order_idx, content, status)
               VALUES (?,?,?,?,?,?)""",
            (PID, sample["level"], "PIVOT 질문 단독", 8, P8_CONTENT, sample["status"]),
        )
        print("idx 8 신규: '그래서 지금 뭘 하고 있지?' 단독")

        conn.commit()

        rows = conn.execute(
            "SELECT order_idx, title FROM sections WHERE proposal_id=? ORDER BY order_idx LIMIT 18",
            (PID,),
        ).fetchall()
        print(f"\n=== V101 최종 ===")
        for r in rows:
            print(f"  idx={r['order_idx']:2d} | {r['title']}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
