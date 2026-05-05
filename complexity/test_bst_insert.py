"""
test_bst_insert.py - Complexity test for ArcadeServer users_bst.insert()

Source: main_server.py lines 84-85 (startup) and line 137 (new user login)
    for i in range(len(self.main_array)):
        self.users_bst.insert(self.main_array[i].name)

self.users_bst is a UserStorage (extends BST from datastructures/bst.py),
a self-balancing AVL tree.  Usernames are inserted as string keys.

Time Complexity
    Per call:  O(log n)    -- AVL tree height is always <= 1.44 * log2(n)
    N inserts: O(n log n)  -- building the BST from scratch at startup

Space Complexity
    Per call:  O(log n)    -- recursion stack depth = tree height
    Total BST: O(n)        -- one node per inserted username

Revision History:
    (ST) 05/05/2026 Create initial file
"""

import sys
import os
import random
import time
import statistics

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_interaction.user_storage import UserStorage
from complexity._timer import (
    bench, bench_space, print_table, print_space_table,
    save_plot, save_space_plot,
)

SIZES = [100, 500, 1_000, 5_000, 10_000, 50_000]


def _usernames(n, seed=42):
    random.seed(seed)
    chars = "abcdefghijklmnopqrstuvwxyz0123456789_"
    names = set()
    while len(names) < n:
        length = random.randint(4, 14)
        names.add("".join(random.choices(chars, k=length)))
    return list(names)


def run():
    print("\n=== users_bst.insert() ===")

    # ── Time: N insertions total (startup pattern) ────────────────────────────
    rows_build = []
    for n in SIZES:
        names = _usernames(n)
        times = []
        for _ in range(3):
            bst = UserStorage()
            start = time.perf_counter()
            for name in names:
                bst.insert(name)
            times.append(time.perf_counter() - start)
        rows_build.append((n, statistics.median(times)))

    print_table(
        "users_bst.insert  (N usernames, startup build)",
        rows_build,
        expected="O(n log n) total  --  O(log n) per AVL insert",
    )

    # ── Time: single insert into an existing BST of size N ───────────────────
    def setup_single(n):
        names = _usernames(n)
        bst   = UserStorage()
        for name in names[:-1]:
            bst.insert(name)
        return (bst, names[-1])

    rows_single = bench(
        lambda bst, name: bst.insert(name),
        SIZES,
        setup=setup_single,
        reps=10,
    )
    print_table(
        "users_bst.insert  (single insert into N-node BST)",
        rows_single,
        expected="O(log n)  --  ratio grows slowly (log factor)",
    )

    # ── Space: single insert into N-node BST ─────────────────────────────────
    rows_space = bench_space(
        lambda bst, name: bst.insert(name),
        SIZES,
        setup=setup_single,
    )
    print_space_table(
        "users_bst.insert  peak heap allocation (single call)",
        rows_space,
        expected="O(log n)  --  recursion stack ~ tree height",
    )

    # ── Graphs ────────────────────────────────────────────────────────────────
    save_plot(
        "bst_insert_time.png",
        "users_bst.insert() -- Time Complexity",
        [
            {"label": "N inserts total  [O(n log n)]",       "rows": rows_build,  "complexity": "O(n log n)"},
            {"label": "single insert into N-node BST  [O(log n)]", "rows": rows_single, "complexity": "O(log n)", "marker": "s"},
        ],
    )
    save_space_plot(
        "bst_insert_space.png",
        "users_bst.insert() -- Space Complexity (single call)",
        [
            {"label": "peak heap allocation  [O(log n)]", "rows": rows_space, "complexity": "O(log n)"},
        ],
    )


if __name__ == "__main__":
    run()
