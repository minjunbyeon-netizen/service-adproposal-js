"""RFP 공고문 교차분석 서비스."""
import json
import re
import logging
from services.claude_client import call_claude

logger = logging.getLogger(__name__)

ANALYSIS_SYSTEM_PROMPT = """당신은 광고 입찰공고문(RFP) 분석 전문가다.
여러 파일의 내용이 ===FILE: 파일명=== 구분자로 합산된 텍스트를 받는다.
교차분석하여 다음을 추출하라:

1. rfp_data (JSON):
   {
     "client_name": "발주처명",
     "project_name": "사업명",
     "budget": "예산 (원)",
     "duration": "수행 기간",
     "eval_criteria": [{"item": "평가항목", "score": 배점}],
     "tasks": ["과업 항목 1", "과업 항목 2"],
     "deadline": "제출 기한"
   }

2. toc (JSON 배열):
   과업요구사항을 강제 골격으로 계층별 목차를 구성하라.
   [
     {"level": 1, "title": "대제목", "order_idx": 0},
     {"level": 2, "title": "소제목", "order_idx": 1}
   ]
   대제목 6-8개, 소제목 2-4개/대제목, 핵심 과업 항목 반드시 포함.

응답 형식: 분석 설명 후 마지막에 아래 두 JSON 블록을 반드시 출력.

```rfp_json
{...}
```

```toc_json
[...]
```

한국어로 작성. 이모지 금지."""


def analyze_rfp(raw_text):
    """공고문 텍스트를 분석하여 rfp_json, rfp_summary, toc_json을 반환한다."""
    prompt = f"다음 공고문을 교차분석하라:\n\n{raw_text}"
    response = call_claude(prompt, system_prompt=ANALYSIS_SYSTEM_PROMPT, model="sonnet")

    rfp_json = _extract_json_block(response, "rfp_json")
    toc_json = _extract_json_block(response, "toc_json")

    if not rfp_json:
        rfp_json = {"client_name": "미상", "project_name": "미상", "tasks": []}
        logger.warning("rfp_json parsing failed, using default")

    if not toc_json:
        toc_json = _default_toc()
        logger.warning("toc_json parsing failed, using default TOC")

    rfp_summary = build_rfp_summary(rfp_json)
    return rfp_json, rfp_summary, toc_json, response


def _extract_json_block(text, block_name):
    """```block_name ... ``` 블록에서 JSON을 추출한다."""
    pattern = rf"```{block_name}\s*\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError as e:
            logger.error("JSON parse error in %s: %s", block_name, e)
    return None


def build_rfp_summary(rfp_json):
    """rfp_json에서 핵심 필드만 추려 요약 문자열을 생성한다."""
    parts = []
    if rfp_json.get("client_name"):
        parts.append(f"발주처: {rfp_json['client_name']}")
    if rfp_json.get("project_name"):
        parts.append(f"사업명: {rfp_json['project_name']}")
    if rfp_json.get("budget"):
        parts.append(f"예산: {rfp_json['budget']}")
    if rfp_json.get("duration"):
        parts.append(f"수행기간: {rfp_json['duration']}")
    if rfp_json.get("deadline"):
        parts.append(f"제출기한: {rfp_json['deadline']}")
    if rfp_json.get("tasks"):
        parts.append("과업항목:\n" + "\n".join(f"- {t}" for t in rfp_json["tasks"]))
    if rfp_json.get("eval_criteria"):
        criteria = [f"- {c['item']} ({c.get('score', '?')}점)" for c in rfp_json["eval_criteria"]]
        parts.append("평가기준:\n" + "\n".join(criteria))
    return "\n".join(parts)


def _default_toc():
    """파싱 실패 시 기본 목차."""
    return [
        {"level": 1, "title": "사업 이해", "order_idx": 0},
        {"level": 2, "title": "사업 배경 및 목적", "order_idx": 1},
        {"level": 2, "title": "현황 분석", "order_idx": 2},
        {"level": 1, "title": "광고 전략", "order_idx": 3},
        {"level": 2, "title": "목표 및 방향", "order_idx": 4},
        {"level": 2, "title": "타겟 분석", "order_idx": 5},
        {"level": 1, "title": "매체 전략", "order_idx": 6},
        {"level": 2, "title": "매체 믹스", "order_idx": 7},
        {"level": 2, "title": "매체 집행 계획", "order_idx": 8},
        {"level": 1, "title": "크리에이티브 전략", "order_idx": 9},
        {"level": 2, "title": "컨셉 및 메시지", "order_idx": 10},
        {"level": 2, "title": "제작물 계획", "order_idx": 11},
        {"level": 1, "title": "운영 계획", "order_idx": 12},
        {"level": 2, "title": "수행 체계", "order_idx": 13},
        {"level": 2, "title": "일정 계획", "order_idx": 14},
        {"level": 1, "title": "예산 계획", "order_idx": 15},
        {"level": 1, "title": "기대 효과", "order_idx": 16},
    ]
