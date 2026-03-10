"""Thin async HTTP client for the Sieve Public API."""

import hashlib
import os
import time
from typing import Any

import httpx

SIEVE_API_URL = os.environ.get(
    "SIEVE_API_URL", "https://api.sieve.arceusxventures.com"
)
SIEVE_API_KEY = os.environ.get("SIEVE_API_KEY", "")

# PostHog analytics — fully optional, never blocks tool execution
try:
    from posthog import Posthog

    _posthog: Posthog | None = Posthog(
        "phc_wUjCwKWRPXHehqDY6jkzHxOgAYwgQXUm0aCO3mCjPGF",
        host="https://us.i.posthog.com",
    )
except Exception:
    _posthog = None


def _anonymous_user_id() -> str:
    """SHA-256 hash of the API key for anonymous usage tracking."""
    if not SIEVE_API_KEY:
        return "anonymous"
    return hashlib.sha256(SIEVE_API_KEY.encode()).hexdigest()[:16]

_BASE = "/api/v1/public"


def _headers() -> dict[str, str]:
    return {"X-API-Key": SIEVE_API_KEY, "Content-Type": "application/json"}


async def _request(
    method: str,
    path: str,
    *,
    json_body: dict[str, Any] | None = None,
    timeout: float = 15.0,
) -> dict[str, Any]:
    """Execute an HTTP request and return the JSON response or an error dict."""
    if not SIEVE_API_KEY:
        return {
            "error": "Missing API key",
            "detail": "Set the SIEVE_API_KEY environment variable. "
            "Get your key at https://app.sieve.arceusxventures.com/settings",
        }

    url = f"{SIEVE_API_URL.rstrip('/')}{_BASE}{path}"
    start = time.monotonic()
    result: dict[str, Any] = {}

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(
                method, url, headers=_headers(), json=json_body
            )
            response.raise_for_status()
            result = response.json()
            return result  # type: ignore[no-any-return]

    except httpx.HTTPStatusError as exc:
        try:
            body = exc.response.json()
        except Exception:
            body = exc.response.text
        result = {
            "error": f"HTTP {exc.response.status_code}",
            "detail": body,
        }
        return result

    except httpx.TimeoutException:
        result = {
            "error": "Request timed out",
            "detail": f"The request to {path} timed out after {timeout}s.",
        }
        return result

    except httpx.RequestError as exc:
        result = {
            "error": "Connection error",
            "detail": str(exc),
        }
        return result

    finally:
        duration_ms = round((time.monotonic() - start) * 1000)
        try:
            if _posthog is not None:
                _posthog.capture(
                    distinct_id=_anonymous_user_id(),
                    event="mcp_tool_called",
                    properties={
                        "tool": path.split("/")[1] if "/" in path else path,
                        "method": method,
                        "path": path,
                        "duration_ms": duration_ms,
                        "success": "error" not in result,
                        "error": result.get("error"),
                    },
                )
        except Exception:
            pass  # Never let analytics break the tool


async def screen(
    company_name: str,
    website_url: str = "",
    pitch_deck_text: str = "",
    description: str = "",
    confirm: bool = False,
) -> dict[str, Any]:
    """Start a Quick Screen analysis (upserts — rescreens if deal exists)."""
    body: dict[str, Any] = {"company_name": company_name}
    if website_url:
        body["website_url"] = website_url
    if pitch_deck_text:
        body["pitch_deck_text"] = pitch_deck_text
    if description:
        body["description"] = description
    if confirm:
        body["confirm"] = True
    return await _request("POST", "/screen", json_body=body, timeout=30.0)


async def status(deal_id: str) -> dict[str, Any]:
    """Check analysis progress."""
    return await _request("GET", f"/screen/{deal_id}/status")


async def results(deal_id: str, sections: str = "") -> dict[str, Any]:
    """Get full results of a completed analysis."""
    query = f"?sections={sections}" if sections else ""
    return await _request("GET", f"/screen/{deal_id}/results{query}")


async def usage() -> dict[str, Any]:
    """Check API usage for the current billing period."""
    return await _request("GET", "/usage")


async def deals(search: str = "", limit: int = 20) -> dict[str, Any]:
    """List/search deals in pipeline."""
    params = []
    if search:
        params.append(f"search={search}")
    if limit != 20:
        params.append(f"limit={limit}")
    query = f"?{'&'.join(params)}" if params else ""
    return await _request("GET", f"/deals{query}")


async def memo(deal_id: str, generate: bool = False, memo_type: str = "internal") -> dict[str, Any]:
    """Get or generate investment memo."""
    if generate:
        return await _request("POST", f"/deals/{deal_id}/memo", json_body={"type": memo_type}, timeout=60.0)
    return await _request("GET", f"/deals/{deal_id}/memo")


