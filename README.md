# ircuitry community workflows

Shareable **`.ircbot`** workflows for [ircuitry](https://github.com/ircuitry/ircuitry), the visual
IRCv3 bot builder. Browse them on the website, copy one, and paste it straight into the app.

> Browse and copy: **https://ircuitry.github.io/workflows**

A workflow is a whole bot flow: its nodes and the wires between them. It carries no server,
nick, or secret settings, so it is safe to share. Import one, fill in your own connection, and run.

## Use a workflow

1. **Paste it (in-app):** copy a workflow from the [website](https://ircuitry.github.io/workflows),
   then in ircuitry press <code>Ctrl+V</code> on the canvas to drop its nodes in.
2. **Import a file:** download the `.ircbot` and click <b>IMPORT</b> in ircuitry (opens it as a new bot tab),
   or drag the file onto the canvas.

After importing, open the Inspector, fill in the server/nick/channels, and press RUN BOT.

> Workflows can include Code nodes that run on your machine. Review one before running it.

## Contribute a workflow

1. In ircuitry, build your bot, then **EXPORT** it to a `.ircbot` file (export never includes your
   connection or secrets).
2. Add it under [`workflows/`](workflows/), optionally with `description`, `author` and `tags` keys.
3. Open a pull request. CI validates it; after merge, `index.json` is rebuilt and it appears on the website.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## What is in here

- [`workflows/`](workflows/) - the workflow files (`*.ircbot`).
- [`index.json`](index.json) - generated catalog the website reads. Do not edit by hand.
- [`tools/build_index.py`](tools/build_index.py) - validates every workflow and rebuilds the index.

## License

[MIT](LICENSE). Authors retain credit via the optional `author` field in each workflow.
