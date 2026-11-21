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

## Next

Find an environment where a subagent can spawn, then run a real two-level tree on a change with a
non-obvious cascade, and see whether the root's context stays small.
