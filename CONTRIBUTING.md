# Contributing to Genius Automation — Community Edition

First off, thank you for considering contributing! 🎉

Genius Automation Community Edition is the **MIT-licensed, public** version of the project. Contributions are welcome from anyone — bug fixes, documentation improvements, new test fixtures, and small feature additions to the 5 community tools.

> **Note**: The 34 advanced tools (Pro Edition) are **not** open-source and contributions to them go through a separate Pro-edition process. Please don't open PRs to the Pro repo from this community repo.

---

## 🐛 Reporting Bugs

1. **Search existing issues** first to avoid duplicates: https://github.com/your-org/genius-automation-community/issues
2. **Use the bug report template** when opening a new issue.
3. **Include reproduction steps** — code snippet, error message, expected vs actual behavior.
4. **Include environment** — OS, Python version, TIA Portal version, MCP server version.

For **security vulnerabilities**, email contato@plccursos.com.br directly (do not open a public issue).

---

## 💡 Suggesting Features

1. **Open an issue first** with the `enhancement` label.
2. Describe the use case, not just the solution.
3. Be specific about which of the 5 community tools it affects.
4. If the feature is large (e.g., adds a new tool), it might be better suited for the Pro Edition — we'll discuss.

---

## 🛠 Submitting a Pull Request

### Setup

```bash
# 1. Fork the repo (click "Fork" on GitHub)

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/genius-automation-community.git
cd genius-automation-community

# 3. Create a branch
git checkout -b feature/my-cool-feature

# 4. Set up Python virtual env
python3.11 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# 5. Install the project with development dependencies
pip install -e ".[dev]"
```

### Code Style

- **Python 3.11+** syntax (no walrus operator abuse, no match/case unless it improves clarity)
- **Type hints** on all public functions
- **Docstrings** on all public functions, classes, and modules (Google style)
- **Black** formatter (88 char line length)
- **isort** for imports
- **pytest** for tests

Run before committing:
```bash
black .
isort .
pytest
mypy src/
```

### Test Requirements

- New features must include unit tests
- Bug fixes must include a regression test
- Aim for **≥80% coverage** on the new code
- All tests must pass in CI

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add connect with auto-detect mode
fix: handle missing project gracefully
docs: clarify TIA Portal V20+ compatibility
test: add unit tests for get_project_tree
chore: bump version to 1.0.1
```

### PR Process

1. Push your branch to your fork.
2. Open a PR against `main` on the original repo.
3. Fill in the PR template.
4. Wait for CI to pass.
5. Address review feedback.
6. Squash-merge once approved.

---

## 📁 Project Structure

```
genius-automation-community/
├── src/                         # Source package (installed via pip install -e .)
│   └── mcp_server_tools/        # Core MCP server code (__init__.py, tools.py)
├── mock/                        # Mock server (runs on Linux, no TIA Portal required)
│   ├── server.py                # HTTP server exposing the 5 community tools
│   ├── fixtures/                # 5 sample JSON payloads (connect, read_tags, list_blocks, get_project_tree, compile)
│   └── README.md                # Mock-specific docs
├── tests/                       # pytest tests (test_packaging.py and friends)
├── README.md                    # Project overview & quick-start
├── CONTRIBUTING.md              # This file
├── CHANGELOG.md                 # Release notes
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── LICENSE                      # MIT
├── pyproject.toml               # PEP 621 build config
└── uv.lock                      # Reproducible Python deps lockfile
```

---

## 🌐 Translations

We welcome translations of the README and docs to other languages. Currently:
- English (primary) — `README.md`
- Brazilian Portuguese (PT-BR) — `docs/README-pt-BR.md` (planned)

If you'd like to add a new translation:
1. Copy the English README
2. Translate the content (keep code blocks, URLs, and proper nouns in English)
3. Open a PR with the filename format `README-LANG.md` (e.g., `README-es.md`)

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the **MIT License** (same as the project).

---

## 💬 Communication

- **GitHub Issues**: https://github.com/your-org/genius-automation-community/issues
- **GitHub Discussions**: https://github.com/your-org/genius-automation-community/discussions
- **Email**: contato@plccursos.com.br
- **Discord** (PLCCursos community): invite link in welcome email

---

<p align="center">Thank you for contributing! 💚</p>
