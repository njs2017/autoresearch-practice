# AutoResearch — SQL Query Optimization

## Overview
You are optimizing SQL queries for maximum performance.
The agent modifies `target.py` (which contains query definitions)
and evaluates execution time on a fixed test database.

## Domain Configuration
- **Domain**: Database query optimization
- **Target file**: `target.py` (SQL queries + Python DB logic)
- **Eval command**: `python evaluate.py`
- **Metric name**: `score` (total execution time in seconds, lower is better)
- **Time budget per run**: 1 minute

## What You CAN Do
- Rewrite SQL queries (JOINs, subqueries, CTEs, window functions)
- Add index creation statements
- Change query execution order
- Use EXPLAIN to guide optimization
- Batch queries, reduce round-trips
- Change data access patterns (pagination, cursors)

## What You CANNOT Do
- Modify `evaluate.py` or the test database schema/data
- Cache results between evaluations (each run starts fresh)
- Use database-specific extensions not in the allowed list

## Strategy Hints
- Missing indexes are usually the #1 win
- Replace correlated subqueries with JOINs
- Avoid SELECT * — specify only needed columns
- LIMIT early, filter early
- CTEs can help readability but sometimes hurt performance
- Batch INSERTs instead of one-by-one
