# TIA MCP Mock Server

A standalone mock server that returns realistic TIA Portal fixture data, enabling
development and testing of MCP-based workflows on **Linux** without TIA Portal, Windows,
or .NET dependencies.

## Quick Start

```bash
# Start the mock server on port 8001
cd /home/sarah/Documents/Projects/genius-automation-community
python3 mock/server.py --port 8001

# Test it
curl http://localhost:8001/health
curl -X POST http://localhost:8001/tools/list_blocks
```

## Why Mock Mode?

The real Genius Automation runs on **Windows 11** (VM at `192.168.37.156`) and requires:
- TIA Portal V21 with Openness API
- pythonnet (.NET interop)
- Windows user in "Siemens TIA Openness" group
- Interactive GUI session (SSH sessions can't connect)

The mock server runs **anywhere Python 3 runs** (Linux, macOS, WSL) with zero external
dependencies. This lets agents (Scribe, Studio, Scout) develop and test MCP tool workflows
without W11 access.

## Mock Data Scenario

All fixtures are based on a realistic **steel plant cold rolling line** (Linha de Laminação a Frio):

| Entity | Value |
|--------|-------|
| Project | `SteelPlant_Line3` |
| PLC | S7-1518 (`6ES7518-4AP00-0AB0`) |
| HMI | TP1500 Comfort Panel |
| Drive | Sinamics S120 (3.5 MW main mill) |
| IO Devices | 2× ET200SP via PROFINET |
| Blocks | 11 (OB1, OB35, OB100, FB10-FB50, FC100-FC300) |
| Tags | 556 across 5 tables |

## Available Tools (5)

### Community Tools (5)
| Tool | Description |
|------|-------------|
| `connect` | Establish a session with TIA Portal. Returns the mode used (`with_user_interface` / `without_user_interface`) and TIA Portal version detected. |
| `read_tags` | Read the current value of one or more tags from a PLC. If `tag_names` is omitted, all tags in the default tag table are returned. Read-only. |
| `list_blocks` | List all blocks in a given PLC inside the project. Returns block names, types (FB/FC/DB/OB), and metadata. Read-only. |
| `get_project_tree` | Get the hierarchical project tree: devices, software containers, block groups, tag tables. Read-only. |
| `compile` | Compile the current project (or a specific PLC). Returns errors and warnings. Does NOT modify the PLC runtime, only validates the offline project. |

> **Note:** The MIT Community Edition ships these 5 tools. The first one (`connect`) establishes
> a session with TIA Portal; the remaining four are strictly read-only or compile-only
> (no PLC runtime writes). The Pro Edition (commercial, BSL) extends this base with
> write-capable HW Config and Diagnostics tools (`open_project`, `close_project`,
> `save_project`, `list_devices`, `get_hardware_info`, `set_ip_address`, `compile_project`,
> and 12 more — 19 in total). The mock fixtures in this repo intentionally cover
> **only the 5 Community tools**.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Server info + endpoint list |
| GET | `/tools` | List all 5 tools with schemas |
| GET | `/health` | Health check (status, uptime, fixture count) |
| POST | `/tools/{name}` | Call a tool (body = JSON arguments) |

## Usage Examples

```bash
# Server info
curl http://localhost:8001/

# List all tools
curl http://localhost:8001/tools

# Call list_blocks (no arguments needed)
curl -X POST http://localhost:8001/tools/list_blocks

# Call read_tags with arguments
curl -X POST http://localhost:8001/tools/read_tags \
  -H 'Content-Type: application/json' \
  -d '{"plc": "PLC_1"}'

# Call get_project_tree with arguments
curl -X POST http://localhost:8001/tools/get_project_tree \
  -H 'Content-Type: application/json' \
  -d '{"max_depth": 3}'

# Call compile with arguments
curl -X POST http://localhost:8001/tools/compile \
  -H 'Content-Type: application/json' \
  -d '{"plc": "PLC_1"}'
```

## Architecture

```
Linux Agent (Scribe/Studio/Scout)
       ↓ HTTP/JSON
       ↓ port 8001
┌──────▼──────────────────┐
│  Mock MCP Server        │
│  (mock/server.py)       │
│                         │
│  Tool Registry (5)      │
│  Fixture Loader         │
│                         │
│  mock/fixtures/         │
│    connect.json         │
│    list_blocks.json     │
│    ... (5 files)        │
└─────────────────────────┘
```

The mock server uses Python's built-in `http.server` — **zero pip dependencies**.
Fixtures are plain JSON files that mirror the real MCP server's response format.

## Argument Override

For tools that accept parameters (like `read_tags`, `compile`), the mock server
intelligently merges the caller's arguments into the fixture data. This means:

```bash
# The response will show YOUR tag values, not the fixture default
curl -X POST http://localhost:8001/tools/read_tags \
  -d '{"plc": "PLC_1", "tag_names": ["Motor_Start", "Motor_Stop"]}'
# → returns only Motor_Start + Motor_Stop, values from fixture merged with override
```

## Integration with MCP Clients

To use the mock server as an MCP tool provider in your MCP client configuration:

```json
{
  "mcpServers": {
    "tia-portal-mock": {
      "url": "http://localhost:8001",
      "transport": "http"
    }
  }
}
```

## Files

```
mock/
├── __init__.py          # Package marker
├── server.py            # HTTP server + tool registry (main entry point)
├── fixtures/            # 5 JSON files with realistic steel plant data
│   ├── connect.json
│   ├── read_tags.json
│   ├── list_blocks.json
│   ├── get_project_tree.json
│   └── compile.json
└── README.md            # This file
```

## License

MIT — Same as parent project.

## Authors

Carlos Gomes & OpenClaw Team
