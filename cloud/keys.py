"""
OpenOSINT Cloud — encrypted customer key storage.

Secrets are encrypted at rest with Fernet symmetric encryption.
CONFIG_ENCRYPTION_KEY must be set when DATABASE_URL is set (production).
In test / in-memory mode an ephemeral key is generated automatically.

Generate a production key:
    python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
"""
from __future__ import annotations

import os

from cryptography.fernet import Fernet

from cloud import db

# In-memory store for tests: (api_key, provider) → encrypted bytes
_MEMORY_KEYS: dict[tuple[str, str], bytes] = {}

_fernet: Fernet | None = None


def _get_fernet() -> Fernet:
    global _fernet
    if _fernet is not None:
        return _fernet
    raw_key = os.environ.get("CONFIG_ENCRYPTION_KEY", "")
    if not raw_key:
        if os.environ.get("DATABASE_URL", ""):
            raise RuntimeError(
                "CONFIG_ENCRYPTION_KEY is required when DATABASE_URL is set. "
                "Generate: python -c \"from cryptography.fernet import Fernet; "
                "print(Fernet.generate_key().decode())\""
            )
        # In-memory / test mode — ephemeral key, never persisted
        raw_key = Fernet.generate_key().decode()
    _fernet = Fernet(raw_key.encode())
    return _fernet


def init_keys() -> None:
    """Validate and cache the Fernet cipher at app startup — fails fast in production."""
    _get_fernet()


def mask(secret: str) -> str:
    """Return '****' + last 4 chars.  Short secrets (≤4 chars) return only '****'."""
    if len(secret) <= 4:
        return "****"
    return "****" + secret[-4:]


def _encrypt(plaintext: str) -> str:
    return _get_fernet().encrypt(plaintext.encode()).decode()


def _decrypt(ciphertext: str) -> str:
    return _get_fernet().decrypt(ciphertext.encode()).decode()


async def store_key(api_key: str, provider: str, secret: str) -> None:
    """Encrypt and upsert a customer's provider key."""
    ciphertext = _encrypt(secret)
    if db._is_memory_mode():
        _MEMORY_KEYS[(api_key, provider)] = ciphertext.encode()
        return
    await db._pool.execute(
        """
        INSERT INTO customer_keys (api_key, provider, secret_encrypted)
        VALUES ($1, $2, $3)
        ON CONFLICT (api_key, provider)
        DO UPDATE SET secret_encrypted = EXCLUDED.secret_encrypted,
                      created_at       = NOW()
        """,
        api_key,
        provider,
        ciphertext,
    )


async def get_key(api_key: str, provider: str) -> str | None:
    """Return the decrypted key for (api_key, provider), or None if not stored."""
    if db._is_memory_mode():
        raw = _MEMORY_KEYS.get((api_key, provider))
        return _decrypt(raw.decode()) if raw is not None else None
    row = await db._pool.fetchrow(
        "SELECT secret_encrypted FROM customer_keys WHERE api_key = $1 AND provider = $2",
        api_key,
        provider,
    )
    return _decrypt(row["secret_encrypted"]) if row is not None else None


async def list_keys(api_key: str) -> list[dict[str, str]]:
    """Return all stored providers for api_key with masked secrets (last 4 only)."""
    if db._is_memory_mode():
        return [
            {"provider": prov, "masked": mask(_decrypt(ct.decode()))}
            for (k, prov), ct in _MEMORY_KEYS.items()
            if k == api_key
        ]
    rows = await db._pool.fetch(
        "SELECT provider, secret_encrypted FROM customer_keys WHERE api_key = $1",
        api_key,
    )
    return [
        {"provider": row["provider"], "masked": mask(_decrypt(row["secret_encrypted"]))}
        for row in rows
    ]


async def delete_key(api_key: str, provider: str) -> bool:
    """Delete a stored key. Returns True if a row was deleted."""
    if db._is_memory_mode():
        key_tuple = (api_key, provider)
        if key_tuple not in _MEMORY_KEYS:
            return False
        del _MEMORY_KEYS[key_tuple]
        return True
    result = await db._pool.execute(
        "DELETE FROM customer_keys WHERE api_key = $1 AND provider = $2",
        api_key,
        provider,
    )
    return result != "DELETE 0"
