# 🛡️ RELATÓRIO DE AUDITORIA DE SEGURANÇA 360° PARA PRODUÇÃO

**Projeto:** `genius-automation-community`  
**Caminho:** `/home/sarah/Documents/Projects/genius-automation-community`  
**Data da Auditoria:** `2026-08-01 12:45:07`  
**Status Global:** **REPROVADO ❌**  

---

## 📊 Matriz de Avaliação dos 7 Pilares

| Pilar | Status | Ocorrências / Bloqueios |
|---|---|---|
| **1. Higiene Git & Repositório** | `PASS` | 0 problema(s) |
| **2. Autenticação, Hashes & 2FA** | `FAIL` | 1 problema(s) |
| **3. Criptografia em Trânsito & Repouso** | `FAIL` | 85 problema(s) |
| **4. Segurança de Sessão & Tokens** | `PASS` | 0 problema(s) |
| **5. Proteção OWASP Top 10** | `PASS` | 0 problema(s) |
| **6. Autorização Backend (RBAC)** | `PASS` | 0 problema(s) |
| **7. Auditoria de Dependências** | `PASS` | 0 problema(s) |

---

## 🔍 Detalhamento das Desconformidades por Pilar

### Pilar 1: Higiene Git & Repositório — Status: `PASS`
- ✅ Nenhum risco ou desconformidade detectada neste pilar.

### Pilar 2: Autenticação, Hashes & 2FA — Status: `FAIL`
- ❌ .venv/lib/python3.11/site-packages/requests/auth.py: Uso de MD5 inseguro para hashes/senhas

### Pilar 3: Criptografia em Trânsito & Repouso — Status: `FAIL`
- ❌ mock/server.py: Endpoint HTTP não seguro: "http://{args.host}:{args.port}"
- ❌ .venv/lib/python3.11/site-packages/requests_toolbelt/adapters/appengine.py: Endpoint HTTP não seguro: "http://a.com"
- ❌ .venv/lib/python3.11/site-packages/requests_toolbelt/auth/handler.py: Endpoint HTTP não seguro: 'http://example.com/example'
- ❌ .venv/lib/python3.11/site-packages/urllib3/connectionpool.py: Endpoint HTTP não seguro: 'http://google.com/'
- ❌ .venv/lib/python3.11/site-packages/urllib3/poolmanager.py: Endpoint HTTP não seguro: "http://google.com/"
- ❌ .venv/lib/python3.11/site-packages/urllib3/util/url.py: Endpoint HTTP não seguro: 'http://google.com/mail/'
- ❌ .venv/lib/python3.11/site-packages/id/_internal/oidc/ambient.py: Endpoint HTTP não seguro: "http://metadata/computeMetadata/v1/instance/service-accounts/default/token"
- ❌ .venv/lib/python3.11/site-packages/requests/sessions.py: Endpoint HTTP não seguro: 'http://domain.tld/path/to/resource'
- ❌ .venv/lib/python3.11/site-packages/mdurl/_parse.py: Endpoint HTTP não seguro: 'http://foo?bar'
- ❌ .venv/lib/python3.11/site-packages/docutils/transforms/peps.py: Endpoint HTTP não seguro: 'http://hg.python.org'
- ❌ .venv/lib/python3.11/site-packages/docutils/transforms/references.py: Endpoint HTTP não seguro: "http://external"
- ❌ .venv/lib/python3.11/site-packages/docutils/writers/_html_base.py: Endpoint HTTP não seguro: "http://purl.org/dc/terms/"
- ❌ .venv/lib/python3.11/site-packages/docutils/writers/docutils_xml.py: Endpoint HTTP não seguro: "http://docutils.sourceforge.net/docs/ref/docutils.dtd"
- ❌ .venv/lib/python3.11/site-packages/docutils/writers/odf_odt/__init__.py: Endpoint HTTP não seguro: 'http://purl.org/dc/elements/1.1/'
- ❌ .venv/lib/python3.11/site-packages/ast_serialize-0.6.0.dist-info/sboms/mypy_parser.cyclonedx.json: Endpoint HTTP não seguro: "http://fizyk20.github.io/generic-array/generic_array/"
- ❌ .venv/lib/python3.11/site-packages/black/resources/black.schema.json: Endpoint HTTP não seguro: "http://json-schema.org/draft-07/schema#"
- ❌ .venv/lib/python3.11/site-packages/cffi/commontypes.py: Endpoint HTTP não seguro: "http://cffi.readthedocs.io/en/latest/cdef.html#ffi-cdef-limitations "
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/_lua_builtins.py: Endpoint HTTP não seguro: 'http://www.lua.org/manual/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/_sourcemod_builtins.py: Endpoint HTTP não seguro: 'http://docs.sourcemod.net/api/index.php'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/algebra.py: Endpoint HTTP não seguro: 'http://www.mupad.com'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/ampl.py: Endpoint HTTP não seguro: 'http://ampl.com/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/asm.py: Endpoint HTTP não seguro: 'http://0x10c.com/doc/dcpu-16.txt'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/automation.py: Endpoint HTTP não seguro: 'http://www.autohotkey.com/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/basic.py: Endpoint HTTP não seguro: 'http://blitzbasic.com'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/c_like.py: Endpoint HTTP não seguro: 'http://claylabs.com/clay'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/clean.py: Endpoint HTTP não seguro: 'http://clean.cs.ru.nl/Clean'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/configs.py: Endpoint HTTP não seguro: 'http://en.wikipedia.org/wiki/Windows_Registry#.REG_files'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/css.py: Endpoint HTTP não seguro: 'http://lesscss.org/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/d.py: Endpoint HTTP não seguro: 'http://jfbillingsley.com/croc'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/dalvik.py: Endpoint HTTP não seguro: 'http://code.google.com/p/smali/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/data.py: Endpoint HTTP não seguro: 'http://yaml.org/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/dotnet.py: Endpoint HTTP não seguro: 'http://nemerle.org'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/dsls.py: Endpoint HTTP não seguro: 'http://en.wikipedia.org/wiki/RAISE'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/dylan.py: Endpoint HTTP não seguro: 'http://www.opendylan.org/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/elpi.py: Endpoint HTTP não seguro: 'http://github.com/LPCIC/elpi'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/esoteric.py: Endpoint HTTP não seguro: 'http://www.muppetlabs.com/~breadbox/bf/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/ezhil.py: Endpoint HTTP não seguro: 'http://ezhillang.org'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/factor.py: Endpoint HTTP não seguro: 'http://factorcode.org'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/felix.py: Endpoint HTTP não seguro: 'http://www.felix-lang.org'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/grammar_notation.py: Endpoint HTTP não seguro: 'http://www.ietf.org/rfc/rfc7405.txt'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/graphics.py: Endpoint HTTP não seguro: 'http://asymptote.sf.net/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/haskell.py: Endpoint HTTP não seguro: 'http://wiki.portal.chalmers.se/agda/pmwiki.php'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/haxe.py: Endpoint HTTP não seguro: 'http://haxe.org/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/igor.py: Endpoint HTTP não seguro: 'http://www.wavemetrics.com'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/inferno.py: Endpoint HTTP não seguro: 'http://www.vitanuova.com/inferno/limbo.html'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/installers.py: Endpoint HTTP não seguro: 'http://nsis.sourceforge.net/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/int_fiction.py: Endpoint HTTP não seguro: 'http://inform-fiction.org/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/iolang.py: Endpoint HTTP não seguro: 'http://iolanguage.com/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/j.py: Endpoint HTTP não seguro: 'http://jsoftware.com/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/javascript.py: Endpoint HTTP não seguro: 'http://rzimmerman.github.io/kal'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/jvm.py: Endpoint HTTP não seguro: 'http://www.eclipse.org/aspectj/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/lisp.py: Endpoint HTTP não seguro: 'http://www.scheme-reports.org/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/maxima.py: Endpoint HTTP não seguro: 'http://maxima.sourceforge.net'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/ml.py: Endpoint HTTP não seguro: 'http://opalang.org'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/modeling.py: Endpoint HTTP não seguro: 'http://www.modelica.org/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/modula2.py: Endpoint HTTP não seguro: 'http://www.modula2.org/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/nimrod.py: Endpoint HTTP não seguro: 'http://nim-lang.org/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/nit.py: Endpoint HTTP não seguro: 'http://nitlanguage.org'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/nix.py: Endpoint HTTP não seguro: 'http://nixos.org/nix/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/parasail.py: Endpoint HTTP não seguro: 'http://www.parasail-lang.org'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/parsers.py: Endpoint HTTP não seguro: 'http://www.colm.net/open-source/ragel/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/phix.py: Endpoint HTTP não seguro: 'http://phix.x10.mx'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/php.py: Endpoint HTTP não seguro: 'http://zephir-lang.com/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/praat.py: Endpoint HTTP não seguro: 'http://www.praat.org'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/prolog.py: Endpoint HTTP não seguro: 'http://logtalk.org/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/python.py: Endpoint HTTP não seguro: 'http://pyos.github.io/dg'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/r.py: Endpoint HTTP não seguro: 'http://cran.r-project.org/doc/manuals/R-exts.html'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/rebol.py: Endpoint HTTP não seguro: 'http://www.rebol.com'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/rnc.py: Endpoint HTTP não seguro: 'http://relaxng.org'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/robotframework.py: Endpoint HTTP não seguro: 'http://robotframework.org'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/ruby.py: Endpoint HTTP não seguro: 'http://www.ruby-lang.org'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/scripting.py: Endpoint HTTP não seguro: 'http://moonscript.org'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/smalltalk.py: Endpoint HTTP não seguro: 'http://www.smalltalk.org/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/sql.py: Endpoint HTTP não seguro: 'http://www.logilab.org/project/rql'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/stata.py: Endpoint HTTP não seguro: 'http://www.stata.com/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/supercollider.py: Endpoint HTTP não seguro: 'http://supercollider.github.io/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/templates.py: Endpoint HTTP não seguro: 'http://www.myghty.org/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/textfmts.py: Endpoint HTTP não seguro: 'http://todotxt.com/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/typoscript.py: Endpoint HTTP não seguro: 'http://docs.typo3.org/typo3cms/TyposcriptReference/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/unicon.py: Endpoint HTTP não seguro: 'http://www.unicon.org'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/webmisc.py: Endpoint HTTP não seguro: 'http://duelengine.org/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/whiley.py: Endpoint HTTP não seguro: 'http://whiley.org/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/x10.py: Endpoint HTTP não seguro: 'http://x10-lang.org/'
- ❌ .venv/lib/python3.11/site-packages/pygments/lexers/zig.py: Endpoint HTTP não seguro: 'http://ziglang.org'
- ❌ build/lib/mock/server.py: Endpoint HTTP não seguro: "http://{args.host}:{args.port}"

### Pilar 4: Segurança de Sessão & Tokens — Status: `PASS`
- ✅ Nenhum risco ou desconformidade detectada neste pilar.

### Pilar 5: Proteção OWASP Top 10 (SQLi/XSS/CSRF) — Status: `PASS`
- ✅ Nenhum risco ou desconformidade detectada neste pilar.

### Pilar 6: Autorização Backend (RBAC) — Status: `PASS`
- ✅ Nenhum risco ou desconformidade detectada neste pilar.

### Pilar 7: Auditoria de Dependências Vulneráveis — Status: `PASS`
- ✅ Nenhum risco ou desconformidade detectada neste pilar.

