# AutoResearch — Prompt Optimization

## Overview
You are optimizing an LLM prompt to maximize task accuracy.
The agent iteratively modifies `target.py` (which contains the prompt
and calling logic) and evaluates against a golden test set.

## Domain Configuration
- **Domain**: Prompt engineering / LLM output quality
- **Target file**: `target.py` (prompt text + LLM call logic)
- **Eval command**: `python evaluate.py`
- **Metric name**: `score` (accuracy on golden test set, higher=better → negate)
- **Metric direction**: lower is better (score = -accuracy)
- **Time budget per run**: 3 minutes

## What You CAN Do
- Rewrite the system prompt entirely
- Add/remove few-shot examples
- Change temperature, max_tokens, stop sequences
- Add chain-of-thought instructions
- Change output parsing logic
- Try different prompt structures (XML tags, markdown, numbered steps)

## What You CANNOT Do
- Modify `evaluate.py` or the golden test set
- Change the LLM model (fixed for fair comparison)
- Hardcode answers from the test set

## Strategy Hints
- Start broad (try completely different prompt styles)
- Then narrow (tune the best-performing style)
- Few-shot examples are high-leverage
- "Think step by step" and structured output often help
- Shorter prompts that perform equally = simplification win

## NEVER STOP
Continue indefinitely. ~20 experiments/hour expected.
