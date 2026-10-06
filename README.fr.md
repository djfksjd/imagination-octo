<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/brand/imagination-octo-logo-dark.png" />
  <img src="assets/brand/imagination-octo-logo.png" alt="IMAGINATION OCTO — Voir large, en choisir une" width="380" />
</picture>

# IMAGINATION OCTO

**REACH WIDE · CHOOSE ONE**

### Un plugin créatif avec l'humain dans la boucle pour Claude Code et Codex —<br/>d'abord des idées distinctes, ensuite votre choix, enfin un concept mis à l'épreuve

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md)

[![Tests](https://img.shields.io/github/actions/workflow/status/djfksjd/imagination-octo/tests.yml?style=flat-square&label=tests)](https://github.com/djfksjd/imagination-octo/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-MIT-1f2937?style=flat-square)](LICENSE)
![Stage](https://img.shields.io/badge/stage-v0.4%20beta-d69526?style=flat-square)
![Skills](https://img.shields.io/badge/skills-3-6d5ef5?style=flat-square)
![Hosts](https://img.shields.io/badge/hosts-Claude%20Code%20%C2%B7%20Codex-0ea5b7?style=flat-square)

</div>

Imagination Octo s'étend dans plusieurs directions à la fois, puis s'arrête. Il renvoie un petit portefeuille d'idées qui diffèrent par leur mécanisme, non par leur formulation, et termine le tour. Ce n'est qu'après votre choix qu'il met cette direction à l'épreuve et la développe. La décision est la seule étape qu'il refuse d'automatiser.

**Ceci est la `v0.4 beta`.** Le tableau ci-dessous provient d'un seul modèle (`gpt-5.4`), jugé par des appels d'IA de la même famille, sur un petit ensemble de briefs. Une expérience ultérieure sur GPT et Claude existe, mais son résultat de préférence est annulé tant qu'il n'a pas été rejugé ; voir *À lire honnêtement*. Rien de tout cela ne prétend à une créativité universelle.

## Ce qu'il fait

| | |
|---|---|
| **Portefeuille divergent** | 3 à 5 directions issues de trois passes : directe, transfert de mécanisme, déplacement de prémisse. Les variantes qui ne diffèrent que par le nom ou le thème sont écartées. |
| **L'adéquation est un veto** | Une idée qui affaiblit une contrainte non négociable est abandonnée, aussi surprenante soit-elle. Une violation renommée reste une violation. |
| **Vous choisissez** | Le routeur ne choisit et ne développe jamais dans le même tour. L'enchaînement automatique a réduit le respect des contraintes lors des tests ; la pause est donc imposée. |
| **Mise à l'épreuve** | L'idée choisie affronte son hypothèse porteuse, son concurrent conventionnel plus simple et l'échec que provoque son propre mécanisme. |
| **Échec assumé** | Si la réponse conventionnelle est meilleure, ou si la direction ne tient pas, il le dit et vous renvoie à la divergence. |
| **Runtime réduit** | Trois fichiers de skill. Ni paquets de cartes, ni listes d'interdits, ni portes, ni scripts à l'exécution ; environ 1,1× les tokens d'un prompt ordinaire lors des tests. |

## Fonctionnement

```text
 your brief ──► ┌──────── diverge · imagination-octo-engine ─────────┐
                │  direct pass · mechanism transfer · premise shift  │
                │    cull by failure · private proof per survivor    │
                └──────────────────────────┬─────────────────────────┘
                                           ▼
                               3–5 distinct directions
                                           ▼
                                    ◆ YOU CHOOSE ◆        the turn always ends here
                                           ▼
                ┌───── develop · imagination-octo-brainstorming ─────┐
                │ load-bearing assumption · conventional competitor  │
                │   native failure mode · boring half · falsifier    │
                └──────────────────────────┬─────────────────────────┘
                                           ▼
                             decision-ready concept memo
```

- La pause entre les deux moitiés fait partie de la méthode, ce n'est pas un détail d'interface.
- La recherche et la preuve restent privées. Vous recevez les idées, pas le compte rendu d'un pipeline.
- Rien n'est implémenté. Le résultat est un concept à porter en planification.

## Démarrage rapide

```bash
curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination-octo/main/install.sh | bash
```

Pour mettre à jour, relancez la même commande. Si elle signale d'anciennes copies de ces skills installées séparément, terminez la commande par `| bash -s -- --clean-legacy` pour les mettre de côté ; rien n'est supprimé.

Puis demandez :

```text
Utilise $imagination-octo pour inventer plusieurs mécaniques de négociation pour un jeu
narratif, sans arbres de dialogue, dés cachés ni statistique de persuasion.
```

Dans `codex exec` ou dans un script, Codex ne reconnaît que le nom complet : `$imagination-octo:imagination-octo`.

La première réponse se termine par un choix. Répondez par un numéro ou une direction :

```text
Développe l'option 2.
```

## Un plugin, trois skills

| Skill | Idéal pour | Renvoie |
|---|---|---|
| `$imagination-octo` | La plupart des demandes | Portefeuille → votre choix → concept développé |
| `$imagination-octo-engine` | La divergence seule | 3 à 5 directions utiles et non évidentes |
| `$imagination-octo-brainstorming` | Une idée déjà choisie | Une note de concept prête pour la décision |

## Mesures (2026-07-30)

Comparaisons à l'aveugle préenregistrées contre un prompt ordinaire solide. 10 nouveaux briefs en anglais et en coréen, 5 exécutions par condition, 5 juges.

| Runtime | Préféré pour continuer | Gains principaux (échelle 1–7) | Tokens |
|---|---|---|---|
| Engine v0.5.3 | **50–0 (100,0 %)** | surprise utile `+0.97` · diversité `+0.66` · adéquation `+0.60` | 1,12× |
| Concept Workshop v0.4.2 | **45–5 (90,0 %)** | actionnabilité `+1.37` · adéquation `+0.95` · robustesse `+0.82` | 1,14× |

À lire honnêtement :

- **Seul `gpt-5.4` a généré et jugé.** Aucune exécution avec Claude ni juge humain pour l'instant. Des juges de la même famille peuvent partager ses goûts.
- **Dix briefs, c'est une petite distribution.** Intervalles de Wilson à 95 % : Engine 92,9–100,0 %, Workshop 78,6–95,7 %.
- **Il peut perdre.** Un brief du Workshop est allé à l'unanimité au prompt ordinaire, et une version antérieure de l'Engine a perdu de la même façon un brief dramatique.
- **Une conception antérieure a échoué nettement.** Le pipeline à cartes et à portes (Engine v0.4.0) a perdu 0–30 contre un prompt ordinaire pour 48× le coût et a été remplacé. Ce bilan est conservé dans le dépôt de l'Engine.
- **Expérience A (2026-10-06) : résultat de préférence annulé pour l'instant.** Une expérience préenregistrée entre modèles ([règle](evals/PREREGISTRATION.md), [résultat](evals/results/2026-10-06-experiment-a.md)) sur 12 briefs inédits, générés par `gpt-5.5` et `claude-opus-5-5` et jugés par l'autre famille. Le moteur a été préféré au prompt simple sur 11 briefs sur 12 avec GPT et 10 sur 12 avec Claude, et un prompt simple à effort égal n'a pas comblé l'écart. Mais les juges ont deviné quel côté utilisait la skill dans 22 tests sur 24 pour chaque modèle ; selon la règle fixée à l'avance, ces chiffres de préférence ne comptent donc pas tant que les sorties n'ont pas été normalisées en format puis rejugées. La vérification à l'aveugle par l'auteur reste aussi à faire. Non concerné par cela : avec le moteur, des exécutions séparées ont moins répété les mêmes mécanismes (recouvrement 0,40 contre 0,54 avec GPT, 0,50 contre 0,63 avec Claude), pour 1,08× les tokens sur GPT et 1,99× sur Claude.
- **Une candidate v0.6.0 a échoué (2026-10-06).** Elle visait à élargir les portefeuilles et à réduire la répétition. Sur 12 briefs inédits, elle n'a pas battu la v0.5.3 (5–5–2 avec GPT, 4–6–2 avec Claude) et n'a pas franchi les seuils préenregistrés sur les deux modèles ; la v0.5.3 est donc conservée ([résultat](evals/results/2026-10-06-experiment-b.md)).
- **Parcours en deux tours :** seul le comportement a été vérifié. Une suite de régression a réussi 13 cas sur 14 ; l'échec, un choix deviné quand la réponse correspondait à deux directions, a conduit à corriger le routeur. Il n'existe pas d'étude de préférence du parcours complet.

Protocoles, règles de décision et fichiers de résultats : [Imagination Octo Engine](https://github.com/djfksjd/imagination-octo-engine) · [Imagination Octo Brainstorming](https://github.com/djfksjd/imagination-octo-brainstorming).

## Quand l'utiliser, et quand s'en passer

**Utilisez-le** quand vous voulez des options réellement différentes : concepts, prémisses, mécaniques, produits, services, mondes, rituels, ou quand les idées précédentes semblaient génériques.

**Utilisez un prompt ordinaire** pour les questions factuelles, l'implémentation courante, le simple nommage, ou tout cas où la réponse conventionnelle est la bonne.

## Journal des choix (optionnel)

Désactivé par défaut. Une fois activé, chaque fois que vous choisissez une direction ou rejetez un portefeuille, une ligne est ajoutée à `~/.imagination-octo/choices.jsonl` sur votre machine : les directions proposées, votre choix et la raison que vous avez donnée. Les briefs sont enregistrés sous forme de hachage, sauf si vous demandez le texte. Rien n'est envoyé et les skills ne lisent jamais ce journal ; il sert à étudier vos propres choix. `enable --hosts` ajoute une ligne balisée à votre `CLAUDE.md` / `AGENTS.md` global pour que la skill voie l'activation, et `disable` la retire.

```bash
LOG=https://raw.githubusercontent.com/djfksjd/imagination-octo/main/skills/imagination-octo/scripts/choice_log.py
curl -fsSL $LOG | python3 - enable --hosts claude,codex   # --with-brief keeps the brief text
curl -fsSL $LOG | python3 - stats
curl -fsSL $LOG | python3 - disable
```

## Anciennement `imagination`

Ce plugin et sa skill de routage s'appelaient `imagination` jusqu'à la v0.1.3. GitHub redirige l'ancienne URL du dépôt, mais le nom du plugin et la commande du routeur ont changé : supprimez l'ancien plugin `imagination`, installez `imagination-octo` et appelez `$imagination-octo`. Depuis la v0.4, les deux skills spécialisées et leurs dépôts portent aussi le nom de la famille : `$imagination-octo-engine` et `$imagination-octo-brainstorming` remplacent `$imagination-engine` et `$imagination-brainstorming`. Depuis la v0.3, l'identifiant du marketplace a lui aussi changé, de `djfksjd` à `imagination-octo`, car l'ancien entrait en collision avec d'autres plugins du même auteur. La cible d'installation est désormais `imagination-octo@imagination-octo`.

## Installation manuelle

```bash
# Claude Code
claude plugin marketplace add djfksjd/imagination-octo
claude plugin install imagination-octo@imagination-octo

# Codex
codex plugin marketplace add djfksjd/imagination-octo
codex plugin add imagination-octo@imagination-octo
```

## Développement

Les runtimes spécialisés sont maintenus et évalués dans leurs propres dépôts. Avant une publication, synchronisez leurs `SKILL.md`, validez les trois skills, lancez les tests du dépôt et testez en conditions réelles la frontière entre les deux tours.

```bash
python3 -m pytest tests/ -q
bash -n install.sh
```

## Licence

[MIT](LICENSE).
