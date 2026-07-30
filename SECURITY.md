# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **contato@plccursos.com.br**

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information in your report:

- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the issue
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

## What to Expect

After you submit a report:

1. **Acknowledgment** within 48 hours
2. **Initial assessment** within 5 business days
3. **Regular updates** on progress (at least every 7 days)
4. **Credit** in the fix release notes (if you wish; you can stay anonymous too)

## Scope

### In Scope
- Code in this repository (`genius-automation-community`)
- The mock server (`mock/server.py`)
- The 5 community tools

### Out of Scope
- TIA Portal Openness API itself (this is a Siemens product — report to Siemens)
- The Pro / Enterprise Edition (separate codebase, contact via support@plccursos.com.br)
- Third-party dependencies (report to their respective maintainers)

## Disclosure Policy

We follow a **coordinated disclosure** model:

1. Security issue reported privately to contato@plccursos.com.br
2. Maintainer investigates and develops a fix
3. Fix released in a patch version
4. Security advisory published (CVE if applicable)
5. Public disclosure 90 days after the report, or sooner if a fix is ready

We will credit reporters who wish to be acknowledged, but we respect the right to remain anonymous.

## Security Best Practices for Users

When deploying Genius Automation:

1. **Run the MCP server on a trusted network** — it has no built-in authentication
2. **Use a firewall** to restrict access to the MCP port (default 8001)
3. **Don't expose the port publicly** without authentication
4. **TIA Portal Openness** runs only on Windows W11 — keep that VM isolated
5. **Update regularly** — security fixes are released as patch versions
6. **Review tags you expose** — `read_tags` returns live PLC state; restrict who can call it
7. **Audit logs** — the server logs all tool calls to stdout

## Recognition

We thank the following researchers for responsibly disclosing security issues:
_None yet — be the first!_

---

For questions about this security policy, email **contato@plccursos.com.br**.