---
name: Feature request
about: Suggest a new feature for Genius Automation Community
title: "[FEATURE] "
labels: ["enhancement", "triage"]
assignees: ""
---

## 💡 Feature Summary

A short, clear title for the feature (e.g., "Add `compile_with_warnings_only` option to `compile`").

## 🎯 Use Case / Problem

Describe the **problem** you're trying to solve, not just the solution.

- **Who** needs this? (programmer, integrator, student, etc.)
- **What** is the workflow without this feature? (manual steps, workarounds)
- **Why** is the workaround painful?

## 📋 Proposed Solution

Describe the proposed API/tool — be specific about:

- **Tool name**: (e.g., `compile`)
- **Input schema**:
  ```json
  {
    "plc": "PLC_1",
    "warnings_only": true
  }
  ```
- **Output schema**:
  ```json
  {
    "warnings": [...],
    "warnings_count": 5
  }
  ```

## 🔀 Alternatives Considered

What other approaches did you consider? Why is the proposed one better?

## 📦 Scope

This feature affects which tools?

- [ ] Affects existing community tool (which one?)
- [ ] Adds a new community tool
- [ ] Requires changes to mock server fixtures
- [ ] Requires changes to MCP server core
- [ ] Requires documentation update

## 💼 Tier Consideration

The Community Edition is **MIT-licensed** and currently **5 read-only tools**. Does this feature:

- [ ] Stay within the Community Edition (MIT, read-only-ish, no extra infra)
- [ ] Belong to the Pro Edition (proprietary, $29/mo, write operations)
- [ ] Belong to the Enterprise Edition (proprietary, $199/mo, multi-vendor)

> **Note**: Write operations (modify PLC state, create blocks, write tags) belong in **Pro**, not Community. Community stays focused on read-only, low-risk tools.

## 📚 References

Links to Siemens documentation, similar features in other tools, etc.

## 🤝 Willingness to Contribute

- [ ] I'm willing to submit a PR for this feature
- [ ] I'd like feedback before implementing
- [ ] I'd like to discuss with maintainers first
- [ ] I'm only suggesting — no implementation plans

---

**For Pro/Enterprise features**: Please contact sales@plccursos.com.br instead — those are not tracked here.