"""
test_leaderboard_top_n.py - Complexity test for Leaderboard.top_n()

Source: game_interaction/leaderboard.py
    def top_n(self, n):
        result = []
        for k in range(1, min(n, len(self)) + 1):
            entry = self.kth_largest(k)
            if entry:
                result.append((entry[1], entry[0]))
        return result

Called by the server to fetch the top-k players for a given game's leaderboard.

Time Complexity
    O(k log n)  -- k calls to kth_largest(), each traversing O(log n) nodes
                   in the AVL BST to find the k-th order statistic.

Space Complexity
    O(k)  -- result list grows linearly with k; BST traversal uses O(log n)
              stack frames but k dominates for the returned list.

Revision History:
    (ST) 05/05/2026 Create initial file
"""

import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_interaction.leaderboard import Leaderboard
from complexity._timer import (
    bench, bench_space, print_table, print_space_table,
    save_plot, save_space_plot,
)

SIZES  = [100, 500, 1_000, 5_000, 10_000, 50_000]
K_LIST = [1, 5, 10, 25, 50]


def _build(n, seed=42):
    random.seed(seed)
    lb = Leaderboard()
    for i in range(n):
        lb.add_score(f"user_{i}", random.randint(1, 1_000_000))
    return lb


def run():
    print("\n=== Leaderboard.top_n() ===")

    # ── Time: fixed k=10, varying N ──────────────────────────────────────────
    K = 10
    boards = {n: _build(n) for n in SIZES}

    rows_n = bench(
        lambda lb: lb.top_n(K),
        SIZES,
        setup=lambda n: (boards[n],),
        reps=10,
    )
    print_table(
        f"top_n({K})  on N-entry leaderboard  (k fixed, N varies)",
        rows_n,
        expected=f"O(k log n)  k={K}  --  ratio grows as log(N); stays near 1x",
    )

    # ── Time: varying k, fixed N=10_000 ──────────────────────────────────────
    N_FIXED = 10_000
    lb_fixed = _build(N_FIXED)

    rows_k = bench(
        lambda k: lb_fixed.top_n(k),
        K_LIST,
        setup=lambda k: (k,),
        reps=10,
    )
    print_table(
        f"top_n(k)  on {N_FIXED:,}-entry leaderboard  (N fixed, k varies)",
        rows_k,
        expected="O(k log n)  --  linear in k for fixed n; ratio ~ k2/k1",
    )

    # ── Space: peak allocation for top_n(k=10) ───────────────────────────────
    rows_space = bench_space(
        lambda lb: lb.top_n(K),
        SIZES,
        setup=lambda n: (boards[n],),
    )
    print_space_table(
        f"top_n({K})  peak heap allocation",
        rows_space,
        expected="O(k)  -- result list of k tuples; k=10 constant so allocation stays flat",
    )

    # ── Graphs ────────────────────────────────────────────────────────────────
    save_plot(
        "leaderboard_top_n_time.png",
        f"Leaderboard.top_n() -- Time Complexity",
        [
            {"label": f"top_n({K})  N varies  [O(k log n)]", "rows": rows_n, "complexity": "O(log n)"},
        ],
    )
    save_space_plot(
        "leaderboard_top_n_space.png",
        f"Leaderboard.top_n({K}) -- Space Complexity vs. leaderboard size N",
        [
            {"label": f"peak heap allocation  [O(k)=O({K})]", "rows": rows_space, "complexity": "O(1)"},
        ],
    )


if __name__ == "__main__":
    run()
