# Genius Automation — Community Edition

> **MCP server for Siemens TIA Portal — open-core, MIT-licensed Community Edition.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-compatible-green.svg)](https://modelcontextprotocol.io/)

---

## 🎯 What is Genius Automation?

Genius Automation is a **Model Context Protocol (MCP) server** that lets AI agents (Claude Code, OpenClaw, Cursor, etc.) control **Siemens TIA Portal V17+** — the leading industrial automation software used in factories worldwide.

This **Community Edition** ships with **5 essential read-only tools** under the **MIT License** — free to use in commercial and non-commercial projects.

For the full **Pro / Enterprise Edition** (39 tools including write operations, multi-vendor, SLA), see: [genius-automation-pro](https://github.com/your-org/genius-automation-pro) (private).

---

## ✨ Available Tools (Community Edition)

This Community Edition exposes **5 tools**, all read-only and safe for production use:

| Tool | Description |
|------|-------------|
| `connect` | Establish a session with TIA Portal. Required first call in any session. |
| `read_tags` | Read current values of one or more tags from a PLC. |
| `list_blocks` | List all blocks (OB/FB/FC/DB) in a given PLC. |
| `get_project_tree` | Get the hierarchical project tree: devices, block groups, tag tables. |
| `compile` | Compile the project (or a specific PLC) and return errors/warnings. **Does NOT modify the PLC runtime** — only validates the offline project. |

For write operations (create/edit blocks, write tags, HMI screens, library management, advanced diagnostics, batch operations), upgrade to **Pro** (below).

---

## 🚀 Quick Start (3 steps)

### Step 1 — Install

```powershell
# Windows (with TIA Portal installed)
git clone https://github.com/your-org/genius-automation-community.git
cd genius-automation-community
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

```bash
# Linux/macOS (mock server only, no TIA Portal)
git clone https://github.com/your-org/genius-automation-community.git
cd genius-automation-community
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Step 2 — Run the Mock Server (Linux/macOS)

For testing without TIA Portal:

```bash
python -m mock.server --port 8001
```

Output:
```
╔══════════════════════════════════════════════════╗
║  Genius Automation Mock Server                   ║
║  Listening: http://0.0.0.0:8001                  ║
║  Mode: MOCK (no TIA Portal connection)            ║
║  Tools: 5/5 fixtures loaded                       ║
╚══════════════════════════════════════════════════╝
```

### Step 3 — Connect from Your AI Agent

Configure your MCP-compatible agent (Claude Code, OpenClaw, Cursor) to point at the server:

```json
{
  "mcpServers": {
    "genius-automation": {
      "command": "python",
      "args": ["-m", "mock.server"],
      "env": {"PORT": "8001"}
    }
  }
}
```

Then in the agent:
> "List all blocks in PLC_1" → calls `list_blocks`
> "Read the motor speed tag" → calls `read_tags`
> "Compile the project and show errors" → calls `compile`

---

## 🏗 Architecture

```
┌─────────────────┐
│  AI Agent       │  (Claude Code, OpenClaw, Cursor, …)
│  (Linux/Mac)    │
└────────┬────────┘
         │ MCP protocol (HTTP/SSE)
         │
┌────────▼────────┐
│  W11 VM         │
│  (Windows)      │
│                 │
│  ┌───────────┐  │
│  │ MCP Server│  │  ← this repo
│  │ (Python)  │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │ pythonnet │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │ TIA Portal│  │  (Siemens software, V17+)
│  │  V17+     │  │
│  └───────────┘  │
└─────────────────┘
```

The MCP server runs on the **same Windows machine as TIA Portal** (because TIA Portal Openness requires Windows + .NET Framework 4.8). AI agents on Linux/macOS connect over the network via MCP.

---

## 🛠 Tools (Community Edition)

### 1. `connect`

Establish a session with a running TIA Portal instance. Required as the first call in any session.

**Input:**
```json
{"mode": "without_user_interface"}
```

**Output:**
```json
{
  "status": "connected",
  "tia_version": "V21",
  "mode": "without_user_interface",
  "openness_version": "V21.0.2",
  "session_id": "mock-session-12345"
}
```

### 2. `read_tags`

Read the current value of one or more tags from a PLC. Read-only.

**Input:**
```json
{
  "plc": "PLC_1",
  "tag_names": ["Motor_Start", "Motor_Speed"]
}
```

**Output:**
```json
{
  "plc": "PLC_1",
  "tags": [
    {"name": "Motor_Start", "address": "%I0.0", "data_type": "Bool", "value": false},
    {"name": "Motor_Speed", "address": "%MW10", "data_type": "Int", "value": 1450}
  ],
  "count": 2
}
```

### 3. `list_blocks`

List all blocks in a given PLC inside the project. Returns block names, types, languages, and metadata. Read-only.

**Input:**
```json
{"plc": "PLC_1"}
```

**Output:**
```json
{
  "plc": "PLC_1",
  "blocks": [
    {"name": "OB1", "type": "OB", "number": 1, "language": "FBD"},
    {"name": "FB10_Steckel_Control", "type": "FB", "number": 10, "language": "SCL"},
    ...
  ],
  "count": 8
}
```

### 4. `get_project_tree`

Get the hierarchical project tree: devices, software containers, block groups, tag tables. Read-only.

**Input:**
```json
{"max_depth": 5}
```

**Output:** hierarchical JSON tree of the project structure.

### 5. `compile`

Compile the current project (or a specific PLC) and return errors/warnings. **Does NOT modify the PLC runtime** — only validates the offline project.

**Input:**
```json
{"plc": "PLC_1"}  // optional
```

**Output:**
```json
{
  "overall_state": "success",
  "devices": [
    {"plc_name": "PLC_1", "state": "success", "errors": 0, "warnings": 2}
  ],
  "errors": [],
  "warnings": [
    {"plc_name": "PLC_1", "block": "FB20", "code": "W001", "message": "Unused variable"}
  ]
}
```

---

## 💎 Upgrade to Pro / Enterprise

For **write operations**, **HMI**, **library management**, **advanced diagnostics**, and **multi-vendor support**, upgrade to the Pro Edition.

| Tier | Tools | License | Price | Use case |
|------|:-----:|---------|-------|----------|
| **Community** | 5 (read-only) | MIT | **Free** | Hobby, evaluation, read-only workflows |
| **Pro** | 39 (read + write) | Proprietary | **$29/mo** (R$ 149) | Professional work, freelancers |
| **Enterprise** | 39 + multi-vendor | Proprietary | **$199/mo** (R$ 999) | Companies, Rockwell/CODESYS, SLA |

**Pro tools include everything in Community, plus:**

- **Block CRUD**: `create_plc`, `import_blocks`, `export_blocks`
- **Tag write**: `write_tags`
- **Hardware**: `add_module`, `remove_module`, `configure_plc`, `configure_profinet`, `set_ip_address`, `list_devices`, `get_hardware_info`
- **Diagnostics**: `get_compile_errors`, `get_online_status`, `read_diagnostic_buffer`, `compare_online_offline`, `upload_from_device`, `get_plc_info`, `read_force_table`, `get_module_diagnostics`, `get_profinet_topology`, `get_security_info`
- **Library**: `list_libraries`, `create_library`, `get_library_info`, `add_to_library`, `publish_library_version`
- **HMI / SCADA**: `create_hmi_screen`, `add_screen_element`, `link_tag_to_screen`, `configure_alarm`, `export_hmi_xml`
- **Capture**: `capture_project_tree`, `capture_tag_table`, `capture_hardware_config`, `capture_watch_table`, `capture_screen`
- **Batch**: `batch_capture_all_blocks`, `batch_import_from_excel`, `generate_project_summary`, `project_audit_report`, `batch_export_format`
- **Multi-vendor** (Enterprise): Rockwell Studio 5000, CODESYS, Beckhoff TwinCAT

👉 See [genius-automation-pro](https://github.com/your-org/genius-automation-pro) (private, $29/mo).

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to file bug reports
- How to suggest features
- How to submit pull requests
- Code style and testing requirements
- Translation guidelines

**Quick links:**
- 🐛 [Issues](https://github.com/your-org/genius-automation-community/issues)
- 💬 [Discussions](https://github.com/your-org/genius-automation-community/discussions)
- 📧 contato@plccursos.com.br

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE).

The Community Edition is **open-core**: the 5 basic tools are MIT-licensed, while advanced functionality (39 tools) lives in the proprietary **Pro / Enterprise Editions**.

---

## 🌟 Acknowledgments

- **Siemens AG** — For TIA Portal and the Openness API
- **Repsay** — [tia-openness-api-client](https://github.com/your-org/tia-openness-api-client) (MIT, the basis for the Openness wrapper)
- **Anthropic** — For MCP (Model Context Protocol) and the [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk)
- **OpenClaw Team** — For the AI agent framework

---

## 📞 Contact

- **Website**: https://plccursos.com.br/genius-automation (PT-BR)
- **Email**: contato@plccursos.com.br
- **Issues**: https://github.com/your-org/genius-automation-community/issues
- **Pro Edition**: https://plccursos.com.br/genius-automation/pricing ($29/mo)

---

<p align="center">
Made with ❤️ by <a href="https://plccursos.com.br">PLCCursos</a> & <a href="https://github.com/openclaw">OpenClaw</a> Team<br>
<em>"Automação sem fronteiras"</em>
</p>