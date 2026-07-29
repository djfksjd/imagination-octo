<div align="center">

# ✨ Imagination

**Gere ideias diferentes. Escolha com intenção. Desenvolva a que resistir.**

Um plugin criativo com decisão humana para Codex e Claude Code.

[![Tests](https://github.com/djfksjd/imagination/actions/workflows/tests.yml/badge.svg)](https://github.com/djfksjd/imagination/actions/workflows/tests.yml)
![Versão](https://img.shields.io/badge/version-0.1.1-7c3aed)
![Licença](https://img.shields.io/badge/license-MIT-0f766e)

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md)

</div>

---

O Imagination deixa com você o que a IA não deve automatizar: **a escolha**.
Primeiro cria direções causalmente diferentes, espera sua decisão e só então
testa e desenvolve a ideia selecionada.

```text
Briefing → 3–5 direções → você escolhe → conceito testado
```

## Início rápido

```bash
curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination/main/install.sh | bash
```

```text
Use $imagination para propor várias direções realmente diferentes.
```

A primeira resposta termina com uma escolha. Responda com o número; no próximo
turno, apenas essa opção será aprofundada.

## Três skills

| Skill | Uso |
|---|---|
| `$imagination` | Entrada recomendada: divergir, escolher e desenvolver |
| `$imagination-engine` | Gerar 3–5 direções úteis e não óbvias |
| `$imagination-brainstorming` | Transformar uma ideia escolhida em conceito decisório |

> [!IMPORTANT]
> O roteador nunca escolhe e desenvolve no mesmo turno. Sua escolha é a
> fronteira obrigatória entre divergência e desenvolvimento.

## Resultados medidos

| Runtime | Preferência contra prompt forte | Principais ganhos |
|---|---:|---|
| Engine v0.5.2 | **25–5 (83,3%)** | surpresa útil `+0,98`, diversidade `+0,93`, aderência `+0,31` |
| Workshop v0.4.1 | **25–5 (83,3%)** | aplicabilidade `+1,37`, aderência `+0,59`, clareza causal `+0,59` |

São resultados de juízes-modelo na distribuição pré-registrada, não garantia de
criatividade universal.

## Instalação manual

```bash
claude plugin marketplace add djfksjd/imagination
claude plugin install imagination@djfksjd
codex plugin marketplace add djfksjd/imagination
codex plugin add imagination@djfksjd
```

Licença MIT.
