"""claude CLI subprocess 래퍼."""
import shutil
import subprocess
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

CLAUDE_TIMEOUT = 300
ALLOWED_MODELS = frozenset({"sonnet", "haiku", "opus"})


def _find_claude_binary():
    """claude CLI 바이너리 절대 경로를 반환한다."""
    found = shutil.which("claude")
    if found:
        return found
    # Windows에서 PATH에 없을 때 알려진 위치 탐색
    candidates = [
        Path.home() / ".local" / "bin" / "claude",
        Path.home() / ".local" / "bin" / "claude.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "claude" / "claude.exe",
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None


def call_claude(prompt, system_prompt=None, model="sonnet"):
    """claude CLI를 호출하여 응답을 반환한다."""
    if model not in ALLOWED_MODELS:
        raise ValueError(f"Invalid model: {model}")

    claude_bin = _find_claude_binary()
    if not claude_bin:
        raise RuntimeError("claude CLI가 설치되어 있지 않습니다. PATH 또는 ~/.local/bin 확인 필요")

    cmd = [claude_bin, "-p", prompt, "--model", model]
    if system_prompt:
        cmd.extend(["--system-prompt", system_prompt])

    logger.info("claude call: model=%s, prompt_len=%d, bin=%s", model, len(prompt), claude_bin)

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
