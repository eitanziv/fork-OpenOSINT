# OPENOSINT(1) - General Commands Manual

## NAME
**openosint** — Model Context Protocol (MCP) server and CLI for Open Source Intelligence.

## SYNOPSIS
**openosint** [**-h**] [**-v**] *command* [*args ...*]

## DESCRIPTION
**openosint** is a modular framework designed to bridge the gap between Large Language Models (LLMs) and OSINT methodologies. By implementing the Model Context Protocol (MCP), it enables AI agents to perform autonomous investigations with high-fidelity tool access.

The framework is built on a non-blocking asynchronous architecture (Python `asyncio`), ensuring that long-running intelligence gathering tasks do not interrupt the agent's reasoning process.

## ARCHITECTURE
The project follows a strict three-tier architecture:

1.  **Core Modules (`openosint/tools/`):** Isolated, task-specific Python wrappers for external OSINT binaries and APIs.
2.  **MCP Server (`openosint/mcp_server.py`):** A standardized gateway that translates core capabilities into LLM-readable tool schemas.
3.  **CLI Interface (`openosint/cli.py`):** A traditional command-line utility for manual human verification and direct execution.

## INSTALLATION
OpenOSINT 2.0.0 is PEP 621 compliant and requires Python 3.10 or higher.

### From Source (Recommended)
```bash
git clone [https://github.com/tuo-username/OpenOSINT.git](https://github.com/tuo-username/OpenOSINT.git)
cd OpenOSINT
pip install -e .

```

### Dependencies

The framework automatically manages the following core dependencies:

* **mcp**: The Anthropic Model Context Protocol SDK.
* **holehe**: Email OSINT tool (must be available in the system PATH).

## CONFIGURATION (AI AGENTS)

To utilize OpenOSINT with **Claude Code** or other MCP-compliant clients, register the server by providing the absolute path to the entry point:

```bash
claude mcp add openosint python /absolute/path/to/openosint/mcp_server.py

```

## USAGE EXAMPLES

Direct manual execution via the system command:

```bash
openosint email target@example.com --timeout 60

```

Agentic execution via Claude Code (after registration):

```bash
claude
> "Investigate target@example.com and summarize findings."

```

## EXIT STATUS

**openosint** exits with one of the following values:

* **0**: Successful execution.
* **1**: General error (invalid parameters or tool failure).
* **130**: Operation terminated by user (SIGINT).

## FILES

* `openosint/mcp_server.py`: Standard I/O MCP server implementation.
* `openosint/cli.py`: Main entry point for the global command-line tool.
* `openosint/tools/`: Directory containing specific OSINT logic modules.
* `pyproject.toml`: Project metadata and dependency definitions.

## AUTHORS

Developed by Tommaso.

## LICENSE

Released under the MIT License.