# -*- coding: utf-8 -*-
"""V30 생성 -- V29(id=137) 복제 후 P2~P5 오프닝 아크 교체."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"

# 새 P2~P5 콘텐츠 (이미지 -> 질문 -> 숫자 -> 증명)
P2_CONTENT = """<!--PARENT:I 제안개요--><div style="padding:var(--s-5) 0;text-align:center"><div class="t-overline is-accent" style="margin-bottom:var(--s-5)">IMAGE</div><div class="t-title" style="margin-bottom:var(--s-4)">대학은, <span class="is-accent">이미지</span>로 기억됩니다</div><div style="width:520px;height:1px;background:#E8E8E8;margin:0 auto var(--s-4)"></div><div class="t-subtitle w-regular" style="line-height:2.2;text-align:left;display:inline-block">동의대 <span class="is-muted">—</span> <span class="is-accent">한의대의 전통</span><br>동서대 <span class="is-muted">—</span> <span class="is-accent">영상·IT의 젊음</span><br>부경대 <span class="is-muted">—</span> <span class="is-accent">국립의 규모</span><br>신라대 <span class="is-muted">—</span> <span class="is-accent">종합대학의 안정</span></div><div style="width:520px;height:1px;background:#E8E8E8;margin:var(--s-4) auto 0"></div><div class="t-caption is-muted" style="margin-top:var(--s-3);font-style:italic">— 모두, '느낌'입니다</div></div><!--SCRIPT_START-->(표지가 뜬 상태에서, 인사 생략)<br><br>"대학은, <strong>이미지로 기억됩니다</strong><br><br>동의대는 한의대의 전통<br>동서대는 영상·IT의 젊음<br>부경대는 국립의 규모<br>신라대는 종합대학의 안정<br><br>모두 <strong>'느낌'</strong>입니다<br>손에 잡히지 않는, 감정입니다"<!--SCRIPT_END-->"""

P3_CONTENT = """<!--PARENT:I 제안개요--><div style="padding:var(--s-5) 0;text-align:center"><div class="t-overline is-accent" style="margin-bottom:var(--s-6)">QUESTION</div><div class="t-heading is-muted" style="margin-bottom:var(--s-5);font-weight:400">그렇다면 —</div><div class="t-title" style="font-size:88px;line-height:1.1;margin-bottom:var(--s-6)">영산대학교는<span class="is-accent">?</span></div><div style="width:520px;height:1px;background:#E8E8E8;margin:0 auto var(--s-3)"></div><div class="t-caption is-muted" style="font-style:italic">— 지금, 어떤 단어가 떠오르셨습니까</div></div><!--SCRIPT_START-->"그렇다면 —<br><br><strong>영산대학교는?</strong><br><br>(3초 멈춤 — 평가위원이 속으로 답을 찾는 시간)<br><br>지금, 어떤 단어가 떠오르셨습니까<br><br>떠오르지 않으셨다면, 그것이 오늘의 시작입니다<br>떠오르셨다면, 그것이 오늘의 증명입니다"<!--SCRIPT_END-->"""

P4_CONTENT = """<!--PARENT:I 제안개요--><div style="padding:var(--s-4) 0;text-align:center"><div class="t-overline is-accent" style="margin-bottom:var(--s-4)">FACT</div><div class="t-title" style="margin-bottom:var(--s-2)">영산대학교는, <span class="is-muted" style="text-decoration:line-through">이미지</span>가 아닙니다</div><div class="t-title" style="margin-bottom:var(--s-5)">영산대학교는, <span class="is-accent">숫자</span>입니다</div><div style="width:520px;height:1px;background:#E8E8E8;margin:0 auto var(--s-4)"></div><div class="t-subtitle w-regular" style="line-height:2.2;text-align:left;display:inline-block"><span class="is-accent w-bold" style="font-size:30px">96.4%</span> <span class="is-muted">—</span> 항공서비스학과 취업률<br><span class="is-accent w-bold" style="font-size:30px">55위</span> <span class="is-muted">—</span> QS 호스피탈리티 글로벌<br><span class="is-accent w-bold" style="font-size:30px">25명</span> <span class="is-muted">—</span> 호텔 총지배인 국내 최다 동문<br><span class="is-accent w-bold" style="font-size:26px">校訓</span> <span class="is-muted">—</span> 지혜로운 가치를 배우는 대학</div></div><!--SCRIPT_START-->"영산대학교는, <strong>이미지가 아닙니다</strong><br>영산대학교는, <strong>숫자</strong>입니다<br><br>항공서비스학과 취업률 <strong>96.4%</strong><br>QS 호스피탈리티 부문 <strong>글로벌 55위</strong><br>호텔 총지배인 국내 최다 동문 <strong>25명</strong><br>그리고 校訓, <strong>지혜로운 가치를 배우는 대학</strong><br><br>모두, <strong>증명 가능한 사실</strong>입니다"<!--SCRIPT_END-->"""

P5_CONTENT = """<!--PARENT:I 제안개요--><div style="padding:var(--s-5) 0;text-align:center"><div class="t-overline is-accent" style="margin-bottom:var(--s-5)">MISSION</div><div class="t-title" style="margin-bottom:var(--s-3)">사실은, <span class="is-accent">이미지보다 강합니다</span></div><div class="t-body is-muted" style="margin-bottom:var(--s-5)">— 보이지 않았을 뿐, 이미 있었습니다</div><div style="width:520px;height:1px;background:#E8E8E8;margin:0 auto var(--s-4)"></div><div class="is-muted" style="font-size:32px;line-height:1;margin-bottom:var(--s-4)">↓</div><div class="t-subtitle w-regular">이 <span class="is-accent w-bold">사실</span>을, 어떻게 <span class="is-accent w-bold">증명</span>으로 바꿀 것인가<br>— 그것이, 저희의 제안입니다</div></div><!--SCRIPT_START-->"사실은, <strong>이미지보다 강합니다</strong><br>보이지 않았을 뿐, 이미 있었습니다<br><br>이제 남은 질문은 하나입니다<br>이 <strong>사실</strong>을, 어떻게 <strong>증명</strong>으로 바꿀 것인가<br><br>그것이, 저희의 제안입니다"<!--SCRIPT_END-->"""

# 섹션 제목/태그 재정의 (P3~P5는 header 안 쓰는 구조로 갈 것)
P2_TITLE, P2_TAG = "", ""
P3_TITLE, P3_TAG = "", ""
P4_TITLE, P4_TAG = "", ""
P5_TITLE, P5_TAG = "", ""

SRC_PID = 137  # V29 원본


def main():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    try:
        # 1. V29 원본 조회
        src = conn.execute("SELECT * FROM proposals WHERE id=?", (SRC_PID,)).fetchone()
        if not src:
            raise RuntimeError(f"V29 (id={SRC_PID}) 없음")

        # 2. V30 proposal 레코드 생성
        cur = conn.execute(
            """INSERT INTO proposals
               (title, status, raw_text, rfp_summary, rfp_json, toc_json,
                selected_concept, version)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                "V30",
                src["status"],
                src["raw_text"],
                src["rfp_summary"],
                src["rfp_json"],
                src["toc_json"],
                src["selected_concept"],
                "V30",
            ),
        )
        new_pid = cur.lastrowid
        print(f"V30 proposal 생성: id={new_pid}")

        # 3. 섹션 복제
        sections = conn.execute(
            "SELECT level, title, order_idx, content, status FROM sections "
            "WHERE proposal_id=? ORDER BY order_idx",
            (SRC_PID,),
        ).fetchall()
        for s in sections:
            conn.execute(
                """INSERT INTO sections
                   (proposal_id, level, title, order_idx, content, status)
                   VALUES (?,?,?,?,?,?)""",
                (new_pid, s["level"], s["title"], s["order_idx"], s["content"], s["status"]),
            )
        print(f"섹션 복제 완료: {len(sections)}개")

        # 4. P2~P5 (order_idx 1~4) 교체
        replacements = [
            (1, P2_TITLE, P2_TAG, P2_CONTENT),
            (2, P3_TITLE, P3_TAG, P3_CONTENT),
            (3, P4_TITLE, P4_TAG, P4_CONTENT),
            (4, P5_TITLE, P5_TAG, P5_CONTENT),
        ]
        for order_idx, title, _tag, content in replacements:
            conn.execute(
                "UPDATE sections SET title=?, content=? "
                "WHERE proposal_id=? AND order_idx=?",
                (title, content, new_pid, order_idx),
            )
        print(f"P2~P5 오프닝 아크 교체 완료")

        # 5. 컨셉 복제 (concepts 테이블)
        concepts = conn.execute(
            "SELECT label, title, body FROM concepts WHERE proposal_id=?",
            (SRC_PID,),
        ).fetchall()
        for cp in concepts:
            conn.execute(
                "INSERT INTO concepts (proposal_id, label, title, body) VALUES (?,?,?,?)",
                (new_pid, cp["label"], cp["title"], cp["body"]),
            )
        if concepts:
            print(f"컨셉 복제: {len(concepts)}개")

        conn.commit()
        print(f"\n완료! V30 proposal id={new_pid}")
        print(f"PT URL: /api/proposals/{new_pid}/export-html")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
