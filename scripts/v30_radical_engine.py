# -*- coding: utf-8 -*-
"""V41~V50: 완전히 참신한 방향 — 각 버전이 독립적 컨셉 재해석."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
V30_ID = 138  # V30을 base로 각 방향성 독립 실험


def clone_from(src_id: int, title: str, version: str) -> int:
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    try:
        src = conn.execute("SELECT * FROM proposals WHERE id=?", (src_id,)).fetchone()
        cur = conn.execute(
            """INSERT INTO proposals (title,status,raw_text,rfp_summary,rfp_json,toc_json,selected_concept,version)
               VALUES (?,?,?,?,?,?,?,?)""",
            (title, src["status"], src["raw_text"], src["rfp_summary"], src["rfp_json"],
             src["toc_json"], src["selected_concept"], version),
        )
        new_id = cur.lastrowid
        sections = conn.execute(
            "SELECT level,title,order_idx,content,status FROM sections WHERE proposal_id=? ORDER BY order_idx",
            (src_id,),
        ).fetchall()
        for s in sections:
            conn.execute(
                "INSERT INTO sections (proposal_id,level,title,order_idx,content,status) VALUES (?,?,?,?,?,?)",
                (new_id, s["level"], s["title"], s["order_idx"], s["content"], s["status"]),
            )
        concepts = conn.execute(
            "SELECT label,title,body FROM concepts WHERE proposal_id=?", (src_id,)
        ).fetchall()
        for cp in concepts:
            conn.execute(
                "INSERT INTO concepts (proposal_id,label,title,body) VALUES (?,?,?,?)",
                (new_id, cp["label"], cp["title"], cp["body"]),
            )
        conn.commit()
        print(f"  -> {title} 생성 (id={new_id})")
        return new_id
    finally:
        conn.close()


def transform_all_sections(pid: int, transform):
    """모든 section content에 transform 함수 적용."""
    conn = sqlite3.connect(str(DB))
    try:
        rows = conn.execute(
            "SELECT id,content FROM sections WHERE proposal_id=?", (pid,)
        ).fetchall()
        for sid, body in rows:
            if not body:
                continue
            new = transform(body)
            if new != body:
                conn.execute("UPDATE sections SET content=? WHERE id=?", (new, sid))
        conn.commit()
    finally:
        conn.close()


def update_section(pid: int, order: int, transform):
    conn = sqlite3.connect(str(DB))
    try:
        r = conn.execute(
            "SELECT id,content FROM sections WHERE proposal_id=? AND order_idx=?",
            (pid, order),
        ).fetchone()
        if r:
            new = transform(r[1])
            if new != r[1]:
                conn.execute("UPDATE sections SET content=? WHERE id=?", (new, r[0]))
        conn.commit()
    finally:
        conn.close()


# ============================================================
# V41: 모노크롬 — accent color 제거, 순수 흑백
# ============================================================
def v41(pid: int):
    """V41: Monochrome — #E84E10 → #1A1A1A 통일, 흑백 미학."""
    def fn(body):
        body = body.replace('#E84E10', '#1A1A1A')
        body = body.replace('#FFF5F0', '#F5F5F5')  # 오렌지 계열 배경 회색
        body = body.replace('#FFD9C0', '#DEDEDE')
        body = body.replace('#FAA478', '#777777')
        body = body.replace('#FFF0E6', '#FAFAFA')
        return body
    transform_all_sections(pid, fn)


# ============================================================
# V42: 풀 페이지 큰 타이포 — 모든 제목 150px+
# ============================================================
def v42(pid: int):
    """V42: Poster-style — 제목 전부 initial 150~200px."""
    def fn(body):
        body = body.replace('class="t-title"', 'class="t-title" data-poster')
        body = body.replace('class="t-heading"', 'class="t-heading" data-poster')
        # 인라인으로 크기 override
        body = body.replace(
            'class="t-title" data-poster',
            'class="t-title" style="font-size:88px !important"',
        )
        body = body.replace(
            'class="t-heading" data-poster',
            'class="t-heading" style="font-size:68px !important"',
        )
        return body
    transform_all_sections(pid, fn)


# ============================================================
# V43: 영문 Hybrid — 주요 구간에 영문 부제 덧대기
# ============================================================
def v43(pid: int):
    """V43: KR/EN Hybrid — 타이틀에 영문 overline 자동 삽입."""
    def fn(body):
        body = body.replace(
            '>영산대학교는, <span class="is-accent">숫자</span>입니다</div>',
            '><span style="display:block;font-size:13px;letter-spacing:4px;color:#6E6E73;margin-bottom:10px">YOUNGSAN IS NUMBERS</span>영산대학교는, <span class="is-accent">숫자</span>입니다</div>',
        )
        body = body.replace(
            '>리프레이밍</div>',
            '><span style="display:block;font-size:13px;letter-spacing:4px;color:#6E6E73;margin-bottom:10px">RE-FRAMING</span>리프레이밍</div>',
        )
        body = body.replace(
            '>증명</div>',
            '><span style="display:block;font-size:13px;letter-spacing:4px;color:#6E6E73;margin-bottom:10px">EVIDENCE</span>증명</div>',
        )
        return body
    transform_all_sections(pid, fn)


# ============================================================
# V44: 슬로건 변주 — "숫자로 말합니다"
# ============================================================
def v44(pid: int):
    """V44: 슬로건 변주 — '지혜로 증명' → '숫자로 말합니다'."""
    def fn(body):
        body = body.replace(
            '<span class="is-accent fx-zihye-punch">지혜</span>로 증명합니다',
            '<span class="is-accent fx-zihye-punch">숫자</span>로 말합니다',
        )
        body = body.replace(
            '지혜로 증명합니다',
            '숫자로 말합니다',
        )
        body = body.replace(
            '영산대학교는, <span style="color:#E84E10">지혜</span>로 증명합니다',
            '영산대학교는, <span style="color:#E84E10">숫자</span>로 말합니다',
        )
        return body
    transform_all_sections(pid, fn)


# ============================================================
# V45: 세리프 하이브리드 — 영문 타이포에 Noto Serif 혼용
# ============================================================
def v45(pid: int):
    """V45: Editorial — 제목 폰트 Serif로 변경 (inline style)."""
    def fn(body):
        body = body.replace(
            'class="t-hero"',
            'class="t-hero" style="font-family:\'Noto Serif KR\',\'Georgia\',serif"',
        )
        body = body.replace(
            'class="t-headline"',
            'class="t-headline" style="font-family:\'Noto Serif KR\',\'Georgia\',serif"',
        )
        return body
    transform_all_sections(pid, fn)


# ============================================================
# V46: 해체 — 모든 슬라이드를 왼쪽 정렬, 비대칭
# ============================================================
def v46(pid: int):
    """V46: Asymmetric — text-align center → left, 비대칭 에디토리얼."""
    def fn(body):
        body = body.replace(';text-align:center;padding:', ';text-align:left;padding:')
        body = body.replace('margin:0 auto var(--s-4)', 'margin:var(--s-2) 0 var(--s-4) 0')
        body = body.replace('margin:0 auto var(--s-5)', 'margin:var(--s-2) 0 var(--s-5) 0')
        return body
    transform_all_sections(pid, fn)


# ============================================================
# V47: 다크 모드 — 배경 반전
# ============================================================
def v47(pid: int):
    """V47: Dark mode — 각 슬라이드 content에 dark background inline 주입."""
    def fn(body):
        # 외곽 wrapper에 dark style 추가
        body = body.replace(
            '<!--PARENT:',
            '<div style="background:#0A0A0A;color:#F5F5F5;width:100%;height:100%;min-height:100%"><!--PARENT:',
            1,
        )
        # 닫는 태그 추가 (모든 경우를 잡기 어려우므로 skip — snapshot 형태로만)
        body = body.replace('color:#1A1A1A', 'color:#F5F5F5')
        body = body.replace('color:#2D2D2D', 'color:#E5E5E5')
        body = body.replace('color:#58595B', 'color:#BDBDBD')
        body = body.replace('color:#6E6E73', 'color:#8E8E93')
        body = body.replace('background:#fff', 'background:#0A0A0A')
        body = body.replace('background:#F5F5F5', 'background:#1A1A1A')
        body = body.replace('background:#F9F9F9', 'background:#151515')
        return body
    transform_all_sections(pid, fn)


# ============================================================
# V48: 질문 중심 — 모든 헤더 앞에 "?"
# ============================================================
def v48(pid: int):
    """V48: Question-driven — 주요 블록 앞에 질문 형식 태그 추가."""
    def fn(body):
        body = body.replace(
            '<div class="t-heading"',
            '<div style="font-size:16px;color:#E84E10;letter-spacing:3px;margin-bottom:10px;font-weight:700">QUESTION</div><div class="t-heading"',
        )
        return body
    transform_all_sections(pid, fn)


# ============================================================
# V49: 1-column 가이드북 — 각 슬라이드를 에디토리얼 페이지처럼
# ============================================================
def v49(pid: int):
    """V49: Editorial guidebook — 본문에 column-count 스타일 유사 처리 어려움 → padding 확대로 책 느낌."""
    def fn(body):
        body = body.replace(
            'padding:var(--s-5) 0',
            'padding:var(--s-5) var(--s-6)',
        )
        body = body.replace(
            'padding:var(--s-4) 0',
            'padding:var(--s-4) var(--s-6)',
        )
        return body
    transform_all_sections(pid, fn)


# ============================================================
# V50: 최소주의 manifesto — 대부분 카피를 1~2 줄로 압축
# ============================================================
def v50(pid: int):
    """V50: Minimalist manifesto — t-caption/subtitle 보조 문구 숨김 (opacity 0.3)."""
    def fn(body):
        body = body.replace(
            'class="t-caption is-muted"',
            'class="t-caption is-muted" style="opacity:0.3"',
        )
        body = body.replace(
            'class="t-subtitle w-regular is-muted"',
            'class="t-subtitle w-regular is-muted" style="opacity:0.45"',
        )
        return body
    transform_all_sections(pid, fn)


# ============================================================
# 실행
# ============================================================
radicals = [
    ("V41", "Monochrome — accent 제거, 흑백 미학", v41),
    ("V42", "Poster — 모든 제목 대형 타이포", v42),
    ("V43", "KR/EN Hybrid — 영문 overline 덧댐", v43),
    ("V44", "슬로건 변주 — '지혜'→'숫자'로 말합니다", v44),
    ("V45", "Editorial Serif — 제목 세리프 폰트", v45),
    ("V46", "Asymmetric — 왼쪽 정렬, 비대칭", v46),
    ("V47", "Dark mode — 검정 배경 반전", v47),
    ("V48", "Question-driven — 각 헤더에 QUESTION 태그", v48),
    ("V49", "Editorial guidebook — 여백 확대", v49),
    ("V50", "Minimalist manifesto — 보조 카피 흐림 처리", v50),
]


def main():
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    for ver, desc, fn in radicals:
        print(f"[{ver}] {desc}")
        new_id = clone_from(V30_ID, ver, ver)
        fn(new_id)
    print(f"\n완료: V41~V50 10개 참신 버전 생성 (모두 V30 base)")


if __name__ == "__main__":
    main()
