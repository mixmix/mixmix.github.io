# Prompts

The experiment ran in a single Claude Code session (cloud, 16 Nov 2026). These are the instructions as I gave them, word for word. Everything else in this folder came out of the work they started.

## 1. Research and proposal

> I'm running experiments on docref, drawing on data from https://legislation.docref.nz/
>
> I am interested in looking for contradictions in nz legislation/acts. I think estonia did something like this recently. Research that story, try and find their method, then propose an experiment for nz law. Ideally some clear cases that some expert could verify relatively easily.

What came back:
- An account of the Estonian story. See the Background section of [METHODOLOGY.md](METHODOLOGY.md).
- A proposed experiment with five stages.
- A small pilot run (`scripts/check1.py`–`check4.py`), which produced `results/pilot-candidates.md`.

## 2. Run it, build the explorer, publish

> run the experiment, then build an artifact which allows someone to see the summary of points, then traverse the legislation to check cases. Order cases you present by confidence. Once the artifact is up, create a new experiment entry Under docref in my site with a good cover image.

What came back:
- the full detector run (`scripts/run.py` → `flags.json`)
- a hand review of each flag and its adjudication (`scripts/build.py` → `data.json`)
- the interactive page (`templates/loose-ends.template.html`)
- the cover (`templates/cover.html`)
- the post (`../index.md`)

## 3. Housekeeping

> open pr

> include in the experiment folder a snapshot of propmt, methodology, scripts etc
