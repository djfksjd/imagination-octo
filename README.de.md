<div align="center">

<img src="assets/brand/imagination-octo-logo.png" alt="IMAGINATION OCTO — Weit ausgreifen, eines wählen" width="380" />

# IMAGINATION OCTO

**REACH WIDE · CHOOSE ONE**

### Ein kreatives Human-in-the-Loop-Plugin für Claude Code und Codex —<br/>erst unterschiedliche Ideen, dann deine Wahl, dann ein belastbares Konzept

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md)

[![Tests](https://img.shields.io/github/actions/workflow/status/djfksjd/imagination-octo/tests.yml?style=flat-square&label=tests)](https://github.com/djfksjd/imagination-octo/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-MIT-1f2937?style=flat-square)](LICENSE)
![Stage](https://img.shields.io/badge/stage-v0.2%20beta-d69526?style=flat-square)
![Skills](https://img.shields.io/badge/skills-3-6d5ef5?style=flat-square)
![Hosts](https://img.shields.io/badge/hosts-Claude%20Code%20%C2%B7%20Codex-0ea5b7?style=flat-square)

</div>

Imagination Octo greift in mehrere Richtungen zugleich aus und hält dann an. Es liefert ein kleines Portfolio von Ideen, die sich im Mechanismus unterscheiden, nicht in der Formulierung, und beendet den Zug. Erst nachdem du eine gewählt hast, prüft und entwickelt es diese Richtung. Die Entscheidung ist der eine Teil, den es nicht automatisiert.

**Dies ist `v0.2 beta`.** Die Messwerte unten stammen von einem einzigen Modell (`gpt-5.4`), bewertet durch KI-Aufrufe derselben Modellfamilie, auf einer kleinen Menge von Briefings. Auf Claude wurde nicht gemessen, und es ist keine Behauptung universeller Kreativität.

## Was es tut

| | |
|---|---|
| **Divergentes Portfolio** | 3–5 Richtungen aus drei Durchgängen: direkt, Mechanismus-Transfer und Prämissenwechsel. Varianten, die sich nur in Name oder Thema unterscheiden, werden aussortiert. |
| **Passung ist ein Veto** | Eine Idee, die eine harte Vorgabe aufweicht, fällt weg, egal wie überraschend sie ist. Ein umbenannter Verstoß bleibt ein Verstoß. |
| **Du wählst** | Der Router wählt und entwickelt nie im selben Zug. Automatisches Verketten senkte in Tests die Einhaltung der Vorgaben, daher ist die Pause Pflicht. |
| **Belastungstest** | Die gewählte Idee trifft auf ihre tragende Annahme, ihren einfacheren konventionellen Konkurrenten und den Fehler, den ihr eigener Mechanismus verursacht. |
| **Ehrliches Scheitern** | Ist die konventionelle Antwort besser oder hält die Richtung nicht stand, sagt es das und schickt dich zurück zum Divergieren. |
| **Kleine Laufzeit** | Drei Skill-Dateien. Zur Laufzeit keine Decks, Sperrlisten, Gates oder Skripte; in Tests etwa das 1,1-Fache der Tokens eines normalen Prompts. |

## So funktioniert es

```text
 your brief ──► ┌─────────── diverge · imagination-engine ───────────┐
                │  direct pass · mechanism transfer · premise shift  │
                │    cull by failure · private proof per survivor    │
                └──────────────────────────┬─────────────────────────┘
                                           ▼
                               3–5 distinct directions
                                           ▼
                                    ◆ YOU CHOOSE ◆        the turn always ends here
                                           ▼
                ┌─────── develop · imagination-brainstorming ────────┐
                │ load-bearing assumption · conventional competitor  │
                │   native failure mode · boring half · falsifier    │
                └──────────────────────────┬─────────────────────────┘
                                           ▼
                             decision-ready concept memo
```

- Die Pause zwischen den beiden Hälften gehört zur Methode und ist kein UI-Detail.
- Suche und Prüfung bleiben intern. Du bekommst die Ideen, nicht den Bericht über eine Pipeline.
- Es wird nichts implementiert. Das Ergebnis ist ein Konzept für die Planung.

## Schnellstart

```bash
curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination-octo/main/install.sh | bash
```

Dann frage:

```text
Nutze $imagination-octo, um mehrere Verhandlungsmechaniken für ein erzählerisches Spiel
zu erfinden, ohne Dialogbäume, verdeckte Würfel oder einen Überzeugungswert.
```

Die erste Antwort endet mit einer Auswahl. Antworte mit einer Nummer oder Richtung:

```text
Entwickle Option 2.
```

## Ein Plugin, drei Skills

| Skill | Geeignet für | Liefert |
|---|---|---|
| `$imagination-octo` | Die meisten Anfragen | Portfolio → deine Wahl → entwickeltes Konzept |
| `$imagination-engine` | Nur Divergenz | 3–5 nützliche, nicht offensichtliche Richtungen |
| `$imagination-brainstorming` | Eine bereits gewählte Idee | Ein entscheidungsreifes Konzeptmemo |

## Messwerte (2026-07-30)

Präregistrierte Blindvergleiche gegen einen starken normalen Prompt. 10 neue englische und koreanische Briefings, 5 Läufe pro Bedingung, 5 Juroren.

| Laufzeit | Lieber weiterentwickeln | Größte Zugewinne (Skala 1–7) | Tokens |
|---|---|---|---|
| Engine v0.5.3 | **50–0 (100,0 %)** | nützliche Überraschung `+0.97` · Vielfalt `+0.66` · Passung `+0.60` | 1,12× |
| Concept Workshop v0.4.2 | **45–5 (90,0 %)** | Umsetzbarkeit `+1.37` · Passung `+0.95` · Robustheit `+0.82` | 1,14× |

Ehrlich gelesen:

- **Nur `gpt-5.4` hat generiert und bewertet.** Bisher keine Läufe mit Claude und keine menschlichen Juroren. Juroren derselben Modellfamilie können denselben Geschmack haben.
- **Zehn Briefings sind eine kleine Verteilung.** 95-%-Wilson-Intervalle: Engine 92,9–100,0 %, Workshop 78,6–95,7 %.
- **Es kann verlieren.** Ein Workshop-Briefing ging einstimmig an den normalen Prompt, und ein früherer Engine-Stand verlor ein Drama-Briefing auf dieselbe Weise.
- **Ein früheres Design ist klar gescheitert.** Die Deck-und-Gate-Pipeline (Engine v0.4.0) verlor 0–30 gegen einen normalen Prompt bei 48-fachen Kosten und wurde ersetzt. Dieser Befund bleibt im Engine-Repository dokumentiert.
- **Nicht gemessen:** ob getrennte Läufe auf dieselben Ideen konvergieren, und der vollständige Zwei-Züge-Ablauf als ein Produkt.

Protokolle, Entscheidungsregeln und Ergebnisdateien: [Imagination Engine](https://github.com/djfksjd/imagination-engine-skill) · [Imagination Brainstorming](https://github.com/djfksjd/imagination-brainstorming-skill).

## Wann einsetzen, wann nicht

**Nutze es**, wenn du Optionen willst, die sich wirklich unterscheiden: Konzepte, Prämissen, Mechaniken, Produkte, Dienste, Welten, Rituale, oder wenn frühere Ideen generisch wirkten.

**Nutze einen normalen Prompt** für Faktenfragen, Routine-Implementierung, reine Namensfindung und alles, wo die konventionelle Antwort die richtige ist.

## Umbenannt von `imagination`

Dieses Plugin und sein Router-Skill hießen bis v0.1.3 `imagination`. GitHub leitet die alte Repository-URL weiter, aber Plugin-Name und Router-Befehl haben sich geändert: Entferne das alte Plugin `imagination`, installiere `imagination-octo` und rufe `$imagination-octo` auf. Die beiden Spezial-Skills behalten ihre Namen.

## Manuelle Installation

```bash
# Claude Code
claude plugin marketplace add djfksjd/imagination-octo
claude plugin install imagination-octo@djfksjd

# Codex
codex plugin marketplace add djfksjd/imagination-octo
codex plugin add imagination-octo@djfksjd
```

## Entwicklung

Die Spezial-Laufzeiten werden in eigenen Repositories gepflegt und evaluiert. Vor einem Release ihre `SKILL.md` synchronisieren, alle drei Skills validieren, die Repository-Tests ausführen und die Zwei-Züge-Grenze vorwärts testen.

```bash
python3 -m pytest tests/ -q
bash -n install.sh
```

## Lizenz

[MIT](LICENSE).
