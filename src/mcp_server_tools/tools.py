"""ToolDef — tool definition container for the Genius Automation.

A ToolDef is a small dataclass-like object that bundles a tool's:
  - name:           stable identifier (snake_case)
  - description:    human-readable description for LLM/agent context
  - input_schema:   JSON-Schema describing the tool's input arguments
  - handler:        callable handler(arguments: dict, state) -> dict

Handlers MUST have the signature:
    handler(arguments: dict, state: Any) -> dict
where `state` is a ServerState-like object exposing at least `get_project(name)`.

This module is intentionally dependency-free (no .NET, no pythonnet) so it can
be imported on Linux for unit tests and mock server runs.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


ToolHandler = Callable[[Dict[str, Any], Any], Dict[str, Any]]


@dataclass(frozen=True)
class ToolDef:
    """A TIA MCP tool definition.

    Attributes:
        name:         Unique tool identifier (e.g. "get_plc_info").
        description:  Human-readable description for the agent/LLM.
        input_schema: JSON-Schema dict describing accepted arguments.
        handler:      Callable implementing the tool. Receives (arguments, state)
                      and returns a JSON-serializable dict.
    """

    name: str
    description: str
    input_schema: Dict[str, Any]
    handler: ToolHandler

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable dict (drops the handler)."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }


__all__ = ["ToolDef", "ToolHandler"]
