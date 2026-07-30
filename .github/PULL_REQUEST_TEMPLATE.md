## Description

<!-- What does this PR do? Why? Reference any related issues. -->

Fixes #<issue-number> (if applicable)

## Type of Change

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to change)
- [ ] 📚 Documentation update
- [ ] 🔧 Refactor / code cleanup
- [ ] 🧪 Test improvement
- [ ] 🌐 Translation

## Affected Tools

Which community tools does this PR affect? (check all that apply)

- [ ] `connect`
- [ ] `read_tags`
- [ ] `list_blocks`
- [ ] `get_project_tree`
- [ ] `compile`
- [ ] Mock server (`mock/server.py`)
- [ ] Mock fixtures (`mock/fixtures/`)
- [ ] Documentation (`README.md`, `CONTRIBUTING.md`, etc.)
- [ ] `.github/` templates / workflows

## Checklist

- [ ] I have read [CONTRIBUTING.md](../../CONTRIBUTING.md)
- [ ] My code follows the project style (Black, isort, type hints, docstrings)
- [ ] I have added tests for new functionality
- [ ] All tests pass locally (`pytest`)
- [ ] I have updated the documentation (if applicable)
- [ ] I have tested the mock server (`python -m mock.server`)
- [ ] My changes don't break existing fixtures

## Test Plan

How did you test this? What did you verify?

```bash
# Example commands
python3 -m pytest tests/
python3 -m mock.server --port 8001 &
curl http://localhost:8001/health
```

## Screenshots / Output (if applicable)

```
Paste output, logs, or screenshots here
```

## Related Issues / PRs

- Related to #
- Depends on #
- Blocks #

## Additional Context

Anything else reviewers should know?

---

**For Pro Edition PRs**: This is the wrong repo. The Pro/Enterprise Edition is private — please open a private PR there instead.