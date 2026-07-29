<div align="center">

# ✨ Imagination

**Générez des idées distinctes. Choisissez. Développez celle qui résiste.**

Un plugin créatif avec décision humaine pour Codex et Claude Code.

[![Tests](https://github.com/djfksjd/imagination/actions/workflows/tests.yml/badge.svg)](https://github.com/djfksjd/imagination/actions/workflows/tests.yml)
![Version](https://img.shields.io/badge/version-0.1.1-7c3aed)
![Licence](https://img.shields.io/badge/license-MIT-0f766e)

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md)

</div>

---

Imagination vous laisse ce que l’IA ne doit pas automatiser : **le choix**. Le
plugin propose d’abord des directions causalement différentes, attend votre
décision, puis éprouve uniquement l’idée retenue.

```text
Brief → 3 à 5 directions → vous choisissez → concept éprouvé
```

## Démarrage rapide

```bash
curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination/main/install.sh | bash
```

```text
Utilise $imagination pour proposer plusieurs directions vraiment différentes.
```

La première réponse s’arrête au choix. Répondez avec un numéro pour développer
cette seule option au tour suivant.

## Trois skills

| Skill | Usage |
|---|---|
| `$imagination` | Entrée recommandée : divergence, choix, développement |
| `$imagination-engine` | Générer 3 à 5 directions utiles et non évidentes |
| `$imagination-brainstorming` | Transformer une idée choisie en concept décisionnel |

> [!IMPORTANT]
> Le routeur ne choisit et ne développe jamais une idée au même tour. Votre
> choix est la frontière obligatoire entre divergence et développement.

## Résultats mesurés

| Runtime | Préférence face à un prompt fort | Principaux gains |
|---|---:|---|
| Engine v0.5.2 | **25–5 (83,3 %)** | surprise utile `+0,98`, diversité `+0,93`, adéquation `+0,31` |
| Workshop v0.4.1 | **25–5 (83,3 %)** | applicabilité `+1,37`, adéquation `+0,59`, clarté causale `+0,59` |

Ces résultats proviennent de juges modèles sur la distribution préenregistrée ;
ils ne garantissent pas une supériorité universelle.

## Installation manuelle

```bash
claude plugin marketplace add djfksjd/imagination
claude plugin install imagination@djfksjd
codex plugin marketplace add djfksjd/imagination
codex plugin add imagination@djfksjd
```

Licence MIT.
