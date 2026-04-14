# -*- coding: utf-8 -*-
"""V31~V60 각 버전에 VERSION BANNER 삽입 + 사이드패널 타이틀에 변경 내용 명시."""
import sqlite3
import sys
import io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"


VERSIONS = [
    # id, ver, persona, what_changed, location
    (139, "V31", "기준 스냅샷", "V30 그대로 보존 (reference)", "-"),
    (140, "V32", "UI 튜닝", "P2 경쟁사 대학명 bold 강조", "P2"),
    (141, "V33", "UI 튜닝", "P5 '들리지 않았을까요?' 오렌지 밑줄", "P5"),
    (142, "V34", "UI 튜닝", "P6 '전부' 단어 오렌지 강조", "P6"),
    (143, "V35", "UI 튜닝", "P12 Before/After 카드 폰트 +6px", "P12"),
    (144, "V36", "UI 튜닝", "P14 '증명' 140px 초대형 타이포", "P14"),
    (145, "V37", "UI 튜닝", "P15 화살표 letter-spacing 튜닝", "P15"),
    (146, "V38", "UI 튜닝", "P31 슬로건 88→96px 확대", "P31"),
    (147, "V39", "UI 튜닝", "P33 퍼널 단계별 전환율 % 추가", "P33"),
    (148, "V40", "UI 튜닝", "P46 대시보드 캡션 재카피", "P46"),

    (159, "V41", "심사위원", "심사 100점 매핑 페이지 추가", "끝 직전"),
    (160, "V42", "발표자 Daniel", "SCRIPT에 [침묵 타이밍] 명시", "P3/P4/P8/P14"),
    (161, "V43", "크리에이티브", "시안 10장 감정 훅 카피", "P15~P24"),
    (162, "V44", "광고주 영산대", "校訓 box 강조 + 단독 페이지", "P4·끝"),
    (163, "V45", "CMO", "Attribution 추적 명시", "P46"),
    (164, "V46", "디자이너", "타이포 7단계 시스템 페이지", "끝"),
    (165, "V47", "카피라이터", "시안→영상 브릿지 페이지", "P28"),
    (166, "V48", "타깃(수험생·학부모)", "가상 보이스 4개 인용 페이지", "끝"),
    (167, "V49", "경쟁 PT 비교자", "5축 차별화 매트릭스", "끝"),
    (168, "V50", "CFO", "P43·P45 단가 산출 근거 캡션", "P43·P45"),

    (169, "V51", "Brand Strategist", "브랜드 포지셔닝 선언 페이지", "끝"),
    (170, "V52", "UX Researcher", "수험생 12개월 저니맵", "끝"),
    (171, "V53", "PR 전문가", "언론 4대 앵글 페이지", "끝"),
    (172, "V54", "행동경제학자", "Kahneman·Heath·Cialdini 3대 이론", "끝"),
    (173, "V55", "영상 PD", "60초 5-shot 스토리보드", "끝"),
    (174, "V56", "퍼포먼스 마케터", "P45 자동화 스택 명시", "P45"),
    (175, "V57", "고등교육 전문가", "지방 사립대 위기 데이터 3개", "끝"),
    (176, "V58", "법무/윤리", "광고 윤리 4중 안전장치", "끝"),
    (177, "V59", "인터뷰어", "졸업생 4인 인터뷰 프리뷰", "끝"),
    (178, "V60", "Senior Partner", "Executive Summary 1장", "끝"),
]


def make_banner(ver, persona, changed, location):
    """각 버전 첫 페이지로 삽입할 VERSION BANNER 슬라이드."""
    return f"""<!--PARENT:VERSION BANNER--><!--TAG:{ver}--><div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;text-align:left;padding:60px 100px;background:#FAFAFA"><div style="font-size:14px;letter-spacing:6px;color:#6E6E73;font-weight:700;margin-bottom:20px">VERSION IDENTIFIER</div><div style="font-size:96px;font-weight:700;color:#E84E10;line-height:1;letter-spacing:-3px;margin-bottom:20px;font-family:Roboto,sans-serif">{ver}</div><div style="width:60px;height:3px;background:#1A1A1A;margin-bottom:32px"></div><div style="font-size:24px;color:#1A1A1A;font-weight:700;margin-bottom:14px;letter-spacing:-0.5px">페르소나 · {persona}</div><div style="font-size:20px;color:#1A1A1A;line-height:1.6;margin-bottom:10px"><strong>변경 내용:</strong> {changed}</div><div style="font-size:16px;color:#6E6E73;font-style:italic">적용 위치: {location}</div><div style="margin-top:60px;font-size:12px;color:#A0A0A5;letter-spacing:2px">※ 이 페이지는 버전 식별용 — 본편은 다음 장부터</div></div><!--SCRIPT_START-->"{ver} 페르소나 · {persona}<br><br>{changed} ({location})<br><br>(본편 넘어갑니다)"<!--SCRIPT_END-->"""


def main():
    conn = sqlite3.connect(str(DB))
    try:
        for pid, ver, persona, changed, location in VERSIONS:
            # 1. 사이드패널 타이틀 업데이트
            new_title = f"{ver} · {persona} · {changed[:30]}"
            conn.execute(
                "UPDATE proposals SET title=? WHERE id=?",
                (new_title, pid),
            )
            # 2. VERSION BANNER를 첫 섹션으로 삽입 (order shift)
            # 기존 section들 order +1
            conn.execute(
                "UPDATE sections SET order_idx = order_idx + 1 WHERE proposal_id=?",
                (pid,),
            )
            # 새 banner를 order 1로 삽입
            banner = make_banner(ver, persona, changed, location)
            conn.execute(
                "INSERT INTO sections (proposal_id, level, title, order_idx, content, status) "
                "VALUES (?, 2, ?, 1, ?, 'pending')",
                (pid, f"VERSION · {ver}", banner),
            )
            print(f"  {ver} · {persona}: title+banner 적용")
        conn.commit()
    finally:
        conn.close()
    print(f"\n완료: 30개 버전 전부 배너·타이틀 적용")


if __name__ == "__main__":
    main()
