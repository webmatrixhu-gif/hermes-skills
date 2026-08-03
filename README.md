# Hermes Skills Tap

Public, installable skills for [Hermes Agent](https://github.com/NousResearch/hermes-agent).

## `visualize-this`

Turns supplied context into a polished, evidence-grounded HTML visual: diagrams, architecture maps, comparisons, reviews, timelines, dashboards, explainers, and slide decks.

The skill activates only when explicitly requested (for example, “visualize this” or `/visualize-this`). It defaults to fast local delivery with one representative browser check. Mobile, interaction, accessibility, and publication checks run only when the artifact or request calls for them.

### Install directly

```bash
hermes skills install webmatrixhu-gif/hermes-skills/skills/visualize-this
```

### Or add this repository as a tap

```bash
hermes skills tap add webmatrixhu-gif/hermes-skills
hermes skills install webmatrixhu-gif/hermes-skills/visualize-this
```

After installation, start a fresh Hermes session (or run `/reset`) and invoke:

```text
/visualize-this
```

### Optional public publishing

Internal artifacts stay local by default. If you explicitly ask for a hosted or shareable URL, install and authenticate the Surge CLI once on the Hermes host:

```bash
npm install --global surge
surge login
surge whoami
```

Surge deployments are public and unguessable, not authenticated. The skill excludes secrets and confidential material from publication and falls back to local artifact delivery when safe publication is impossible.

## Provenance and license

`visualize-this` is a Hermes-native adaptation of [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer), release `v0.8.1`, under the MIT License. Full upstream attribution and license text are included at `skills/visualize-this/references/upstream-license.md`.
