#!/usr/bin/env python3
"""Validate every .ircbot in workflows/ and build index.json.

Usage:
  python3 tools/build_index.py            # validate + write index.json
  python3 tools/build_index.py --check    # validate only, fail if index.json is stale

A .ircbot is an exported ircuitry flow: a JSON object with `name`, `nodes` and
`connections` (and optional `description`, `author`, `tags` for the gallery). It carries
no server or secret settings. This mirrors the app's importer so a bad submission is
caught in CI instead of at import time.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WF_DIR = os.path.join(ROOT, "workflows")
INDEX_PATH = os.path.join(ROOT, "index.json")

# settings/secret keys must never appear in a shared workflow
FORBIDDEN_KEYS = {"settings", "host", "port", "nick", "password", "sasl", "saslPassword", "secrets"}


def fail(errors, f, msg):
    errors.append(f"{f}: {msg}")


def validate(f, m, errors):
    if not isinstance(m, dict):
        fail(errors, f, "top level must be a JSON object")
        return
    if not isinstance(m.get("name", ""), str) or not str(m.get("name", "")).strip():
        fail(errors, f, "missing non-empty 'name'")
    nodes = m.get("nodes")
    if not isinstance(nodes, list) or len(nodes) == 0:
        fail(errors, f, "'nodes' must be a non-empty array")
        nodes = []
    ids = set()
    for n in nodes:
        if not isinstance(n, dict) or "id" not in n or "type" not in n:
            fail(errors, f, "each node needs an 'id' and a 'type'")
            break
        ids.add(n["id"])
    conns = m.get("connections", [])
    if not isinstance(conns, list):
        fail(errors, f, "'connections' must be an array")
        conns = []
    for c in conns:
        if not isinstance(c, dict) or "from" not in c or "to" not in c:
            fail(errors, f, "each connection needs 'from' and 'to'")
            break
    for k in FORBIDDEN_KEYS:
        if k in m:
            fail(errors, f, f"must not contain connection/secret key '{k}'")


def entry(f, m):
    return {
        "name": m.get("name", f[:-7]),
        "description": m.get("description", ""),
        "author": m.get("author", "ircuitry"),
        "tags": m.get("tags", []),
        "nodeCount": len(m.get("nodes", [])),
        "connectionCount": len(m.get("connections", [])),
        "nodeTypes": sorted({n.get("type", "") for n in m.get("nodes", []) if isinstance(n, dict)}),
        "file": f"workflows/{f}",
        "workflow": m,  # full .ircbot so the website can copy with a single fetch
    }


def main():
    check = "--check" in sys.argv
    errors = []
    seen = {}
    wfs = []
    files = sorted(x for x in os.listdir(WF_DIR) if x.endswith(".ircbot"))
    for f in files:
        try:
            with open(os.path.join(WF_DIR, f), encoding="utf-8") as fh:
                m = json.load(fh)
        except Exception as ex:
            fail(errors, f, f"invalid JSON: {ex}")
            continue
        validate(f, m, errors)
        name = (m.get("name") or "").strip().lower()
        if name in seen:
            fail(errors, f, f"duplicate workflow name '{m.get('name')}' (also in {seen[name]})")
        elif name:
            seen[name] = f
        wfs.append(entry(f, m))

    if errors:
        print(f"VALIDATION FAILED ({len(errors)} problem(s)):", file=sys.stderr)
        for e in errors:
            print("  - " + e, file=sys.stderr)
        sys.exit(1)

    index = {"count": len(wfs), "workflows": wfs}
    new = json.dumps(index, indent=2, ensure_ascii=False) + "\n"

    if check:
        old = open(INDEX_PATH, encoding="utf-8").read() if os.path.exists(INDEX_PATH) else ""
        if old != new:
            print("index.json is stale; run: python3 tools/build_index.py", file=sys.stderr)
            sys.exit(1)
        print(f"OK: {len(wfs)} workflows valid, index.json current")
        return

    with open(INDEX_PATH, "w", encoding="utf-8") as fh:
        fh.write(new)
    print(f"OK: {len(wfs)} workflows valid, wrote index.json")


if __name__ == "__main__":
    main()
