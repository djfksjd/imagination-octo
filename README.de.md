<div align="center">

# ✨ Imagination

**Unterschiedliche Ideen erzeugen. Bewusst wählen. Die beste vertiefen.**

Ein kreatives Human-in-the-Loop-Plugin für Codex und Claude Code.

[![Tests](https://github.com/djfksjd/imagination/actions/workflows/tests.yml/badge.svg)](https://github.com/djfksjd/imagination/actions/workflows/tests.yml)
![Version](https://img.shields.io/badge/version-0.1.2-7c3aed)
![Lizenz](https://img.shields.io/badge/license-MIT-0f766e)

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md)

</div>

---

Imagination überlässt dir, was eine KI nicht automatisieren sollte: **die
Entscheidung**. Zuerst entstehen kausal unterschiedliche Richtungen. Erst nach
deiner Wahl wird genau diese Idee geprüft und ausgearbeitet.

```text
Briefing → 3–5 Richtungen → du wählst → belastbares Konzept
```

## Schnellstart

```bash
curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination/main/install.sh | bash
```

```text
Nutze $imagination und entwickle mehrere wirklich unterschiedliche Richtungen.
```

Die erste Antwort endet mit einer Auswahl. Antworte mit einer Nummer; im
nächsten Schritt wird nur diese Option vertieft.

## Drei Skills

| Skill | Einsatz |
|---|---|
| `$imagination` | Empfohlener Einstieg: divergieren, wählen, vertiefen |
| `$imagination-engine` | 3–5 nützliche, nicht offensichtliche Richtungen |
| `$imagination-brainstorming` | Eine gewählte Idee entscheidungsreif machen |

> [!IMPORTANT]
> Der Router wählt und entwickelt nie im selben Zug. Deine Wahl ist die
> verbindliche Grenze zwischen Ideenfindung und Ausarbeitung.

## Messergebnisse

| Runtime | Präferenz gegenüber starkem Prompt | Wichtigste Gewinne |
|---|---:|---|
| Engine v0.5.3 | **50–0 (100,0 %)** | nützliche Überraschung `+0,97`, Vielfalt `+0,66`, Passung `+0,60` |
| Workshop v0.4.1 | **25–5 (83,3 %)** | Umsetzbarkeit `+1,37`, Passung `+0,59`, kausale Klarheit `+0,59` |

Dies sind Modellrichter-Ergebnisse für die vorregistrierte Testverteilung, kein
Nachweis universeller Kreativität.

## Manuelle Installation

```bash
claude plugin marketplace add djfksjd/imagination
claude plugin install imagination@djfksjd
codex plugin marketplace add djfksjd/imagination
codex plugin add imagination@djfksjd
```

MIT-Lizenz.
