# Genius Automation — Community Edition

**Última atualização:** 2026-08-01 (Scribe — vault standardization)
**Kanban ID:** `genius-automation` (compartilhado com Pro)
**Caminho:** `/home/sarah/Documents/Projects/genius-automation-community/`
**Licença:** MIT

---

## 📋 Descrição

Edição open-source (MIT) do servidor MCP para Siemens TIA Portal V17+. Expõe **5 ferramentas read-only** (connect, read_tags, list_blocks, get_project_tree, compile) que permitem agentes AI interagir com PLCs Siemens de forma segura. Modelo open-core: a edição Community é gratuita para uso comercial e não-comercial; funcionalidades avançadas (write operations, multi-vendor, HMI) vivem na edição Pro proprietária ($29/mo). Suporte completo a mock-mode para desenvolvimento/testes sem TIA Portal instalado.

## 🛠️ Stack Tecnológica

| Componente | Tecnologia |
|------------|-----------|
| Linguagem | Python 3.11+ |
| Protocolo | MCP (Model Context Protocol) |
| .NET Interop | pythonnet (Python ↔ .NET Framework 4.8) |
| Siemens | TIA Portal Openness API (V17+) |
| Plataforma | Windows (full) / Linux+macOS (mock only) |
| Build | pyproject.toml, uv.lock |
| Mock Server | `python -m mock.server --port 8001` |

## 📊 Status Atual

**🟢 Code Ready — Pronto para publicação GitHub**

- ✅ 5 tools MIT implementados (read-only: connect, read_tags, list_blocks, get_project_tree, compile)
- ✅ Mock server funcional em Linux (5/5 fixtures carregados)
- ✅ Git init + push ready (auditoria: 0 blocking issues)
- ✅ LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md presentes
- ✅ CHANGELOG.md mantido
- ✅ Community → Pro upgrade path documentado

## 🚧 Bloqueios Conhecidos

1. **GitHub repo** — auditoria de prontidão passou (git_init_push_ready=true), mas publicação ainda pendente
2. **Sem bloqueios técnicos** — code ready, 0 blocking issues identificados

## 🎯 Tarefas Ativas (Kanban)

Tarefas compartilhadas com Genius Automation Pro:

| Tarefa | Status |
|--------|--------|
| Genius Automation — Deploy rebrand to W11 server | 🔴 blocked |
| Testar Genius Automation com TIA Portal v16, v17 e v18 | todo |
| Testar Genius Automation com TIA Portal v19, v20 e v21 | todo |

## 📜 Últimos Marcos (Kanban)

- **[2026-07-29]** Auditoria de prontidão para git init + repo GitHub: git_init_push_ready=true, 0 blocking issues
- **[2026-07-29]** Pro auditoria canônica: 97 tools, 219/219 tests PASS, veredito GO
- **[2026-07-20]** Landing Page Genius Automation criada na VPS
- **[N/A]** Rebrand TIA MCP Server → Genius Automation

## 📁 Estrutura do Vault

```
vault/
└── overview.md              ← este arquivo (resumo executivo)
```

## 🔗 Links

- **README:** `README.md` (5 tools, quick start, architecture)
- **Mock Server:** `mock/` (server + fixtures)
- **Pro Edition:** `genius-automation-pro/` (119 tools, 7 vendors)
- **Website:** `https://plccursos.com.br/genius-automation`
- **Pricing:** `https://plccursos.com.br/genius-automation/pricing` ($29/mo Pro)

## 📜 Histórico de Entregas Recentes (Kanban Sync)
> *Atualizado automaticamente pelo motor de orquestração do Hermes em 2026-08-01 22:38 BRT*

- **[2026-07-29] Genius Automation Pro: Auditoria de prontidão para restauração + repo GitHub privado (BSL, 119 tools)** (`t_8a45f0b7`)
  - _Resumo:_ Auditoria Pro canônico: 97 tools, 219/219 tests PASS, working tree dirty, LICENSE ausente. Veredito GO.
- **[2026-07-29] Genius Automation Community: Auditoria de prontidão para git init + repo GitHub (MIT, 5 tools)** (`t_d7e0218d`)
  - _Resumo:_ git_init_push_ready=true, blocking_issues_remaining=0, files_created=1, files_modified=0, atomic deliverable
- **[2026-07-20] Sarah: Criar Landing Page Genius Automation na VPS** (`sarah-vps-genius-landing-page`)
  - _Resumo:_ Sarah: Criar Landing Page Genius Automation na VPS
- **[N/A] Genius Automation — Commercial Expansion Study** (`tia-mcp-commercial-expansion`)
  - _Resumo:_ Genius Automation — Commercial Expansion Study
- **[N/A] Genius Automation Tutorial — Script PT-BR (12-15 min)** (`tutorial-script-pt-br`)
  - _Resumo:_ Genius Automation Tutorial — Script PT-BR (12-15 min)
- **[N/A] Genius Automation — Multi-Vendor Strategy (Beckhoff/Schneider/ABB)** (`tia-mcp-multi-vendor`)
  - _Resumo:_ Genius Automation — Multi-Vendor Strategy (Beckhoff/Schneider/ABB)
- **[N/A] Genius Automation — Demo Project Package (downloadable)** (`demo-project-package`)
  - _Resumo:_ Genius Automation — Demo Project Package (downloadable)
- **[N/A] Genius Automation H3: Full Expansion (200+ tools) — VCI, Safety, Startdrive, SiVArc, Marketplace** (`tia-mcp-h3-full-expansion`)
  - _Resumo:_ Genius Automation H3: Full Expansion (200+ tools) — VCI, Safety, Startdrive, SiVArc, Marketplace
- **[N/A] Genius Automation H3: SCADA/WinCC Tools (10 tools implemented)** (`genius-h3-scada-wincc`)
  - _Resumo:_ Genius Automation H3: SCADA/WinCC Tools (10 tools implemented)
- **[N/A] Genius Automation — Rebrand TIA MCP Server (rename codebase, repo, W11)** (`genius-automation-rebrand`)
  - _Resumo:_ Genius Automation — Rebrand TIA MCP Server (rename codebase, repo, W11)
