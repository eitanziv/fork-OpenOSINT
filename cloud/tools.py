"""
OpenOSINT Cloud — tool dispatch for the gateway.

ALLOW_LIST is the single source of truth for the v1 synchronous tool set.
Every tool here must complete under the Heroku 30 s HTTP router limit
(TOOL_TIMEOUT_SECONDS = 25 s with headroom).

Adding a tool later: append one entry to ALLOW_LIST and update .env.example.
"""
from __future__ import annotations

import logging
from typing import Any, Callable, Coroutine

from cloud.config import TOOL_TIMEOUT_SECONDS
from openosint.json_output import format_tool_result
from openosint.tools.generate_dorks import run_dork_osint
from openosint.tools.search_abuseipdb import run_abuseipdb_osint
from openosint.tools.search_dns import run_dns_osint
from openosint.tools.search_github import run_github_osint
from openosint.tools.search_ip import run_ip_osint
from openosint.tools.search_ip2location import run_ip2location_osint
from openosint.tools.search_paste import run_paste_osint
from openosint.tools.search_whois import run_whois_osint

logger = logging.getLogger(__name__)

# Each value is a coroutine factory: (target: str, api_key: str | None) → Awaitable[str].
ALLOW_LIST: dict[str, Callable[[str, str | None], Coroutine[Any, Any, str]]] = {
    "search_ip":          lambda t, k: run_ip_osint(ip=t, timeout_seconds=TOOL_TIMEOUT_SECONDS, api_key=k),
    "search_whois":       lambda t, _: run_whois_osint(domain=t, timeout_seconds=TOOL_TIMEOUT_SECONDS),
    "search_github":      lambda t, k: run_github_osint(query=t, timeout_seconds=TOOL_TIMEOUT_SECONDS, api_key=k),
    "generate_dorks":     lambda t, _: run_dork_osint(target=t),
    "search_paste":       lambda t, _: run_paste_osint(query=t, timeout_seconds=TOOL_TIMEOUT_SECONDS),
    "search_dns":         lambda t, _: run_dns_osint(domain=t, timeout_seconds=TOOL_TIMEOUT_SECONDS),
    "search_abuseipdb":   lambda t, k: run_abuseipdb_osint(ip=t, timeout_seconds=TOOL_TIMEOUT_SECONDS, api_key=k),
    "search_ip2location": lambda t, k: run_ip2location_osint(ip=t, timeout_seconds=TOOL_TIMEOUT_SECONDS, api_key=k),
    # ── v1.1 (async job queue required — exceed Heroku 30 s router limit) ────
    # "search_email":    ...,   # holehe ~2–3 min
    # "search_username": ...,   # sherlock ~2–3 min
    # ── v1.1 (requires custom Heroku buildpack for Go / Python binary) ────────
    # "search_phone":    ...,   # phoneinfoga Go binary
    # "search_domain":   ...,   # sublist3r subprocess, 120 s default
    # ── v2 (paid upstream API keys required) ─────────────────────────────────
    # "search_breach":     ..., # HaveIBeenPwned paid key
    # "search_shodan":     ..., # Shodan paid key
    # "search_censys":     ..., # Censys paid key
    # "search_virustotal": ..., # VirusTotal paid key
    # "search_dorks_live": ..., # Bright Data paid
    # "scrape_url":        ..., # Bright Data paid
}


async def dispatch(tool: str, target: str, api_key: str | None = None) -> dict:
    """
    Run a tool from the allow-list and return a format_tool_result dict.

    Raises ValueError if tool is not in ALLOW_LIST.
    The caller is responsible for wrapping this in asyncio.wait_for.
    """
    if tool not in ALLOW_LIST:
        raise ValueError(f"Tool '{tool}' is not available in v1")
    raw = await ALLOW_LIST[tool](target, api_key)
    return format_tool_result(tool, target, raw)
