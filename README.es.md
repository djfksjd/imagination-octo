<div align="center">

# ✨ Imagination

**Genera ideas distintas. Elige con intención. Desarrolla la que resista.**

Un plugin creativo con decisión humana para Codex y Claude Code.

[![Tests](https://github.com/djfksjd/imagination/actions/workflows/tests.yml/badge.svg)](https://github.com/djfksjd/imagination/actions/workflows/tests.yml)
![Version](https://img.shields.io/badge/version-0.1.2-7c3aed)
![License](https://img.shields.io/badge/license-MIT-0f766e)

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md)

</div>

---

Imagination deja en tus manos lo que la IA no debe automatizar: **la elección**.
Primero crea direcciones causalmente distintas, espera tu decisión y después
somete a prueba únicamente la idea elegida.

```text
Brief → 3–5 direcciones → tú eliges → concepto validado
```

## Inicio rápido

```bash
curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination/main/install.sh | bash
```

```text
Usa $imagination para proponer varias direcciones realmente distintas.
```

La primera respuesta termina con una elección. Responde con el número y la
siguiente iteración desarrollará solo esa opción.

## Tres skills

| Skill | Uso |
|---|---|
| `$imagination` | Entrada recomendada: divergir, elegir y desarrollar |
| `$imagination-engine` | Generar 3–5 direcciones útiles y no obvias |
| `$imagination-brainstorming` | Convertir una idea elegida en un concepto listo para decidir |

> [!IMPORTANT]
> El router nunca elige y desarrolla una idea en el mismo turno. Tu elección es
> la frontera obligatoria entre divergencia y desarrollo.

## Resultados medidos

| Runtime | Preferencia frente a un prompt fuerte | Mejoras principales |
|---|---:|---|
| Engine v0.5.3 | **50–0 (100,0 %)** | sorpresa útil `+0,97`, diversidad `+0,66`, ajuste `+0,60` |
| Workshop v0.4.1 | **25–5 (83,3 %)** | aplicabilidad `+1,37`, ajuste `+0,59`, claridad causal `+0,59` |

Son resultados de jueces modelo sobre la distribución prerregistrada, no una
garantía de creatividad universal.

## Instalación manual

```bash
claude plugin marketplace add djfksjd/imagination
claude plugin install imagination@djfksjd
codex plugin marketplace add djfksjd/imagination
codex plugin add imagination@djfksjd
```

Licencia MIT.
