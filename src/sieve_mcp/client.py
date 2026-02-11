"""Thin async HTTP client for the Sieve Public API."""

import os
from typing import Any

import httpx

SIEVE_API_URL = os.environ.get(
    "SIEVE_API_URL", "https://api.sieve.arceusxventures.com"
)
SIEVE_API_KEY = os.environ.get("SIEVE_API_KEY", "")

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

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(
                method, url, headers=_headers(), json=json_body
            )
            response.raise_for_status()
            return response.json()  # type: ignore[no-any-return]

    except httpx.HTTPStatusError as exc:
        try:
            body = exc.response.json()
        except Exception:
            body = exc.response.text
        return {
            "error": f"HTTP {exc.response.status_code}",
            "detail": body,
        }

    except httpx.TimeoutException:
        return {
            "error": "Request timed out",
            "detail": f"The request to {path} timed out after {timeout}s.",
        }

    except httpx.RequestError as exc:
        return {
            "error": "Connection error",
            "detail": str(exc),
        }


async def screen(
    company_name: str,
    website_url: str = "",
    pitch_deck_text: str = "",
    description: str = "",
) -> dict[str, Any]:
    """Start a Quick Screen analysis."""
    body: dict[str, Any] = {"company_name": company_name}
    if website_url:
        body["website_url"] = website_url
    if pitch_deck_text:
        body["pitch_deck_text"] = pitch_deck_text
    if description:
        body["description"] = description
    return await _request("POST", "/screen", json_body=body, timeout=30.0)


async def status(analysis_id: str) -> dict[str, Any]:
    """Check analysis progress."""
    return await _request("GET", f"/analysis/{analysis_id}/status")


async def summary(analysis_id: str) -> dict[str, Any]:
    """Get full results of a completed analysis."""
    return await _request("GET", f"/analysis/{analysis_id}/summary")


async def usage() -> dict[str, Any]:
    """Check API usage for the current billing period."""
    return await _request("GET", "/usage")
