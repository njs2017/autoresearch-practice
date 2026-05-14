"""
AutoResearch Practice — Target File (AGENT MODIFIES THIS)

This is the file the AI agent optimizes.
Default: a sorting function (simple starting point for practice).

The agent can change ANYTHING here: algorithm, data structures,
imports, add functions, delete code — whatever improves the score.
"""


def sort(data: list[int]) -> list[int]:
    """
    Sort a list of integers in ascending order.
    This is a naive bubble sort — intentionally slow as a starting point.
    The agent's job is to make this faster while keeping correctness.
    """
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
