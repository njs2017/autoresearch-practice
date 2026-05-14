# AutoResearch — Web Performance Optimization

## Overview
You are optimizing a web application's performance score.
Modify `target.py` (the app/build config) to minimize load time.

## Domain Configuration
- **Domain**: Web performance (Lighthouse / response time)
- **Target file**: `target.py` (server code, build config, or page logic)
- **Eval command**: `python evaluate.py`
- **Metric name**: `score` (load time in ms, lower is better)
- **Time budget per run**: 2 minutes

## What You CAN Do
- Optimize algorithms and data structures
- Add caching layers (in-memory, memoization)
- Reduce payload sizes (remove unused code, compress)
- Optimize database queries (indexing hints, query rewriting)
- Change serialization format (JSON → msgpack, etc.)
- Lazy loading, code splitting logic

## What You CANNOT Do
- Modify `evaluate.py` (the benchmark harness)
- Change the test dataset/requests
- Remove required functionality

## Strategy Hints
- Profile first (add timing to hot paths)
- Low-hanging fruit: unnecessary copies, O(n²) loops, repeated computation
- Caching is usually the biggest single win
- Async/batch processing for I/O-bound code
- Simplification wins: removing unused imports/code = free speedup
