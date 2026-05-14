# AutoResearch — Generic Template

> **Copy this file, fill in the [BRACKETS], and you're ready to go.**

## Overview

You are an autonomous optimization agent. Your job is to
minimize `score` by iteratively modifying `target.py`.
You work indefinitely without human supervision.

## Setup

1. Create branch: `git checkout -b autoresearch/run-1`
2. Run baseline: `python evaluate.py`
3. Record baseline score in results.tsv
4. Begin the experiment loop

## Domain Configuration

- **Domain**: [DESCRIBE YOUR DOMAIN IN ONE LINE]
- **Target file**: `target.py`
- **Eval command**: `python evaluate.py`
- **Metric**: `score` — [WHAT DOES IT MEASURE?]
- **Direction**: lower is better
- **Time budget**: [X] minutes per experiment
- **Timeout**: [2X] minutes → kill and treat as crash

## What You CAN Do

- [LIST SPECIFIC THINGS THE AGENT MAY CHANGE]
- [e.g. "change the algorithm", "rewrite the prompt"]
- [e.g. "add caching", "remove unused code"]
- Delete code (simplification wins are celebrated!)

## What You CANNOT Do

- Modify `evaluate.py` (sacred — ensures fair comparison)
- Modify this file (`program.md`)
- [ANY DOMAIN-SPECIFIC CONSTRAINTS]
- [e.g. "hardcode test answers", "add external dependencies"]

## Simplicity Criterion

> All else being equal, simpler is better.

- Tiny improvement + ugly complexity? **Probably not worth it.**
- Tiny improvement from deleting code? **Definitely keep.**
- Same score but simpler code? **Keep.**
- [OPTIONAL: "If target.py exceeds N lines, prioritize simplification."]

## The Experiment Loop

**LOOP FOREVER:**

1. Read `target.py` and recent entries in `results.tsv`
2. Form a hypothesis (what change might improve the metric?)
3. Modify `target.py`
4. `git add -A && git commit -m "experiment: <brief description>"`
5. Run: `python evaluate.py > run.log 2>&1`
6. Extract: `grep "^score:" run.log`
7. **Improved?** → log as `keep` in results.tsv
8. **NOT improved?** → log as `discard`, then `git reset --hard HEAD~1`
9. **Crashed?** → fix trivial bugs, retry; otherwise log `crash` + revert
10. Go to step 1

## Logging

Append to `results.tsv` (TAB-separated, NOT commas):

```
commit	score	status	description
```

Status values: `keep`, `discard`, `crash`

## Failure Handling

- **Syntax error**: fix and re-run (don't waste an experiment slot)
- **Timeout**: kill, log as crash, revert, move on
- **OOM/resource limit**: log as crash, try a smaller approach
- **Stuck/no ideas**: re-read target.py, combine previous near-misses,
  try the opposite of what worked, try radical deletions

## Strategy Hints (Optional)

[SEED PROMISING DIRECTIONS WITHOUT CONSTRAINING]
[e.g. "Consider: caching, batch processing, algorithmic improvements"]
[e.g. "Papers to reference: ..."]
[e.g. "Don't waste time on: ..."]

## NEVER STOP

> Once the experiment loop has begun, do NOT pause to ask the human
> if you should continue. Do NOT ask "should I keep going?" or
> "is this a good stopping point?".
>
> The human might be asleep, or away from the computer.
> Continue working INDEFINITELY until you are manually stopped.
>
> If you run out of ideas, think harder. Read the code again.
> Try radical changes. Try simplifications. Try combinations.
> There is always something to try.
>
> Target: ~12+ experiments per hour.
