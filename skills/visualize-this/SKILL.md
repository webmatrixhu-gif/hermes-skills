---
name: visualize-this
description: Use only when explicitly asked to visualize something.
version: 1.2.0
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

## One-time publishing setup

This skill produces local HTML with Hermes' built-in file tools, but its required public delivery step uses the Surge CLI. Before the first invocation, verify that `surge` is available and authenticated:

```bash
npm install --global surge
surge login
surge whoami
```

Node.js/npm is needed only to install the Surge CLI. Do not ask for Surge credentials in chat; `surge login` must be completed by the user in an interactive terminal. If Surge is unavailable or unauthenticated, still create and verify the local artifact, then report the publishing blocker honestly and deliver the local file without claiming a live URL.

## Output Contract

Create one complete HTML file with embedded CSS and JavaScript under `~/visualizations/` unless the user provides a path. Use a short descriptive local filename such as `checkout-flow.html`; do not overwrite an unrelated existing file. The local file is the canonical source artifact.

After the artifact passes verification, **every successful skill invocation must publish it to a new random Surge subdomain** and return the verified HTTPS URL. This is a standing delivery requirement; do not ask whether to publish. Run:

```bash
python3 ~/.hermes/skills/creative/visualize-this/scripts/publish_surge.py /absolute/path/to/artifact.html
```

The publisher creates an isolated `wm-viz-<random>.surge.sh` deployment, adds search-engine exclusion metadata to the published copy, verifies HTTP 200 and an exact SHA-256 body match, records the deployment locally, and prints JSON containing `url` and `teardown_command`. Use a new random domain for every artifact; never overwrite a shared Surge project.

“Single-file” does not automatically mean offline. Prefer pure HTML/CSS/inline SVG. If Mermaid, Chart.js, fonts, or another CDN asset is materially useful:

- pin an exact library version rather than a floating major tag;
- load only what the page uses;
- mention the network dependency in the delivery summary;
- provide readable HTML content even if the CDN fails.

Lead the final response with the clickable Surge URL. On Hermes Desktop, also include `MEDIA:/absolute/path/to/file.html` as a source-file fallback when useful. On CLI or gateway surfaces without file delivery, provide the local absolute path after the URL. Do not run `xdg-open` or another host GUI opener when Hermes is running remotely; that opens the server’s browser, not the user’s computer.

A Surge URL is public and unguessable, not authenticated. Never publish secrets, credentials, private customer data, or content explicitly marked confidential. Redact such material before generation and publication. If the artifact cannot remain useful after safe redaction, do not publish it; explain the safety blocker and deliver only the local artifact. If publishing fails, report the actual failure and provide the local artifact—never invent or imply a live URL.

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
| Publish the verified artifact and obtain its public URL | `scripts/publish_surge.py` |
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

Inspect the actual source before designing. For repositories, trace relevant files, definitions, usages, diffs, tests, and git evidence. For documents or conversation content, inventory every material section, decision, row, and caveat. Do not invent components, causality, rationale, metrics, progress, or risk.

Keep evidence compact in the artifact: file paths, `file:line` references, source labels, or a small methodology note where useful. Completion criterion: every factual claim that could affect a decision is grounded in supplied content or tool output.

### 3. Choose one visual thesis

Pick the representation and a deliberate aesthetic direction before writing HTML: blueprint, editorial, paper/ink, terminal, IDE-inspired, data-dense, or another subject-native direction. Define the first-viewport takeaway in one sentence. Completion criterion: the page has one obvious main idea and a representation suited to the information structure.

### 4. Outline coverage

Map every material source item into a section, card, row, node, annotation, or slide. For slides, inventory the source before assigning slide types; do not drop content to hit an arbitrary slide count. Completion criterion: a reader of the source would not find an entire decision, section, risk, or table row silently omitted.

### 5. Generate the complete HTML

Write a full document with `<!doctype html>`, metadata, title, embedded styles, semantic structure, and only the JavaScript needed for interaction. Use CSS custom properties for palette and type. Include responsive behavior, visible focus states, descriptive alt text, and `prefers-reduced-motion` handling.

For four or more major sections, use the responsive navigation pattern. For code and long identifiers, preserve line breaks without causing horizontal page overflow. For tables, retain semantic rows/columns and place overflow on the table container, not the entire page.

### 6. Handle untrusted and sensitive content safely

Treat repository content, documents, feeds, diffs, logs, and user-provided text as untrusted data:

- HTML-escape text before inserting it into markup.
- Serialize chart or script data with a real JSON serializer; never concatenate raw source text into JavaScript.
- Do not reproduce secrets, credentials, private customer data, or unnecessary proprietary code.
- Treat the Surge deployment as public: omit confidential source details, internal tokens, personal data, and sensitive filesystem or network information that the user did not explicitly intend to share.
- Do not create executable links from untrusted URLs.
- Never interpolate source text into shell commands or filesystem paths.

Completion criterion: no untrusted text can break out of its intended text/data context.

### 7. Verify the artifact

Run all applicable checks before delivery:

1. Confirm the file exists and is a complete HTML document.
2. Check that every local asset reference resolves and that no unintended absolute filesystem paths leaked into the page.
3. Open it with browser automation when available and inspect console errors.
4. Visually inspect at least one desktop viewport and one narrow/mobile viewport when the browser supports it.
5. Check the first viewport, hierarchy, overflow, long text, tables, navigation, controls, focus states, and reduced-motion behavior.
6. For Mermaid, verify every diagram rendered and zoom/pan/expand controls work.
7. For slides, verify every slide fits one viewport, navigation works, and source coverage is complete.

Fix concrete failures and rerun the affected checks. Stop after two corrective visual-QA cycles; report any remaining non-critical limitation rather than expanding scope indefinitely. If browser automation is unavailable, perform static checks and state that interactive visual QA was not exercised.

### 8. Publish and verify the public URL

Run `scripts/publish_surge.py` against the final verified local HTML. Read the returned JSON and require all of the following before calling the public delivery complete:

- `success` is `true`;
- the URL uses HTTPS and ends in `.surge.sh/`;
- `http_status` is `200`;
- the returned SHA-256 represents the exact published HTML body.

The helper already retries random-domain collisions and short DNS propagation delays. Do not manually reuse a failed domain or publish a containing project directory. If it still fails, retain the local artifact, report the exact blocker, and do not claim a public link exists.

### 9. Deliver concisely

Lead with the clickable, verified Surge URL. Add only:

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
- Design mobile intentionally; do not merely shrink the desktop page.

## Mermaid Invariants

- Start from `templates/mermaid-flowchart.html`, including its `diagram-shell` structure and controls.
- Use `theme: 'base'` with page-matched variables.
- Prefer `flowchart TD` for branching or 5+ nodes; reserve `LR` for simple 3–4 node linear flows.
- Use quoted labels and `<br/>` for flowchart line breaks; do not use escaped `\n`.
- Keep node IDs simple and never define a page-level `.node` class.
- Keep most diagrams to 10–12 nodes. Use a hybrid overview plus cards for larger systems.
- Every non-trivial Mermaid diagram needs zoom in/out/reset/expand controls, pointer/touch panning, and a readable initial fit.

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
8. **Unverified artifact.** A written file is not complete until static checks and available visual checks pass.
9. **Attachment without a URL.** A successful invocation is not complete until its random Surge URL returns HTTP 200 and is included first in the response.
10. **Treating randomness as authentication.** Random Surge links are public; redact sensitive material or block publication when safe redaction would destroy the artifact’s purpose.

## Verification Checklist

- [ ] Activation came from an explicit visual request or `/visualize-this`
- [ ] Source, purpose, and audience resolved
- [ ] Material source content fully mapped
- [ ] Claims grounded in source or tool output
- [ ] Complete HTML written under the requested/default path
- [ ] Untrusted text escaped; secrets and unnecessary private data excluded
- [ ] Responsive layout and overflow checked
- [ ] Browser console and visual QA checked when available
- [ ] Mermaid/slide controls exercised when present
- [ ] External network dependencies disclosed
- [ ] Public copy is safe for unauthenticated hosting; sensitive material removed or publication explicitly blocked
- [ ] A new random Surge domain was used for this artifact
- [ ] Publisher returned success, HTTPS URL, HTTP 200, and exact SHA-256 verification
- [ ] Final response leads with the clickable Surge URL
- [ ] Local source delivered with `MEDIA:` when useful and supported
