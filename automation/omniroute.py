"""Minimal OpenAI-compatible LLM transport for the Actions worker.

No user-supplied URL or model is accepted. Secrets never enter prompts, logs or Git.
"""
from __future__ import annotations

import json
import os
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


class ModelError(RuntimeError):
    pass


def config(role: str) -> tuple[str, str, str]:
    if role not in {"TRANSLATOR", "REVIEWER", "CORRECTOR"}:
        raise ModelError("unsupported model role")
    base = os.environ.get("OMNIROUTE_BASE_URL", "").rstrip("/")
    key = os.environ.get("OMNIROUTE_API_KEY", "")
    model = os.environ.get(f"OMNIROUTE_{role}_MODEL", "")
    parsed = urlsplit(base)
    if (parsed.scheme != "https" or not parsed.netloc or parsed.username or
            parsed.password or parsed.query or parsed.fragment or not key or not model):
        raise ModelError("OmniRoute HTTPS base URL, key and role model must be configured")
    if not model.strip() or len(model) > 150:
        raise ModelError("invalid model identifier")
    return base, key, model


def complete(role: str, system: str, user: str) -> str:
    base, key, model = config(role)
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2 if role != "TRANSLATOR" else 0.4,
    }, ensure_ascii=False).encode("utf-8")
    request = Request(
        base + "/chat/completions",
        data=body,
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    for attempt in range(3):
        try:
            with urlopen(request, timeout=240) as response:
                payload = json.loads(response.read(8_000_000).decode("utf-8"))
            choice = payload["choices"][0]
            reason = choice.get("finish_reason")
            if reason in {"length", "content_filter"}:
                raise ModelError("model output incomplete or filtered")
            answer = choice["message"]["content"]
            if isinstance(answer, list):
                answer = "".join(part.get("text", "") for part in answer if isinstance(part, dict))
            if not isinstance(answer, str) or not answer.strip():
                raise ModelError("model returned empty content")
            return answer.strip() + "\n"
        except HTTPError as exc:
            if exc.code not in {429, 500, 502, 503, 504} or attempt == 2:
                raise ModelError(f"model HTTP status {exc.code}") from None
        except (URLError, TimeoutError) as exc:
            if attempt == 2:
                raise ModelError("model transport timeout or connection failure") from exc
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise ModelError("model response is not a valid chat completion") from exc
        time.sleep(2 ** attempt)
    raise ModelError("model retries exhausted")


def parse_review(text: str) -> tuple[str, dict]:
    """Require strict, actionable source-comparison evidence before promotion."""
    candidate = text.strip()
    fence = chr(96) * 3
    if candidate.startswith(fence):
        lines = candidate.splitlines()
        if len(lines) < 3 or not lines[-1].strip().startswith(fence):
            raise ModelError("reviewer returned incomplete JSON fence")
        candidate = "\n".join(lines[1:-1])
    try:
        obj = json.loads(candidate)
    except ValueError as exc:
        raise ModelError("reviewer did not return valid JSON") from exc
    if not isinstance(obj, dict) or set(obj) != {"outcome", "checks", "findings"}:
        raise ModelError("reviewer JSON schema mismatch")
    outcome = obj["outcome"]
    checks = obj["checks"]
    if outcome not in {"PASS", "CORRECTIONS_REQUIRED"}:
        raise ModelError("reviewer outcome invalid")
    expected = {"coverage", "meaning", "terminology", "style", "structure"}
    if not isinstance(checks, dict) or set(checks) != expected or any(
        checks[k] is not True for k in expected
    ):
        raise ModelError("reviewer has not confirmed all five checks were performed")
    findings = obj["findings"]
    if not isinstance(findings, list) or len(findings) > 30:
        raise ModelError("reviewer findings are not bounded")
    for item in findings:
        if not isinstance(item, dict) or set(item) != {"severity", "detail", "resolved"}:
            raise ModelError("reviewer finding has invalid fields")
        if item["severity"] not in {"minor", "major", "critical"}:
            raise ModelError("reviewer finding has invalid severity")
        if not isinstance(item["detail"], str) or not 1 <= len(item["detail"].strip()) <= 1000:
            raise ModelError("reviewer finding needs a specific detail")
        if type(item["resolved"]) is not bool:
            raise ModelError("reviewer finding resolved must be boolean")
    unresolved = [f for f in findings if not f["resolved"]]
    if outcome == "CORRECTIONS_REQUIRED" and not unresolved:
        raise ModelError("corrections required without concrete unresolved findings")
    if outcome == "PASS" and unresolved:
        raise ModelError("unresolved reviewer findings cannot be promoted")
    return outcome, {
        "context": "independent_session",
        "checks": checks,
        "findings": findings,
    }
