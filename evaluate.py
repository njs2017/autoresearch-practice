"""
AutoResearch — Evaluator Template (IMMUTABLE)

INSTRUCTIONS:
1. Replace the evaluate() function with YOUR domain's metric
2. The only requirement: print "score: <number>" to stdout
3. Once set up, NEVER modify this file again — it's the ground truth

EXAMPLES INCLUDED BELOW — uncomment the one closest to your domain,
or write your own following the same pattern.
"""

import time
import importlib
import traceback
import sys


def evaluate():
    """
    Import target.py and measure its performance.
    Must return a single scalar number (lower = better).
    
    If your metric is "higher = better" (accuracy, Sharpe, etc.),
    just negate it: return -accuracy
    """

    # ─── EXAMPLE: Sorting Algorithm ───────────────────────────────
    import random
    random.seed(42)
    import target
    importlib.reload(target)

    sizes = [100, 1_000, 5_000, 10_000]
    total_time = 0

    for size in sizes:
        data = [random.randint(-10**6, 10**6) for _ in range(size)]
        expected = sorted(data)

        start = time.time()
        result = target.sort(data.copy())
        total_time += time.time() - start

        # CORRECTNESS CHECK — the output must be correct!
        assert result == expected, f"Wrong output for size {size}!"

    return total_time  # seconds, lower = better

    # ─── EXAMPLE: Prompt Engineering ──────────────────────────────
    # import target
    # importlib.reload(target)
    # TEST_CASES = [
    #     {"input": "Great movie!", "expected": "positive"},
    #     {"input": "Terrible.", "expected": "negative"},
    # ]
    # correct = sum(1 for tc in TEST_CASES
    #               if target.classify(tc["input"]).strip().lower() == tc["expected"])
    # return -(correct / len(TEST_CASES))  # negate: lower = better

    # ─── EXAMPLE: Compression ─────────────────────────────────────
    # import target
    # importlib.reload(target)
    # test_data = open("data/test_corpus.txt", "rb").read()
    # compressed = target.compress(test_data)
    # assert target.decompress(compressed) == test_data, "Lossy!"
    # return len(compressed) / len(test_data)  # ratio, lower = better

    # ─── EXAMPLE: API/Server Response Time ────────────────────────
    # import target
    # importlib.reload(target)
    # requests = [{"method": "GET", "path": f"/item/{i}"} for i in range(100)]
    # start = time.time()
    # for req in requests:
    #     target.handle(req)
    # return time.time() - start  # seconds, lower = better

    # ─── EXAMPLE: Game AI Win Rate ────────────────────────────────
    # import target
    # importlib.reload(target)
    # wins = 0
    # for game_seed in range(100):
    #     result = play_game(target.decide_move, opponent=random_opponent, seed=game_seed)
    #     if result == "win": wins += 1
    # return -(wins / 100)  # negate: lower = better


# ══════════════════════════════════════════════════════════════════
# DO NOT MODIFY BELOW — standard runner
# ══════════════════════════════════════════════════════════════════

def main():
    start_total = time.time()
    try:
        score = evaluate()
        elapsed = time.time() - start_total
        print(f"score: {score:.6f}")
        print(f"elapsed_seconds: {elapsed:.1f}")
        print(f"status: ok")
    except Exception as e:
        elapsed = time.time() - start_total
        print(f"score: 0.000000")
        print(f"elapsed_seconds: {elapsed:.1f}")
        print(f"status: crash")
        print(f"error: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
