"""섹션 생성 + 대화형 수정 + 컨셉 A/B/C 생성 서비스."""
import json
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


CONCEPT_SYSTEM_PROMPT = """당신은 대한민국 최고의 광고 크리에이티브 디렉터다.
입찰공고문 분석 결과를 기반으로 광고 제안서의 컨셉 방향 3가지(A/B/C)를 제안한다.

=== 절대 금지 표현 (클리셰 블랙리스트) ===
{blacklist}

=== 컨셉 방향 기준 ===
A: 데이터/수치 기반 접근 -- 통계, 실적, 수치로 설득하는 전략
B: 감성/스토리텔링 접근 -- 내러티브, 감정, 경험으로 공감을 이끄는 전략
C: 역발상/파격 접근 -- 기존 틀을 깨는 반전, 의외성으로 주목도를 높이는 전략

=== 출력 형식 (JSON 배열, 반드시 준수) ===
```json
[
  {{"label": "A", "title": "컨셉A 제목", "body": "컨셉A 설명 (3-5문장)"}},
  {{"label": "B", "title": "컨셉B 제목", "body": "컨셉B 설명 (3-5문장)"}},
  {{"label": "C", "title": "컨셉C 제목", "body": "컨셉C 설명 (3-5문장)"}}
]
```

한국어로 작성. 이모지 금지. JSON 블록 외 다른 텍스트 출력 금지."""


def build_concept_prompt(rfp_json: dict, proposal_title: str, direction: str = "") -> str:
    parts = [f"제안서 제목: {proposal_title}"]
    if rfp_json.get("client_name"):
        parts.append(f"발주처: {rfp_json['client_name']}")
    if rfp_json.get("project_name"):
        parts.append(f"사업명: {rfp_json['project_name']}")
    if rfp_json.get("budget"):
        parts.append(f"예산: {rfp_json['budget']}")
    if rfp_json.get("tasks"):
        parts.append(f"과업항목: {', '.join(rfp_json['tasks'])}")
    if direction:
        parts.append(f"추가 방향 지시: {direction}")
    parts.append("위 공고 정보를 기반으로 광고 컨셉 A/B/C 3가지를 JSON 배열로 제안하라.")
    return "\n".join(parts)


def parse_concept_response(raw: str) -> list[dict]:
    """claude 응답에서 JSON 배열을 추출한다. 실패 시 placeholder 반환."""
    # ```json ... ``` 블록 추출 시도
    text = raw
    if "```json" in text:
        start = text.index("```json") + 7
        end = text.index("```", start)
        text = text[start:end].strip()
    elif "```" in text:
        start = text.index("```") + 3
        end = text.index("```", start)
        text = text[start:end].strip()

    # [ 로 시작하는 JSON 배열 찾기
    bracket_start = text.find("[")
    bracket_end = text.rfind("]")
    if bracket_start >= 0 and bracket_end > bracket_start:
        text = text[bracket_start:bracket_end + 1]

    try:
        items = json.loads(text)
        if isinstance(items, list) and len(items) >= 3:
            result = []
            for item in items[:3]:
                result.append({
                    "label": item.get("label", ["A", "B", "C"][len(result)]),
                    "title": item.get("title", f"컨셉 {['A','B','C'][len(result)]}"),
                    "body": item.get("body", ""),
                })
            return result
    except (json.JSONDecodeError, KeyError, IndexError):
        pass

    logger.warning("concept JSON parse failed, returning placeholders")
    return [
        {"label": "A", "title": "데이터 기반 접근", "body": "(생성 실패 -- 수동 입력 필요)"},
        {"label": "B", "title": "감성 스토리텔링", "body": "(생성 실패 -- 수동 입력 필요)"},
        {"label": "C", "title": "역발상 전략", "body": "(생성 실패 -- 수동 입력 필요)"},
    ]


def generate_concepts(rfp_json: dict, proposal_title: str, direction: str = "") -> list[dict]:
    """claude CLI 1회 호출로 A/B/C 3개 컨셉을 생성한다."""
    blacklist = "\n".join(f'- "{c}"' for c in CLICHE_BLACKLIST)
    system = CONCEPT_SYSTEM_PROMPT.format(blacklist=blacklist)
    prompt = build_concept_prompt(rfp_json, proposal_title, direction)
    raw = call_claude(prompt, system_prompt=system, model="sonnet")
    return parse_concept_response(raw)


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
