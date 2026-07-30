# Changelog

All notable changes to Genius Automation Community Edition will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `pyproject.toml` (PEP 621 / setuptools) — enables `pip install -e .` and PyPI release.
  - Runtime dependencies: none (Community Edition is stdlib-only; pythonnet lives in Pro).
  - `[project.optional-dependencies] dev` — pytest, pytest-cov, mypy, black, isort, build, twine.
  - `[project.scripts]` entry point `genius-mock = mock.server:main` (CLI wrapper).
  - Tool configs for pytest, mypy, black, isort aligned with CONTRIBUTING.md.
- `MANIFEST.in` — bundles README, CHANGELOG, LICENSE, fixtures into sdist.

### Changed
- README "Step 1" no longer references the non-existent `requirements.txt`; the install
  command now uses `pip install -e .`, matching the canonical mechanism declared in
  `pyproject.toml`. (Fixes the gap called out in CHANGELOG line 19 of the previous
  Unreleased section — that entry was forward-looking and is now realised.)
- `mock/server.py` now reads its identity version from the installed `genius-automation-community`
  distribution metadata (`importlib.metadata.version`) instead of the hard-coded literal
  `1.0.0`. Both the `Server:` HTTP header and the `version` field exposed at `GET /` /
  `GET /info` now reflect the version declared in `pyproject.toml`, eliminating the
  drift between the package metadata (`0.1.0`) and the mock server's identity (`1.0.0`).
  The fallback `"0+unknown"` is used when the distribution is not importable (e.g. a
  source checkout that has not been installed), keeping the server bootable in dev
  environments.
- Added two regression tests in `tests/test_packaging.py` that pin the package version
  to the HTTP identity (`test_mock_server_reports_installed_package_version`) and to
  the live `/info` JSON payload (`test_mock_server_info_reports_package_version`).
  Both will fail (RED) if the hard-coded literal returns in any future commit.

### Planned
- PyPI package (`pip install genius-automation-community`)
- Docker image (`docker run genius-automation/community-mock`)
- GitHub Actions CI workflow (pytest + mypy + black)

## [0.1.0] - 2026-06-17

### Added
- 🎉 Initial release of Genius Automation Community Edition
- 5 read-only tools:
  - `connect` — establish TIA Portal session
  - `read_tags` — read PLC tag values
  - `list_blocks` — list blocks in a PLC
  - `get_project_tree` — get hierarchical project tree
  - `compile` — compile project and return errors/warnings
- Mock server (`mock/server.py`) for Linux/macOS development without TIA Portal
- Sample fixtures for all 5 tools (`mock/fixtures/*.json`)
- MIT License
- Comprehensive English README with feature comparison, quickstart, tool docs
- Contributing guide (`CONTRIBUTING.md`)
- GitHub templates:
  - Issue templates: bug report, feature request, question
  - Pull request template
  - Issue config (links to Discussions, Docs, Pro Edition, Security email)

### Notes
- This is the **open-core** Community Edition. 34 advanced tools live in the proprietary
  Pro / Enterprise Edition ($29/mo and $199/mo).
- The W11 production server (Windows VM) requires TIA Portal V17+ and an Openness license.
- Mock server runs on any OS with Python 3.11+.

---

[Unreleased]: https://github.com/your-org/genius-automation-community/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/your-org/genius-automation-community/releases/tag/v0.1.0