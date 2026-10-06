# Repository guide

The plugin exposes three skills:

- `skills/imagination-octo/SKILL.md` is the user-facing state router.
- `skills/imagination-octo-engine/SKILL.md` is the evaluated divergence runtime.
- `skills/imagination-octo-brainstorming/SKILL.md` is the evaluated development runtime.

Preserve the user-choice boundary. The router must never select and develop a
direction in the same turn. Keep both specialist runtimes synchronized with
their source repositories before release, and rerun forward tests after any
runtime change.

`skills/imagination-octo/scripts/choice_log.py` is the opt-in choice log. It
must stay local-only, disabled by default, and write-only for the skills.

`evals/` holds the cross-model harness. Change a runtime only in response to a
diagnosed loss, freeze `evals/PREREGISTRATION.md` and the briefs before a
confirmation run, and retire a brief set once its outputs have been read.

Do not commit local evaluation runs, caches, secrets, or generated work.
Validate all three skills and the plugin manifest before committing.
