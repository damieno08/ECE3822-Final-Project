"""
run_all.py - Run all complexity tests and save graphs.

Two groups:
  Core Algorithms  -- the six functions identified as performance-critical
  Data Structures  -- the underlying structures and supporting components

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

import test_merge_sort
import test_leaderboard
import test_chat
import test_user_history
import test_user_storage
import test_user_indexing
import test_game_recommendation
import test_profanity_filter
import test_rate_limiter

CORE_MODULES = [
    ("HeapSortGames.heap_sort()",  test_heap_sort),
    ("find_user_by_name()",        test_find_user),
    ("users_bst.insert()",         test_bst_insert),
    ("Leaderboard.top_n()",        test_leaderboard_top_n),
    ("Leaderboard.add_score()",    test_add_score),
    ("load_play_history()",        test_load_play_history),
]

DS_MODULES = [
    ("MergeSort",                  test_merge_sort),
    ("Leaderboard (full)",         test_leaderboard),
    ("Chat (CircularBuffer)",      test_chat),
    ("User History (Stack)",       test_user_history),
    ("UserStorage (BST)",          test_user_storage),
    ("UserIndexing (HashTable)",   test_user_indexing),
    ("GameRecommendation",         test_game_recommendation),
    ("ProfanityFilter",            test_profanity_filter),
    ("RateLimiter",                test_rate_limiter),
]

WIDTH = 62


def _banner(title, char="#"):
    print(f"\n{char * WIDTH}")
    print(f"{char}  {title}")
    print(f"{char * WIDTH}")


def _run_group(label, modules):
    _banner(f"[ {label} ]", char="=")
    group_start = time.perf_counter()
    for title, module in modules:
        _banner(title)
        t0 = time.perf_counter()
        module.run()
        print(f"  Done in {time.perf_counter() - t0:.2f}s")
    print(f"\n  Group total: {time.perf_counter() - group_start:.2f}s")


def main():
    wall_start = time.perf_counter()

    _run_group("Core Algorithms", CORE_MODULES)
    _run_group("Data Structures & Components", DS_MODULES)

    total = time.perf_counter() - wall_start
    print("\n" + "=" * WIDTH)
    print(f"  All tests complete.  Wall time: {total:.2f}s")
    print(f"  Graphs saved to: complexity/graphs/")
    print("=" * WIDTH + "\n")


if __name__ == "__main__":
    main()
