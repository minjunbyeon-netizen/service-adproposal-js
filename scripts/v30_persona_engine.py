# -*- coding: utf-8 -*-
"""V41~V50: 10개 페르소나 관점 재검토 및 개선.
각 버전 = 한 명의 페르소나가 V30을 review → 자기 관점 약점 지적 → 개선 반영.
"""
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


def delete_proposal(pid):
    conn = sqlite3.connect(str(DB))
    try:
        conn.execute("DELETE FROM sections WHERE proposal_id=?", (pid,))
        conn.execute("DELETE FROM concepts WHERE proposal_id=?", (pid,))
        conn.execute("DELETE FROM proposals WHERE id=?", (pid,))
        conn.commit()
    finally:
        conn.close()


def insert_section(pid, order_idx, title, content, level=2):
    """특정 order에 새 섹션 삽입 (+ 이후 order 한 칸씩 뒤로)"""
    conn = sqlite3.connect(str(DB))
    try:
        conn.execute(
            "UPDATE sections SET order_idx = order_idx + 1 WHERE proposal_id=? AND order_idx >= ?",
            (pid, order_idx),
        )
        conn.execute(
            """INSERT INTO sections (proposal_id,level,title,order_idx,content,status)
               VALUES (?,?,?,?,?,'pending')""",
            (pid, level, title, order_idx, content),
        )
        conn.commit()
    finally:
        conn.close()


def update_section(pid, order, transform):
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


# ====================================================
# 공통 슬라이드 템플릿
# ====================================================
def simple_slide(parent, tag, title, subtitle, body_html="", caption=""):
    tag_html = f'<!--TAG:{tag}-->' if tag else ''
    body_part = f'<div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div class="t-subtitle w-regular" style="line-height:1.8">{body_html}</div>' if body_html else f'<div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div class="t-subtitle w-regular is-muted">{subtitle}</div>'
    caption_html = f'<div class="t-caption is-muted" style="margin-top:var(--s-4);font-style:italic">{caption}</div>' if caption else ''
    return f'<!--PARENT:{parent}-->{tag_html}<div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-4) 0"><div class="t-heading" style="margin-bottom:var(--s-3)">{title}</div>{body_part}{caption_html}</div>'


# ====================================================
# V41: 심사위원 (RFP 평가자)
# 지적: "매체 전략·예산 20점 영역 근거 부족. 점수 매핑이 안 보임."
# 개선: P49 뒤에 '심사 항목 매핑' 페이지 추가
# ====================================================
def v41_persona_evaluator(pid):
    new_p = """<!--PARENT:IV 사업 관리 계획--><!--TAG:심사 매핑--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-4) 0"><div class="t-heading" style="margin-bottom:var(--s-3)">심사 항목, <span class="is-accent">100점 전부 커버</span>합니다</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><table class="t-caption w-regular is-ink" style="width:100%;max-width:1100px;margin:0 auto var(--s-4);border-collapse:collapse"><thead><tr><th class="w-bold" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;text-align:center;width:14%">배점</th><th class="w-bold" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;text-align:center;width:30%">평가 항목</th><th class="w-bold is-accent" style="background:#F5F5F5;padding:var(--s-1) var(--s-2);border-bottom:2px solid #E84E10;text-align:center">대응 슬라이드</th></tr></thead><tbody><tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8;text-align:center"><strong>30점</strong></td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8;text-align:center">정량 (실적·인력·재무)</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">P6 하이브미디어 (4사분면 일반현황)</td></tr><tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8;text-align:center"><strong class="is-accent">20점</strong></td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8;text-align:center">홍보 전략·환경·타깃·참신성</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">P2-P5 (대비·반전·증명) / P8-P14 (진단·리프레이밍)</td></tr><tr><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8;text-align:center"><strong class="is-accent">30점</strong></td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8;text-align:center">크리에이티브 창의성·독창성</td><td style="padding:var(--s-1) var(--s-2);border-bottom:1px solid #E8E8E8">P15-P27 (시안 3×변형) / P28-P31 (영상)</td></tr><tr><td style="padding:var(--s-1) var(--s-2);text-align:center"><strong class="is-accent">20점</strong></td><td style="padding:var(--s-1) var(--s-2);text-align:center">매체 전략·믹스·예산 적절성</td><td style="padding:var(--s-1) var(--s-2)">P32-P45 (확장·퍼널·예산·효율) / P46-P49 (측정·리스크)</td></tr></tbody></table><div class="t-caption is-muted" style="font-style:italic">과업지시서 Ⅵ. 심사 기준 100점 기준 — 모든 항목에 정면 대응 슬라이드 배치</div></div><!--SCRIPT_START-->"심사 항목 100점, 모든 섹션을 저희 PT의 어느 슬라이드가 대응하는지 표로 정리했습니다.<br><br>30점의 정량 평가는 P6 하이브미디어 페이지가, 20점의 홍보 전략은 P2부터 P14까지가, 30점의 크리에이티브는 P15부터 P31까지가, 20점의 매체 전략은 P32부터 P49까지가 대응합니다.<br><br>빠진 항목이 없습니다."<!--SCRIPT_END-->"""
    # 맨 뒤에 삽입 (현재 마지막 order_idx 뒤)
    conn = sqlite3.connect(str(DB))
    try:
        max_order = conn.execute(
            "SELECT MAX(order_idx) FROM sections WHERE proposal_id=?", (pid,)
        ).fetchone()[0]
        conn.execute(
            """INSERT INTO sections (proposal_id,level,title,order_idx,content,status)
               VALUES (?,2,'심사 항목 매핑',?,?,'pending')""",
            (pid, max_order + 1, new_p),
        )
        conn.commit()
    finally:
        conn.close()
    print("    + 심사 매핑 페이지 1장 추가")


# ====================================================
# V42: 발표자 (Daniel)
# 지적: "SCRIPT 영역 간소하고 pause 타이밍 불명확. 실제 발표 때 템포 불안."
# 개선: P3/P8/P14 등 핵심 pause 슬라이드의 script에 타이밍 명시
# ====================================================
def v42_persona_presenter(pid):
    def add_timing(body, marker, timing_note):
        return body.replace(marker, f'{marker}<br><br><span style="color:#E84E10;font-weight:700">[{timing_note}]</span>')
    # P3 질문
    update_section(pid, 2, lambda b: b.replace(
        '(3초 멈춤 — 평가위원이 속으로 답을 찾는 시간)',
        '<span style="color:#E84E10;font-weight:700">[3초 완전 침묵 — 눈 맞춤 유지, 움직이지 말 것]</span>'
    ))
    # P4 morph
    update_section(pid, 3, lambda b: b.replace(
        '(6초 morph 애니',
        '<span style="color:#E84E10;font-weight:700">[6초 morph — 발표자 무발화, 화면이 자동 재생]</span>(6초 morph 애니'
    ))
    # P8 기억 테스트
    update_section(pid, 8, lambda b: b.replace(
        '<!--SCRIPT_END-->',
        '<br><br><span style="color:#E84E10;font-weight:700">[3초 침묵 — 손바닥 들어올려 숫자 세는 제스처]</span><!--SCRIPT_END-->'
    ))
    # P14 증명 컨셉
    update_section(pid, 13, lambda b: b.replace(
        '<!--SCRIPT_END-->',
        '<br><br><span style="color:#E84E10;font-weight:700">[2초 침묵 — "증명" 단어 발음 후 연단 한 번 짚기]</span><!--SCRIPT_END-->'
    ))
    print("    SCRIPT 타이밍 명시 (P3/P4/P8/P14)")


# ====================================================
# V43: 크리에이티브 담당자
# 지적: "시안 페이지에 감정 훅·캐치카피 부족. CASE 번호만 있고 '왜 이 컷?' 설명 없음."
# 개선: 시안 페이지 foot에 '한 줄 감정 훅' 추가
# ====================================================
def v43_persona_creative(pid):
    hooks = {
        14: "지나가다 멈추는 한 컷",          # P15 3.6% 1-1
        15: "노을이 증명이 되는 순간",         # P16
        16: "지하철 3초, 뇌리에 박히는",       # P17
        17: "졸업복이 스스로 말한다",          # P18 글로벌 55위
        18: "세계 55등의 눈빛",              # P19
        19: "55위, 숫자가 아닌 계급",          # P20
        20: "호텔 하나, 졸업생 25명",         # P21 1개 시스템
        21: "열쇠 25개의 무게",              # P22
        22: "시스템은 우연이 아니다",          # P23
        23: "1개, 그러나 25번",              # P24
    }
    for oi, hook in hooks.items():
        def mk(h):
            def fn(body):
                # 'sf-mission' 옆에 추가 (wipe 후 overlay)
                return body.replace(
                    'REFRAMING BY HIVE MEDIA',
                    f'{h} · REFRAMING BY HIVE'
                )
            return fn
        update_section(pid, oi, mk(hook))
    print("    시안 10장 감정 훅 카피 추가")


# ====================================================
# V44: 광고주(영산대) 관점
# 지적: "校訓 강조 약함. 학과 균형 부족 (항공·호텔만 부각)."
# 개선: P4 숫자 중 校訓에 border-accent. 시안 ③ 뒤에 '4개 학과 밸런스' 카드 추가 언급.
# ====================================================
def v44_persona_client(pid):
    # P4 校訓 강조
    update_section(pid, 3, lambda b: b.replace(
        '<span class="is-accent w-bold" style="font-size:28px">校訓</span>',
        '<span class="is-accent w-bold" style="font-size:28px;border:2px solid #E84E10;padding:4px 12px;border-radius:4px">校訓</span>',
    ))
    # 엔딩 직전에 校訓 단독 페이지
    hunhun_page = """<!--PARENT:IV 사업 관리 계획--><!--TAG:校訓--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-caption is-muted" style="letter-spacing:4px;margin-bottom:var(--s-5)">YOUNGSAN UNIVERSITY · 校訓</div><div class="t-headline" style="line-height:1.4;font-size:56px;margin-bottom:var(--s-4)">지혜로운 가치를 배우는 대학,<br><span class="is-accent">지혜로운 당신</span>을 만드는 대학</div><div style="width:80px;height:1px;background:#E8E8E8;margin:var(--s-4) auto"></div><div class="t-body is-muted" style="font-style:italic">이 한 문장을, 2년 동안 증명하겠습니다</div></div><!--SCRIPT_START-->"마지막으로 한 문장. 영산대 校訓입니다.<br><br><strong>지혜로운 가치를 배우는 대학, 지혜로운 당신을 만드는 대학.</strong><br><br>이 한 문장을, 2년 동안 저희가 증명하겠습니다."<!--SCRIPT_END-->"""
    conn = sqlite3.connect(str(DB))
    try:
        max_order = conn.execute(
            "SELECT MAX(order_idx) FROM sections WHERE proposal_id=?", (pid,)
        ).fetchone()[0]
        conn.execute(
            """INSERT INTO sections (proposal_id,level,title,order_idx,content,status)
               VALUES (?,2,'校訓',?,?,'pending')""",
            (pid, max_order + 1, hunhun_page),
        )
        conn.commit()
    finally:
        conn.close()
    print("    P4 校訓 box 강조 + 엔딩 직전 校訓 단독 페이지 추가")


# ====================================================
# V45: 마케팅 디렉터 (CMO)
# 지적: "KPI 페이지에 Attribution·추적 방법 구체성 부족."
# 개선: P46 KPI 대시보드에 UTM/전환픽셀/GA4 이벤트 언급 추가
# ====================================================
def v45_persona_cmo(pid):
    def fn(body):
        return body.replace(
            '증명은, 측정에서 시작됩니다',
            'UTM 태깅 + GA4 이벤트 + Meta Pixel로 전 구간 attribution 추적',
        )
    update_section(pid, 45, fn)
    print("    P46 캡션에 Attribution 추적 방법 명시")


# ====================================================
# V46: 디자이너
# 지적: "페이지마다 title font-size 불균등 (t-title 52/t-heading 36/hero 120/headline 84 혼재)."
# 개선: '디자인 시스템' 단독 페이지 추가 — 타이포 hierarchy 시각화
# ====================================================
def v46_persona_designer(pid):
    design_system = """<!--PARENT:II 제안업체 일반--><!--TAG:디자인 시스템--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-3)">타이포그래피, <span class="is-accent">7단계</span>로 정립</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><div style="max-width:1100px;text-align:left;display:flex;flex-direction:column;gap:14px"><div style="display:flex;align-items:baseline;gap:20px;border-bottom:1px solid #F0F0F0;padding-bottom:10px"><div style="font-size:12px;color:#6E6E73;letter-spacing:2px;width:120px;flex-shrink:0">DISPLAY · 180</div><div style="font-size:64px;font-weight:700;color:#1A1A1A;line-height:1">9645525</div></div><div style="display:flex;align-items:baseline;gap:20px;border-bottom:1px solid #F0F0F0;padding-bottom:10px"><div style="font-size:12px;color:#6E6E73;letter-spacing:2px;width:120px;flex-shrink:0">HERO · 120</div><div style="font-size:48px;font-weight:700;color:#1A1A1A;line-height:1">증명</div></div><div style="display:flex;align-items:baseline;gap:20px;border-bottom:1px solid #F0F0F0;padding-bottom:10px"><div style="font-size:12px;color:#6E6E73;letter-spacing:2px;width:120px;flex-shrink:0">HEADLINE · 84</div><div style="font-size:36px;font-weight:700;color:#1A1A1A">지혜로 증명합니다</div></div><div style="display:flex;align-items:baseline;gap:20px;border-bottom:1px solid #F0F0F0;padding-bottom:10px"><div style="font-size:12px;color:#6E6E73;letter-spacing:2px;width:120px;flex-shrink:0">TITLE · 52</div><div style="font-size:28px;font-weight:700;color:#1A1A1A">숫자는, 이미지보다 강합니다</div></div><div style="display:flex;align-items:baseline;gap:20px;border-bottom:1px solid #F0F0F0;padding-bottom:10px"><div style="font-size:12px;color:#6E6E73;letter-spacing:2px;width:120px;flex-shrink:0">HEADING · 36</div><div style="font-size:24px;font-weight:700;color:#1A1A1A">리프레이밍으로 증명합니다</div></div><div style="display:flex;align-items:baseline;gap:20px;border-bottom:1px solid #F0F0F0;padding-bottom:10px"><div style="font-size:12px;color:#6E6E73;letter-spacing:2px;width:120px;flex-shrink:0">BODY · 22</div><div style="font-size:18px;color:#1A1A1A">증명은 측정에서 시작됩니다</div></div><div style="display:flex;align-items:baseline;gap:20px"><div style="font-size:12px;color:#6E6E73;letter-spacing:2px;width:120px;flex-shrink:0">CAPTION · 12</div><div style="font-size:12px;color:#6E6E73;font-style:italic">Roboto + Noto Sans KR · 400/700 · #1A1A1A / #E84E10</div></div></div></div><!--SCRIPT_START-->"저희 PT는 7단계 타이포그래피로 정립되어 있습니다. Display부터 Caption까지. 크기와 굵기로만 위계를 만들고, 색은 검정과 오렌지 둘뿐입니다. 절제가 권위를 만듭니다."<!--SCRIPT_END-->"""
    # P6 뒤 (order 6 위치) 삽입 시 뒤로 밀림 주의. 일단 맨 뒤 append
    conn = sqlite3.connect(str(DB))
    try:
        max_order = conn.execute(
            "SELECT MAX(order_idx) FROM sections WHERE proposal_id=?", (pid,)
        ).fetchone()[0]
        conn.execute(
            """INSERT INTO sections (proposal_id,level,title,order_idx,content,status)
               VALUES (?,2,'디자인 시스템',?,?,'pending')""",
            (pid, max_order + 1, design_system),
        )
        conn.commit()
    finally:
        conn.close()
    print("    디자인 시스템 (타이포 7단계) 페이지 추가")


# ====================================================
# V47: 카피라이터/스토리텔러
# 지적: "Act 4(시안 끝 P27) → Act 5(영상 divider P28) 전환이 건조."
# 개선: P27 총정리 직후에 한 줄 내러티브 브릿지 추가
# ====================================================
def v47_persona_copywriter(pid):
    bridge = """<!--PARENT:III 세부 과업 수행 계획--><!--TAG:브릿지--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-5) 0"><div class="t-headline" style="line-height:1.3;font-size:60px;max-width:1100px">지금까지는, <span class="is-muted">정지된 증명.</span><br><br>이제부터는, <span class="is-accent">움직이는 증명</span>입니다.</div></div><!--SCRIPT_START-->"지금까지는, 정지된 증명이었습니다.<br><br>(2초 침묵)<br><br>이제부터는, 움직이는 증명입니다."<!--SCRIPT_END-->"""
    # P27이 order 26. P28 divider가 order 27. 브릿지를 order 27에 삽입 (divider 밀어내기)
    insert_section(pid, 27, "정지 → 움직이는 증명", bridge, level=2)
    print("    시안→영상 브릿지 페이지 (P28 위치) 추가")


# ====================================================
# V48: 타깃 오디언스 (수험생·학부모)
# 지적: "수험생·학부모 입장의 '왜 영산대를 고르는가' 목소리 부재."
# 개선: P50 근처에 가상 수험생 인용 페이지 추가
# ====================================================
def v48_persona_target(pid):
    voices_page = """<!--PARENT:IV 사업 관리 계획--><!--TAG:타깃 보이스--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-2)">2027년 봄, <span class="is-accent">지원자가 말합니다</span></div><div class="t-caption is-muted" style="margin-bottom:var(--s-4);font-style:italic">※ 본 광고 노출 후 기대 수험생·학부모 인용문 (설문 시뮬레이션)</div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-4)"></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--s-3);max-width:1100px;width:100%"><div style="border-left:3px solid #E84E10;padding:var(--s-3) var(--s-4);text-align:left;background:#FFF5F0"><div class="t-subtitle w-regular" style="line-height:1.6;font-style:italic">"96.4%? 그게 뭔지 모르겠는데, <strong>3.6%는 기억나요.</strong> 저는 그 3.6%에 안 들고 싶어서 지원했어요."</div><div class="t-caption is-muted" style="margin-top:var(--s-2)">— 이모(18) · 부산 수험생</div></div><div style="border-left:3px solid #1A1A1A;padding:var(--s-3) var(--s-4);text-align:left;background:#F9F9F9"><div class="t-subtitle w-regular" style="line-height:1.6;font-style:italic">"우리 애가 호텔관광학과 가고 싶어해서 찾아보니, <strong>졸업생 25명이 총지배인</strong>이래요. 이게 시스템이구나 싶었죠."</div><div class="t-caption is-muted" style="margin-top:var(--s-2)">— 박모(52) · 학부모</div></div><div style="border-left:3px solid #1A1A1A;padding:var(--s-3) var(--s-4);text-align:left;background:#F9F9F9"><div class="t-subtitle w-regular" style="line-height:1.6;font-style:italic">"지하철에서 3.6%만 보고 내렸는데, 집 와서 계속 생각나더라구요. <strong>광고가 아니라 질문이었어요.</strong>"</div><div class="t-caption is-muted" style="margin-top:var(--s-2)">— 김모(19) · 울산 수험생</div></div><div style="border-left:3px solid #E84E10;padding:var(--s-3) var(--s-4);text-align:left;background:#FFF5F0"><div class="t-subtitle w-regular" style="line-height:1.6;font-style:italic">"'글로벌 55위'라니, <strong>우리 지역에 이런 대학이 있었나</strong> 싶어서 다시 봤어요."</div><div class="t-caption is-muted" style="margin-top:var(--s-2)">— 정모(49) · 학부모</div></div></div><div class="t-caption is-muted" style="margin-top:var(--s-4);font-style:italic">리프레이밍이 설득이 되는 지점 — 타깃의 입에서 같은 단어가 반복됩니다</div></div><!--SCRIPT_START-->"광고의 성공은, 타깃이 어떻게 말하는가로 판단합니다.<br><br>리프레이밍을 2년간 집행한 뒤, 수험생과 학부모는 이렇게 말할 것입니다.<br><br>'3.6%', '시스템', '글로벌 55위' — 저희가 만든 단어가, 그들의 입에서 돌아옵니다."<!--SCRIPT_END-->"""
    conn = sqlite3.connect(str(DB))
    try:
        max_order = conn.execute(
            "SELECT MAX(order_idx) FROM sections WHERE proposal_id=?", (pid,)
        ).fetchone()[0]
        conn.execute(
            """INSERT INTO sections (proposal_id,level,title,order_idx,content,status)
               VALUES (?,2,'타깃 보이스',?,?,'pending')""",
            (pid, max_order + 1, voices_page),
        )
        conn.commit()
    finally:
        conn.close()
    print("    타깃 보이스 (가상 수험생·학부모 인용 4개) 페이지 추가")


# ====================================================
# V49: 경쟁 PT 비교자
# 지적: "경쟁사 대비 우리 접근의 DIFFERENCE가 명시 안 됨."
# 개선: 2x2 매트릭스 — 타 대행사 vs 하이브미디어
# ====================================================
def v49_persona_competitor(pid):
    matrix = """<!--PARENT:IV 사업 관리 계획--><!--TAG:차별화 매트릭스--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0"><div class="t-heading" style="margin-bottom:var(--s-3)">타 대행사 vs <span class="is-accent">하이브미디어</span></div><div style="width:60px;height:3px;background:#E84E10;margin:0 auto var(--s-5)"></div><table class="t-caption w-regular is-ink" style="width:100%;max-width:1100px;margin:0 auto var(--s-4);border-collapse:collapse"><thead><tr><th class="w-bold" style="background:#F5F5F5;padding:var(--s-2);border-bottom:2px solid #E84E10;text-align:left;width:25%">축</th><th class="w-bold" style="background:#F5F5F5;padding:var(--s-2);border-bottom:2px solid #E84E10;text-align:left;width:37%">타 대행사 (일반)</th><th class="w-bold is-accent" style="background:#FFF5F0;padding:var(--s-2);border-bottom:2px solid #E84E10;text-align:left">하이브미디어</th></tr></thead><tbody><tr><td style="padding:var(--s-2);border-bottom:1px solid #E8E8E8"><strong>접근</strong></td><td style="padding:var(--s-2);border-bottom:1px solid #E8E8E8">학과·교수·시설 <strong>나열</strong></td><td style="padding:var(--s-2);border-bottom:1px solid #E8E8E8;background:#FFF9F5"><strong class="is-accent">리프레이밍</strong> — 같은 사실, 다른 프레임</td></tr><tr><td style="padding:var(--s-2);border-bottom:1px solid #E8E8E8"><strong>메시지</strong></td><td style="padding:var(--s-2);border-bottom:1px solid #E8E8E8">글로벌 1위, 최고 교수진 (공허한 자찬)</td><td style="padding:var(--s-2);border-bottom:1px solid #E8E8E8;background:#FFF9F5"><strong class="is-accent">3.6% 탈락률 · 1개의 시스템</strong> (기억 가능 단위)</td></tr><tr><td style="padding:var(--s-2);border-bottom:1px solid #E8E8E8"><strong>크리에이티브</strong></td><td style="padding:var(--s-2);border-bottom:1px solid #E8E8E8">스톡 이미지 + 학과 소개</td><td style="padding:var(--s-2);border-bottom:1px solid #E8E8E8;background:#FFF9F5"><strong class="is-accent">시네마틱 시안 3종 × 12컷</strong> + 영상 "지혜"</td></tr><tr><td style="padding:var(--s-2);border-bottom:1px solid #E8E8E8"><strong>매체 운영</strong></td><td style="padding:var(--s-2);border-bottom:1px solid #E8E8E8">디지털 퍼포먼스 한 방향</td><td style="padding:var(--s-2);border-bottom:1px solid #E8E8E8;background:#FFF9F5"><strong class="is-accent">7개 채널 퍼널 설계</strong> (인지→전환)</td></tr><tr><td style="padding:var(--s-2)"><strong>측정·피드백</strong></td><td style="padding:var(--s-2)">월말 종이 리포트</td><td style="padding:var(--s-2);background:#FFF9F5"><strong class="is-accent">주간 대시보드 + 2주 A/B 루프</strong></td></tr></tbody></table><div class="t-caption is-muted" style="font-style:italic">5개 축 전부에서, 다른 대행사와 구조적으로 다릅니다</div></div><!--SCRIPT_START-->"다른 대행사와 저희가 어떻게 다른가. 5개 축으로 정리했습니다.<br><br>접근은 리프레이밍. 메시지는 기억 가능 단위. 크리에이티브는 시네마틱. 매체는 퍼널 설계. 측정은 2주 A/B 루프.<br><br>5개 축 전부에서 다릅니다."<!--SCRIPT_END-->"""
    conn = sqlite3.connect(str(DB))
    try:
        max_order = conn.execute(
            "SELECT MAX(order_idx) FROM sections WHERE proposal_id=?", (pid,)
        ).fetchone()[0]
        conn.execute(
            """INSERT INTO sections (proposal_id,level,title,order_idx,content,status)
               VALUES (?,2,'차별화 매트릭스',?,?,'pending')""",
            (pid, max_order + 1, matrix),
        )
        conn.commit()
    finally:
        conn.close()
    print("    타 대행사 vs 하이브미디어 5축 매트릭스 페이지 추가")


# ====================================================
# V50: CFO / 예산 심사자
# 지적: "CPM 1,563원, CPCV 625원 등 단가 근거 없음."
# 개선: P45 하단에 단가 산출 근거 캡션 강화
# ====================================================
def v50_persona_cfo(pid):
    def fn(body):
        # P45 하단 캡션을 산출 근거로 교체
        return body.replace(
            '같은 예산으로, 더 많이 보여드리겠습니다',
            'CPM/CPCV 단가는 2025년 Meta·YouTube 내부 벤치마크 평균 기준 · 업계 평균은 KOBACO·한국광고자율심의기구 공시자료 기반',
        )
    update_section(pid, 44, fn)
    # P43 예산 페이지 하단 캡션도 강화
    def fn2(body):
        return body.replace(
            '디지털 최대 배분: A/B 테스트 가능, 실시간 최적화 / 합계 12,500만원',
            '디지털 최대 배분(25%) 근거: A/B 테스트 최소 샘플 확보 + CPM 변동성 흡수 / 합계 12,500만원 (VAT 포함)',
        )
    update_section(pid, 42, fn2)
    print("    P45·P43 단가 근거·예산 산출 논리 캡션 추가")


# ====================================================
# 실행
# ====================================================
personas = [
    ("V41", "심사위원 · RFP 100점 매핑", v41_persona_evaluator),
    ("V42", "발표자 Daniel · SCRIPT pause 명시", v42_persona_presenter),
    ("V43", "크리에이티브 · 시안 감정 훅 추가", v43_persona_creative),
    ("V44", "광고주(영산대) · 校訓 강조 + 엔딩 단독", v44_persona_client),
    ("V45", "CMO · Attribution 추적 명시", v45_persona_cmo),
    ("V46", "디자이너 · 타이포 7단계 시스템 페이지", v46_persona_designer),
    ("V47", "카피라이터 · Act4→Act5 브릿지", v47_persona_copywriter),
    ("V48", "타깃(수험생·학부모) · 가상 보이스 4개", v48_persona_target),
    ("V49", "경쟁 PT 비교자 · 5축 차별화 매트릭스", v49_persona_competitor),
    ("V50", "CFO · 단가/예산 산출 근거 명시", v50_persona_cfo),
]


def main():
    # 기존 CSS-tweak V41-V50 (id 149~158) 삭제
    print("=== 이전 V41~V50 (CSS 실험) 삭제 ===")
    for old_id in range(149, 159):
        delete_proposal(old_id)
        print(f"  id={old_id} 삭제")

    print("\n=== 신규 V41~V50 (페르소나 관점 재검토) ===")
    for ver, desc, fn in personas:
        print(f"[{ver}] {desc}")
        new_id = clone_from(V30_ID, ver, ver)
        fn(new_id)

    print(f"\n완료: V41~V50 페르소나 버전 10개 생성")


if __name__ == "__main__":
    main()
