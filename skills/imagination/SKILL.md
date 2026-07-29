---
name: imagination
description: "Guide a creative request through idea generation, a required user choice, and pressure-tested concept development. Use when the user explicitly invokes $imagination to invent concepts, premises, mechanics, products, services, worlds, rituals, or other non-obvious directions, or follows up in the same conversation by selecting one of the generated ideas. Do not use for factual work, routine implementation, naming-only requests, or tasks with a known conventional answer."
---

# Imagination

Provide one simple entrance to two distinct creative phases:

1. diverge into a portfolio with `imagination-engine`;
2. wait for the user to choose;
3. develop that choice with `imagination-brainstorming`.

The pause is part of the method. Never collapse the phases into one response.
Work in the user's language.

## Determine the phase

Use the conversation state:

- **Diverge:** The user has a brief but has not selected a direction.
- **Develop:** The user explicitly selects a prior direction, names a shortlist
  winner, or arrives with one chosen idea.
- **Re-diverge:** The user rejects the portfolio and asks for new directions.

If a reply such as “the second one” has only one reasonable referent in the
conversation, treat it as an explicit selection. Ask one concise question only
when the selected direction is genuinely ambiguous.

## Diverge

Read [`../imagination-engine/SKILL.md`](../imagination-engine/SKILL.md) fully,
then follow it for the current brief. Preserve constraints already stated in
the conversation.

Return three to five directions and the engine's discriminating choice
question. End the turn there. Do not:

- select a winner for the user;
- silently rank one as the answer;
- load the concept workshop;
- produce a specification or implementation plan.

If the user asks the model to choose and continue automatically, it may state
which direction appears strongest and why in one sentence, but it must still
wait for the user to confirm that choice before development.

## Develop

Proceed only after an explicit choice. Read
[`../imagination-brainstorming/SKILL.md`](../imagination-brainstorming/SKILL.md)
fully, then follow it using the selected direction, original brief, and
constraints from the conversation.

Do not make the user restate available context. If the chosen direction
conflicts with the brief, surface the conflict instead of polishing it. Stop at
a decision-ready concept; do not implement it.

## Continue cleanly

- If the user rejects all directions, return to divergence with new mechanism
  families.
- If the user rejects part of a developed concept, rework only the failed
  assumption, mechanism, or operational burden.
- If the user selects a different portfolio item, develop the new selection
  without regenerating the portfolio.
- If the concept is accepted, summarize unresolved decisions and hand off to
  planning in a later turn.

Never read both specialist skills in the same turn. The user should experience
one coherent conversation, not the internal routing.
