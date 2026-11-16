# Loose Ends: method snapshot

A snapshot of everything behind [the post](../index.md) and its embedded page, as of 16 Nov 2026.

| File | What it is |
|---|---|
| [PROMPTS.md](PROMPTS.md) | The instructions that started the work, word for word |
| [METHODOLOGY.md](METHODOLOGY.md) | Estonia background, detectors, review buckets, confidence bands, limitations |
| `scripts/fetch.sh` | Downloads the corpus snapshot from legislation.docref.nz |
| `scripts/run.py` | Detectors D1–D5 → `flags.json` |
| `scripts/build.py` | The 13 adjudicated findings and the ruled-out groups, with evidence text pulled from the corpus → `data.json` |
| `scripts/show.py` | Small helper: print blocks matching an ID regex (`python3 scripts/show.py 'gas-act-1992:s43D-defn'`) |
| `scripts/check1–4.py` | Pilot detectors from the proposal stage |
| `scripts/shot.js`, `page.js`, `cover.js` | Playwright screenshots of the page, site and cover |
| `templates/loose-ends.template.html` | The interactive page. `/*DATA*/` is replaced by `data.json` |
| `templates/cover.html` | Source for `../loose-ends.jpg` |
| `results/flags.json` | Every detector flag with the citing and target context (raw, unreviewed) |
| `results/data.json` | The reviewed findings the page shows |
| `results/check2.csv`, `check3.csv`, `pilot-candidates.md` | Pilot outputs |
| `results/latest.tsv` | The document versions used |

## Reproduce

Work in an empty directory with the scripts copied into `scripts/`:

```sh
bash scripts/fetch.sh                      # ~55 MB into data/, cl/, dl/, pages/
python3 -I scripts/run.py data cl flags.json
python3 -I scripts/build.py                # writes data.json (needs flags.json, data/, dl/, pages/)
python3 -I - <<'PY'
t = open('templates/loose-ends.template.html').read()
d = open('data.json').read().replace('</', '<\\/')
open('statute-book-loose-ends.html', 'w').write(t.replace('/*DATA*/', d))
PY
node scripts/cover.js templates/cover.html cover.jpg
```

docref publishes new versions continually, so a fresh run will see newer text. Some findings may already have been fixed, and new ones may appear. To reproduce this snapshot exactly, edit `fetch.sh` to use `results/latest.tsv`. Only each document's latest version has a dataset, so older snapshots eventually can't be downloaded again.

The legislation is the work of the New Zealand Parliamentary Counsel Office, published as structured data by Syncopate's docref. Nothing here is legal advice.
