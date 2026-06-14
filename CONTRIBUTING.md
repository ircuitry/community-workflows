# Contributing a workflow

A workflow is one file, `workflows/<Name>.ircbot`, produced by ircuitry's **EXPORT** button. Open a PR;
CI runs `tools/build_index.py` and rejects an invalid or unsafe file before it can merge.

## Format

An exported `.ircbot` is a JSON object:

```json
{
  "format": "ircbot/1",
  "name": "My Bot",
  "description": "One clear sentence about what the bot does.",
  "author": "your-github-handle",
  "tags": ["game", "fun"],
  "nodes": [ ... ],
  "connections": [ ... ]
}
```

- `name` (required) - the bot name shown on the website and used as the tab name on import.
- `description`, `author`, `tags` - optional gallery metadata. The app ignores them on import.
- `nodes` / `connections` (required) - the graph. ircuitry writes these for you on export.

You only need to add `description`, `author` and `tags`; everything else comes straight from EXPORT.

## Safety rules (enforced by CI)

- No connection or secret data. A shared workflow must not contain `settings`, `host`, `port`,
  `nick`, `password`, `sasl`/`saslPassword`, or `secrets`. ircuitry's EXPORT already strips these.
- Reference secrets as `{{secret.name}}` so importers supply their own, never literal keys.
- Keep Code nodes safe and useful; importers can read them before running.

## Test it locally

```bash
python3 tools/build_index.py        # validate all workflows + rebuild index.json
```

Or import the `.ircbot` into ircuitry (IMPORT, or drag it onto the canvas) and run it.

By submitting, you license your contribution under this repo's [MIT license](LICENSE).
