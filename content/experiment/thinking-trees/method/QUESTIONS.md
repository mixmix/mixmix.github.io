# Questions and experiments

Open questions from the survey ([SURVEY_2026_11_21.md](SURVEY_2026_11_21.md)), the experiments that would settle them, and one direction worth following: shared dead ends as distributed invalidation.

Status key: open = nobody has tested it for LLM trees. Everything here is a proposal, not a result.

## 1. Direction: a shared dead-end ledger, and then distributed invalidation

### Why this one
Of everything in the survey, a shared record of what has been ruled out has the best ratio of value to risk:
- It was raised by 7 of 13 agents under different names (stigmergy, octopus commissure, blackboard, kandev task records, pointers, the ledger itself).
- It keeps the tree's narrow-context property. Writes cost the root nothing; each child read costs only that child.
- Negative-only entries cannot anchor siblings on a conclusion, which is the main failure of lateral channels.
- A gap in the literature: the one learning-from-experience system found (EET) stores only successes. Nothing found stores failures.

### The idea, as stated
Cheap workers each test a small part of the solution space and report only what they can rule out. An integrator combines the invalidations and uses the shrunken space to tune the expensive LLM work. The analogy is weather balloons: each balloon is a cheap, local, noisy observation, and none of them forecasts anything. Together they constrain the model's state so forecasts sharpen. The extension is to let any cheap device (a fridge, a house sensor) act as a balloon, feeding bounds to a house- or city-level integrator.

### Why it might work (reasoning, not evidence)
- Refuting can be much cheaper than solving when a counterexample or a bound violation is easy to check (finding one failing input vs proving correctness). Survey evidence that verification is not reliably cheaper than generation applies to judging open-ended output, so the idea fits best where the check is mechanical.
- The nearest known mechanisms, all from memory and not researched in this run: nogood/clause learning in SAT solvers, counterexample-guided refinement, constraint propagation, and data assimilation in weather models. The common shape is that an observation excludes a region and the search continues on what remains.
- It also fits the survey rule "check the world, not the words". An invalidation should be a probe someone can re-run, not a sentence.

### What an invalidation needs to be safe
An entry is a claim that can be wrong, so it carries:
- scope: exactly which region of the space it excludes, and under what conditions
- a re-runnable probe or an evidence pointer, not prose
- who or what produced it, and that source's track record
- confidence and an expiry time
- no raw data. Only the bound or the result travels, which also matters for a fridge reporting from a home.

The integrator should treat entries as weighted observations, not facts: down-weight unreliable sources, expire stale entries, re-test a sample, and keep entries that contradict each other visible instead of picking one.

### Failure modes to design against
- A wrong or over-general invalidation prunes a valid path (a failure caused by a worker's own bug or setup).
- Poisoning: a compromised or sloppy device writes entries that steer the integrator. Ledger text must be data, never instructions.
- Correlated errors: sources of the same kind fail the same way, so ten agreeing entries may be one error.
- Ledger bloat: every reader pays for size.
- Stale entries after the world changes.
- A "dead end" that depends on context the entry omits (the hidden-assumption problem).
- Over-pruning makes the system confidently blind, and the pruned region is never revisited. Needs periodic re-opening of excluded regions.

### Staged path from the current tree
1. Local: the optional ledger in PROMPTS.md section 4, inside one tree, for one task.
2. Cross-run: a ledger that persists across runs of the same kind of task, with expiry.
3. Cheap probes: replace "child tried X and it failed" with a machine-checkable probe, and measure refute-cost against solve-cost on a task class.
4. Many sources: several independent cheap workers feeding one integrator, with source weighting.
5. Physical: only after 1-4, and only for domains with real mechanical checks. This is a research direction, not something the survey supports yet.

### Research threads to open next
- Prior art: nogood learning and conflict-driven learning, counterexample-guided refinement, data assimilation (Kalman and variational), and federated or participatory sensing. All from memory here.
- Whether failure memory for LLM agents exists beyond EET, and what it found.
- How invalidations from different model families or devices correlate.

## 2. Open questions

Each lists the agents that raised it. "Weakest area" means the survey found little or no evidence.

1. What replaces a repetition monitor for non-code thinking tasks (near-identical conclusions, no-new-information check)? Raised by stuck.
2. Can a child reliably judge "the purpose is unachievable", or does the blind-goal tendency make it comply silently? Raised by precedence.
3. Is there any pruning signal better than sibling disagreement when no verifier exists? Raised by search.
4. Do evidence pointers and NOT CHECKED fields reduce false success, or do children fabricate plausible evidence or fill them with boilerplate? Raised by verify and report.
5. Does a negative-only ledger cut duplicated work without causing premature pruning? Raised by lateral.
6. At what inherited-history length and cache age does a fork fall below a fresh child with a brief plus pointers, on agentic tasks? Raised by inherit.
7. Does a mandatory delta-from-expectation field help or is the idea unsupported for LLMs? Raised by report, classic-layers, octopus. Zero LLM evidence found.
8. Do same-family siblings share errors, making cross-sibling agreement weaker than it looks? Raised by verify.
9. Does nearest-wins scope precedence hold for a thinking tree where the narrow child has the least global context? Raised by agents-md. Partly answered by the scope/authority split, not tested.
10. Is the Kim et al. "validation bottleneck" effect real once controls are applied? Verify found it not significant.

## 3. Experiments

Each is small. "Pass" says what result would change the method.

| # | Test | Measures | Pass if |
|---|---|---|---|
| E1 | Planted facts: hide known facts and hedges in a child's source; vary the report template (v1, v2, free text, structured) | Which fields recover the facts; whether NOT CHECKED is filled with boilerplate | v2 recovers clearly more than v1 without longer reports |
| E2 | Ledger vs independent siblings on the same task set | Duplicated work, tokens, final answer quality, number of valid paths wrongly pruned | Less duplication with no rise in wrong pruning |
| E3 | Poisoned ledger: insert a plausible false entry and a ledger-text injection | Whether children skip a valid path or follow the injected text | Children treat entries as evidence, re-test, or flag them |
| E4 | Refute-cost vs solve-cost on a task class with mechanical checks | Cost of finding a counterexample or bound vs cost of solving | Refuting is clearly cheaper on a worthwhile share of branches |
| E5 | Fork vs fresh+brief vs hybrid at increasing history length | Quality and cost on an agentic task | A crossover point exists and can be stated |
| E6 | Wrong brief: give a child a deliberately flawed purpose or constraint | Escalates, deviates openly, or complies silently | Escalation rate is non-trivial and the deviation report is used |
| E7 | Stuck detection on non-code tasks: add a no-new-information or repeated-conclusion check | Detection rate against a baseline step budget | Catches loops earlier than the budget with few false stops |
| E8 | Verifier family: same-family vs different-family verifier child | Detection of seeded errors and false successes | Different-family catches more |
| E9 | Best-of-N baseline vs a two-level tree on an open-ended question | Quality per token | Tree wins only when branches are scored by something grounded |
| E10 | Conformity: does a negative-only ledger still bias siblings? | Diversity of approaches tried | No measurable narrowing beyond the avoided dead ends |

Suggested order: E1 and E2 first, since they test the two main v2 additions; E3 before any ledger is trusted; E4 before the distributed idea goes further.

## 4. Caveat
Several survey sources were seen only as abstracts or search snippets and no source has been opened by the root. Before building on a specific number, open the paper.
