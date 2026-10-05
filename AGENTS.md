# Repository guide

The plugin exposes three skills:

- `skills/imagination-octo/SKILL.md` is the user-facing state router.
- `skills/imagination-engine/SKILL.md` is the evaluated divergence runtime.
- `skills/imagination-brainstorming/SKILL.md` is the evaluated development runtime.

Preserve the user-choice boundary. The router must never select and develop a
direction in the same turn. Keep both specialist runtimes synchronized with
their source repositories before release, and rerun forward tests after any
runtime change.

Do not commit local evaluation runs, caches, secrets, or generated work.
Validate all three skills and the plugin manifest before committing.
