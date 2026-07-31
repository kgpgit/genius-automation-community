"""Genius Automation Community Edition — top-level tools package.

This is the **Community Edition** (MIT-licensed) tool registry. It contains
only the **5 basic tools** that are safe to release under MIT:

  - connect          (establish TIA Portal session)
  - read_tags        (read PLC tag values)
  - list_blocks      (list blocks in a PLC)
  - get_project_tree (read-only: get project structure)
  - compile          (compile project to validate offline)

The remaining advanced tools (block CRUD, hardware config, library
management, HMI, diagnostics, batch operations, project open/close/save)
live in the **Pro Edition** (proprietary, $29/mo). See
https://plccursos.com.br/genius-automation

The full tool list (with schemas) is loaded on demand by the mock server
from `mock/server.py` — see TOOL_DEFINITIONS there.

This module is intentionally minimal in the Community Edition to make the
open-core split explicit: the Pro/Enterprise handlers depend on
TIA Portal Openness (pythonnet, .NET Framework 4.8) and are not portable
to Linux, so they live in the Pro repository.
"""

from __future__ import annotations

import logging
from typing import Dict, List

from mcp_server_tools.tools import ToolDef

logger = logging.getLogger(__name__)

# Community Edition: no advanced tool families registered here.
# The Pro Edition registers H2D (diagnostics) and H2B (library) tool families
# from the corresponding register modules.

ALL_TOOLS: List[ToolDef] = []

# ---------------------------------------------------------------------------
# Sanity checks (run at import time — fail fast on misconfiguration)
# ---------------------------------------------------------------------------


def _validate_all_tools() -> None:
    """Sanity check the global tool registry at import time.

    Verifies that:
      - every ToolDef has a name, description, schema, and callable handler
      - tool names are unique across all families
      - input_schema is a JSON-Schema object with a 'properties' field
    """
    seen: Dict[str, str] = {}
    errors: List[str] = []

    for tool in ALL_TOOLS:
        if not tool.name:
            errors.append("ToolDef with empty name")
            continue
        if not tool.description or len(tool.description) < 10:
            errors.append(f"{tool.name}: description missing or too short")
        if not isinstance(tool.input_schema, dict):
            errors.append(f"{tool.name}: input_schema is not a dict")
        elif tool.input_schema.get("type") != "object":
            errors.append(f"{tool.name}: input_schema.type != 'object'")
        elif "properties" not in tool.input_schema:
            errors.append(f"{tool.name}: input_schema has no 'properties'")
        if not callable(tool.handler):
            errors.append(f"{tool.name}: handler is not callable")

        if tool.name in seen:
            errors.append(f"Duplicate tool name: {tool.name!r} (also in {seen[tool.name]})")
        else:
            seen[tool.name] = tool.__class__.__module__

    if errors:
        for err in errors:
            logger.error("ALL_TOOLS validation: %s", err)
        raise RuntimeError(f"ALL_TOOLS validation failed with {len(errors)} error(s); see log.")

    logger.info("ALL_TOOLS: %d tools registered across all families", len(ALL_TOOLS))


_validate_all_tools()

__all__ = ["ALL_TOOLS", "ToolDef"]
