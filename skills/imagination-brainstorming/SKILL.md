---
name: imagination-brainstorming
description: "Develop and pressure-test an idea the user has already selected, turning it into a coherent concept before implementation. Use only when the user explicitly invokes imagination-brainstorming during v0.4 evaluation and provides a chosen direction, shortlist winner, or rough concept to deepen. Not for initial idea generation, open-ended brainstorming, naming, factual work, or implementation planning."
---

# Imagination Brainstorming

Turn a chosen idea into a concept that can survive contact with its purpose,
users, constraints, and ordinary operation. Preserve what made the direction
worth choosing while exposing what it costs.

This is a concept workshop, not an idea generator. If the user has not selected
a direction, ask them to choose one or use `imagination-engine` when available.
Do not manufacture three alternatives, an unsafe option, or a ban contract.

Work in the user's language. Use relevant project files when they exist, but do
not make the user repeat information already available.

## Establish the decision

Identify:

- the selected idea in one sentence;
- the outcome and audience it must serve;
- the non-negotiable constraints;
- why this direction was preferred over the obvious alternative;
- the next decision the concept must enable.

Ask one question at a time only when its answer can change the concept. Do not
run a fixed interview or delay useful work to collect complete requirements.
When the brief is already sufficient, proceed and mark genuine uncertainties
as open questions.

Before elaborating, test the selected direction literally against every
non-negotiable and the intended outcome. Treat a renamed, relocated, or
indirect version of an excluded mechanism as the same mechanism. Do not let a
polished memo launder a constraint violation or an idea that lacks a credible
path to the outcome. If the conflict is direct, stop development, name it, and
ask the user to approve the smallest viable repair or return to divergence.
For each exclusion, privately map the job the forbidden mechanism performs to
the proposed components and actions. If a component performs the same job
under a new name, owner, location, or scale, treat it as a conflict. Treat
material ambiguity as a blocker rather than explaining it away.

## Pressure-test before elaborating

Test the selected direction against three challenges:

1. **Load-bearing assumption:** Which single assumption would collapse the idea
   if false? Seek the strongest evidence or observation on both sides.
2. **Conventional competitor:** What simpler or more familiar approach serves
   the same outcome? State why the selected idea earns its extra complexity. If
   it does not, recommend the conventional approach.
3. **Native failure mode:** How does this idea fail because of its defining
   mechanism, not because of generic poor execution?

Check the direction of every important “because”:

- premise or evidence;
- proposed conclusion;
- strongest opposite conclusion supported by the same premise;
- the observation that distinguishes them;
- who can actually observe that distinction.

Cut or qualify a claim when the evidence supports the opposite equally well.
Do not turn an unsupported rationale into confident prose.

## Build the concept

Develop only the sections the decision needs. Cover these elements in some
form, without forcing a universal document shape:

- **Core mechanism:** what happens, between whom or what, and why it changes the
  current outcome.
- **First concrete use:** one realistic moment that reveals the mechanism and
  the user's required action.
- **Intentional refusal:** what the concept does not support on purpose, why,
  and who bears the cost.
- **Boring half:** ownership, recurring work, queue, exception, sign-off,
  maintenance, or reconciliation that makes the concept operational.
- **Failure response:** how the design detects, contains, or learns from its
  native failure mode.
- **Falsifier:** an observable result that would show the mechanism or its
  rationale is wrong.
- **Nearest existing approaches:** what is already similar and the specific
  operational difference. Never claim historical novelty.
- **Open decisions:** questions whose answers would materially change scope,
  feasibility, or value.

Prefer concrete mechanisms and decisions to persuasive language. Do not add
features to make every stakeholder happy; a concept with no refusal is not yet
a choice.

When the comparison depends on current law, medicine, safety practice, or
technical standards, verify it with authoritative sources and distinguish the
verified fact from your inference.

## Review proportionately

Use a lightweight adversarial pass:

- Could the conventional competitor achieve the outcome with fewer new
  behaviours or dependencies?
- Is the distinctive mechanism visible to the person or system whose behaviour
  is supposed to change?
- Does the failure response alter the failure, or merely restate it?
- Is the boring half owned by someone with the capacity and incentive to do it?
- Could a competent team build the obvious version and still claim it followed
  this concept?
- Which open question is a blocker, and which can safely wait?

Revise once around the strongest objection. Do not create a mechanical gate or
absolute self-score. If the idea loses on its own terms, say so plainly and
recommend returning to divergence.

## Deliver the decision artifact

Default to a concise concept memo in the conversation. Include:

1. the decision and its purpose;
2. the mechanism;
3. the intentional refusal and trade-off;
4. the first concrete use;
5. the boring half;
6. the native failure, response, and falsifier;
7. nearest existing approaches;
8. blockers and open decisions.

Adapt length and headings to the subject. A ritual, story premise, service, and
software feature should not be rendered through one identical template.

Write a project file only when the user asks for a spec or when producing one is
clearly part of the requested deliverable. Follow the project's convention; if
none exists, use `docs/concepts/YYYY-MM-DD-<topic>.md`. Do not create a JSON
sidecar or hidden contract.

End with the single decision the user should make next. Do not implement,
scaffold, or invoke an implementation workflow while this skill is active.
When the concept is accepted, state what remains unresolved and hand off to the
appropriate planning workflow.

## Rework

When the user rejects the concept, identify whether the failure is in the goal,
assumption, mechanism, or operational burden. Revisit that layer only. Do not
restart a scripted process, redeal random frames, or make the concept stranger
to avoid the criticism.
