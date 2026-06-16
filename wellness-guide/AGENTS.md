# AGENTS.md — Wellness Guide skill

Notes for humans and coding agents working on this Puras skill.

## What this is

A [Puras](https://puras.co) **skill**: an agent you deploy once and call like an API.
This folder is a single, self-contained skill.

```
wellness-guide/
├── skill.yaml   # manifest: typed inputs/outputs, model, entrypoint
├── SKILL.md     # the system prompt (entrypoint for this agentic skill)
└── AGENTS.md    # this file
```

## Editing guidelines

- **Behavior changes** go in `SKILL.md` (the system prompt). Keep the safety rules section
  intact — this skill must never act as a diagnostic/prescribing tool.
- **Contract changes** (inputs/outputs, model) go in `skill.yaml`. If you change
  `input_schema` or `output_schema`, update the corresponding instructions in `SKILL.md`
  so the model knows what to return.
- Keep `entrypoint: SKILL.md` unless you convert this to a deterministic (`main.py:run`) skill.

## Deploy & test

From this folder:

```bash
pip install puras           # one-time
puras login                 # or export PURAS_API_KEY=puras_live_...
puras deploy                # bundles this dir and pushes a deployment
puras run wellness-guide -i question="How can I sleep better?"
```

Use `puras deployments` to list versions and `puras activate <version>` to roll back.
