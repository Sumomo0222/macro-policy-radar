#!/usr/bin/env python3
"""Parse raw JSON output of autoglm websearch.py into compact lines."""
import json, sys

try:
    d = json.load(sys.stdin)
except Exception as e:
    print("PARSE_ERR", e)
    sys.exit()

def walk(x, out):
    if isinstance(x, dict):
        if 'webPages' in x and isinstance(x['webPages'], dict):
            out.extend(x['webPages'].get('value', []))
        for v in x.values():
            walk(v, out)
    elif isinstance(x, list):
        for v in x:
            walk(v, out)

res = []
walk(d, res)
seen = set()
for r in res:
    u = r.get('url') or ''
    if not u or u in seen:
        continue
    seen.add(u)
    name = (r.get('name') or '').strip()[:120]
    snip = (r.get('snippet') or '').replace('\n', ' ').strip()[:260]
    print(f"- {name}\n  {u}\n  {snip}")
