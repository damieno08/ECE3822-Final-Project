"""
test_merge_sort.py - Complexity test for algorithms.merge_sort.MergeSort

Process tested: MergeSort(items) -- full sort of a random list of N integers.

Expected: O(n log n)
  Each time N doubles the ratio should be slightly above 2x
  (the log factor grows slowly, so at large N it converges toward 2x).

Revision History:
    (ST) 05/05/2026 Create initial file
"""

import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.merge_sort import MergeSort
from complexity._timer import bench, print_table, save_plot

SIZES = [100, 500, 1_000, 5_000, 10_000, 50_000, 100_000]


def run():
    print("\n=== MergeSort Complexity ===")

    random.seed(0)

    def setup(n):
        data = list(range(n))
        random.shuffle(data)
        return (data,)

    rows = bench(MergeSort, SIZES, setup=setup, reps=5)
    print_table(
        "MergeSort(N random ints)",
        rows,
        expected="O(n log n)  --  ratio ~ 2.0x-2.2x when N doubles",
    )

    def sort_with_key(pairs):
        MergeSort(pairs, key=lambda x: x[1], reverse=True)

    def setup_pairs(n):
        pairs = [(f"game_{i}", random.randint(0, 10_000)) for i in range(n)]
        return (pairs,)

    rows_key = bench(sort_with_key, SIZES, setup=setup_pairs, reps=5)
    print_table(
        "MergeSort(N pairs, key=value, reverse=True)  [recommend pattern]",
        rows_key,
        expected="O(n log n)  --  same asymptotic; key adds a constant factor",
    )

    save_plot(
        "merge_sort.png",
        "MergeSort -- O(n log n)",
        [
            {"label": "MergeSort (plain list)",  "rows": rows,     "complexity": "O(n log n)"},
            {"label": "MergeSort (key+reverse)", "rows": rows_key, "complexity": "O(n log n)", "marker": "s"},
        ],
    )


if __name__ == "__main__":
    run()
