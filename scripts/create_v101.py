# -*- coding: utf-8 -*-
"""V101 생성 -- V30(id=138) 복제 후 빌드업 재구성.

새 빌드업 (P1~P10, 시안 직전까지):
  P1  표지 (유지, 0825503)
  P2  본질 (많이 팔 것 × 각인) -- 신규
  P3  소음 진단 -- 재편
  P4  시대 선언 ('대단한 대학' 통하지 않는다) -- 신규
  P5  morph 0825503 (유지)
  P6  전략 선언 (전공 특화) -- 신규
  P7  컨셉 (증명) -- 재편
  P8  제안업체 일반 (유지)
  P9  divider (유지)
  P10 프리뷰 (3학과 테마: 산업·글로벌·총지배인) -- 신규
  P11~ 시안 (기존 V30 시안 유지)

V30 대비:
  - P2~P7 교체
  - 기존 P10~P15 (6장) 삭제
  - 기존 P16 프리뷰 → 새 P10 + 3학과 테마
  - 시안 order_idx 재번호
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
SRC_PID = 138  # V30 원본
NEW_VERSION = "V101"

# =============================================================================
# 빌드업 콘텐츠 (PARENT + HTML + SCRIPT)
# =============================================================================

P2_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-5)">THE ESSENCE</div><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-5)">광고대행사 선정의 본질은,</div><div class="t-hero" style="margin-bottom:var(--s-5);line-height:1.2">많이 팔 것 &nbsp;<span class="is-accent">×</span>&nbsp; 각인</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div class="t-subtitle w-regular" style="line-height:1.8">이 2개로만 평가받습니다<br>나머지는, <span class="is-accent w-bold">수단</span>입니다</div></div><!--SCRIPT_START-->"광고대행사 선정의 본질은 두 개로 압축됩니다.<br><br>① 얼마나 <strong>많이 팔 것이냐</strong><br>② 얼마나 <strong>각인시킬 것이냐</strong><br><br>이 2개로만 평가받습니다. 나머지는 모두 수단입니다."<!--SCRIPT_END-->"""

P3_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-4)">NOISE DIAGNOSIS</div><div class="t-heading" style="margin-bottom:var(--s-4)">모든 대학이 <span class="is-accent">같은 말</span>을 합니다</div><div style="background:#F5F5F5;border-radius:8px;padding:var(--s-5) var(--s-6);max-width:760px;margin:0 auto var(--s-4)"><div class="t-body is-ink" style="line-height:2.2;text-align:left;padding:0 var(--s-2)"><span class="is-accent" style="font-size:75%">●</span> &nbsp;글로벌 경쟁력 1위<br><span class="is-accent" style="font-size:75%">●</span> &nbsp;최고의 교수진<br><span class="is-accent" style="font-size:75%">●</span> &nbsp;미래형 인재 양성<br><span class="is-accent" style="font-size:75%">●</span> &nbsp;4차 산업혁명 선도<br><span class="is-accent" style="font-size:75%">●</span> &nbsp;국내 최고 수준 취업률</div><div class="t-caption is-muted" style="margin-top:var(--s-3);padding-top:var(--s-2);border-top:1px solid #E0E0E0;font-style:italic">어느 대학인지 맞추실 수 있으십니까?</div></div><div class="t-caption is-muted" style="font-style:italic">정보 나열은 광고가 아닙니다. <span class="is-accent w-bold">소음입니다.</span></div></div><!--SCRIPT_START-->"모든 대학이 <strong>같은 말</strong>을 합니다.<br><br>글로벌 경쟁력 1위, 최고의 교수진, 미래형 인재 양성, 4차 산업혁명 선도, 국내 최고 수준 취업률 —<br><br>이 카피가 어느 대학의 것인지, <strong>맞추실 수 있으십니까?</strong><br><br>정보 나열은 광고가 아닙니다. <strong>소음</strong>입니다."<!--SCRIPT_END-->"""

P4_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-4) 0"><div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-4)">ERA SHIFT</div><div class="t-headline" style="margin-bottom:var(--s-4);line-height:1.3">'<span class="is-muted">대단한 대학</span>'은 이제 통하지 않습니다</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-4)"></div><div class="t-subtitle w-regular is-muted" style="line-height:1.8;margin-bottom:var(--s-4)">'세계 최상위' '국내 최고' —<br>사람들은 더 이상 놀라지 않습니다</div><div class="t-subtitle w-regular" style="margin-bottom:var(--s-5)">반응하는 건 딱 하나 —<br><span class="is-accent w-bold" style="font-size:130%">"이미 뭘 하고 있지?"</span></div><div class="t-caption is-muted" style="line-height:1.9;font-style:italic;max-width:760px">'대단한 대학'처럼 말할수록 <span class="is-ink">약해지고</span>,<br>'<span class="is-accent w-bold">이미 움직이고 있는 대학</span>'처럼 보일수록 강해집니다</div></div><!--SCRIPT_START-->"'대단한 대학'은 이제 통하지 않습니다.<br><br>'세계 최상위' '국내 최고' — 그런 외침이 쏟아질수록, 사람들은 더 이상 놀라지 않습니다.<br><br>지금 반응하는 건 딱 하나. <strong>'이미 뭘 하고 있지?'</strong><br><br>대학도 이제, '대단한 대학'처럼 말할수록 약해지고, <strong>'이미 움직이고 있는 대학'</strong>처럼 보일수록 강해집니다.<br><br>그러면 — 영산대는, 이미 뭘 하고 있을까요?"<!--SCRIPT_END-->"""

P6_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-4) 0"><div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-3)">STRATEGY</div><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-3)">그래서 우리의 전략은 하나 —</div><div class="t-hero" style="margin-bottom:var(--s-5)">전공 특화</div><div style="display:grid;grid-template-columns:1fr auto 1fr;gap:var(--s-3) var(--s-4);max-width:960px;width:100%;align-items:center;margin-bottom:var(--s-4)"><div style="text-align:right;font-size:18px;color:#A0A0A5;line-height:1.4">전체 대학 브랜드</div><div style="font-size:28px;color:#E84E10;font-weight:700">→</div><div style="text-align:left;font-size:20px;color:#1A1A1A;font-weight:700;line-height:1.4">전공 특화 브랜드</div><div style="text-align:right;font-size:18px;color:#A0A0A5;line-height:1.4">'세계 최상위' 외침</div><div style="font-size:28px;color:#E84E10;font-weight:700">→</div><div style="text-align:left;font-size:20px;color:#1A1A1A;font-weight:700;line-height:1.4">'이미 움직이는' 증거</div><div style="text-align:right;font-size:18px;color:#A0A0A5;line-height:1.4">네임밸류</div><div style="font-size:28px;color:#E84E10;font-weight:700">→</div><div style="text-align:left;font-size:20px;color:#1A1A1A;font-weight:700;line-height:1.4">움직임</div></div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-3)"></div><div class="t-caption is-muted" style="font-style:italic">같은 대학을, <span class="is-ink w-bold">다른 프레임</span>에 &nbsp;(= 리프레이밍)</div></div><!--SCRIPT_START-->"숫자들은 이미 단단합니다.<br>하지만 이 숫자들을 묶어 <strong>'세계 최상위 대학'</strong>으로 외치는 순간, 다시 소음이 됩니다.<br><br>그래서 우리의 전략은 하나 — <strong>전공 특화</strong>입니다.<br><br>전체 대학 브랜드가 아니라, 이미 세계가 주목하는 <strong>'전공'</strong>에서, 이미 움직이고 있는 <strong>'증거'</strong>로 말합니다.<br><br>같은 대학을, 다른 프레임에 — 이것이 <strong>리프레이밍</strong>입니다."<!--SCRIPT_END-->"""

P7_CONTENT = """<!--PARENT:I 제안개요--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-4)">CONCEPT</div><div class="t-subtitle w-regular is-muted" style="margin-bottom:var(--s-4);line-height:1.6">이 '전공 특화' 증거를, 기억에 박히게 —</div><div class="t-hero" style="margin-bottom:var(--s-4)">증명</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div class="t-subtitle w-regular" style="line-height:1.8">주장이 아닌, <span class="is-accent w-bold">숫자</span>가 기억에 박히는 일<br>이 <span class="is-accent w-bold">증명</span>이, 저희 광고의 컨셉입니다</div></div><!--SCRIPT_START-->"이 '전공 특화' 증거를, 기억에 박히게 하는 일 — 그것이 한 단어로 <strong>증명</strong>입니다.<br><br>주장이 아닌, <strong>숫자가 기억에 박히는 일</strong>.<br><br>이 <strong>증명</strong>이, 저희 광고의 컨셉입니다."<!--SCRIPT_END-->"""

P10_PREVIEW_CONTENT = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:프리뷰--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-4) 0"><div class="t-heading" style="margin-bottom:var(--s-2)">3가지 <span class="is-accent">증명</span></div><div class="t-body is-muted" style="margin-bottom:var(--s-4)">소음을, <span class="is-ink w-bold">증명</span>으로 바꾸는 일</div><div style="display:grid;grid-template-columns:auto auto 60px 1fr;align-items:center;max-width:1200px;margin:0 auto;gap:var(--s-3) var(--s-3);text-align:left"><div class="fx-stagger-1" style="font-size:13px;color:#C5C5C9;font-weight:700;letter-spacing:1px">01</div><div class="fx-stagger-1" style="font-size:18px;color:#A0A0A5;line-height:1.4;white-space:nowrap">지역대학</div><div class="fx-stagger-1" style="font-size:32px;font-weight:700;color:#E84E10;line-height:1;text-align:center">→</div><div class="fx-stagger-1"><div class="fx-pop-1" style="font-size:30px;font-weight:700;color:#E84E10;line-height:1.3;letter-spacing:-0.5px">산업이 선택하는 대학</div><div style="font-size:13px;color:#6E6E73;margin-top:4px">총지배인 25명 · 승무원 동남권 최다 · 셰프 오브 더 셰프 4명</div></div><div style="grid-column:1/-1;height:1px;background:#E8E8E8;margin:var(--s-1) 0"></div><div class="fx-stagger-2" style="font-size:13px;color:#C5C5C9;font-weight:700;letter-spacing:1px">02</div><div class="fx-stagger-2" style="font-size:18px;color:#A0A0A5;line-height:1.4;white-space:nowrap">네임밸류</div><div class="fx-stagger-2" style="font-size:32px;font-weight:700;color:#E84E10;line-height:1;text-align:center">→</div><div class="fx-stagger-2"><div class="fx-pop-2" style="font-size:30px;font-weight:700;color:#E84E10;line-height:1.3;letter-spacing:-0.5px">글로벌이 증명하는 대학</div><div style="font-size:13px;color:#6E6E73;margin-top:4px">QS 호스피탈리티 55위 · 연구력 세계 8위 · 세종·경희 Top 3</div></div><div style="grid-column:1/-1;height:1px;background:#E8E8E8;margin:var(--s-1) 0"></div><div class="fx-stagger-3" style="font-size:13px;color:#C5C5C9;font-weight:700;letter-spacing:1px">03</div><div class="fx-stagger-3" style="font-size:18px;color:#A0A0A5;line-height:1.4;white-space:nowrap">숫자 25</div><div class="fx-stagger-3" style="font-size:32px;font-weight:700;color:#E84E10;line-height:1;text-align:center">→</div><div class="fx-stagger-3"><div class="fx-pop-3" style="font-size:30px;font-weight:700;color:#E84E10;line-height:1.3;letter-spacing:-0.5px">25개 호텔의 꼭대기</div><div style="font-size:13px;color:#6E6E73;margin-top:4px">호텔 총지배인 25명 배출</div></div></div></div><!--SCRIPT_START-->"저희가 보여드릴 <strong>3가지 증명</strong>입니다.<br><br>첫째, 지역대학이 아니라 <strong>산업이 선택하는 대학</strong>.<br>둘째, 네임밸류가 아니라 <strong>글로벌이 증명하는 대학</strong>.<br>셋째, 숫자 25가 아니라 <strong>25개 호텔의 꼭대기</strong>.<br><br>지금부터, 각 시안으로 보여드리겠습니다."<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    try:
        # 1. V30 원본 조회
        src = conn.execute("SELECT * FROM proposals WHERE id=?", (SRC_PID,)).fetchone()
        if not src:
            raise RuntimeError(f"V30 (id={SRC_PID}) 없음")

        # 2. V101 proposal 레코드 생성
        cur = conn.execute(
            """INSERT INTO proposals
               (title, status, raw_text, rfp_summary, rfp_json, toc_json,
                selected_concept, version)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                NEW_VERSION,
                src["status"],
                src["raw_text"],
                src["rfp_summary"],
                src["rfp_json"],
                src["toc_json"],
                src["selected_concept"],
                NEW_VERSION,
            ),
        )
        new_pid = cur.lastrowid
        print(f"{NEW_VERSION} proposal 생성: id={new_pid}")

        # 3. V30 섹션 전체 복제
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
        print(f"섹션 복제: {len(sections)}개")

        # 4. 빌드업 P2~P7 교체 (order_idx 1~6)
        # P5 (morph, order_idx 4)는 유지
        build_updates = [
            (1, "본질", P2_CONTENT),
            (2, "소음 진단", P3_CONTENT),
            (3, "시대 선언", P4_CONTENT),
            (5, "전략 선언", P6_CONTENT),
            (6, "컨셉", P7_CONTENT),
        ]
        for order_idx, title, content in build_updates:
            conn.execute(
                "UPDATE sections SET title=?, content=? "
                "WHERE proposal_id=? AND order_idx=?",
                (title, content, new_pid, order_idx),
            )
        print(f"빌드업 P2~P7 교체 (P5 morph 유지)")

        # 5. 기존 P10~P15 삭제 (order_idx 9~14)
        deleted = conn.execute(
            "DELETE FROM sections WHERE proposal_id=? AND order_idx BETWEEN 9 AND 14",
            (new_pid,),
        ).rowcount
        print(f"기존 P10~P15 삭제: {deleted}개")

        # 6. 기존 P16 프리뷰 (order_idx 15) → 새 P10 + 3학과 테마
        conn.execute(
            "UPDATE sections SET title=?, content=? "
            "WHERE proposal_id=? AND order_idx=?",
            ("대학 광고에 필요한 소재 발굴 및 콘텐츠 기획", P10_PREVIEW_CONTENT, new_pid, 15),
        )
        print(f"P16 프리뷰 → 새 P10 (3학과 테마)")

        # 7. order_idx 재번호 (15 → 9, 16+ → 10+)
        # 프리뷰부터 시안 끝까지 -6 시프트
        conn.execute(
            "UPDATE sections SET order_idx = order_idx - 6 "
            "WHERE proposal_id=? AND order_idx >= 15",
            (new_pid,),
        )
        print(f"order_idx 재번호 (15+ → 9+)")

        # 8. 컨셉 복제
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

        # 9. 결과 확인
        final_sections = conn.execute(
            "SELECT order_idx, title FROM sections WHERE proposal_id=? ORDER BY order_idx",
            (new_pid,),
        ).fetchall()
        print(f"\n=== {NEW_VERSION} 최종 섹션 ({len(final_sections)}개) ===")
        for s in final_sections[:12]:
            print(f"  idx={s['order_idx']:2d} | {s['title']}")
        if len(final_sections) > 12:
            print(f"  ... (+{len(final_sections)-12}개 시안)")

        print(f"\n완료! {NEW_VERSION} proposal id={new_pid}")
        print(f"PT URL: http://localhost:8881/api/proposals/{new_pid}/export-html")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
