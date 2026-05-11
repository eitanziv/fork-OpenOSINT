# openosint/cli.py
"""
OpenOSINT command-line interface.

Default behaviour  : launches the interactive REPL (Claude Code style).
Subcommands        : direct tool execution without AI (email, username).

Usage:
    openosint                          # interactive REPL
    openosint email target@example.com # direct, no AI
    openosint username johndoe99       # direct, no AI
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from openosint.tools.search_email import run_email_osint
from openosint.tools.search_username import run_username_osint

_DIVIDER = "=" * 60


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(level=level, format="[%(levelname)s] %(name)s: %(message)s")


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openosint",
        description=(
            "OpenOSINT — AI-powered OSINT framework.\n"
            "Run without arguments to start the interactive REPL."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  openosint                           # interactive AI session\n"
            "  openosint email target@example.com  # direct email scan\n"
            "  openosint username johndoe99        # direct username scan\n"
        ),
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug-level logging.",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        metavar="KEY",
        help="Anthropic API key (overrides ANTHROPIC_API_KEY env var).",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="command")

    # shell subcommand (explicit alias for REPL)
    subparsers.add_parser(
        "shell",
        help="Start the interactive REPL (default when no command given).",
    )

    # email subcommand
    email_cmd = subparsers.add_parser(
        "email",
        help="Direct email scan via holehe (no AI).",
    )
    email_cmd.add_argument("target", type=str, metavar="ADDRESS")
    email_cmd.add_argument(
        "-t", "--timeout",
        type=int,
        default=120,
        metavar="SECONDS",
        help="Maximum execution time (default: 120).",
    )

    # username subcommand
    username_cmd = subparsers.add_parser(
        "username",
        help="Direct username scan via sherlock (no AI).",
    )
    username_cmd.add_argument("target", type=str, metavar="USERNAME")
    username_cmd.add_argument(
        "-t", "--timeout",
        type=int,
        default=180,
        metavar="SECONDS",
        help="Maximum execution time (default: 180).",
    )

    return parser


# ---------------------------------------------------------------------------
# Direct command handlers (no AI)
# ---------------------------------------------------------------------------

def _print_result(result: str) -> None:
    print(_DIVIDER)
    print(" SCAN RESULTS ".center(60, "="))
    print(_DIVIDER)
    print(result)
    print(_DIVIDER)


async def _handle_email(target: str, timeout: int) -> None:
    print(f"[*] Email scan: {target}")
    print(f"[*] Timeout: {timeout}s\n")
    result = await run_email_osint(email=target, timeout_seconds=timeout)
    _print_result(result)


async def _handle_username(target: str, timeout: int) -> None:
    print(f"[*] Username scan: {target}")
    print(f"[*] Timeout: {timeout}s\n")
    result = await run_username_osint(username=target, timeout_seconds=timeout)
    _print_result(result)


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------

async def _async_main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    _configure_logging(args.verbose)

    # No subcommand or explicit 'shell' → launch REPL
    if args.command in (None, "shell"):
        from openosint.repl import run_repl
        run_repl(api_key=getattr(args, "api_key", None))
        return

    if args.command == "email":
        await _handle_email(args.target, args.timeout)
    elif args.command == "username":
        await _handle_username(args.target, args.timeout)
    else:
        parser.print_help()
        sys.exit(1)


def main() -> None:
    """Synchronous entry point registered in pyproject.toml."""
    try:
        asyncio.run(_async_main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted.", file=sys.stderr)
        sys.exit(130)
    except Exception as exc:
        print(f"[!] Fatal: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
