# 🔬 AutoResearch Practice Kit — Generic Template

A hands-on practice template based on Karpathy's AutoResearch pattern.
Adaptable to **any domain** with a single file + scalar metric.

## Quick Start

```bash
cd ~/autoresearch-practice
# 1. Edit config in program.md (your domain, metric, file)
# 2. Run: uv run prepare.py   (or your eval setup)
# 3. Point your coding agent here and say:
#    "Read program.md and start the experiment loop"
```

## Structure

```
program.md       — Agent instructions (THE ONLY FILE YOU EDIT)
target.py        — The file the agent optimizes (your domain code)
evaluate.py      — Immutable evaluator (produces the scalar metric)
results.tsv      — Auto-generated experiment log
examples/        — Domain-specific program.md examples
```

## The Pattern

```
Human writes program.md
        │
        ▼
┌─────────────────────┐
│  Agent reads program │
│  + target.py         │
│  + results.tsv       │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Propose hypothesis  │
│  Modify target.py    │
│  git commit          │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Run evaluate.py     │
│  (fixed time budget) │
└─────────┬───────────┘
          │
     ┌────┴────┐
     │improved?│
     └────┬────┘
    YES   │   NO
     │    │    │
     ▼    │    ▼
  [keep]  │  [git reset HEAD~1]
     │    │    │
     └────┴────┘
          │
          ▼
       [LOOP]
```
