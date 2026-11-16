#!/usr/bin/env bash
# Download the corpus snapshot used by the experiment into ./data, ./cl, ./dl, ./pages
# Run from the experiment working directory (the parent of scripts/).
set -euo pipefail
mkdir -p data cl dl pages
curl -sS https://legislation.docref.nz/.well-known/docref.json -o dl/docref.json
# latest API version per document (results/latest.tsv is the snapshot used on 2026-11-16)
python3 -I - <<'PY'
import json
d=json.load(open('dl/docref.json')); latest={}
for x in d['documents']:
    if x['version'] and (x['slug'] not in latest or x['version']>latest[x['slug']]): latest[x['slug']]=x['version']
open('latest.tsv','w').write(''.join(f"{s}\t{v}\n" for s,v in sorted(latest.items())))
PY
while IFS=$'\t' read -r s v; do
  curl -sS -o "data/$s-$v-en-full.json" "https://legislation.docref.nz/$s/$v/en/$s-$v-en-full.json"
  curl -sS -o "cl/$s-$v.json" "https://legislation.docref.nz/$s/$v/en/changelog.json"
done < latest.tsv
# earlier Public Service Act version, for the s 52 before/after in the RSA finding
curl -sS -o pages/psa-2026-04-01.html https://legislation.docref.nz/public-service-act-2020/2026-04-01/en/
