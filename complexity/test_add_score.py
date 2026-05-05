"""
test_add_score.py - Complexity test for Leaderboard.add_score()

Source: game_interaction/leaderboard.py
    def add_score(self, user, score):
        if user in self._user_scores:
            old_score = self._user_scores[user]
            if score <= old_score:
                return False
            self.delete((old_score, user))
        self._user_scores[user] = score
        self.insert((score, user))
        return True

Called by the server after every SAVE_SESSION to update the leaderboard
for a given game. Uses an AVL BST for ordered score storage and a dict
for O(1) user->score lookup.

Time Complexity
    O(log n)  -- one AVL insert (new user) or one delete + insert (score update)
    The AVL tree stays balanced, so height is always O(log n).

Space Complexity
    O(1) per call  -- AVL rebalance uses the call stack (not heap); no extra
                      heap allocation is made beyond the single new BST node.
    O(n) total     -- the BST itself stores one node per unique user.

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
from complexity._timer import (
    bench, bench_space, print_table, print_space_table,
    save_plot, save_space_plot,
)

SIZES = [100, 500, 1_000, 5_000, 10_000, 50_000]


def run():
    print("\n=== Leaderboard.add_score() ===")

    # ── Time: build leaderboard (N unique users, first insert each) ───────────
    rows_build = []
    for n in SIZES:
        random.seed(0)
        times = []
        for _ in range(3):
            lb = Leaderboard()
            start = time.perf_counter()
            for i in range(n):
                lb.add_score(f"user_{i}", random.randint(1, 1_000_000))
            times.append(time.perf_counter() - start)
        rows_build.append((n, statistics.median(times)))

    print_table(
        "add_score  (N unique users -- build leaderboard from scratch)",
        rows_build,
        expected="O(log n) per call  --  N calls total = O(n log n) aggregate",
    )

    # ── Time: score update (user already exists) ──────────────────────────────
    rows_update = []
    for n in SIZES:
        random.seed(0)
        lb = Leaderboard()
        for i in range(n):
            lb.add_score(f"user_{i}", random.randint(1, 500))
        times = []
        for _ in range(3):
            start = time.perf_counter()
            for i in range(n):
                lb.add_score(f"user_{i}", random.randint(501, 1_000_000))
            times.append(time.perf_counter() - start)
        rows_update.append((n, statistics.median(times)))

    print_table(
        "add_score  (N score updates -- every user already in leaderboard)",
        rows_update,
        expected="O(log n) per call  --  N calls total = O(n log n) aggregate",
    )

    # ── Time: single add_score into N-entry leaderboard ──────────────────────
    def setup_single(n):
        random.seed(0)
        lb = Leaderboard()
        for i in range(n):
            lb.add_score(f"user_{i}", random.randint(1, 1_000_000))
        return (lb, f"new_user_{n}", random.randint(1, 1_000_000))

    rows_single = bench(
        lambda lb, u, s: lb.add_score(u, s),
        SIZES,
        setup=setup_single,
        reps=10,
    )
    print_table(
        "add_score  (single new-user insert into N-entry leaderboard)",
        rows_single,
        expected="O(log n)  --  single AVL insert; ratio grows slowly",
    )

    # ── Space ─────────────────────────────────────────────────────────────────
    rows_space = bench_space(
        lambda lb, u, s: lb.add_score(u, s),
        SIZES,
        setup=setup_single,
    )
    print("  Space Complexity: O(1) per call -- AVL rebalance uses call stack (not heap).")
    print("  Total BST storage: O(n) -- one node per unique user.\n")

    # ── Graphs ────────────────────────────────────────────────────────────────
    save_plot(
        "add_score_time.png",
        "Leaderboard.add_score() -- Time Complexity  O(log n) per call",
        [
            {"label": "N new users (build)   [O(log n)/call]",  "rows": rows_build,  "complexity": "O(n log n)"},
            {"label": "N updates (existing)  [O(log n)/call]",  "rows": rows_update, "complexity": "O(n log n)", "marker": "s"},
            {"label": "single insert into N  [O(log n)]",       "rows": rows_single, "complexity": "O(log n)",   "marker": "^"},
        ],
    )
    save_space_plot(
        "add_score_space.png",
        "Leaderboard.add_score() -- Space: O(1)/call, O(n) total BST",
        [
            {"label": "per-call heap allocation  [O(1)]", "rows": rows_space, "complexity": "O(1)"},
        ],
    )


if __name__ == "__main__":
    run()
