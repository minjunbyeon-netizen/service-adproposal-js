"""섹션 생성 + 대화형 수정 서비스."""
import logging
from services.claude_client import call_claude

logger = logging.getLogger(__name__)

CLICHE_BLACKLIST = [
    "글로벌 경쟁력 강화를 위해",
    "4차 산업혁명 시대에",
    "MZ세대의 감성을 자극하는",
    "소통과 공감의",
    "대학의 브랜드 가치 제고",
    "혁신적이고 창의적인",
    "시대의 흐름에 발맞추어",
    "차별화된 경쟁력 확보",
    "글로컬 인재 양성",
    "4차 산업혁명에 대비한",
    "미래 지향적",
    "특성화된 교육",
    "산학협력 활성화",
    "지역사회와 함께하는",
    "세계를 선도하는",
    "무한한 가능성",
    "새로운 패러다임",
    "시너지 효과 극대화",
    "비전 2030",
    "글로벌 스탠다드",
]

GENERATION_SYSTEM_PROMPT = """당신은 대한민국 최고의 광고 제안서 컨설턴트다.
공고 요약을 기반으로 제안서 섹션 내용을 작성한다.

=== 절대 금지 표현 (클리셰 블랙리스트) ===
{blacklist}

=== 작성 원칙 (일론머스크식 첫 원리 사고) ===
1. "이 대학이 왜 이 광고를 해야 하는가?"를 먼저 물어라.
2. 기존 대학 광고의 틀을 의도적으로 깨라.
3. 구체적 수치와 근거로 주장을 뒷받침하라.
4. 발표용 스크립트 수준의 간결함을 유지하라.
5. 과업요구사항에 명시된 항목은 반드시 반영하라.

한국어로 작성. 이모지 금지. 마크다운 형식."""


def _build_system_prompt(rfp_summary):
    """rfp_summary를 포함한 시스템 프롬프트를 생성한다."""
    blacklist = "\n".join(f'- "{c}"' for c in CLICHE_BLACKLIST)
    base = GENERATION_SYSTEM_PROMPT.format(blacklist=blacklist)
    return f"{base}\n\n=== 공고 요약 ===\n{rfp_summary}"


def generate_section(rfp_summary, section_title, section_level):
    """섹션 초안을 생성한다."""
    system = _build_system_prompt(rfp_summary)
    level_name = {1: "대제목", 2: "소제목", 3: "본문"}.get(section_level, "섹션")
    prompt = (
        f"{level_name} '{section_title}'의 내용을 작성하라.\n"
        f"제목 수준: level {section_level}\n"
        "과업요구사항에 근거하여 구체적으로 작성하되, "
        "기존 대학 광고의 천편일률적 표현은 절대 사용하지 마라."
    )
    return call_claude(prompt, system_prompt=system, model="sonnet")


def reply_section(rfp_summary, section_title, section_content, history):
    """사용자 피드백에 따라 섹션을 수정한다."""
    system = _build_system_prompt(rfp_summary)

    # 대화 이력 구성 (최근 20턴)
    recent = history[-20:] if len(history) > 20 else history
    context_parts = [f"현재 섹션 '{section_title}'의 내용:\n{section_content or '(아직 없음)'}"]
    for msg in recent:
        role_label = "CEO" if msg["role"] == "user" else "AI"
        context_parts.append(f"{role_label}: {msg['content']}")

    prompt = "\n\n".join(context_parts) + "\n\n위 피드백을 반영하여 섹션 내용을 수정하라."
    return call_claude(prompt, system_prompt=system, model="sonnet")
