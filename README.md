# 🔬 AutoResearch Cookbook

**Take Karpathy's autonomous experimentation loop and apply it to any domain.**

This is a step-by-step recipe for building your own AutoResearch setup — whether you're optimizing ML models, prompts, algorithms, SQL queries, trading strategies, or anything else with a measurable metric.

---

## What Is AutoResearch?

An AI coding agent runs experiments in a loop while you sleep:

```
You write program.md (goals + rules)
         ↓
Agent reads it → modifies code → runs eval → keeps/reverts
         ↓                                        ↑
         └────────────────────────────────────────┘
                    repeats forever
```

**The only human input is a markdown file.** Everything else is autonomous.

The "ratchet" mechanism ensures the codebase can only improve — every change that doesn't beat the current best is instantly reverted via `git reset`.

> Created by Andrej Karpathy (March 2026). 66K+ GitHub stars.
> Original repo: [karpathy/autoresearch](https://github.com/karpathy/autoresearch)

---

## The Recipe — 5 Steps

### Step 1: Define Your Metric

**This is the most important decision.** Everything else follows from it.

Your metric must be:
- ✅ **Scalar** — a single number (not "looks better" or "feels faster")
- ✅ **Automated** — computed by code, no human judgment needed
- ✅ **Deterministic** — same code → same score (use fixed seeds/data)
- ✅ **Fast** — measurable in under 5 minutes

| Domain | Metric | Direction |
|--------|--------|-----------|
| ML Training | `val_bpb` (bits per byte) | lower = better |
| Sorting Algorithm | execution time (seconds) | lower = better |
| Prompt Engineering | accuracy on test set | higher = better |
| Web Performance | Lighthouse score / load time | depends |
| Compression | compressed_size / original_size | lower = better |
| Trading Strategy | Sharpe ratio | higher = better |
| SQL Optimization | query execution time | lower = better |
| Code Golf | character count (while passing tests) | lower = better |
| Game AI | win rate vs baseline opponent | higher = better |
| Image Quality | SSIM / PSNR score | higher = better |

> **Tip:** When your metric is "higher = better", just negate it in the evaluator
> so the agent always minimizes. Keeps the keep/discard logic simple.

> ⚠️ **If you can't define a single number, AutoResearch is not the right tool.**

---

### Step 2: Build the Evaluator (the Sacred File)

The evaluator is the **one file nobody touches** — not you, not the agent.
It guarantees fair comparison across all experiments.

Create `evaluate.py`:

```python
"""Evaluator — IMMUTABLE. Do not modify."""

import time
import sys

def evaluate():
    # Import the target (the file the agent modifies)
    import target
    
    # Run your benchmark
    # ... your domain-specific evaluation logic ...
    
    score = ...  # must return a single number
    return score

if __name__ == "__main__":
    try:
        score = evaluate()
        print(f"score: {score:.6f}")
        print(f"status: ok")
    except Exception as e:
        print(f"score: 0.000000")
        print(f"status: crash")
        print(f"error: {e}")
        sys.exit(1)
```

**Rules for the evaluator:**
1. Always imports `target.py` (the file the agent modifies)
2. Uses fixed test data / fixed random seeds — no randomness between runs
3. Prints `score: <number>` to stdout (the agent greps for this)
4. Returns exit code 1 on crash
5. Has a correctness check (not just speed — must produce correct output)

---

### Step 3: Create the Starting Point (the Sandbox)

Create `target.py` — this is the **only file the agent modifies**.

Make it deliberately naive. The worse your starting point, the more room the agent has to improve. Examples:

| Domain | Naive Starting Point |
|--------|---------------------|
| Sorting | Bubble sort |
| Prompt | "Answer the question: {input}" |
| SQL | SELECT * with no indexes, no JOINs |
| Compression | No compression (passthrough) |
| Trading | Buy-and-hold |
| Game AI | Random moves |

> **Why naive?** The agent needs quick wins early to build momentum.
> If you start with a near-optimal solution, most experiments will `discard`
> and the agent gets "stuck" generating tiny variations.

---

### Step 4: Write program.md (Your Only Job)

This is where you invest your thinking. The quality of `program.md` directly determines how well the agent performs.

**Template:**

```markdown
# AutoResearch — [Your Domain]

## Overview
You are an autonomous optimization agent. Your job is to 
minimize `score` by iteratively modifying `target.py`.
You work indefinitely without human supervision.

## Setup
1. Create branch: `git checkout -b autoresearch/run-1`
2. Run baseline: `python evaluate.py`
3. Record baseline score in results.tsv
4. Begin the experiment loop

## Rules
- **Modify ONLY**: `target.py`
- **DO NOT modify**: `evaluate.py`, `program.md`
- **Eval command**: `python evaluate.py`
- **Metric**: `score` (lower is better)
- **Time budget**: [X] minutes per experiment
- **Timeout**: [2X] minutes → kill and treat as crash

## Simplicity Criterion
All else being equal, simpler is better.
- Tiny improvement + ugly complexity? Probably not worth it.
- Tiny improvement from DELETING code? Definitely keep.
- Same score but simpler code? Keep.

## The Loop
FOREVER:
1. Read `target.py` and `results.tsv`
2. Propose a hypothesis
3. Modify `target.py`
4. `git commit -am "experiment: <description>"`
5. `python evaluate.py > run.log 2>&1`
6. `grep "^score:" run.log`
7. Improved? → keep. Not improved? → `git reset --hard HEAD~1`
8. Log to `results.tsv`
9. Go to 1

## Logging
Append to `results.tsv` (TAB-separated):
commit  score  status  description

## NEVER STOP
Do NOT pause to ask if you should continue.
The human is away. Continue INDEFINITELY.
If stuck, think harder — re-read the code, try radical 
changes, try the opposite of what worked, try deletions.
```

**What makes a great `program.md`:**

| Element | Why It Matters |
|---------|---------------|
| Clear metric definition | Agent knows exactly what to optimize |
| Explicit boundaries | What CAN vs CANNOT be modified |
| Simplicity criterion | Prevents complexity creep |
| Failure handling rules | Crashes don't stall the loop |
| "NEVER STOP" directive | Agent doesn't pause for confirmation |
| Strategy hints (optional) | Seed promising directions without constraining |

---

### Step 5: Launch and Walk Away

```bash
# Initialize
git init
git add -A
git commit -m "initial setup"

# Open your coding agent in this directory
# (Claude Code, Cursor, Codex, etc.)

# Say:
# "Read program.md and start the experiment loop"

# Walk away. Check results.tsv in the morning.
```

**What to expect:**
- ~12 experiments/hour (with 5-min budget)
- ~80-100 experiments overnight
- ~15-20 improvements kept (the rest discarded)
- A staircase pattern in your score over time

---

## Worked Examples

### Example A: Sorting Algorithm

**Goal:** Optimize a sort function for speed.

<details>
<summary>evaluate.py</summary>

```python
"""Sorting benchmark — IMMUTABLE."""
import time, random, sys

def evaluate():
    random.seed(42)
    import importlib, target
    importlib.reload(target)
    
    sizes = [100, 1_000, 5_000, 10_000]
    total_time = 0
    
    for size in sizes:
        data = [random.randint(-10**6, 10**6) for _ in range(size)]
        expected = sorted(data)
        
        start = time.time()
        result = target.sort(data.copy())
        total_time += time.time() - start
        
        assert result == expected, f"Wrong output for size {size}!"
    
    return total_time

if __name__ == "__main__":
    try:
        score = evaluate()
        print(f"score: {score:.6f}")
        print("status: ok")
    except Exception as e:
        print("score: 0.000000")
        print("status: crash")
        print(f"error: {e}")
        sys.exit(1)
```
</details>

<details>
<summary>target.py (naive starting point)</summary>

```python
def sort(data: list[int]) -> list[int]:
    """Bubble sort — intentionally slow."""
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```
</details>

**Expected agent trajectory:**
1. Baseline: ~10 seconds (bubble sort)
2. Switch to insertion sort → ~4s
3. Switch to quicksort → ~0.1s  
4. Add median-of-three pivot → ~0.08s
5. Hybrid quicksort + insertion for small arrays → ~0.05s
6. Try radix sort for integers → ~0.03s
7. Eventually: `return sorted(data)` → ~0.01s (Python's Timsort in C)

---

### Example B: Prompt Engineering

**Goal:** Maximize accuracy of an LLM on a classification task.

<details>
<summary>evaluate.py</summary>

```python
"""Prompt evaluator — IMMUTABLE."""
import sys

# Golden test set (fixed, never changes)
TEST_CASES = [
    {"input": "The movie was absolutely wonderful!", "expected": "positive"},
    {"input": "Terrible waste of time.", "expected": "negative"},
    {"input": "It was okay, nothing special.", "expected": "neutral"},
    # ... more test cases ...
]

def evaluate():
    import importlib, target
    importlib.reload(target)
    
    correct = 0
    for case in TEST_CASES:
        prediction = target.classify(case["input"])
        if prediction.strip().lower() == case["expected"]:
            correct += 1
    
    accuracy = correct / len(TEST_CASES)
    return -accuracy  # negate: lower = better

if __name__ == "__main__":
    try:
        score = evaluate()
        print(f"score: {score:.6f}")
        print("status: ok")
    except Exception as e:
        print("score: 0.000000")
        print("status: crash")
        print(f"error: {e}")
        sys.exit(1)
```
</details>

<details>
<summary>target.py (naive starting point)</summary>

```python
import openai

SYSTEM_PROMPT = "Classify the sentiment."

def classify(text: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0
    )
    return response.choices[0].message.content
```
</details>

**Expected agent trajectory:**
1. Baseline: ~60% accuracy (vague prompt)
2. Add "respond with exactly one word: positive/negative/neutral" → 75%
3. Add few-shot examples → 85%
4. Add chain-of-thought → 88%
5. Switch to XML-structured output → 90%
6. Fine-tune few-shot selection for edge cases → 93%

---

### Example C: Trading Strategy

**Goal:** Maximize Sharpe ratio on historical crypto data.

<details>
<summary>evaluate.py</summary>

```python
"""Backtest evaluator — IMMUTABLE."""
import sys
import pandas as pd
import numpy as np

# Fixed historical data window
DATA = pd.read_csv("data/btc_hourly_2024.csv", parse_dates=["timestamp"])

def evaluate():
    import importlib, target
    importlib.reload(target)
    
    signals = target.generate_signals(DATA.copy())
    
    # Calculate returns
    returns = signals["position"].shift(1) * DATA["returns"]
    
    # Sharpe ratio (annualized)
    if returns.std() == 0:
        return 0.0  # no trades = no score
    
    sharpe = (returns.mean() / returns.std()) * np.sqrt(8760)
    return -sharpe  # negate: lower = better (we want high Sharpe)

if __name__ == "__main__":
    try:
        score = evaluate()
        print(f"score: {score:.6f}")
        print("status: ok")
    except Exception as e:
        print("score: 0.000000")
        print("status: crash")
        print(f"error: {e}")
        sys.exit(1)
```
</details>

<details>
<summary>target.py (naive starting point)</summary>

```python
import pandas as pd

def generate_signals(data: pd.DataFrame) -> pd.DataFrame:
    """Buy and hold — simplest possible strategy."""
    data["position"] = 1.0  # always long
    return data
```
</details>

---

### Example D: SQL Query Optimization

**Goal:** Minimize total query execution time.

<details>
<summary>evaluate.py</summary>

```python
"""SQL benchmark — IMMUTABLE."""
import time, sys, sqlite3

DB_PATH = "data/benchmark.db"

def evaluate():
    import importlib, target
    importlib.reload(target)
    
    conn = sqlite3.connect(DB_PATH)
    queries = target.get_queries()
    
    total_time = 0
    for name, query in queries.items():
        start = time.time()
        result = conn.execute(query).fetchall()
        total_time += time.time() - start
        
        # Correctness check against known row counts
        expected_counts = {"users_active": 1523, "revenue_monthly": 12}
        if name in expected_counts:
            assert len(result) == expected_counts[name], \
                f"{name}: expected {expected_counts[name]} rows, got {len(result)}"
    
    conn.close()
    return total_time

if __name__ == "__main__":
    try:
        score = evaluate()
        print(f"score: {score:.6f}")
        print("status: ok")
    except Exception as e:
        print("score: 0.000000")
        print("status: crash")
        print(f"error: {e}")
        sys.exit(1)
```
</details>

<details>
<summary>target.py (naive starting point)</summary>

```python
def get_queries():
    return {
        "users_active": """
            SELECT * FROM users 
            WHERE id IN (
                SELECT user_id FROM orders 
                WHERE created_at > '2024-01-01'
            )
        """,
        "revenue_monthly": """
            SELECT * FROM (
                SELECT strftime('%Y-%m', created_at) as month,
                       SUM(amount) as revenue
                FROM orders
                GROUP BY month
            ) WHERE revenue > 0
        """
    }
```
</details>

---

## Pitfalls & Anti-Patterns

### ❌ Reward Hacking
The agent finds a way to "game" the metric without real improvement.

**Example:** A trading agent that overfits to exact historical dates.

**Fix:** Use a train/test split in your evaluator. Evaluate on held-out data the agent has never seen.

### ❌ Complexity Creep  
After 50 experiments, `target.py` is 500 lines of spaghetti.

**Fix:** The simplicity criterion in `program.md` is your defense. Emphasize it. Add: *"If target.py exceeds 200 lines, prioritize simplification experiments."*

### ❌ Local Optima
The ratchet can only move forward — it can't take a step back to enable a bigger leap.

**Fix:** This is a fundamental limitation. Periodically check in and manually create a "fresh start" branch with the best ideas but cleaner code.

### ❌ Non-Deterministic Metric
If your evaluator gives different scores for the same code, the agent will keep/discard randomly.

**Fix:** Fixed random seeds, fixed test data, fixed environment. Run eval 3x and average if you must.

### ❌ Slow Evaluation
If each experiment takes 30 minutes, you get 2 experiments/hour instead of 12.

**Fix:** Reduce dataset size, use proxy metrics, or set a strict time budget.

---

## Adapting the Pattern — Decision Flowchart

```
Can you define a single number to optimize?
├── NO → AutoResearch won't work. Try manual iteration.
└── YES
    ├── Can you evaluate it in under 5 minutes?
    │   ├── NO → Can you use a proxy metric? (subset, sampling)
    │   │   ├── NO → Not a good fit.
    │   │   └── YES → Use the proxy metric.
    │   └── YES
    │       ├── Can you isolate the code to a single file?
    │       │   ├── NO → Refactor until you can.
    │       │   └── YES
    │       │       └── ✅ Build your AutoResearch setup!
    │       │           1. evaluate.py (sacred)
    │       │           2. target.py (naive start)
    │       │           3. program.md (rules + hints)
    │       │           4. git init → launch agent → sleep
    │       └──
    └──
```

---

## Requirements

- **Coding agent**: Claude Code (recommended), Cursor, Codex, or any agent that can read files + run commands + use git
- **Git**: for the ratchet (keep/revert) mechanism
- **Python 3.10+**: (or your language of choice — adapt the template)
- **For ML domains**: NVIDIA GPU with 20+ GB VRAM

---

## Quick Start

```bash
git clone https://github.com/njs2017/autoresearch-practice.git
cd autoresearch-practice

# Try the included sorting example:
python evaluate.py          # see the baseline score

# Or adapt for your domain:
# 1. Edit evaluate.py with your metric
# 2. Edit target.py with your naive starting point
# 3. Edit program.md with your rules
# 4. git init && git add -A && git commit -m "setup"
# 5. Open coding agent → "Read program.md and start"
```

---

## Credits

Based on [Andrej Karpathy's AutoResearch](https://github.com/karpathy/autoresearch) (March 2026).

This cookbook generalizes the pattern for any domain. The original was built for LLM training optimization on a single GPU.

## License

MIT
