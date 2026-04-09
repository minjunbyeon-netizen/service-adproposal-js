"""claude CLI subprocess 래퍼. meeting 도구와 동일 패턴."""
import subprocess
import os
import logging

logger = logging.getLogger(__name__)

CLAUDE_TIMEOUT = 300
ALLOWED_MODELS = frozenset({"sonnet", "haiku", "opus"})


def call_claude(prompt, system_prompt=None, model="sonnet"):
    """claude CLI를 호출하여 응답을 반환한다."""
    if model not in ALLOWED_MODELS:
        raise ValueError(f"Invalid model: {model}")

    cmd = ["claude", "-p", prompt, "--model", model]
    if system_prompt:
        cmd.extend(["--system-prompt", system_prompt])

    logger.info("claude call: model=%s, prompt_len=%d", model, len(prompt))

    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        result = subprocess.run(cmd, capture_output=True, timeout=CLAUDE_TIMEOUT, env=env)
        stdout = result.stdout.decode("utf-8", errors="replace").strip()
        stderr = result.stderr.decode("utf-8", errors="replace").strip()

        if result.returncode != 0:
            detail = stderr or stdout or f"exit code {result.returncode}"
            logger.error("claude CLI error (code %d): %s", result.returncode, detail[:500])
            raise RuntimeError(f"claude CLI failed: {detail[:500]}")
        if not stdout:
            raise RuntimeError("claude CLI returned empty response")
        return stdout
    except subprocess.TimeoutExpired:
        logger.error("claude CLI timeout (%ds)", CLAUDE_TIMEOUT)
        raise RuntimeError(f"AI 응답 시간 초과 ({CLAUDE_TIMEOUT}s)")
    except FileNotFoundError:
        raise RuntimeError("claude CLI가 설치되어 있지 않습니다")
