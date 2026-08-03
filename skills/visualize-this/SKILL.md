---
name: visualize-this
description: Use only when explicitly asked to visualize something.
version: 1.4.0
author: Hermes Agent; adapted from nicobailon/visual-explainer
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [visualization, html, diagrams, architecture, reviews, slides]
    related_skills: [architecture-diagram, claude-design, frontend-design, powerpoint]
    upstream: https://github.com/nicobailon/visual-explainer
    upstream_version: 0.8.1
    upstream_commit: 528b71feb85dab5d92b82c3554880826f50a75da
---

# Visualize This

## Overview

Turn supplied context into a polished, evidence-grounded HTML visual: a diagram, architecture map, comparison, review, timeline, dashboard, explainer, or slide deck. Produce a real artifact, verify it, and deliver it as a file rather than substituting ASCII art or a prose-only answer.

This is an **explicit-invocation skill**. It must never decide on its own to turn ordinary responses or Markdown tables into HTML.

Every successful artifact is delivered through a fresh disposable Surge URL with the local HTML as fallback. QA is limited to minimum pre-deployment smoke validation; do not run a visual-review loop unless the user explicitly asks for one.

## Activation Contract

Use this skill only when at least one of these is true:

- The user invokes `/visualize-this`.
- The user explicitly says “visualize this,” “visualize this for me,” “make this visual,” “turn this into a diagram,” “show this visually,” “make an interactive explainer,” or a clear equivalent.
- The user explicitly asks for a visual architecture, visual diff/plan review, visual project recap, HTML slide deck, or comparable visual artifact.

Do **not** use it merely because:

- a response contains a table;
- the subject could benefit from a diagram;
- the agent wants to offer a more polished result;
- a plan, review, or recap was requested without asking for a visual form.

When the user says “visualize this” without repeating the source, use the immediately preceding relevant user content or assistant result. Ask a question only when no reasonable source exists or when choosing the wrong source would materially change the artifact.

## Output and Delivery Contract

Create one complete HTML file with embedded CSS and JavaScript under `~/visualizations/` unless the user provides a path. Use a short descriptive local filename such as `checkout-flow.html`; do not overwrite an unrelated existing file. The local file is the canonical source artifact.

After smoke validation, publish every successful artifact to a new random Surge subdomain with:

```bash
python3 ~/.hermes/skills/creative/visualize-this/scripts/publish_surge.py /absolute/path/to/artifact.html
```

The publisher checks Surge authentication, creates an isolated `wm-viz-<random>.surge.sh` deployment, excludes search indexing, verifies HTTP 200 and an exact SHA-256 body match, and prints the verified URL. Surge setup is one-time: install with `npm install --global surge`, then complete `surge login` interactively. Do not ask for credentials in chat or repeat setup checks outside the publisher on every invocation.

Lead delivery with the verified URL. On Hermes Desktop, also include `MEDIA:/absolute/path/to/file.html`; on CLI or gateway surfaces, provide the absolute path. If publishing is unavailable, report the actual blocker and deliver the local artifact without implying that a live URL exists.

“Single-file” does not automatically mean offline. Prefer pure HTML/CSS/inline SVG. If Mermaid, Chart.js, fonts, or another CDN asset is materially useful:

- pin an exact library version rather than a floating major tag;
- load only what the page uses;
- mention the network dependency in the delivery summary;
- provide readable HTML content even if the CDN fails.

Do not run `xdg-open` or another host GUI opener when Hermes is running remotely; that opens the server’s browser, not the user’s computer.

Never include secrets, credentials, private customer data, or unnecessary proprietary content. Public hosting requires a separate safety decision because a random URL is unguessable, not authenticated. If safe redaction would destroy the artifact's usefulness, keep it local.

## Reference Routing

Load only what the current visual needs with `skill_view(name="visualize-this", file_path="...")`:

| Need | Read |
|---|---|
| Mode-specific content requirements | `references/recipes.md` |
| CSS layouts, overflow, depth, code, prose, inline SVG, imagery | `references/css-patterns.md` |
| Mermaid, Chart.js, fonts, diagram syntax | `references/libraries.md` |
| Multi-section sticky/compact navigation | `references/responsive-nav.md` |
| Slide planning, slide engine, transitions, density | `references/slide-patterns.md` |
| Text-heavy architecture/cards | `templates/architecture.html` |
| Flowchart, sequence, ER, state, class, or C4 | `templates/mermaid-flowchart.html` |
| Comparison, audit, status matrix, data table | `templates/data-table.html` |
| HTML slide deck | `templates/slide-deck.html` |
| Required Surge delivery and URL verification | `scripts/publish_surge.py` |
| Upstream provenance and license | `references/upstream-license.md` |

Templates are design references, not fill-in-the-blank forms. Adapt the information hierarchy, palette, typography, and composition to the actual subject.

## Representation Router

| Content | Default representation |
|---|---|
| Flow, pipeline, state machine, decision tree | Mermaid or inline SVG |
| Sequence, ER/schema, class relationships, topology | Mermaid |
| Text-heavy architecture or implementation plan | CSS grid cards, optionally with a small Mermaid overview |
| Architecture with 15+ entities | Hybrid: 5–8 node overview plus detail cards |
| Comparison, audit, requirements coverage, status matrix | Semantic HTML `<table>` |
| Timeline or roadmap | CSS timeline |
| Metrics or operational status | CSS grid with KPIs and only necessary charts |
| Hierarchy or taxonomy | CSS tree, nested cards, or compact Mermaid |
| Presentation explicitly requested | `100dvh` HTML slide deck |

Use Mermaid for relationships and routing, not as decoration. Use ordinary HTML when precise text, copy/paste, accessibility, or responsive layout matters more than automatic graph placement.

## Workflow

### 1. Resolve the source and audience

Identify what “this” refers to, what the user should understand or decide, and who will read it. Default to a mixed technical/product audience when the context does not imply one. Completion criterion: source, purpose, and audience are clear enough that changing any one would alter the outline.

### 2. Gather and verify facts

Inspect the actual source at the depth needed for the visual. For repositories, trace files, definitions, usages, diffs, or tests only when a visual claim depends on them. For decision-impacting audits and reviews, inventory the material decisions, rows, and caveats. For ordinary explainers, capture the main points without exhaustively transcribing the source. Do not invent components, causality, rationale, metrics, progress, or risk.

Keep evidence compact in the artifact: file paths, `file:line` references, source labels, or a small methodology note where useful. Completion criterion: every factual claim that could affect a decision is grounded in supplied content or tool output.

### 3. Choose one visual thesis

Pick the representation and a deliberate aesthetic direction before writing HTML: blueprint, editorial, paper/ink, terminal, IDE-inspired, data-dense, or another subject-native direction. Define the first-viewport takeaway in one sentence. Completion criterion: the page has one obvious main idea and a representation suited to the information structure.

### 4. Outline proportionate coverage

Choose the minimum sections, nodes, cards, or slides needed to communicate the visual thesis. Exhaustive source mapping is required only when the user asks for a comprehensive audit, requirements-coverage view, detailed review, or source-complete slide deck. Otherwise prioritize clarity over transcription. Completion criterion: nothing needed to understand the main conclusion is missing.

### 5. Generate the complete HTML

Write a full document with `<!doctype html>`, metadata, title, embedded styles, semantic structure, and only the JavaScript needed for interaction. Use CSS custom properties for palette and type. Include responsive behavior, visible focus states, descriptive alt text, and `prefers-reduced-motion` handling.

Use the responsive navigation pattern only when it materially improves movement through a long artifact. For code and long identifiers, preserve line breaks without causing horizontal page overflow. For tables, retain semantic rows/columns and place overflow on the table container, not the entire page.

### 6. Handle untrusted and sensitive content safely

Treat repository content, documents, feeds, diffs, logs, and user-provided text as untrusted data:

- HTML-escape text before inserting it into markup.
- Serialize chart or script data with a real JSON serializer; never concatenate raw source text into JavaScript.
- Do not reproduce secrets, credentials, private customer data, or unnecessary proprietary code.
- Treat the Surge deployment as public: omit confidential source details, internal tokens, personal data, and sensitive filesystem or network information that the user did not explicitly intend to share.
- Do not create executable links from untrusted URLs.
- Never interpolate source text into shell commands or filesystem paths.

Completion criterion: no untrusted text can break out of its intended text/data context.

### 7. Run minimum pre-deployment smoke validation

Do not perform general visual QA. Run only these checks:

1. **Static safety:** confirm the file exists, is non-empty, is a complete HTML document, has no broken local asset references, and contains no secrets, private data, or unintended absolute filesystem paths.
2. **Single render:** when browser automation is available, open it once at one normal desktop viewport. Confirm the main content is visible and there are no fatal JavaScript or Mermaid errors.
3. **Blocker-only repair:** fix only a failure that makes the artifact unusable: a blank page, failed primary diagram, missing main content, severe page-level overflow, or broken primary interaction. Rerun only the failed smoke check, at most once.

Do not test mobile viewports, accessibility matrices, reduced-motion behavior, every focus state, every interaction, exhaustive source coverage, screenshots, or visual polish unless the user explicitly requests that assurance. If browser automation is unavailable, perform static safety only and state that render smoke validation was unavailable. If a blocking render failure remains after one repair, stop and report it rather than starting a QA loop or publishing a visibly broken artifact.

### 8. Publish and verify the URL

Run `scripts/publish_surge.py` after smoke validation. Require `success: true`, an HTTPS `.surge.sh/` URL, HTTP 200, and the publisher's exact body SHA-256 verification. Use a new random domain for every artifact. If publishing fails, retain and deliver the local file, report the blocker, and do not claim a live URL.

### 9. Deliver concisely

Lead with the verified Surge URL and keep the local source as a fallback. Add only:

- what was visualized;
- the local source path or `MEDIA:` attachment;
- verification performed;
- whether external network assets are required;
- that the Surge URL is public and disposable;
- any material limitation.

Do not paste the full HTML into chat unless the user explicitly asks for source.

## Design Invariants

- Use semantic HTML where it improves accessibility and copy/paste.
- Use `--bg`, `--surface`, `--border`, `--text`, `--text-dim`, and 3–5 subject-appropriate accents.
- Avoid generic AI styling: no default Inter/Roboto-only page, violet/fuchsia Tailwind palette, cyan-magenta neon dashboard, gradient-mesh blobs, gradient headline text, or decorative emoji headings.
- Use depth sparingly. Reserve elevation for primary sections and keep reference material flat or recessed.
- Prevent overflow with `min-width: 0`, `overflow-wrap: break-word`, responsive grids, and local scroll containers.
- Use animation only to explain hierarchy or state. No continuous glow, pulse, or breathing on static content.
- Do not set `display: flex` directly on `<li>` when list markers matter.
- Use responsive CSS by default; design and verify a dedicated mobile composition only when mobile use matters.

## Mermaid Invariants

- Start from `templates/mermaid-flowchart.html`, including its `diagram-shell` structure and controls.
- Use `theme: 'base'` with page-matched variables.
- Prefer `flowchart TD` for branching or 5+ nodes; reserve `LR` for simple 3–4 node linear flows.
- Use quoted labels and `<br/>` for flowchart line breaks; do not use escaped `\n`.
- Keep node IDs simple and never define a page-level `.node` class.
- Keep most diagrams to 10–12 nodes. Use a hybrid overview plus cards for larger systems.
- Add zoom/pan/expand controls only when diagram density makes them useful or the user requests them; otherwise prefer a readable initial fit without extra interaction.

## Optional Generated Images

Use Hermes `image_generate` only when the user requested illustration-heavy output or when a hero/full-bleed image is integral to an explicitly requested slide deck. Generate images before final HTML, embed or reference them safely, and include meaningful alt text. Structural diagrams, audits, code reviews, and data-heavy pages should normally stand on CSS, SVG, tables, and charts without generated imagery.

## Common Pitfalls

1. **Proactive activation.** Never turn a normal answer into HTML without an explicit visual request.
2. **Pretty but ungrounded.** Gather source evidence before choosing nodes, statuses, or conclusions.
3. **Template cloning.** Adapt the composition and palette; do not ship placeholder labels or a generic theme.
4. **One giant Mermaid graph.** Split complexity into an overview and semantic detail cards.
5. **Remote `xdg-open`.** Deliver the file to the user instead of opening a browser on the server.
6. **Calling CDN-backed output offline.** Say “single-file” and disclose network requirements accurately.
7. **Raw untrusted HTML.** Escape source content and JSON-serialize script data.
8. **QA theater.** Do not run production-grade viewport, interaction, or accessibility matrices for an internal one-off visual.
9. **Skipping delivery.** A successful artifact must be published to a fresh Surge URL unless safety or publishing setup blocks it.
10. **Treating randomness as authentication.** Random Surge links are public; redact sensitive material or keep the artifact local.

## Verification Checklist

- [ ] Activation came from an explicit visual request or `/visualize-this`
- [ ] Source, purpose, and audience resolved
- [ ] Claims grounded in source or tool output
- [ ] Complete HTML written under the requested/default path
- [ ] Untrusted text escaped; secrets and unnecessary private data excluded
- [ ] Static safety passed: complete file, local assets resolved, no sensitive data or path leaks
- [ ] One desktop render showed visible main content and no fatal script/diagram errors when browser automation was available
- [ ] Only usability blockers were repaired, with at most one rerun of the failed smoke check
- [ ] No broader visual QA was run unless explicitly requested
- [ ] External network dependencies disclosed
- [ ] New random Surge URL returned HTTP 200 and passed SHA-256 body verification
- [ ] Final response leads with the verified URL and includes the local source fallback
