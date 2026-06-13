"""
OpenOSINT Cloud — per-tool key-source configuration.

KeySource controls where /v1/enrich resolves the upstream API key:
  server            — server's own env var (sponsored / included perk)
  customer          — customer's stored BYOK key (required — 422 if absent)
  customer_optional — customer's stored key when present, else call unauth
  none              — tool needs no credential

To move a tool between server-provided and customer-provided, change its
entry here.  No other files need to change.

Canonical provider strings (used by POST /v1/keys and 422 messages):
  "ipinfo"      — ipinfo.io token (search_ip)
  "abuseipdb"   — AbuseIPDB API key (search_abuseipdb)
  "github"      — GitHub personal access token (search_github, optional)
"""
from __future__ import annotations

from enum import Enum
from typing import NamedTuple


class KeySource(str, Enum):
    server = "server"
    customer = "customer"
    customer_optional = "customer_optional"
    none = "none"


class ToolKeyConfig(NamedTuple):
    env_var: str | None      # server env-var name; None when source is customer/none
    source: KeySource
    provider: str | None     # canonical customer-facing provider string; None for server/none tools


# Single source of truth for v1 tool credentials.
TOOL_KEY_CONFIG: dict[str, ToolKeyConfig] = {
    # Sponsored — key is server-provided; customers get this included.
    "search_ip2location": ToolKeyConfig("IP2LOCATION_API_KEY", KeySource.server,            provider=None),
    # BYOK required — customer must POST /v1/keys with the provider string below.
    "search_ip":          ToolKeyConfig("IPINFO_TOKEN",        KeySource.customer,          provider="ipinfo"),
    "search_abuseipdb":   ToolKeyConfig("ABUSEIPDB_API_KEY",   KeySource.customer,          provider="abuseipdb"),
    # Optional BYOK — works unauth at 60 req/h; better with token at 5 000 req/h.
    "search_github":      ToolKeyConfig("GITHUB_TOKEN",        KeySource.customer_optional, provider="github"),
    # No credential required.
    "generate_dorks":     ToolKeyConfig(None,                  KeySource.none,              provider=None),
    "search_dns":         ToolKeyConfig(None,                  KeySource.none,              provider=None),
    "search_whois":       ToolKeyConfig(None,                  KeySource.none,              provider=None),
    "search_paste":       ToolKeyConfig(None,                  KeySource.none,              provider=None),
}
