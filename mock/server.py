"""
Genius Automation Mock Server
=============================

A standalone MCP server that returns realistic fixture data instead of
calling the real TIA Portal Openness API. Runs on Linux without any
Windows/.NET dependencies.

Usage:
    python -m mock.server                          # Default port 8001
    python -m mock.server --port 8001              # Explicit port
    python -m mock.server --host 0.0.0.0           # Bind all interfaces
    python mock/server.py                          # Direct execution

Endpoints:
    GET  /               — Server info + tool list
    GET  /tools          — List all available tools
    POST /tools/{name}   — Call a tool (body = arguments JSON)
    GET  /health         — Health check
    SSE  /sse            — MCP SSE endpoint (optional)
"""
from __future__ import annotations

import argparse
import json
import logging
import time
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any, Dict, List, Optional

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

logger = logging.getLogger("genius-automation-mock")

try:
    PACKAGE_VERSION = version("genius-automation-community")
except PackageNotFoundError:
    PACKAGE_VERSION = "0+unknown"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

FIXTURES_DIR = Path(__file__).parent / "fixtures"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8001

# ---------------------------------------------------------------------------
# Tool registry — mirrors the real MCP server's 19 tools
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS: List[Dict[str, Any]] = [
    # --- Genius Automation Community Edition: 5 basic tools (MIT) ---
    {
        "name": "connect",
        "description": "Establish a session with TIA Portal. Required first call in any session. Returns the mode used (with_user_interface / without_user_interface) and TIA Portal version detected.",
        "input_schema": {
            "type": "object",
            "properties": {
                "mode": {
                    "type": "string",
                    "enum": ["with_user_interface", "without_user_interface", "attach"],
                    "default": "without_user_interface",
                    "description": "How to open the TIA Portal session. 'with_user_interface' requires a desktop session."
                },
            },
        },
    },
    {
        "name": "read_tags",
        "description": "Read the current value of one or more tags from a PLC. If tag_names is omitted, all tags in the default tag table are returned. Read-only.",
        "input_schema": {
            "type": "object",
            "required": ["plc"],
            "properties": {
                "plc": {"type": "string", "description": "PLC name (e.g. 'PLC_Steckel_Mill')."},
                "tag_names": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional whitelist of tag names to read."
                },
            },
        },
    },
    {
        "name": "list_blocks",
        "description": "List all blocks in a given PLC inside the project. Returns block names, types (FB/FC/DB/OB), and metadata. Read-only.",
        "input_schema": {
            "type": "object",
            "required": ["plc"],
            "properties": {
                "plc": {"type": "string", "description": "PLC name (e.g. 'PLC_1')."},
            },
        },
    },
    {
        "name": "get_project_tree",
        "description": "Get the hierarchical project tree: devices, software containers, block groups, tag tables. Read-only.",
        "input_schema": {
            "type": "object",
            "properties": {
                "max_depth": {
                    "type": "integer",
                    "default": 5,
                    "minimum": 1,
                    "maximum": 10,
                    "description": "Maximum depth of the returned tree (1-10, default 5).",
                },
            },
        },
    },
    {
        "name": "compile",
        "description": "Compile the current project (or a specific PLC). Returns errors and warnings. Does NOT modify the PLC runtime, only validates the offline project.",
        "input_schema": {
            "type": "object",
            "properties": {
                "plc": {"type": "string", "description": "Omit to compile the entire project. Otherwise compile only this PLC."},
            },
        },
    },
]

TOOL_NAMES = {t["name"] for t in TOOL_DEFINITIONS}


# ---------------------------------------------------------------------------
# Fixture loader
# ---------------------------------------------------------------------------

def load_fixture(tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Load a fixture file for the given tool name.

    If the tool accepts arguments that affect the fixture (e.g. plc_name),
    the fixture data is annotated with the provided arguments so it feels
    realistic to the caller.
    """
    fixture_path = FIXTURES_DIR / f"{tool_name}.json"

    if not fixture_path.is_file():
        return {
            "error": f"No fixture available for tool '{tool_name}'",
            "tool": tool_name,
            "available_fixtures": sorted(f.stem for f in FIXTURES_DIR.glob("*.json")),
        }

    try:
        data = json.loads(fixture_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"error": f"Fixture parse error: {exc}", "tool": tool_name}

    # Annotate with caller's arguments (for tools that take parameters)
    if arguments:
        # For set_ip_address: override with actual requested values
        if tool_name == "set_ip_address":
            data["changed"]["ip_address"] = arguments.get("ip_address", data["changed"].get("ip_address"))
            data["changed"]["subnet_mask"] = arguments.get("subnet_mask", data["changed"].get("subnet_mask"))
            if arguments.get("gateway"):
                data["changed"]["gateway"] = arguments["gateway"]
        # For add_module: override with actual requested values
        elif tool_name == "add_module":
            data["plc_name"] = arguments.get("plc_name", data.get("plc_name"))
            data["module_identifier"] = arguments.get("module_identifier", data.get("module_identifier"))
            data["position"] = arguments.get("position", data.get("position"))
        # For remove_module: override
        elif tool_name == "remove_module":
            data["plc_name"] = arguments.get("plc_name", data.get("plc_name"))
            if arguments.get("module_name"):
                data["removed_module"] = arguments["module_name"]
        # For configure_plc: merge changed fields
        elif tool_name == "configure_plc":
            data["plc_name"] = arguments.get("plc_name", data.get("plc_name"))
        # For configure_profinet: override action
        elif tool_name == "configure_profinet":
            action = arguments.get("action", "list_devices")
            data["action"] = action
            data["plc_name"] = arguments.get("plc_name", data.get("plc_name"))
        # For create_library: override with actual requested values
        elif tool_name == "create_library":
            data["name"] = arguments.get("name", data.get("name"))
            data["version"] = arguments.get("version", data.get("version", "0.1.0"))
            if arguments.get("description"):
                data["description"] = arguments["description"]
        # For add_to_library: override with actual requested values
        elif tool_name == "add_to_library":
            data["library_name"] = arguments.get("library_name", data.get("library_name"))
            data["added_object"] = arguments.get("object_name", data.get("added_object"))
            data["source_plc"] = arguments.get("plc_name", data.get("source_plc"))
        # For publish_library_version: compute new version
        elif tool_name == "publish_library_version":
            import copy
            prev = data.get("previous_version", "1.3.0")
            bump = arguments.get("bump", "patch")
            explicit = arguments.get("version")
            if explicit:
                data["new_version"] = explicit
                data["bump_type"] = "explicit"
            else:
                major, minor, patch = [int(x) for x in prev.split(".")]
                if bump == "major":
                    data["new_version"] = f"{major + 1}.0.0"
                elif bump == "minor":
                    data["new_version"] = f"{major}.{minor + 1}.0"
                else:
                    data["new_version"] = f"{major}.{minor}.{patch + 1}"
                data["bump_type"] = bump
            data["previous_version"] = prev
            data["library_name"] = arguments.get("library_name", data.get("library_name"))
            if arguments.get("changelog"):
                data["changelog"] = arguments["changelog"]
        # For list_libraries: filter by type
        elif tool_name == "list_libraries":
            lib_type = arguments.get("library_type", "all")
            if lib_type != "all":
                data["libraries"] = [l for l in data.get("libraries", []) if l.get("type") == lib_type]
                data["count"] = len(data["libraries"])
            data["filter"] = lib_type

    # Add mock metadata
    data["_mock"] = True
    data["_mock_timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    return data


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------

class MockMCPServerHandler(BaseHTTPRequestHandler):
    """HTTP handler that serves mock MCP tool responses."""

    server_version = f"Genius-Automation-Mock/{PACKAGE_VERSION}"

    def _send_json(self, status_code: int, payload: Any) -> None:
        body = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        try:
            raw = self.rfile.read(length)
            return json.loads(raw) if raw.strip() else {}
        except (json.JSONDecodeError, ValueError):
            return {"_error": "Invalid JSON body"}

    def do_OPTIONS(self) -> None:
        self._send_json(204, {})

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"

        if path == "/" or path == "/info":
            self._send_json(200, {
                "server": "Genius Automation Mock Server",
                "version": PACKAGE_VERSION,
                "mode": "mock",
                "project": "SteelPlant_Line3 (mock)",
                "tool_count": len(TOOL_DEFINITIONS),
                "endpoints": {
                    "GET /": "This info page",
                    "GET /tools": "List all available tools",
                    "POST /tools/{name}": "Call a tool with JSON arguments",
                    "GET /health": "Health check",
                },
                "note": "All responses are mock data from fixtures/. No TIA Portal connection.",
            })
        elif path == "/tools":
            self._send_json(200, {
                "tools": [
                    {
                        "name": t["name"],
                        "description": t["description"],
                        "input_schema": t["input_schema"],
                    }
                    for t in TOOL_DEFINITIONS
                ],
                "count": len(TOOL_DEFINITIONS),
            })
        elif path == "/health":
            self._send_json(200, {
                "status": "healthy",
                "server": "genius-automation-mock",
                "mode": "mock",
                "fixtures_loaded": len(list(FIXTURES_DIR.glob("*.json"))),
                "uptime_seconds": round(time.time() - self.server._start_time, 1),  # type: ignore
            })
        else:
            self._send_json(404, {"error": f"Not found: {path}"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        parts = parsed.path.strip("/").split("/")

        # Pattern: /tools/{tool_name}
        if len(parts) == 2 and parts[0] == "tools":
            tool_name = parts[1]

            if tool_name not in TOOL_NAMES:
                self._send_json(404, {
                    "error": f"Unknown tool: '{tool_name}'",
                    "available_tools": sorted(TOOL_NAMES),
                })
                return

            arguments = self._read_body()
            logger.info("Tool call: %s args=%s", tool_name, list(arguments.keys()))

            result = load_fixture(tool_name, arguments)
            self._send_json(200, result)
        else:
            self._send_json(404, {"error": f"Unknown endpoint: POST {parsed.path}"})

    def log_message(self, format: str, *args: Any) -> None:
        # Custom log format
        logger.info("%s - %s", self.address_string(), format % args)


# ---------------------------------------------------------------------------
# Server startup
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Genius Automation Mock Server — returns fixture data on Linux"
    )
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"Bind host (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port (default: {DEFAULT_PORT})")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # Validate fixtures
    fixture_files = sorted(f.stem for f in FIXTURES_DIR.glob("*.json"))
    missing = TOOL_NAMES - set(fixture_files)
    if missing:
        logger.warning("Missing fixtures for tools: %s", sorted(missing))

    logger.info("Genius Automation Mock Server starting on %s:%d", args.host, args.port)
    logger.info("Fixtures directory: %s", FIXTURES_DIR)
    logger.info("Fixtures loaded: %d/%d tools", len(fixture_files), len(TOOL_DEFINITIONS))
    logger.info("Tool registry: %d tools", len(TOOL_DEFINITIONS))

    server = HTTPServer((args.host, args.port), MockMCPServerHandler)
    server._start_time = time.time()  # type: ignore

    banner_host = f"http://{args.host}:{args.port}"
    fixture_info = f"{len(fixture_files)}/{len(TOOL_DEFINITIONS)} fixtures loaded"
    print()
    print("╔══════════════════════════════════════════════════╗")
    print("║  Genius Automation Mock Server                   ║")
    print(f"║  Listening: {banner_host:<37s}║")
    print("║  Mode: MOCK (no TIA Portal connection)          ║")
    print(f"║  Tools: {fixture_info:<40s}║")
    print("╚══════════════════════════════════════════════════╝")
    print(f"\nEndpoints:")
    print(f"  GET  /            — Server info")
    print(f"  GET  /tools       — List all tools")
    print(f"  POST /tools/{{name}} — Call a tool")
    print(f"  GET  /health      — Health check")
    print(f"\nExample:")
    print(f"  curl -X POST http://localhost:{args.port}/tools/list_devices")
    print(f"  curl -X POST http://localhost:{args.port}/tools/get_block_code \\")
    print(f"       -H 'Content-Type: application/json' \\")
    print(f"       -d '{{\"block_name\": \"FB10_Steckel_Control\"}}'\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()
        print("Server stopped.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
