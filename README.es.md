<div align="center">

<img src="assets/brand/imagination-octo-logo.png" alt="IMAGINATION OCTO — Alcanza lejos, elige una" width="380" />

# IMAGINATION OCTO

**REACH WIDE · CHOOSE ONE**

### Un plugin creativo con la persona en el circuito para Claude Code y Codex —<br/>primero ideas distintas, después tu elección, al final un concepto puesto a prueba

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md)

[![Tests](https://img.shields.io/github/actions/workflow/status/djfksjd/imagination-octo/tests.yml?style=flat-square&label=tests)](https://github.com/djfksjd/imagination-octo/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-MIT-1f2937?style=flat-square)](LICENSE)
![Stage](https://img.shields.io/badge/stage-v0.2%20beta-d69526?style=flat-square)
![Skills](https://img.shields.io/badge/skills-3-6d5ef5?style=flat-square)
![Hosts](https://img.shields.io/badge/hosts-Claude%20Code%20%C2%B7%20Codex-0ea5b7?style=flat-square)

</div>

Imagination Octo se extiende en varias direcciones a la vez y luego se detiene. Devuelve un pequeño portafolio de ideas que difieren en su mecanismo, no en su redacción, y termina el turno. Solo cuando eliges una la pone a prueba y la desarrolla. La decisión es lo único que se niega a automatizar.

**Esto es `v0.2 beta`.** Las mediciones de abajo provienen de un solo modelo (`gpt-5.4`), evaluado por llamadas de IA de la misma familia, sobre un conjunto pequeño de briefs. No se ha medido en Claude y no es una afirmación de creatividad universal.

## Qué hace

| | |
|---|---|
| **Portafolio divergente** | 3–5 direcciones construidas con tres pasadas: directa, transferencia de mecanismos y cambio de premisa. Se descartan las variantes que solo cambian de nombre o de tema. |
| **El ajuste es un veto** | Una idea que debilita un requisito innegociable se descarta, por sorprendente que sea. Una infracción con otro nombre sigue siendo una infracción. |
| **Tú eliges** | El enrutador nunca elige y desarrolla en el mismo turno. El encadenamiento automático redujo el ajuste a las restricciones en las pruebas, así que la pausa es obligatoria. |
| **Prueba de presión** | La idea elegida se enfrenta a su supuesto de carga, a su competidor convencional más simple y al fallo que provoca su propio mecanismo. |
| **Fracaso honesto** | Si la respuesta convencional es mejor, o la dirección no sobrevive, lo dice y te devuelve a divergir. |
| **Runtime pequeño** | Tres archivos de skill. Sin mazos, listas de prohibición, compuertas ni scripts en ejecución; alrededor de 1,1× los tokens de un prompt normal en las pruebas. |

## Cómo funciona

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

- La pausa entre las dos mitades es parte del método, no un detalle de interfaz.
- La búsqueda y la prueba son privadas. Recibes las ideas, no un informe de que se ejecutó un pipeline.
- No se implementa nada. El resultado es un concepto que puedes llevar a planificación.

## Inicio rápido

```bash
curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination-octo/main/install.sh | bash
```

Luego pide:

```text
Usa $imagination-octo para inventar varias mecánicas de negociación para un juego
narrativo sin árboles de diálogo, dados ocultos ni estadística de persuasión.
```

La primera respuesta termina con una elección. Responde con un número o una dirección:

```text
Desarrolla la opción 2.
```

## Un plugin, tres skills

| Skill | Ideal para | Devuelve |
|---|---|---|
| `$imagination-octo` | La mayoría de las peticiones | Portafolio → tu elección → concepto desarrollado |
| `$imagination-engine` | Solo divergencia | 3–5 direcciones útiles y no obvias |
| `$imagination-brainstorming` | Una idea que ya elegiste | Un memo de concepto listo para decidir |

## Mediciones (2026-07-30)

Comparaciones ciegas prerregistradas contra un prompt normal sólido. 10 briefs nuevos en inglés y coreano, 5 ejecuciones por condición, 5 jueces.

| Runtime | Preferido para continuar | Mayores mejoras (escala 1–7) | Tokens |
|---|---|---|---|
| Engine v0.5.3 | **50–0 (100,0 %)** | sorpresa útil `+0.97` · diversidad `+0.66` · ajuste `+0.60` | 1,12× |
| Concept Workshop v0.4.2 | **45–5 (90,0 %)** | accionabilidad `+1.37` · ajuste `+0.95` · robustez `+0.82` | 1,14× |

Léelas con honestidad:

- **Solo `gpt-5.4` generó y juzgó.** Aún no hay ejecuciones con Claude ni jueces humanos. Los jueces de la misma familia pueden compartir su gusto.
- **Diez briefs son una distribución pequeña.** Intervalos de Wilson al 95 %: Engine 92,9–100,0 %, Workshop 78,6–95,7 %.
- **Puede perder.** Un brief del Workshop fue por unanimidad para el prompt normal, y una versión anterior del Engine perdió igual un brief de drama.
- **Un diseño anterior fracasó por completo.** El pipeline de mazos y compuertas (Engine v0.4.0) perdió 0–30 contra un prompt normal con 48× el coste y fue reemplazado. Ese registro se conserva en el repositorio del Engine.
- **Sin medir:** si ejecuciones separadas convergen en las mismas ideas, y el flujo completo de dos turnos como un solo producto.

Protocolos, reglas de decisión y archivos de resultados: [Imagination Engine](https://github.com/djfksjd/imagination-engine-skill) · [Imagination Brainstorming](https://github.com/djfksjd/imagination-brainstorming-skill).

## Cuándo usarlo y cuándo no

**Úsalo** cuando quieras opciones que de verdad difieran: conceptos, premisas, mecánicas, productos, servicios, mundos, rituales, o cuando las ideas anteriores resultaron genéricas.

**Usa un prompt normal** para preguntas factuales, implementación rutinaria, solo nombres, o cualquier caso en que la respuesta convencional sea la correcta.

## Antes se llamaba `imagination`

Este plugin y su skill enrutadora se llamaban `imagination` hasta la v0.1.3. GitHub redirige la URL antigua del repositorio, pero el nombre del plugin y el comando del enrutador cambiaron: elimina el plugin `imagination` antiguo, instala `imagination-octo` e invoca `$imagination-octo`. Las dos skills especializadas conservan su nombre.

## Instalación manual

```bash
# Claude Code
claude plugin marketplace add djfksjd/imagination-octo
claude plugin install imagination-octo@djfksjd

# Codex
codex plugin marketplace add djfksjd/imagination-octo
codex plugin add imagination-octo@djfksjd
```

## Desarrollo

Los runtimes especializados se mantienen y evalúan en sus propios repositorios. Antes de publicar, sincroniza sus `SKILL.md`, valida las tres skills, ejecuta las pruebas del repositorio y prueba hacia adelante el límite de dos turnos.

```bash
python3 -m pytest tests/ -q
bash -n install.sh
```

## Licencia

[MIT](LICENSE).
