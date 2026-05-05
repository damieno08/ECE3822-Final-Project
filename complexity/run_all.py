"""
run_all.py - Run all core-algorithm complexity tests and save graphs.

Revision History:
    (ST) 05/05/2026 Create initial file
"""

import sys
import os
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for p in (_ROOT, _HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

import test_heap_sort
import test_find_user
import test_bst_insert
import test_leaderboard_top_n
import test_add_score
import test_load_play_history

MODULES = [
    ("HeapSortGames.heap_sort()",    test_heap_sort),
    ("find_user_by_name()",          test_find_user),
    ("users_bst.insert()",           test_bst_insert),
    ("Leaderboard.top_n()",          test_leaderboard_top_n),
    ("Leaderboard.add_score()",      test_add_score),
    ("load_play_history()",          test_load_play_history),
]

WIDTH = 60


def _banner(title):
    print("\n" + "#" * WIDTH)
    print(f"#  {title}")
    print("#" * WIDTH)


def main():
    wall_start = time.perf_counter()

    for label, module in MODULES:
        _banner(label)
        t0 = time.perf_counter()
        module.run()
        print(f"  Done in {time.perf_counter() - t0:.2f}s")

    total = time.perf_counter() - wall_start
    print("\n" + "=" * WIDTH)
    print(f"  All tests complete.  Wall time: {total:.2f}s")
    print(f"  Graphs saved to: complexity/graphs/")
    print("=" * WIDTH + "\n")


if __name__ == "__main__":
    main()
