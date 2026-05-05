"""
test_leaderboard.py - Complexity test for game_interaction.leaderboard.Leaderboard

Processes tested:
  add_score(user, score)  -- O(log n) per call via AVL BST insert/delete
  top_n(k)                -- O(k log n) via k kth_largest queries on the BST
  rank_of(user)           -- O(n) via sorted(set(all_scores))
  score_of(user)          -- O(1) via plain dict lookup

Revision History:
    (ST) 05/05/2026 Create initial file
"""

import sys
import os
import random
import time
import statistics

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_interaction.leaderboard import Leaderboard
from complexity._timer import print_table, save_plot

SIZES = [100, 500, 1_000, 5_000, 10_000]
TOP_K = 10
REPS  = 3


def _build(n, seed=42):
    random.seed(seed)
    lb = Leaderboard()
    for i in range(n):
        lb.add_score(f"user_{i}", random.randint(1, 1_000_000))
    return lb


def _bench_add_score():
    rows = []
    for n in SIZES:
        times = []
        for _ in range(REPS):
            random.seed(0)
            lb = Leaderboard()
            start = time.perf_counter()
            for i in range(n):
                lb.add_score(f"user_{i}", random.randint(1, 1_000_000))
            times.append(time.perf_counter() - start)
        rows.append((n, statistics.median(times)))
    return rows


def _bench_top_n():
    boards = {n: _build(n) for n in SIZES}
    rows = []
    for n in SIZES:
        lb = boards[n]
        times = []
        for _ in range(REPS * 5):
            start = time.perf_counter()
            lb.top_n(TOP_K)
            times.append(time.perf_counter() - start)
        rows.append((n, statistics.median(times)))
    return rows


def _bench_rank_of():
    boards = {n: _build(n) for n in SIZES}
    rows = []
    for n in SIZES:
        lb = boards[n]
        times = []
        for _ in range(REPS * 5):
            start = time.perf_counter()
            lb.rank_of("user_0")
            times.append(time.perf_counter() - start)
        rows.append((n, statistics.median(times)))
    return rows


def _bench_score_of():
    boards = {n: _build(n) for n in SIZES}
    rows = []
    for n in SIZES:
        lb = boards[n]
        times = []
        for _ in range(REPS * 10):
            start = time.perf_counter()
            lb.score_of("user_0")
            times.append(time.perf_counter() - start)
        rows.append((n, statistics.median(times)))
    return rows


def run():
    print("\n=== Leaderboard Complexity ===")

    rows_add   = _bench_add_score()
    rows_top   = _bench_top_n()
    rows_rank  = _bench_rank_of()
    rows_score = _bench_score_of()

    print_table(
        "Leaderboard.add_score  (build N-entry leaderboard)",
        rows_add,
        expected="O(n log n) total  --  O(log n) per AVL insert",
    )
    print_table(
        f"Leaderboard.top_n({TOP_K})  (query on N-entry leaderboard)",
        rows_top,
        expected=f"O(k log n)  k={TOP_K}  --  ratio grows as log(N) increases",
    )
    print_table(
        "Leaderboard.rank_of  (query on N-entry leaderboard)",
        rows_rank,
        expected="O(n)  --  uses sorted(set(all_scores)); ratio ~ N2/N1",
    )
    print_table(
        "Leaderboard.score_of  (O(1) dict baseline)",
        rows_score,
        expected="O(1)  --  plain dict lookup; ratio stays near 1x",
    )

    save_plot(
        "leaderboard_build.png",
        "Leaderboard -- build cost (N insertions total)",
        [
            {"label": "add_score  N total  [O(n log n)]", "rows": rows_add, "complexity": "O(n log n)"},
        ],
    )
    save_plot(
        "leaderboard_query.png",
        "Leaderboard -- single-query latency vs. N",
        [
            {"label": f"top_n({TOP_K})  [O(k log n)]", "rows": rows_top,   "complexity": "O(log n)", "marker": "s"},
            {"label": "rank_of  [O(n)]",               "rows": rows_rank,  "complexity": "O(n)",     "marker": "^"},
            {"label": "score_of  [O(1)]",              "rows": rows_score, "complexity": "O(1)",     "marker": "D"},
        ],
    )


if __name__ == "__main__":
    run()
