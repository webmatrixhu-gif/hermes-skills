# Visualize This — Mode Recipes

Use the recipe that best matches the user’s explicit request. These define content coverage, not a fixed visual style.

## General explainer

Use for “visualize this,” a concept, a pasted explanation, a document, or a conversation result.

1. State the first-viewport takeaway.
2. Show the core entities or ideas and their relationships.
3. Separate “how it works” from “why it matters.”
4. Add detail progressively: overview first, evidence and caveats later.
5. End with a compact takeaway or decision panel when the source supports one.

Do not add a recommendation unless the source or user’s decision goal calls for it.

## Architecture or process flow

Gather actual components, boundaries, entry points, data/control flow, storage, external systems, and failure paths.

Recommended sections:

1. System purpose and scope boundary.
2. Small relationship overview (Mermaid or inline SVG).
3. Layer/module cards with responsibilities and evidence.
4. Primary request/data flow.
5. State, persistence, or integration boundaries.
6. Failure modes, risks, or operational notes supported by evidence.
7. Useful files/commands when visualizing a repository.

For 15+ entities, keep the overview to 5–8 conceptual nodes and move implementation detail into cards.

## Visual diff review

Resolve the requested branch, commit, range, PR, or working tree before generating. Gather diff stats, name-status, changed files, public API/type/function changes, tests, dependencies/config, docs/changelog, and relevant surrounding paths.

Required sections:

1. Executive summary and exact scope.
2. Complete file map: added, modified, deleted.
3. Architecture or behavior impact.
4. Before/after comparison.
5. Risk review: correctness, tests, compatibility, security/privacy, performance, maintainability.
6. Coupling and migration/release concerns.
7. Readiness recommendation: blockers and follow-ups.

Use red for removed/before, green for added/after, amber for changed/risk, and a neutral accent for context. Cite file paths and `file:line` evidence; do not invent implementation rationale.

## Visual plan review

Read the complete plan and inspect the affected code paths before judging feasibility.

Required sections:

1. Plan objective and assumptions.
2. Current-state architecture relevant to the plan.
3. Proposed-state architecture or sequence.
4. Requirement/step coverage matrix.
5. Dependencies and ordering.
6. Edge cases, rollback, migration, observability, and test coverage.
7. Risks and contradictions grounded in source evidence.
8. Recommended amendments and readiness decision.

Distinguish plan statements, observed code facts, and reviewer inferences visually.

## Visual implementation plan

Use when the user explicitly asks for a visual plan rather than a review of an existing plan.

Required sections:

1. Problem and desired outcome.
2. Current versus target state.
3. Architecture/data-flow changes.
4. Dependency-ordered phases.
5. Files/modules likely affected, only after inspecting them.
6. State transitions, edge cases, and error paths.
7. Tests and verification gates.
8. Rollback/deployment considerations.
9. Open decisions and assumptions.

Do not present guessed file names or APIs as facts.

## Visual project recap

Gather project identity files, build manifests, top-level structure, current git status, recent commits, key entry points, uncommitted work, and evidence-backed blockers/TODOs.

Required sections:

1. Project identity, stack, and purpose.
2. Architecture snapshot.
3. Recent activity grouped into a narrative.
4. Current state: branch, uncommitted work, blockers.
5. Mental model: modules, data flow, build/test/deploy paths.
6. Risks, hotspots, and cognitive debt.
7. Useful commands and files.
8. Likely next steps, clearly marked as evidence-backed or inferred.

Never fabricate momentum, ownership, rationale, or project status.

## Visual fact check

Identify the claims in the supplied document or explanation, then verify them against authoritative source material.

Required sections:

1. Scope and source hierarchy.
2. Claim summary with status counts.
3. Claim-by-claim matrix: supported, contradicted, incomplete, unverifiable.
4. Evidence with source/file references.
5. Material omissions or misleading framing.
6. Corrected mental model.
7. Recommended edits, separated from factual findings.

Do not treat absence from a secondary source as proof of falsity.

## Data comparison, audit, or status matrix

Use semantic `<table>` markup. Preserve all rows and columns from the source.

Include:

- a compact headline finding;
- legend/status definitions;
- sortable/filterable controls only if they materially help;
- row/column headers and captions;
- local horizontal scrolling on narrow screens;
- notes/evidence columns when conclusions need traceability.

Do not convert sparse qualitative material into fake metrics.

## Timeline or roadmap

Separate observed history, committed future work, and speculative next steps.

Include dates only when supplied or verified. Represent uncertainty visibly instead of inventing precision. Show dependencies and milestones when they affect sequencing.

## Dashboard or metrics explainer

Use charts only for real numeric data. State units, time windows, aggregation, and source. Avoid decorative charts whose shape implies unsupported trends.

Recommended hierarchy:

1. One headline metric or status.
2. Small set of supporting KPIs.
3. One or two charts answering explicit questions.
4. Explanatory annotations and caveats.
5. Source/methodology note.

## HTML slide deck

Use only when the user explicitly requests slides, a deck, or presentation format.

1. Inventory every material source item.
2. Map every item to a slide before generating.
3. Assign varied slide types and compositions.
4. Keep each slide to `100dvh`; split rather than scroll.
5. Include navigation, count/progress, keyboard, wheel/touch behavior, and visible focus.
6. Preserve source coverage; do not force a fixed slide count.
7. Verify at common desktop and short landscape heights.

Generated images are optional. Use Hermes `image_generate` only when imagery is part of the requested tone or materially improves a title/full-bleed moment. Structural and data-heavy decks should work without it.
