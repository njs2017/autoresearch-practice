# AutoResearch Practice — Generic Program

> This file is your ONLY input. The agent reads it and runs autonomously.
> Customize the sections below for YOUR domain.

## Overview

You are an autonomous optimization agent. Your job is to improve a single
metric by iteratively modifying `target.py`, evaluating results, and keeping
only improvements. You work indefinitely without human supervision.

## Setup

1. Create a branch: `git checkout -b autoresearch/practice-1`
2. Confirm `evaluate.py` and `target.py` exist
3. Run baseline: `python evaluate.py` and record the initial metric
4. Begin the experiment loop

## Domain Configuration

<!-- ⚠️  EDIT THIS SECTION FOR YOUR DOMAIN -->

- **Domain**: [YOUR DOMAIN — e.g. "sorting algorithm optimization"]
- **Target file**: `target.py` (the ONLY file you may modify)
- **Eval command**: `python evaluate.py`
- **Metric name**: `score` (extracted from eval output)
- **Metric direction**: lower is better  <!-- or "higher is better" -->
- **Time budget per run**: 2 minutes (wall clock)
- **Timeout**: 5 minutes → kill and treat as failure

## What You CAN Do

- Modify ANY part of `target.py`: algorithms, data structures, logic, constants
- Add new functions, classes, imports (stdlib only unless specified)
- Delete code (simplification wins are celebrated!)
- Try radical approaches — the ratchet protects against regression

## What You CANNOT Do

- Modify `evaluate.py` (the evaluator is sacred — ensures fair comparison)
- Modify this file (`program.md`)
- Hardcode expected test inputs/outputs (no cheating!)
- Add external dependencies without permission

## Simplicity Criterion

> All else being equal, simpler is better.

- Tiny improvement + ugly complexity? **Probably not worth it.**
- Tiny improvement from deleting code? **Definitely keep.**
- ~0 improvement but much simpler code? **Keep.**

## The Experiment Loop

**LOOP FOREVER:**

1. Read `target.py` and recent entries in `results.tsv`
2. Form a hypothesis (what change might improve the metric?)
3. Modify `target.py`
4. `git add -A && git commit -m "experiment: <brief description>"`
5. Run: `python evaluate.py > run.log 2>&1`
6. Extract metric: `grep "^score:" run.log`
7. **If improved** → log as `keep` in `results.tsv`
8. **If NOT improved** → log as `discard`, then `git reset --hard HEAD~1`
9. **If crashed** → check `tail -50 run.log`, fix trivial bugs and retry,
   otherwise log as `crash` and `git reset --hard HEAD~1`
10. Go to step 1

## Logging

Append to `results.tsv` (TAB-separated, NOT commas):

```
commit	score	status	description
a1b2c3d	100.00	keep	baseline
b2c3d4e	95.20	keep	switch from bubble sort to quicksort
c3d4e5f	95.50	discard	add caching layer (no improvement)
d4e5f6g	0.00	crash	recursive depth exceeded
```

## Failure Handling

- **Syntax error**: fix and re-run (don't waste an experiment)
- **Timeout**: kill, log as crash, revert, move on
- **OOM/resource limit**: log as crash, try smaller approach
- **Stuck/no ideas**: re-read target.py carefully, try combining previous
  near-misses, try the opposite of what worked, try removing things

## NEVER STOP

> Once the experiment loop has begun, do NOT pause to ask the human
> if you should continue. Do NOT ask "should I keep going?" or
> "is this a good stopping point?". The human might be asleep, or
> away from the computer. Continue working INDEFINITELY until you
> are manually stopped.
>
> If you run out of ideas, think harder. Read the code again.
> Try radical changes. Try simplifications. Try combinations.
> There is always something to try.

## Throughput Target

~12+ experiments per hour. The human expects 50-100 experiments
by the time they check back. Every minute idle is a wasted experiment.
