# Methodology

## Background: what Estonia did

- **Dec 2025:** an amendment to Estonia's Gambling Tax Act was meant to raise tax on remote gambling. It named skill games (*osavusmängud*) but left out games of chance (*õnnemängud*). As a result online casinos are untaxed for 2026, at a cost of about €2m a month.
- **12 Jan 2026:** Luukas Ilves (Estonia's government CIO 2022–24) gave Claude and Gemini the existing Act plus the amendment and asked whether they were inconsistent. Both found the gap.
- **14 Jan 2026:** he released *Apsakaleidja* ("mistake finder"). He built it in Lovable in about 3–4 hours. It pulls every draft bill from the Riigikogu's open API and asks a model to check for:
  - inconsistent defined terms
  - broken references
  - an explanatory memo that contradicts the bill
  - arithmetic errors and impossible dates

  Severity comes from a simple prompt. The Prime Minister and the Justice Minister both endorsed it.
- **Limits Ilves stated:** no formal evaluation, some pedantic flags, and it only reads bills. Comparing bills with existing law was his planned next step, because "draft bills do not map one-to-one onto existing laws".
- **Secondary coverage:** some outlets call it the "F***up Finder" and give a "$28 million" cost. I couldn't trace either to a primary source.

Sources:
- [ERR](https://news.err.ee/1609910593/estonian-prime-minister-recommends-parliament-use-ai-to-check-bills)
- [POPVOX Foundation](https://www.popvox.org/blog/from-slip-up-to-solution)
- [Acteurs Publics](https://acteurspublics.fr/articles/lia-pour-soutenir-le-travail-legislatif-en-estonie/)

**What this experiment takes from it:** the original catch worked because the model was given the right *pair* of texts. Choosing which pairs to compare is the method. docref makes that possible for New Zealand: every block of every version has a stable ID and URL, so a textual reference like "section 73 of the Electricity Industry Act 2010" can be resolved to the actual text it points at.

## Corpus

- The latest docref version of each of the 70 instruments on legislation.docref.nz, as of 16 Nov 2026. Versions are listed in `results/latest.tsv`.
- Each instrument's `-full.json` dataset: 248,341 blocks.
- Each instrument's `changelog.json`.
- One earlier, page-only version of the Public Service Act (2026-04-01). It shows s 52 before it was repealed.

**Limit:** only references *between* these 70 instruments can be resolved. A reference to an Act outside the corpus is invisible to every detector.

## Stage 1: detectors (`scripts/run.py`)

The detectors are deliberately broad, so they catch more than they should. Each one resolves a textual reference against the target's block IDs. The ID patterns are documented in docref's [llms.txt](https://legislation.docref.nz/llms.txt): for example `part4-subpart9-s54C-subs4-defn1`, a `-lineN-` segment for unnumbered lead-ins, and `-repealed` suffixes or `_[Repealed]_` text.

| ID | Detector | Examined | Flagged |
|---|---|---|---|
| D1 | `section N(k)(p) of the X Act YYYY`, where X is in the corpus. Flags targets that are repealed, or a section, subsection or paragraph that doesn't exist. | 1,286 | 21 |
| D2 | Acts the corpus itself says are repealed (`The X Act YYYY (… No …) is repealed`), still named elsewhere. Notes transitional wording and schedules. | 116 | 87 |
| D3 | Borrowed definitions (`==term== … meaning … section N of the X Act`). Flags a target section that doesn't contain the term, and records where the target Act does define it. | 238 | 21 |
| D4 | Plain-text (unlinked) `section N` inside an Act where no section N exists. | 1,576 | 227 |
| D5 | Version drift: cross-Act references into provisions changed in the target's latest changelog, where the citing Act's version is older. | 77 | 77 |

`scripts/check1.py`–`check4.py` are the earlier pilot versions. check1 (internal links) found 0 broken links out of 39,644: docref only creates a link when it resolves.

## Stage 2: review of each pair

Claude read every flag in the session, alongside the citing provision, the target provision and any repeal or transitional provisions involved. Each flag was sorted into one of four buckets:

1. **Genuine defect:** the reference doesn't land where the drafter meant.
2. **Cured by Legislation Act 2019 s 38(2):** a reference to repealed legislation is read as a reference to whatever replaces or corresponds to it. It's untidy but probably works.
3. **Intentional:** transitional or savings provisions, deliberate dual tracks (for example, the Airport Authorities Act repeal is deferred), or a provision that disestablishes a body and must name its origin.
4. **False positive:** paraphrase, a list item whose lead-in names a different Act, or a citing Act that is itself repealed.

A few leads were traced further:
- **Gas Act Part 4A:** enumerated its subparts and counted the uses of "the Commission".
- **Telecommunications Act:** enumerated its Parts and the 156-series sections.
- **Public Service Act s 52:** checked each page-only version back to 2025-09-25 to date the repeal. It first appears in the 2026-06-03 version.

**Grouping:** flags were grouped into 13 findings. Results by detector:
- D1 and D2 supplied most findings.
- D3 contributed one (Commerce Act "associate"); the other 20 flags were paraphrase.
- D4 was about 95% noise but produced two of the four strongest findings (Gas Act and Telecommunications Act).
- D5 produced nothing actionable. When narrowed to the specific definition cited, none of the changed definitions was the one being relied on.

## Confidence

The 0–100 score is a reviewer's judgement that the item is a real defect worth fixing. It is not a measure of legal effect.

| Band | Meaning |
|---|---|
| 80+ | Objective defect. The target is absent or plainly wrong, and s 38 doesn't obviously fix it. |
| 60–79 | References to repealed Acts in operative text, probably cured by s 38 but worth updating. |
| <60 | Cosmetic, illustrative or spent provisions. |

## Limitations

- No expert has verified the findings yet. Every finding is a lead, not a legal opinion.
- Text is docref's consolidation, with every version marked "Unstable". Confirm against legislation.govt.nz.
- Regex-based reference extraction misses some forms: "that Act", ranges, Schedules of other Acts.
- The review was done in-session by one model. There was no second reviewer and no scripted API run, so precision is not yet measured.
- The changelogs only record the most recent change to each Act, so drift detection beyond that needs the page-only history.

## Next steps

1. Have an expert check the 13 findings, recording the bucket and minutes spent on each. That gives precision for each detector.
2. Replace the regexes with a proper citation parser and widen the corpus.
3. Rebuild drift detection from the full version history rather than the latest changelog only, and run it every time docref publishes.
4. Apply the same pairwise review to provisions that are linked (cross-referenced, sharing a defined term, or saying "despite …"). This targets real conflicts between live rules.
