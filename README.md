# Imagination

Imagination is one plugin with a simple, human-in-the-loop creative workflow:

```text
$imagination → 3–5 distinct ideas → you choose → one pressure-tested concept
```

It bundles three skills:

- `$imagination` — the recommended entry point and conversation router;
- `$imagination-engine` — direct access to divergent idea generation;
- `$imagination-brainstorming` — direct access to development of a chosen idea.

The router never chooses a direction and develops it in the same turn.
Automatic chaining reduced constraint fit in testing; the user's choice is the
boundary between divergence and development.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination/main/install.sh | bash
```

Manual installation:

```bash
claude plugin marketplace add djfksjd/imagination
claude plugin install imagination@djfksjd

codex plugin marketplace add djfksjd/imagination
codex plugin add imagination@djfksjd
```

## Use

Start with one command:

```text
Use $imagination to design several negotiation mechanics for a narrative game
without dialogue trees, hidden dice, or a persuasion stat.
```

The first response returns a portfolio and asks a question. Reply with a number
or direction:

```text
2번을 발전시켜 줘.
```

The next response pressure-tests and develops only that selection. It stops
before implementation so you can decide whether the concept is ready.

## Evidence

The bundled specialist runtimes are the evaluated versions:

- Imagination Engine v0.5.1: preferred 26–4 over a strong plain prompt in a
  fresh preregistered holdout.
- Imagination Brainstorming v0.4.1: preferred 25–5 over a strong plain prompt
  in a fresh preregistered holdout.

See the full reports in
[`imagination-engine-skill`](https://github.com/djfksjd/imagination-engine-skill)
and
[`imagination-brainstorming-skill`](https://github.com/djfksjd/imagination-brainstorming-skill).
The judges were independent calls to the same model family, not human domain
users, so these results do not establish universal creativity.

## Development

The specialist skills remain independently maintained and evaluated. Before a
release, sync their runtime `SKILL.md` files, validate all three skills, run the
repository tests, and forward-test the two-turn choice boundary.
