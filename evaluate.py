"""
AutoResearch Practice — Generic Evaluator (IMMUTABLE)

This file measures the quality of target.py.
The agent CANNOT modify this file — it ensures fair comparison.

HOW TO CUSTOMIZE:
Replace the evaluate() function with your domain's metric.
The only requirement: print "score: <number>" to stdout.
"""

import time
import importlib
import traceback
import sys

# ============================================================
# ⚠️  CUSTOMIZE THIS SECTION FOR YOUR DOMAIN
# ============================================================

def evaluate():
    """
    Import target.py and measure its performance.
    Returns a scalar score (lower is better by default).

    EXAMPLES BY DOMAIN:

    1. SORTING ALGORITHM:
       from target import sort_function
       data = generate_test_data()
       start = time.time()
       result = sort_function(data)
       elapsed = time.time() - start
       assert result == sorted(data), "Incorrect!"
       return elapsed

    2. STRING PROCESSING:
       from target import process
       test_cases = load_test_cases()
       correct = sum(1 for inp, exp in test_cases if process(inp) == exp)
       return -correct  # negative because lower=better

    3. COMPRESSION:
       from target import compress, decompress
       data = load_test_data()
       compressed = compress(data)
       assert decompress(compressed) == data, "Lossy!"
       return len(compressed) / len(data)  # compression ratio

    4. API RESPONSE TIME:
       from target import handle_request
       requests = load_benchmark_requests()
       start = time.time()
       for req in requests:
           handle_request(req)
       return time.time() - start

    5. ML INFERENCE:
       from target import predict
       X_test, y_test = load_test_data()
       preds = predict(X_test)
       return mean_squared_error(y_test, preds)
    """

    # ── DEFAULT: Sorting benchmark (replace with your domain) ──
    import random
    random.seed(42)

    # Import the target module
    import target

    # Generate test data
    test_sizes = [100, 1_000, 5_000, 10_000]
    total_time = 0
    all_correct = True

    for size in test_sizes:
        data = [random.randint(-1_000_000, 1_000_000) for _ in range(size)]
        expected = sorted(data)

        start = time.time()
        result = target.sort(data.copy())
        elapsed = time.time() - start
        total_time += elapsed

        if result != expected:
            all_correct = False

    if not all_correct:
        raise ValueError("CORRECTNESS CHECK FAILED — output does not match expected")

    return total_time  # lower is better (seconds)


# ============================================================
# DO NOT MODIFY BELOW THIS LINE
# ============================================================

def main():
    start_total = time.time()

    try:
        # Reload target module to pick up changes
        if 'target' in sys.modules:
            importlib.reload(sys.modules['target'])

        score = evaluate()
        elapsed_total = time.time() - start_total

        print(f"score: {score:.6f}")
        print(f"elapsed_seconds: {elapsed_total:.1f}")
        print(f"status: ok")

    except Exception as e:
        elapsed_total = time.time() - start_total
        print(f"score: 0.000000")
        print(f"elapsed_seconds: {elapsed_total:.1f}")
        print(f"status: crash")
        print(f"error: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
