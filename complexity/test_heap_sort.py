"""
test_heap_sort.py - Complexity test for algorithms.heap_sort.HeapSortGames.heap_sort()

Called by ArcadeClient.show_game_history() to sort a user's session list
by start_time (mode="time") or score (mode="score") before display.

Time Complexity
    Build-heap phase:  O(n)          -- n/2 heapify calls, each O(log n), sums to O(n)
    Extract phase:     O(n log n)    -- n swaps + n heapify(log n) calls
    Total:             O(n log n)

Space Complexity
    In-place sort -- no auxiliary array allocated.
    Recursion stack depth = height of heap = O(log n).

Revision History:
    (ST) 05/05/2026 Create initial file
"""

import sys
import os
import random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.heap_sort import HeapSortGames
from complexity._timer import (
    bench, bench_space, print_table, print_space_table,
    save_plot, save_space_plot,
)

SIZES  = [100, 500, 1_000, 5_000, 10_000, 50_000]
SORTER = HeapSortGames()
BASE   = datetime(2025, 1, 1)


class _Session:
    """Minimal stand-in for GameSession."""
    __slots__ = ("start_time", "score")
    def __init__(self, start_time, score):
        self.start_time = start_time
        self.score      = score


def _make_sessions(n, seed=0):
    random.seed(seed)
    return [
        _Session(BASE + timedelta(seconds=random.randint(0, 10_000_000)),
                 random.randint(0, 500))
        for _ in range(n)
    ]


def run():
    print("\n=== HeapSortGames.heap_sort() ===")

    # ── Time: sort by start_time ──────────────────────────────────────────────
    def setup_time(n):
        return ([_make_sessions(n)],)          # wrap in list so bench unpacks cleanly

    rows_time = bench(
        lambda sessions: SORTER.heap_sort(sessions, mode="time"),
        SIZES,
        setup=lambda n: (_make_sessions(n),),
        reps=5,
    )
    print_table(
        "heap_sort(N sessions, mode='time')",
        rows_time,
        expected="O(n log n)  --  ratio ~ 2x when N doubles",
    )

    # ── Time: sort by score ───────────────────────────────────────────────────
    rows_score = bench(
        lambda sessions: SORTER.heap_sort(sessions, mode="score"),
        SIZES,
        setup=lambda n: (_make_sessions(n),),
        reps=5,
    )
    print_table(
        "heap_sort(N sessions, mode='score')",
        rows_score,
        expected="O(n log n)  --  same asymptotic as time-mode",
    )

    # ── Space ─────────────────────────────────────────────────────────────────
    rows_space = bench_space(
        lambda sessions: SORTER.heap_sort(sessions, mode="time"),
        SIZES,
        setup=lambda n: (_make_sessions(n),),
    )
    print_space_table(
        "heap_sort  peak heap allocation",
        rows_space,
        expected="O(log n)  -- in-place; only recursion overhead on heap",
    )

    # ── Graphs ────────────────────────────────────────────────────────────────
    save_plot(
        "heap_sort_time.png",
        "HeapSortGames.heap_sort() -- Time Complexity",
        [
            {"label": "mode='time'   [O(n log n)]",  "rows": rows_time,  "complexity": "O(n log n)"},
            {"label": "mode='score'  [O(n log n)]",  "rows": rows_score, "complexity": "O(n log n)", "marker": "s"},
        ],
    )
    save_space_plot(
        "heap_sort_space.png",
        "HeapSortGames.heap_sort() -- Space Complexity",
        [
            {"label": "peak heap allocation  [O(log n)]", "rows": rows_space, "complexity": "O(log n)"},
        ],
    )


if __name__ == "__main__":
    run()
