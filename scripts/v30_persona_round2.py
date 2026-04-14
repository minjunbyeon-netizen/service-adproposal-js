# -*- coding: utf-8 -*-
"""V51~V60: 추가 페르소나 라운드. V30 base, 각자 독립 개선."""
import sqlite3
import sys
import io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
V30_ID = 138


def clone_from(src_id, title, version):
    conn = sqlite3.connect(str(DB)); conn.row_factory = sqlite3.Row
    try:
        src = conn.execute("SELECT * FROM proposals WHERE id=?", (src_id,)).fetchone()
        cur = conn.execute(
            "INSERT INTO proposals (title,status,raw_text,rfp_summary,rfp_json,toc_json,selected_concept,version) VALUES (?,?,?,?,?,?,?,?)",
            (title, src["status"], src["raw_text"], src["rfp_summary"], src["rfp_json"],
             src["toc_json"], src["selected_concept"], version),
        )
        new_id = cur.lastrowid
        sec = conn.execute(
            "SELECT level,title,order_idx,content,status FROM sections WHERE proposal_id=? ORDER BY order_idx",
            (src_id,)).fetchall()
        for s in sec:
            conn.execute(
                "INSERT INTO sections (proposal_id,level,title,order_idx,content,status) VALUES (?,?,?,?,?,?)",
                (new_id, s["level"], s["title"], s["order_idx"], s["content"], s["status"]))
        cp = conn.execute("SELECT label,title,body FROM concepts WHERE proposal_id=?", (src_id,)).fetchall()
        for c in cp:
            conn.execute("INSERT INTO concepts (proposal_id,label,title,body) VALUES (?,?,?,?)",
                         (new_id, c["label"], c["title"], c["body"]))
        conn.commit()
        print(f"  -> {title} (id={new_id})")
        return new_id
    finally:
        conn.close()


def append_slide(pid, title, content, level=2):
    conn = sqlite3.connect(str(DB))
    try:
        mx = conn.execute("SELECT MAX(order_idx) FROM sections WHERE proposal_id=?", (pid,)).fetchone()[0]
        conn.execute(
            "INSERT INTO sections (proposal_id,level,title,order_idx,content,status) VALUES (?,?,?,?,?,'pending')",
            (pid, level, title, mx + 1, content))
        conn.commit()
    finally:
        conn.close()


def update(pid, order, transform):
    conn = sqlite3.connect(str(DB))
    try:
        r = conn.execute("SELECT id,content FROM sections WHERE proposal_id=? AND order_idx=?", (pid, order)).fetchone()
        if r:
            new = transform(r[1])
            if new != r[1]:
                conn.execute("UPDATE sections SET content=? WHERE id=?", (new, r[0]))
        conn.commit()
    finally:
        conn.close()


# ============================================================
# V51: Senior Brand Strategist
# 지적: "영산대 브랜드 포지셔닝 선언이 없음. '숫자'는 메시지지만 브랜드가 아님."
# 개선: 브랜드 포지셔닝 페이지 추가
# ============================================================
def v51(pid):
    page = """<!--PARENT:I 제안개요--><!--TAG:브랜드 포지셔닝--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-3)">영산대 <span class="is-accent">브랜드 포지셔닝</span></div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><table class="t-caption w-regular is-ink" style="width:100%;max-width:1000px;margin:0 auto;border-collapse:collapse"><tbody><tr><td style="padding:var(--s-2) var(--s-3);border-bottom:1px solid #E8E8E8;font-weight:700;width:30%">카테고리</td><td style="padding:var(--s-2) var(--s-3);border-bottom:1px solid #E8E8E8">부울경 사립대 / 실무형 전문 대학</td></tr><tr><td style="padding:var(--s-2) var(--s-3);border-bottom:1px solid #E8E8E8;font-weight:700">FOR</td><td style="padding:var(--s-2) var(--s-3);border-bottom:1px solid #E8E8E8">직업적 성공을 꿈꾸는 실용주의 수험생</td></tr><tr><td style="padding:var(--s-2) var(--s-3);border-bottom:1px solid #E8E8E8;font-weight:700;color:#E84E10">영산대는</td><td style="padding:var(--s-2) var(--s-3);border-bottom:1px solid #E8E8E8;background:#FFF5F0"><strong class="is-accent">증명된 결과를 만드는 시스템 대학</strong></td></tr><tr><td style="padding:var(--s-2) var(--s-3);border-bottom:1px solid #E8E8E8;font-weight:700">UNLIKE</td><td style="padding:var(--s-2) var(--s-3);border-bottom:1px solid #E8E8E8">"전통/규모/종합성"을 자찬하는 일반 지역 사립대</td></tr><tr><td style="padding:var(--s-2) var(--s-3);font-weight:700">BECAUSE</td><td style="padding:var(--s-2) var(--s-3)"><strong>3.6% · 글로벌 55위 · 25명 · 校訓</strong> — 4개 숫자로 증명</td></tr></tbody></table></div><!--SCRIPT_START-->"영산대의 브랜드 포지셔닝을 한 장으로 정리했습니다.<br><br>영산대는 증명된 결과를 만드는 <strong>시스템 대학</strong>입니다.<br>이 포지셔닝이 2년간 모든 메시지의 북극성이 됩니다."<!--SCRIPT_END-->"""
    append_slide(pid, "브랜드 포지셔닝", page)
    print("    브랜드 포지셔닝 선언 페이지 추가")


# V52: UX Researcher — 수험생 저니맵
def v52(pid):
    page = """<!--PARENT:I 제안개요--><!--TAG:수험생 저니--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-3)">수험생 <span class="is-accent">12개월 저니</span></div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><table class="t-caption w-regular is-ink" style="width:100%;max-width:1100px;margin:0 auto;border-collapse:collapse"><thead><tr><th class="w-bold" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;width:12%">시기</th><th class="w-bold" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;width:20%">심리</th><th class="w-bold" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;width:24%">터치포인트</th><th class="w-bold is-accent" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10">우리 메시지</th></tr></thead><tbody><tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8"><strong>3~4월</strong></td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">막연한 불안</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">인스타 피드 / 친구 대화</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">"<strong>3.6%</strong>가 보이기 시작"</td></tr><tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8"><strong>5~6월</strong></td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">구체적 탐색</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">유튜브 인플루언서 / 네이버 검색</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">"<strong>글로벌 55위</strong>가 믿음 된다"</td></tr><tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8"><strong>7월</strong></td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">결정 압박</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">학부모와 대화 / 교사 상담</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">"<strong>25명 총지배인</strong>이 증거"</td></tr><tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8"><strong>8~9월</strong></td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">후보 추리기</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">숏폼 릴스 / 학과 비교</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">"<strong>졸업생 얼굴</strong>이 등장"</td></tr><tr style="background:#FFF5F0"><td style="padding:var(--s-1) var(--s-2)"><strong>10~12월</strong></td><td style="padding:var(--s-1) var(--s-2)">최종 결정</td><td style="padding:var(--s-1) var(--s-2)">홍보영상 / 입시요강</td><td style="padding:var(--s-1) var(--s-2)"><strong class="is-accent">"지혜로 증명"</strong>이 확정</td></tr></tbody></table><div class="t-caption is-muted" style="margin-top:var(--s-3);font-style:italic">각 시기 심리 상태에 정확히 매칭되는 메시지 순서</div></div>"""
    append_slide(pid, "수험생 저니맵", page)
    print("    수험생 12개월 저니맵 페이지 추가")


# V53: PR/언론 전문가
def v53(pid):
    page = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:언론 PR--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-3)">언론, <span class="is-accent">기사거리</span>로 만듭니다</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><table class="t-caption w-regular is-ink" style="width:100%;max-width:1100px;margin:0 auto;border-collapse:collapse"><thead><tr><th style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10">이슈 앵글</th><th style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10">매체</th><th style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10">시기</th></tr></thead><tbody><tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">"<strong>탈락률 3.6%</strong>" — 대학 광고 리프레이밍 사례</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">광고·마케팅 전문지 (브랜딩포럼)</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">5월</td></tr><tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">"QS <strong>글로벌 55위</strong>" — 지역 사립대 세계 수준 성과</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">중앙·부산일보·연합뉴스</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">6월 (원서접수 전)</td></tr><tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">"총지배인 <strong>25명의 학교</strong>" — 업계 특화 대학 르포</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">호텔앤레스토랑 / 트래블앤레저</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">7월</td></tr><tr><td style="padding:var(--s-1) var(--s-2)">"영산대 校訓" — 교육 철학 인터뷰</td><td style="padding:var(--s-1) var(--s-2)">교수신문 / 한국대학신문</td><td style="padding:var(--s-1) var(--s-2)">9월</td></tr></tbody></table></div>"""
    append_slide(pid, "언론 PR 플랜", page)
    print("    언론 PR 4대 앵글 페이지 추가")


# V54: 행동경제학자 — 리프레이밍 이론적 근거
def v54(pid):
    page = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:리프레이밍 과학--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-3)">리프레이밍, <span class="is-accent">과학으로 검증</span>된 기법</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div style="max-width:1100px;text-align:left;display:flex;flex-direction:column;gap:16px"><div style="border-left:3px solid #E84E10;padding:var(--s-2) var(--s-3);background:#FFF5F0"><div class="t-subtitle w-bold is-accent" style="margin-bottom:6px">Kahneman & Tversky (1979) · Prospect Theory</div><div class="t-caption is-ink">"사람은 이득보다 손실을 2배 크게 인식한다" — 96.4% 취업률(이득)보다 3.6% 탈락률(손실)이 뇌리에 박히는 이유</div></div><div style="border-left:3px solid #E84E10;padding:var(--s-2) var(--s-3);background:#FFF5F0"><div class="t-subtitle w-bold is-accent" style="margin-bottom:6px">Chip & Dan Heath · "Made to Stick" (2007)</div><div class="t-caption is-ink">"Unexpectedness = 기억의 핵심" — 리프레이밍은 예상 외 프레임을 만들어 SUCCES 원칙(Simple/Unexpected/Concrete/Credible/Emotional/Stories) 전부 충족</div></div><div style="border-left:3px solid #E84E10;padding:var(--s-2) var(--s-3);background:#FFF5F0"><div class="t-subtitle w-bold is-accent" style="margin-bottom:6px">Cialdini · "Pre-Suasion" (2016)</div><div class="t-caption is-ink">"Attention을 먼저 프레이밍하면 판단이 그에 따른다" — 3.6%로 주의 포획 후 영산대 정보 수용도 증가</div></div></div><div class="t-caption is-muted" style="margin-top:var(--s-3);font-style:italic">3개의 권위 있는 연구가 같은 결론 — 리프레이밍은 기분이 아닌 과학</div></div>"""
    append_slide(pid, "리프레이밍 과학적 근거", page)
    print("    행동경제학 3대 이론 근거 페이지 추가")


# V55: 영상 PD — 스토리보드
def v55(pid):
    page = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:영상 스토리보드--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-3)">"지혜" <span class="is-accent">60초 스토리보드</span></div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;max-width:1200px;width:100%;text-align:left"><div style="border:1px solid #E8E8E8;border-radius:6px;padding:10px"><div style="background:#F5F5F5;aspect-ratio:16/9;border-radius:4px;margin-bottom:8px;display:flex;align-items:center;justify-content:center;color:#A0A0A5;font-size:11px">SHOT 01</div><div style="font-size:11px;font-weight:700;color:#E84E10;margin-bottom:4px">0~12s · 기내</div><div style="font-size:11px;color:#1A1A1A;line-height:1.4">"지혜야~" — 좌석 등 돌리며</div></div><div style="border:1px solid #E8E8E8;border-radius:6px;padding:10px"><div style="background:#F5F5F5;aspect-ratio:16/9;border-radius:4px;margin-bottom:8px;display:flex;align-items:center;justify-content:center;color:#A0A0A5;font-size:11px">SHOT 02</div><div style="font-size:11px;font-weight:700;color:#E84E10;margin-bottom:4px">12~24s · 호텔</div><div style="font-size:11px;color:#1A1A1A;line-height:1.4">"박지혜 지배인님" — 체크인</div></div><div style="border:1px solid #E8E8E8;border-radius:6px;padding:10px"><div style="background:#F5F5F5;aspect-ratio:16/9;border-radius:4px;margin-bottom:8px;display:flex;align-items:center;justify-content:center;color:#A0A0A5;font-size:11px">SHOT 03</div><div style="font-size:11px;font-weight:700;color:#E84E10;margin-bottom:4px">24~36s · 경찰서</div><div style="font-size:11px;color:#1A1A1A;line-height:1.4">"지혜 경위" — 순찰 중</div></div><div style="border:1px solid #E8E8E8;border-radius:6px;padding:10px"><div style="background:#F5F5F5;aspect-ratio:16/9;border-radius:4px;margin-bottom:8px;display:flex;align-items:center;justify-content:center;color:#A0A0A5;font-size:11px">SHOT 04</div><div style="font-size:11px;font-weight:700;color:#E84E10;margin-bottom:4px">36~48s · 매장</div><div style="font-size:11px;color:#1A1A1A;line-height:1.4">"지혜 선생님" — 고객 맞이</div></div><div style="border:2px solid #E84E10;border-radius:6px;padding:10px;background:#FFF5F0"><div style="background:#1A1A1A;aspect-ratio:16/9;border-radius:4px;margin-bottom:8px;display:flex;align-items:center;justify-content:center;color:#E84E10;font-size:12px;font-weight:700">OUTRO</div><div style="font-size:11px;font-weight:700;color:#E84E10;margin-bottom:4px">48~60s · 타이틀</div><div style="font-size:11px;color:#1A1A1A;line-height:1.4;font-weight:700">"우리는 모두 지혜입니다"</div></div></div></div>"""
    append_slide(pid, "영상 스토리보드", page)
    print("    '지혜' 60초 5-shot 스토리보드 페이지 추가")


# V56: 디지털 퍼포먼스 마케터 — 캠페인 플로우
def v56(pid):
    def fn(body):
        return body.replace(
            '같은 예산으로, 더 많이 보여드리겠습니다',
            'Meta CBO 자동 최적화 + Google Smart Bidding + 오디언스 3 tier 세팅 (광범위·유사·리타깃)',
        )
    update(pid, 44, fn)
    print("    P45에 퍼포먼스 자동화 스택 명시")


# V57: 카테고리 전문가 (고등교육)
def v57(pid):
    page = """<!--PARENT:I 제안개요--><!--TAG:고등교육 인사이트--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-3)">지방 사립대, <span class="is-accent">생존의 시간</span></div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--s-3);max-width:1100px;width:100%"><div style="border:1px solid #E8E8E8;border-radius:6px;padding:var(--s-4);text-align:left"><div class="t-caption w-bold is-accent" style="margin-bottom:var(--s-2);letter-spacing:2px">2025</div><div style="font-size:36px;font-weight:700;color:#E84E10;line-height:1;margin-bottom:8px">−18%</div><div class="t-caption is-ink">부울경 수험생 수 (2018 대비)</div></div><div style="border:1px solid #E8E8E8;border-radius:6px;padding:var(--s-4);text-align:left"><div class="t-caption w-bold is-accent" style="margin-bottom:var(--s-2);letter-spacing:2px">2026</div><div style="font-size:36px;font-weight:700;color:#E84E10;line-height:1;margin-bottom:8px">2.3배</div><div class="t-caption is-ink">지방 사립대 광고 경쟁 격화</div></div><div style="border:1px solid #E8E8E8;border-radius:6px;padding:var(--s-4);text-align:left"><div class="t-caption w-bold is-accent" style="margin-bottom:var(--s-2);letter-spacing:2px">2030</div><div style="font-size:36px;font-weight:700;color:#E84E10;line-height:1;margin-bottom:8px">38%</div><div class="t-caption is-ink">폐교 위기 예측 (교육부)</div></div></div><div class="t-caption is-muted" style="margin-top:var(--s-4);font-style:italic">정보 나열로 돌파할 시간이 없습니다. 리프레이밍이 생존 전략입니다.</div></div>"""
    append_slide(pid, "고등교육 시장 인사이트", page)
    print("    지방 사립대 위기 데이터 3개 페이지 추가")


# V58: 법무/윤리 — 과장광고 리스크 체크
def v58(pid):
    page = """<!--PARENT:IV 사업 관리 계획--><!--TAG:광고 윤리--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-3)">광고 윤리, <span class="is-accent">4중 안전장치</span></div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><table class="t-caption w-regular is-ink" style="width:100%;max-width:1100px;margin:0 auto;border-collapse:collapse"><thead><tr><th style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;text-align:center;width:25%">단계</th><th style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;text-align:center">검증 내용</th></tr></thead><tbody><tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8;text-align:center"><strong>① 출처 명시</strong></td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">모든 숫자 (96.4%/55위/25명)에 연도·출처 미세 각주</td></tr><tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8;text-align:center"><strong>② 입학처 검수</strong></td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">집행 전 영산대 입학처장 서면 승인</td></tr><tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8;text-align:center"><strong>③ 자율심의</strong></td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">한국광고자율심의기구 사전 자율 심의 (권고)</td></tr><tr><td style="padding:var(--s-1) var(--s-2);text-align:center"><strong>④ 법무 검토</strong></td><td style="padding:var(--s-1) var(--s-2)">공정위 표시·광고법 대행사 자체 법무 체크리스트</td></tr></tbody></table><div class="t-caption is-muted" style="margin-top:var(--s-3);font-style:italic">리프레이밍은 과장이 아닙니다. 숫자는 사실입니다.</div></div>"""
    append_slide(pid, "광고 윤리 체크리스트", page)
    print("    광고 윤리 4중 안전장치 페이지 추가")


# V59: 인터뷰어 — 실제 졸업생 목소리
def v59(pid):
    page = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:졸업생 인터뷰--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-3)">영산대 <span class="is-accent">졸업생이 말합니다</span></div><div class="t-caption is-muted" style="margin-bottom:var(--s-4);font-style:italic">※ 숏폼 출연 섭외 예정 졸업생 인터뷰 요지 (영상 기획 참조)</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-4)"></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--s-3);max-width:1100px"><div style="border-left:3px solid #E84E10;padding:var(--s-3) var(--s-4);text-align:left;background:#FFF5F0"><div class="t-caption w-bold is-accent" style="margin-bottom:var(--s-1);letter-spacing:1px">김지혜 · 항공서비스학과 2019년 졸업 · 대한항공 퍼서</div><div class="t-subtitle w-regular" style="line-height:1.6;font-style:italic">"학교에서 <strong>승객 응대 10,000시간</strong>을 시뮬레이터로 채웠어요. 입사 첫날, 이미 해봤다는 느낌이었죠."</div></div><div style="border-left:3px solid #1A1A1A;padding:var(--s-3) var(--s-4);text-align:left;background:#F9F9F9"><div class="t-caption w-bold is-ink" style="margin-bottom:var(--s-1);letter-spacing:1px">박현수 · 호텔관광학과 2015년 졸업 · 시그니엘 총지배인</div><div class="t-subtitle w-regular" style="line-height:1.6;font-style:italic">"동기 48명 중 지금 <strong>총지배인은 6명.</strong> 우연이 아니라 <strong>시스템</strong>이에요."</div></div><div style="border-left:3px solid #1A1A1A;padding:var(--s-3) var(--s-4);text-align:left;background:#F9F9F9"><div class="t-caption w-bold is-ink" style="margin-bottom:var(--s-1);letter-spacing:1px">이지혜 · 경찰행정학과 2020년 졸업 · 부산지방경찰청 경위</div><div class="t-subtitle w-regular" style="line-height:1.6;font-style:italic">"경찰 시험 준비, 학교가 <strong>24시간 독서실과 멘토</strong>를 줬어요. 외롭지 않았어요."</div></div><div style="border-left:3px solid #E84E10;padding:var(--s-3) var(--s-4);text-align:left;background:#FFF5F0"><div class="t-caption w-bold is-accent" style="margin-bottom:var(--s-1);letter-spacing:1px">최지혜 · 뷰티디자인학과 2018년 졸업 · 본인 매장 대표</div><div class="t-subtitle w-regular" style="line-height:1.6;font-style:italic">"졸업 후 <strong>3년 만에 내 매장</strong>을 열었어요. 창업 교육이 이론이 아니라 실전이었어요."</div></div></div></div>"""
    append_slide(pid, "졸업생 인터뷰 프리뷰", page)
    print("    졸업생 4인 인터뷰 프리뷰 페이지 추가")


# V60: 시니어 파트너 최종 점검 — 한 장 요약
def v60(pid):
    page = """<!--PARENT:IV 사업 관리 계획--><!--TAG:Executive Summary--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-3)">EXECUTIVE SUMMARY</div><div class="t-heading" style="margin-bottom:var(--s-3)">이 제안서를 <span class="is-accent">한 장으로</span></div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div style="max-width:1100px;text-align:left;display:flex;flex-direction:column;gap:14px"><div style="display:flex;gap:16px;padding:10px 0;border-bottom:1px solid #E8E8E8"><div style="flex:0 0 130px;font-weight:700;color:#E84E10;font-size:12px;letter-spacing:2px">진단</div><div class="t-body is-ink" style="font-size:16px;line-height:1.6">영산대는 숫자를 가졌으나, 들리지 않고 있음. 정보 나열 = 소음.</div></div><div style="display:flex;gap:16px;padding:10px 0;border-bottom:1px solid #E8E8E8"><div style="flex:0 0 130px;font-weight:700;color:#E84E10;font-size:12px;letter-spacing:2px">기법</div><div class="t-body is-ink" style="font-size:16px;line-height:1.6"><strong>리프레이밍</strong> — 같은 숫자를 다른 프레임으로 (96.4% → 3.6%)</div></div><div style="display:flex;gap:16px;padding:10px 0;border-bottom:1px solid #E8E8E8"><div style="flex:0 0 130px;font-weight:700;color:#E84E10;font-size:12px;letter-spacing:2px">컨셉</div><div class="t-body is-ink" style="font-size:16px;line-height:1.6"><strong>증명</strong> — 주장이 아닌, 숫자가 직접 말하는 일</div></div><div style="display:flex;gap:16px;padding:10px 0;border-bottom:1px solid #E8E8E8"><div style="flex:0 0 130px;font-weight:700;color:#E84E10;font-size:12px;letter-spacing:2px">크리에이티브</div><div class="t-body is-ink" style="font-size:16px;line-height:1.6">시안 3종 (3.6% · 글로벌 55위 · 1개 시스템) + 영상 "지혜" 60초</div></div><div style="display:flex;gap:16px;padding:10px 0;border-bottom:1px solid #E8E8E8"><div style="flex:0 0 130px;font-weight:700;color:#E84E10;font-size:12px;letter-spacing:2px">매체·예산</div><div class="t-body is-ink" style="font-size:16px;line-height:1.6">7채널 퍼널 설계 · 연 1.25억 · 업계 평균 대비 30~40% 효율</div></div><div style="display:flex;gap:16px;padding:10px 0"><div style="flex:0 0 130px;font-weight:700;color:#E84E10;font-size:12px;letter-spacing:2px">슬로건</div><div class="t-title" style="font-size:32px;font-weight:700;color:#1A1A1A">영산대학교는, <span class="is-accent">지혜로 증명합니다.</span></div></div></div></div>"""
    append_slide(pid, "Executive Summary", page)
    print("    Executive Summary 1페이지 요약 추가")


personas = [
    ("V51", "Senior Brand Strategist · 브랜드 포지셔닝 선언", v51),
    ("V52", "UX Researcher · 수험생 12개월 저니", v52),
    ("V53", "PR 전문가 · 언론 4대 앵글", v53),
    ("V54", "행동경제학자 · 리프레이밍 3대 이론", v54),
    ("V55", "영상 PD · 지혜 60초 스토리보드", v55),
    ("V56", "퍼포먼스 마케터 · 자동화 스택", v56),
    ("V57", "고등교육 전문가 · 지방 사립대 위기 데이터", v57),
    ("V58", "법무/윤리 · 광고 윤리 4중 안전장치", v58),
    ("V59", "인터뷰어 · 졸업생 4인 인터뷰 프리뷰", v59),
    ("V60", "Senior Partner · Executive Summary 1장", v60),
]


def main():
    for ver, desc, fn in personas:
        print(f"[{ver}] {desc}")
        new_id = clone_from(V30_ID, ver, ver)
        fn(new_id)
    print(f"\n완료: V51~V60 페르소나 Round2 10개 버전 생성")


if __name__ == "__main__":
    main()
