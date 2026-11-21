# Method

## Idea

Keep every context window small by pushing detail down a tree of nested subagents. The root holds the goal and the summaries. Branches explore options and cascades of change. A branch that goes nowhere is reported as a dead end and dropped.

## What the platform gives you

From the Claude Code sub-agents docs:

- A child receives only its delegation prompt, not the parent's history.
- Only the child's final report returns to the parent.
- Siblings do not talk to each other. Peers exist only in the experimental agent teams feature (mailbox plus shared task list).
- A subagent can be resumed with SendMessage and keeps its full history.
- Nesting defaults to 3 layers below the main session (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`).
- 20 subagents can run concurrently by default.
- Deep trees multiply token use.

## Rules

1. The root explores and synthesizes. It does not edit.
2. Only leaves edit, each in its own git worktree and branch.
3. Every node returns the same report format (see [PROMPTS.md](PROMPTS.md)).
4. Every report has BLAST RADIUS and RULED OUT.
5. Resume a child rather than respawn it, so it keeps what it learned.
6. Restate the rules in every delegation prompt, because children don't inherit them.
7. Keep depth at 2-3. Each level adds cost and one more summary that can lose detail.
8. Use cheaper models on exploratory leaves, and a stronger one for the root and for leaves that edit.

## Why these rules

- Siblings can't talk, so the parent is the only place where findings are compared. That is why the report format is fixed and why BLAST RADIUS is required: it is how one branch's change gets checked against another's.
- RULED OUT is there because a parent that can't see a child's history would otherwise send someone to repeat the same dead end.
- Edits are isolated in worktrees so a failed branch costs nothing to throw away.

## Known limits

- Whether a subagent can spawn at all depends on the environment. In the first run it couldn't (see the first update, 2026_11_21).
- Token cost grows with depth and breadth. Not yet measured.
- Confidence in a report is the child's own claim. The "one fact it rests on" is there so the parent can spot-check it.
