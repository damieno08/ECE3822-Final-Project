"""
run_all.py - Run all complexity tests in sequence and print a summary.
Revision History:
    (ST) 05/05/2026 Create initial file

Usage:
    python complexity/run_all.py          # from the project root
    python run_all.py                     # from inside the complexity/ folder

Each test module exposes a run() function that prints its own timing tables.
This script calls them in order and prints a header/footer around each group.
"""

import sys
import os
import time

# Ensure the project root is on sys.path regardless of where this script is invoked
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for p in (_ROOT, _HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

import test_merge_sort
import test_leaderboard
import test_chat
import test_user_history
import test_user_storage
import test_user_indexing
import test_game_recommendation
import test_profanity_filter
import test_rate_limiter

MODULES = [
    ("MergeSort",               test_merge_sort),
    ("Leaderboard",             test_leaderboard),
    ("Chat (CircularBuffer)",   test_chat),
    ("User History (Stack)",    test_user_history),
    ("UserStorage (BST)",       test_user_storage),
    ("UserIndexing (HashTable)",test_user_indexing),
    ("GameRecommendation",      test_game_recommendation),
    ("ProfanityFilter",         test_profanity_filter),
    ("RateLimiter",              test_rate_limiter),
]

WIDTH = 66

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
        elapsed = time.perf_counter() - t0
        print(f"  Done in {elapsed:.2f}s")

    total = time.perf_counter() - wall_start
    print("\n" + "=" * WIDTH)
    print(f"  All complexity tests complete.  Total wall time: {total:.2f}s")
    print(f"  Graphs saved to: complexity/graphs/")
    print("=" * WIDTH + "\n")


if __name__ == "__main__":
    main()
