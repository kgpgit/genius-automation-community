"""Smoke tests for the pyproject.toml packaging claim.

These tests verify that the packaging metadata added in t_7d3df6fc is
correct: the package is installable, importable, exposes the right
metadata, and the mocked MCP server can boot a real HTTP listener.
"""

from __future__ import annotations

import importlib
import importlib.metadata
import json
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Package metadata
# ---------------------------------------------------------------------------


def test_package_metadata_name_and_version():
    md = importlib.metadata.metadata("genius-automation-community")
    assert md["Name"] == "genius-automation-community"
    assert md["Version"] == "0.1.0"


def test_package_metadata_summary_starts_with_mcp():
    md = importlib.metadata.metadata("genius-automation-community")
    assert md["Summary"].lower().startswith("mcp server")


def test_package_metadata_requires_python_311():
    md = importlib.metadata.metadata("genius-automation-community")
    assert md["Requires-Python"] == ">=3.11"


def test_package_metadata_license_is_mit():
    md = importlib.metadata.metadata("genius-automation-community")
    assert md["License"] == "MIT"


def test_package_has_no_runtime_dependencies():
    """Community Edition is intentionally stdlib-only."""
    requires = importlib.metadata.requires("genius-automation-community") or []
    # `requires` returns all deps including extras; filter un-extras
    runtime = [r for r in requires if "extra ==" not in r]
    assert runtime == [], f"Expected zero runtime deps, got {runtime}"


def test_package_has_dev_extras():
    md = importlib.metadata.metadata("genius-automation-community")
    all_deps = importlib.metadata.requires("genius-automation-community") or []
    dev_deps = [d for d in all_deps if 'extra == "dev"' in d]
    expected = {"pytest", "pytest-cov", "mypy", "black", "isort", "build", "twine"}
    declared = set()
    for dep in dev_deps:
        # Each entry looks like: 'pytest>=7.0; extra == "dev"'
        name = dep.split(">=")[0].split("==")[0].split(";")[0].split("[")[0].strip()
        declared.add(name.lower())
    assert expected.issubset(declared), f"Missing dev extras: {expected - declared}"


def test_mock_server_reports_installed_package_version():
    """The HTTP identity must not drift from the distributable package version."""
    from mock.server import PACKAGE_VERSION, MockMCPServerHandler

    expected = importlib.metadata.version("genius-automation-community")
    assert PACKAGE_VERSION == expected
    assert MockMCPServerHandler.server_version == f"Genius-Automation-Mock/{expected}"


# ---------------------------------------------------------------------------
# Package importability
# ---------------------------------------------------------------------------


def test_mock_package_importable():
    """`mock` is a package; `mock.server` is its submodule."""
    mock = importlib.import_module("mock")
    assert mock is not None
    # Verify the server submodule is reachable via dotted import
    server = importlib.import_module("mock.server")
    assert server is not None
    assert hasattr(server, "main")


def test_mcp_server_tools_importable():
    tools = importlib.import_module("mcp_server_tools.tools")
    assert hasattr(tools, "ToolDef")


def test_fixtures_dir_present():
    """Fixtures must ship inside the wheel so the server can find them."""
    mock = importlib.import_module("mock")
    fix_dir = Path(mock.__file__).parent / "fixtures"
    assert fix_dir.is_dir()
    fixtures = sorted(p.name for p in fix_dir.glob("*.json"))
    assert fixtures == [
        "compile.json",
        "connect.json",
        "get_project_tree.json",
        "list_blocks.json",
        "read_tags.json",
    ]


def test_mock_server_main_is_callable():
    from mock.server import main

    assert callable(main)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def test_genius_mock_console_script_exists():
    """The `genius-mock` script should be installed by `pip install -e .`.

    Resolves the entry point via package metadata so the test doesn't depend
    on the test runner's PATH (e.g. when pytest is invoked outside an
    activated virtualenv). Also accepts shutil.which() when the venv's bin/
    happens to be on PATH.
    """
    import importlib.metadata as md

    # Authoritative check: does pyproject declare the console_scripts entry?
    eps = md.entry_points(group="console_scripts")
    names = {ep.name for ep in eps}
    assert "genius-mock" in names, (
        "genius-mock console script not declared in package metadata; " f"found: {sorted(names)}"
    )

    # Sanity check: if the script happens to be on PATH, the resolved path
    # should mention 'genius-mock'. Non-fatal when PATH doesn't include the
    # project venv (e.g. CI runs `pytest` without `source .venv/bin/activate`).
    import shutil

    path = shutil.which("genius-mock")
    if path is not None:
        assert "genius-mock" in path


def test_genius_mock_serves_health_endpoint():
    """Boot the mock server on a free port and hit /health."""
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    proc = subprocess.Popen(
        [sys.executable, "-m", "mock.server", "--port", str(port), "--host", "127.0.0.1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        # Wait for server to come up (max 5s)
        deadline = time.time() + 5.0
        last_err = None
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=1) as resp:
                    assert resp.status == 200
                    body = json.loads(resp.read())
                    assert body["status"] == "healthy"
                    assert body["fixtures_loaded"] == 5
                    return  # success
            except Exception as e:
                last_err = e
                time.sleep(0.2)
        pytest.fail(f"Server never came up: {last_err}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()


def test_genius_mock_lists_5_tools():
    """GET /tools should return the 5 community tools."""
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    proc = subprocess.Popen(
        [sys.executable, "-m", "mock.server", "--port", str(port), "--host", "127.0.0.1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        deadline = time.time() + 5.0
        last_err = None
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/tools", timeout=1) as resp:
                    body = json.loads(resp.read())
                    assert body["count"] == 5
                    names = {t["name"] for t in body["tools"]}
                    assert names == {
                        "connect",
                        "read_tags",
                        "list_blocks",
                        "get_project_tree",
                        "compile",
                    }
                    return
            except Exception as e:
                last_err = e
                time.sleep(0.2)
        pytest.fail(f"Server never came up: {last_err}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()


def test_mock_server_info_reports_package_version():
    """Live /info response must echo the distributable version, not a hardcoded literal."""
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    proc = subprocess.Popen(
        [sys.executable, "-m", "mock.server", "--port", str(port), "--host", "127.0.0.1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        deadline = time.time() + 5.0
        last_err = None
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/info", timeout=1) as resp:
                    assert resp.status == 200
                    body = json.loads(resp.read())
                    server_header = resp.headers["Server"]
                    expected = importlib.metadata.version("genius-automation-community")
                    assert body["version"] == expected
                    assert server_header.startswith(
                        f"Genius-Automation-Mock/{expected} "
                    ), f"Server header drifted: {server_header!r}"
                    return
            except Exception as e:
                last_err = e
                time.sleep(0.2)
        pytest.fail(f"Server never came up: {last_err}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()


# ---------------------------------------------------------------------------
# Docstring ↔ TOOL_DEFINITIONS contract (yellow polish B)
# ---------------------------------------------------------------------------


def test_mcp_server_tools_init_docstring_lists_real_tools():
    """The __init__.py docstring is the public contract of the Community
    Edition tool set. It MUST list exactly the tools present in
    ``mock.server.TOOL_DEFINITIONS`` so a reader can rely on it without
    booting the mock server.

    Catches silent drift when a tool is renamed in TOOL_DEFINITIONS but the
    docstring is forgotten.
    """
    import re

    import mcp_server_tools
    from mock.server import TOOL_DEFINITIONS

    assert mcp_server_tools.__doc__ is not None, "missing package docstring"

    # Extract bullet-listed tool names. Each line starts with
    # "  - <name>" inside the Community Edition tool list.
    bullets = re.findall(
        r"^\s*-\s+([a-z_][a-z0-9_]*)\s*\(",
        mcp_server_tools.__doc__,
        flags=re.MULTILINE,
    )
    documented = set(bullets)

    expected = {t["name"] for t in TOOL_DEFINITIONS}
    assert documented == expected, (
        "mcp_server_tools docstring lists "
        f"{sorted(documented) or '∅'}, "
        f"but TOOL_DEFINITIONS declares {sorted(expected)}. "
        "Sync the docstring to the real registry in mock/server.py."
    )
