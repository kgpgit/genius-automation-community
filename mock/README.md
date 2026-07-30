# TIA MCP Mock Server

A standalone mock server that returns realistic TIA Portal fixture data, enabling
development and testing of MCP-based workflows on **Linux** without TIA Portal, Windows,
or .NET dependencies.

## Quick Start

```bash
# Start the mock server on port 8001
cd /home/sarah/Documents/Projects/TIA-Automation/genius-automation
python3 mock/server.py --port 8001

# Test it
curl http://localhost:8001/health
curl -X POST http://localhost:8001/tools/list_devices
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

## Available Tools (19)

### Base Tools (7)
| Tool | Description |
|------|-------------|
| `open_project` | Open a .ap21 project file |
| `close_project` | Close current project |
| `get_project_tree` | Hierarchical tree of devices, blocks, tags |
| `get_tag_table` | List PLC tags from a tag table |
| `get_block_code` | Source code, interface, metadata of a block |
| `compile_project` | Compile project/PLC, return errors |
| `save_project` | Save project to disk |

### HW Config Tools (7)
| Tool | Description |
|------|-------------|
| `list_devices` | List all devices (PLC, HMI, Drive) |
| `get_hardware_info` | Detailed module/rack configuration |
| `set_ip_address` | Set PROFINET IP address |
| `configure_plc` | Set rack, slot, station name |
| `add_module` | Add I/O module from hardware catalog |
| `remove_module` | Remove module by name or slot |
| `configure_profinet` | List/add/remove PROFINET IO devices |

### Diagnostics Tools (5)
| Tool | Description |
|------|-------------|
| `get_compile_errors` | Detailed compile diagnostics |
| `get_online_status` | PLC connection + CPU state (RUN/STOP) |
| `read_diagnostic_buffer` | PLC event log (diagnostic buffer) |
| `compare_online_offline` | Diff online vs offline blocks/config |
| `upload_from_device` | Upload blocks from PLC to project |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Server info + endpoint list |
| GET | `/tools` | List all 19 tools with schemas |
| GET | `/health` | Health check (status, uptime, fixture count) |
| POST | `/tools/{name}` | Call a tool (body = JSON arguments) |

## Usage Examples

```bash
# Server info
curl http://localhost:8001/

# List all tools
curl http://localhost:8001/tools

# Call list_devices (no arguments needed)
curl -X POST http://localhost:8001/tools/list_devices

# Call get_block_code with arguments
curl -X POST http://localhost:8001/tools/get_block_code \
  -H 'Content-Type: application/json' \
  -d '{"block_name": "FB10_Steckel_Control"}'

# Call get_online_status
curl -X POST http://localhost:8001/tools/get_online_status \
  -H 'Content-Type: application/json' \
  -d '{"plc_name": "PLC_Steckel_Mill"}'

# Set IP address (arguments override fixture defaults)
curl -X POST http://localhost:8001/tools/set_ip_address \
  -H 'Content-Type: application/json' \
  -d '{"device_name": "PLC_Steckel_Mill", "ip_address": "10.0.0.50"}'
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
│  Tool Registry (19)     │
│  Fixture Loader         │
│                         │
│  mock/fixtures/         │
│    open_project.json    │
│    list_devices.json    │
│    ... (19 files)       │
└─────────────────────────┘
```

The mock server uses Python's built-in `http.server` — **zero pip dependencies**.
Fixtures are plain JSON files that mirror the real MCP server's response format.

## Argument Override

For tools that accept parameters (like `set_ip_address`, `add_module`), the mock server
intelligently merges the caller's arguments into the fixture data. This means:

```bash
# The response will show YOUR ip_address, not the fixture default
curl -X POST http://localhost:8001/tools/set_ip_address \
  -d '{"device_name": "PLC", "ip_address": "10.99.99.99"}'
# → changed: {"ip_address": "10.99.99.99", "subnet_mask": "255.255.255.0"}
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
├── fixtures/            # 19 JSON files with realistic steel plant data
│   ├── open_project.json
│   ├── close_project.json
│   ├── get_project_tree.json
│   ├── get_tag_table.json
│   ├── get_block_code.json
│   ├── compile_project.json
│   ├── save_project.json
│   ├── list_devices.json
│   ├── get_hardware_info.json
│   ├── set_ip_address.json
│   ├── configure_plc.json
│   ├── add_module.json
│   ├── remove_module.json
│   ├── configure_profinet.json
│   ├── get_compile_errors.json
│   ├── get_online_status.json
│   ├── read_diagnostic_buffer.json
│   ├── compare_online_offline.json
│   └── upload_from_device.json
└── README.md            # This file
```

## License

MIT — Same as parent project.

## Authors

Carlos Gomes & OpenClaw Team
