# openosint/regexes.py
"""Shared compiled regular expressions used across the package."""

import re

# Strict anchored match — validates that the entire string is an email address.
EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[a-z]{2,}$", re.IGNORECASE)

# Search-in-string variant — extracts email addresses embedded in larger text.
EMAIL_FIND_RE = re.compile(r"[\w.+-]+@[\w-]+\.[a-z]{2,}")
