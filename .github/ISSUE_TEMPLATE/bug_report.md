---
name: Bug report
about: Create a report to help us improve
title: "[BUG] "
labels: ["bug", "triage"]
assignees: ""
---

## 🐛 Bug Description

A clear and concise description of what the bug is.

## 📋 Reproduction Steps

Steps to reproduce the behavior:

1. **Tool called**: (e.g., `read_tags`)
2. **Input**:
   ```json
   {"plc": "PLC_1", "tag_names": ["Motor_Speed"]}
   ```
3. **Expected behavior**: (what you expected to happen)
4. **Actual behavior**: (what actually happened)

## 🖼 Error Output / Logs

```
Paste error message, stack trace, or relevant log lines here
```

## 🧩 Environment

| Component | Version |
|-----------|---------|
| **Genius Automation Community** | (e.g., 1.0.0 — see `python -m mock.server --version`) |
| **Python** | (e.g., 3.11.5) |
| **OS** | (e.g., Windows 11 23H2 / Ubuntu 22.04) |
| **TIA Portal** | (e.g., V21 + Openness license) |
| **MCP client** | (e.g., Claude Code 2.1.88, OpenClaw) |

## 📎 Additional Context

- [ ] I have searched existing issues to avoid duplicates
- [ ] I have read the [README.md](../../README.md)
- [ ] I have tried with the mock server (Linux) — same issue?
- [ ] I can provide a minimal reproduction (fixture data + script)

## 🎯 Severity

How severe is this bug? (check one)

- [ ] **Critical** — Blocks core functionality, no workaround
- [ ] **High** — Major functionality broken, workaround exists
- [ ] **Medium** — Minor functionality broken
- [ ] **Low** — Cosmetic, typo, or edge case

---

**For security vulnerabilities**: Email contato@plccursos.com.br directly. Do NOT file a public issue.