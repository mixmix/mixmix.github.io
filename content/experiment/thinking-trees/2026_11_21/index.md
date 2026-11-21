---
title: First Run
date: 2026-11-21T10:00:00+13:00
image:
---

A long session fills its own context window. By the time I'm deep in a change I'm carrying the whole
history of how I got there, and every new idea has to fit alongside it. I wanted to try the opposite:
one small agent at the top that only thinks and decides, handing narrow questions to children, who hand
narrower ones to theirs. Each branch explores one possibility, reports back, and can be abandoned if it
goes nowhere. The shape is closer to an octopus than a to-do list, each arm feeling out a different
direction while the head keeps the overall picture.

The part I'm most interested in is cascades. If I change one thing, what else moves? A child can follow
that chain in its own context and come back with a short answer, without the root ever reading the files.

{{< embed src="thinking-tree.embed.html" title="Thinking Tree" height="420" >}}

## How it's meant to work

From the Claude Code sub-agents docs, the facts the design rests on:

- A child gets only its delegation prompt, not the parent's history. Critical rules have to be restated
  in every prompt.
- Only the child's final report returns to the parent.
- Siblings can't talk to each other. Peers only exist in the experimental agent teams feature.
- A subagent can be resumed with SendMessage and keeps its full history.
- Nesting defaults to 3 layers below the main session (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`), and 20
  agents can run at once by default.
- Deep trees multiply token use.

The rules I'm testing: the root explores and synthesizes but never edits. Only leaf agents edit, each in
its own git worktree and branch. Every node returns the same report format, including a BLAST RADIUS (what
else changes) and RULED OUT (so nobody repeats it). Resume a child rather than respawn it. Keep depth at 2
or 3, and use cheaper models for exploratory leaves. Every node
returns the same report, so the parent can compare branches:

```
REPORT:
BRANCH:
VERDICT: promising | dead end | blocked
CONFIDENCE: low | medium | high, plus the one fact it rests on
FINDINGS: (3-5 bullets)
BLAST RADIUS: what else changes if this is adopted
CHANGES MADE: worktree, files, whether it builds
RULED OUT: so nobody repeats it
OPEN QUESTIONS / NEXT STEP:
```

Siblings can't talk, so the parent is the only place findings get compared. That's why BLAST RADIUS and
RULED OUT are required. Worktrees mean a failed branch costs nothing to throw away. The full prompts are
in the repo under `method/`.

## What actually happened

1. I launched a root subagent with the full tree prompt. It reported **blocked**: subagents in this
   session had no Agent tool, so nesting couldn't work and no tree ran under it. It correctly refused to
   do the leaf work itself or fake a run.
2. So the main session acted as the root and spawned three leaves directly, at depth 1:

| Leaf | Job | Outcome |
|---|---|---|
| conventions | explore-only: how existing experiments are laid out | promising. Found the layout to copy, and that `preview=` on an embed breaks the build if the image is missing |
| writeup | this page and the method files | promising. Followed the conventions report, build unverified |
| viz | an SVG of the tree | promising. Inline SVG, no JS, no external fonts; checked as a static render only |

This is a flat fan-out, not a tree. It shows the report format and worktree rules work, but nothing about
depth.

**Dead ends so far:** a nested root subagent. This environment doesn't give subagents a way to spawn.

## The actual prompts

These are the prompts as sent in this run, not the cleaned-up templates. The full reports that came back are in `method/RUN_2026_11_21.md` in the repo (not published on this site).

<details>
<summary>Show the prompts (root, three leaves, and one relay message)</summary>

#### 1. Root prompt (nested root subagent, general-purpose)

```
You are the root of an exploration tree, working in the Hugo site repo at /home/claude/mixmix.github.io (a Hugo "Stack" theme site; master deploys it, so NEVER commit to or push master).

GOAL: Create a new experiment called "thinking-trees" under content/experiment/thinking-trees/, following the conventions of the existing experiment content/experiment/docref/ (an _index.md intro, plus dated update folders like 2026_11_21/index.md, optional method/ folder, optional *.embed.html). The experiment is about using trees of nested subagents to keep context windows small, reason about cascades of change, and explore/back out of rabbit holes ("an octopus exploring possibility space"). The first dated update should document the method AND be produced by running it: this very tree is the first run, so record what the tree actually did (branches, verdicts, ruled-out ideas) in the write-up.

Facts about Claude Code subagents you can rely on (from docs.code.claude.com/docs/en/sub-agents): a child receives only its delegation prompt (not parent history; restate critical rules in each prompt); only its final report returns to the parent; siblings do not talk to each other; a subagent can be resumed with SendMessage to keep its full history; nesting defaults to 3 layers below main; 20 concurrent subagents by default; deep trees multiply token use.

RULES
- You explore and synthesize. You do not edit files yourself.
- Split work into independent branches (competing hypotheses, or separate modules). Spawn one subagent per branch, in parallel, in a single turn.
- Max tree depth: 2. A child may spawn its own children only if its task clearly splits into independent parts.
- Only leaf agents may edit, and only in their own git worktree on a branch named explore/<short-label>, created from a local branch `thinking-trees` (create that branch from master first; do this yourself via git, no file edits). Never touch master.
- Restate in every delegation prompt: don't modify anything outside content/experiment/thinking-trees/ (and nothing in layouts/, config/, themes); match the front-matter style of content/experiment/docref; no push to any remote.
- Every agent must end with the REPORT FORMAT below, nothing else.

SUGGESTED FIRST BRANCHES (adjust if you see better): 
1. conventions (explore-only): read how docref's _index.md, dated index.md, method/, and *.embed.html are structured and rendered (layouts/project/*), report the exact front matter and file layout to copy.
2. writeup (may edit): draft _index.md, the first dated update index.md, and method/ files (PROMPTS.md containing the root prompt, child delegation prompt, and report template below; METHOD.md explaining how agents communicate: parent->child via prompt only, child->parent via final report only, resume via SendMessage, peers only via experimental agent teams).
3. viz (may edit): a self-contained thinking-tree.embed.html (inline SVG, no external deps, works in light and dark) showing this run's tree: nodes coloured by verdict (promising / dead end / blocked), edges parent->child. Keep it simple and legible on a phone.
Branches 2 and 3 depend on branch 1's findings only for front matter/layout, so tell them to inspect docref themselves or run after 1 reports, your call; justify it in your summary.

CHILD DELEGATION PROMPT TEMPLATE (fill per branch):
Branch: <label>. Hypothesis / task: <one sentence>. Scope: <files or modules>. Out of scope: <list>. Mode: explore-only | may edit in worktree explore/<label>. Budget: stop after ~<N> tool calls or when confident. Return the report format exactly, under 300 words.

REPORT FORMAT (every node returns this):
BRANCH: <label>
VERDICT: promising | dead end | blocked
CONFIDENCE: low | medium | high, plus the one fact it rests on
FINDINGS: 3-5 bullets, most important first
BLAST RADIUS (what else changes if adopted): <file/module/API/test>: <how affected>
CHANGES MADE: none | branch explore/<label>, <files>, <tests/build pass? y/n>
RULED OUT (so nobody repeats it): <idea>: <why it failed>
OPEN QUESTIONS / NEXT STEP: <what you'd do next if resumed>

AFTER THE CHILDREN REPORT
1. Compare reports; flag conflicts and overlapping blast radii.
2. Merge chosen branches into `thinking-trees` (resolve conflicts yourself via git, content only inside content/experiment/thinking-trees/). Resume a promising agent via SendMessage rather than spawning a new one if rework is needed.
3. Discard ruled-out branches; list them with reasons (include them in the write-up as the "dead ends" section).
4. If `hugo` is available (or installable offline via the repo's go.mod without network trouble), run a build to check the page renders; if it isn't possible say so, do not fake it.
5. Commit on branch `thinking-trees` with a clear message ending with these exact lines:
Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01FW1F4WrmmD47f6eGL3hG2o
Do NOT push anywhere.
6. Final answer, under 250 words: what you built, tree shape and verdicts per branch, what was ruled out, build status, and the branch/commit hash.
```

#### 2. Leaf prompt: viz (general-purpose, may edit)

```
Branch: viz. Task: build a self-contained thinking-tree.embed.html showing the tree of this experiment run.
Repo: /home/claude/mixmix.github.io (Hugo Stack site; local branch `thinking-trees` already exists, created from master). Mode: you MAY edit, but only in your own git worktree: run `git -C /home/claude/mixmix.github.io worktree add /home/claude/wt-viz -b explore/viz thinking-trees` and work there. Never touch master, never push, no network git ops.
Scope: only create content/experiment/thinking-trees/2026_11_21/thinking-tree.embed.html in the worktree. Out of scope: anything else, layouts/, config/. First look at content/experiment/docref/*/*.embed.html and the matching index.md to see how embeds are written and referenced (match that approach: inline CSS/JS, no external deps).
Tree to draw (nodes, verdicts): ROOT "main session (root)" = promising; attempt "nested root subagent" = dead end (subagents had no Agent tool, so it could not spawn children; the root spawn depth failed); children of ROOT: "conventions" (explore-only), "writeup", "viz". Colour by verdict: promising / dead end / blocked, plus grey for pending. Include a small legend and a one-line note that parent->child is the delegation prompt and child->parent is the final report only. Inline SVG, legible on a phone (viewBox, responsive width), works in light and dark (use prefers-color-scheme or currentColor with CSS variables), accessible (title/desc, not colour alone: add shape or text marker for the verdict).
Budget: ~25 tool calls. Do NOT spawn subagents. Do NOT commit; leave changes uncommitted in the worktree.
Return exactly this format, under 300 words:
BRANCH / VERDICT (promising|dead end|blocked) / CONFIDENCE / FINDINGS (3-5 bullets) / BLAST RADIUS / CHANGES MADE (worktree path, files, build or render check done y/n) / RULED OUT / OPEN QUESTIONS / NEXT STEP.
```

#### 3. Leaf prompt: writeup (general-purpose, may edit)

```
Branch: writeup. Task: draft the content of a new experiment "thinking-trees" for the Hugo Stack site in /home/claude/mixmix.github.io (local branch `thinking-trees` exists, created from master).
Mode: you MAY edit, but only in your own git worktree: run `git -C /home/claude/mixmix.github.io worktree add /home/claude/wt-writeup -b explore/writeup thinking-trees` and work there. Never touch master, never push, no network git ops. Do NOT commit; leave changes uncommitted.
Scope: create only under content/experiment/thinking-trees/ : _index.md (intro), 2026_11_21/index.md (first dated update), method/PROMPTS.md, method/METHOD.md. Out of scope: layouts/, config/, other content. First inspect content/experiment/docref/ (its _index.md, a dated index.md, method/) and copy the front-matter and structure style exactly (title, description, image/badge/date fields, etc). In 2026_11_21/index.md you may reference an embed named thinking-tree.embed.html in the same folder (another branch is building it; reference it the same way docref's index.md files reference theirs).
Content facts (from code.claude.com/docs/en/sub-agents): a child receives only its delegation prompt (not parent history; restate critical rules in each prompt); only its final report returns to the parent; siblings do not talk to each other; a subagent can be resumed with SendMessage and keeps its full history; nesting defaults to 3 layers below main (CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH); 20 concurrent by default; peers only via experimental agent teams (mailbox + shared task list); deep trees multiply token use.
Idea of the experiment: trees of nested subagents to keep context windows small, reason about cascades of change, explore and back out of rabbit holes, like an octopus exploring possibility space. Method rules: root explores and synthesizes and does not edit; only leaf agents edit, in their own git worktree/branch; every node returns the same report format; report includes BLAST RADIUS and RULED OUT; resume rather than respawn; keep depth at 2-3; cheaper models on exploratory leaves.
PROMPTS.md must contain, in code blocks: the root prompt, the child delegation prompt template, and the report template:
REPORT: BRANCH, VERDICT (promising|dead end|blocked), CONFIDENCE (low|medium|high + the one fact it rests on), FINDINGS (3-5 bullets), BLAST RADIUS (what else changes if adopted), CHANGES MADE, RULED OUT (so nobody repeats it), OPEN QUESTIONS / NEXT STEP.
First-run log to include honestly in the update (a "What actually happened" section): (1) I launched a root subagent with the full tree prompt; it reported blocked because subagents in this session had no Agent tool, so nesting did not work and no tree ran under it; it correctly refused to do the leaf work itself or fake a run. (2) The main session then acted as the root and spawned three leaves directly (depth 1): conventions (explore-only), writeup (this branch), viz (SVG of the tree). Mark those leaf outcomes as 'see commit/branch' placeholders you can fill in plainly as 'pending' since you don't know the others' results. Dead ends so far: nested root subagent (no spawn tool in this environment).
Keep the prose short, plain, first person singular is fine, no hype. Budget ~30 tool calls. Do NOT spawn subagents.
Return exactly this format, under 300 words:
BRANCH / VERDICT (promising|dead end|blocked) / CONFIDENCE / FINDINGS / BLAST RADIUS / CHANGES MADE (worktree path, files, build check y/n) / RULED OUT / OPEN QUESTIONS / NEXT STEP.
```

#### 4. Leaf prompt: conventions (Explore agent, read-only)

```
Branch: conventions. Mode: explore-only (read-only, change nothing). Repo: /home/claude/mixmix.github.io, a Hugo site using the Stack theme via Hugo modules. Task: report exactly how experiments are structured and rendered so a new experiment "thinking-trees" can copy them. Look at: content/experiment/_index.md, content/experiment/docref/_index.md, one dated update like content/experiment/docref/2026_11_16/index.md (front matter fields, how the *.embed.html is referenced, image fields, dates), the method/ folder there, and layouts/project/* plus any shortcodes in layouts/shortcodes/ that handle embeds. Also check .github/workflows for what triggers deploy (which branches) and whether `hugo` can be built locally (check `which hugo`, go.mod, config/_default). Out of scope: editing anything.
Return exactly this format, under 300 words:
BRANCH: conventions / VERDICT (promising|dead end|blocked) / CONFIDENCE / FINDINGS (exact front-matter keys to copy, embed mechanism, file layout) / BLAST RADIUS / CHANGES MADE: none / RULED OUT / OPEN QUESTIONS / NEXT STEP.
```

#### 5. Relay message to writeup (sent after the conventions report arrived)

```
Findings from the conventions branch (read-only recon). (1) Project _index.md keys: title, description, date, image (bundle-relative, optional), tags, weight. Dated update index.md keys: title, date (ISO with offset, e.g. 2026-11-21T23:30:00+13:00), optional image, optional description (rendered as subtitle). (2) Embed shortcode: {{< embed src="thinking-tree.embed.html" title="..." preview="x.jpg" >}}. If you pass preview it MUST be an existing image in the same bundle or the build errors, so omit preview and use the optional height param instead (default 420px). (3) config ignores experiment/*/method/ so method/ files are not published; that is fine for PROMPTS.md and METHOD.md, but the update page itself must contain the key method content (summary of the rules, report format, and the 'What actually happened' log), not just link to method/. (4) hugo is not installed locally, so say the build is unverified.
```

</details>

## Next

Find an environment where a subagent can spawn, then run a real two-level tree on a change with a
non-obvious cascade, and see whether the root's context stays small.
