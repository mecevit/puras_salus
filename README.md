# puras_salus

Puras skills for health & wellness use cases.

A [Puras](https://puras.co) **skill** is an agent you deploy once and call like an API.
Each skill lives in its own folder with a `skill.yaml` manifest and a `SKILL.md` prompt.

## Skills

| Skill | Folder | Description |
| --- | --- | --- |
| Wellness Guide | [`wellness-guide/`](./wellness-guide) | General, educational health & wellness guidance (not medical advice). |

## Deploy a skill

Requires Python 3.10+ and a Puras API key (mint one in the dashboard).

```bash
pip install puras
puras login                       # or: export PURAS_API_KEY=puras_live_<prefix>.<secret>

cd wellness-guide
puras deploy                      # bundle this folder and push a deployment
```

## Run it

```bash
puras run wellness-guide -i question="How can I improve my sleep?"
```

Other useful commands: `puras deployments` (list versions), `puras activate <version>`
(switch active version), `puras logs <job_id>` (stream a run), `puras whoami` (check workspace + balance).
See the [CLI reference](https://puras.co/docs/cli-reference) for the full list.
