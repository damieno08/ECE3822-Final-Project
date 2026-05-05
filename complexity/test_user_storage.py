"""
test_user_storage.py - Complexity test for user_interaction.user_storage.UserStorage

UserStorage extends BST. The high-level methods (add_user, find_user, autocomplete)
are currently stubs, so this file tests the inherited BST operations directly --
those are exactly what the stubs would delegate to once implemented.

Processes tested:
  UserStorage.insert(key)          -- O(log n) per AVL insert
  UserStorage.search(key)          -- O(log n) per AVL search
  UserStorage.range_query(lo, hi)  -- O(log n + k) where k = matches returned
  UserStorage.inorder()            -- O(n): full in-order traversal

Keys are integer ASCII-weighted sums, matching the _ascii_key approach.

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
from complexity._timer import bench, print_table, save_plot

SIZES = [100, 500, 1_000, 5_000, 10_000]


def _ascii_key(name):
    return sum(ord(c) for c in name)


def _usernames(n, seed=42):
    random.seed(seed)
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    names = set()
    while len(names) < n:
        length = random.randint(4, 12)
        names.add("".join(random.choices(chars, k=length)))
    return [(_ascii_key(name), name) for name in names]


def _build(pairs):
    us = UserStorage()
    for key, _ in pairs:
        us.insert(key)
    return us


def run():
    print("\n=== UserStorage (BST) Complexity ===")
    print("  Note: add_user / find_user are stubs; testing inherited BST methods.\n")

    rows_insert = []
    for n in SIZES:
        pairs = _usernames(n)
        times = []
        for _ in range(3):
            us = UserStorage()
            start = time.perf_counter()
            for key, _ in pairs:
                us.insert(key)
            times.append(time.perf_counter() - start)
        rows_insert.append((n, statistics.median(times)))

    print_table(
        "UserStorage.insert  (build N-node BST from ascii-weighted keys)",
        rows_insert,
        expected="O(n log n) total  --  O(log n) per AVL insert",
    )

    def setup_search(n):
        pairs = _usernames(n)
        us    = _build(pairs)
        key   = pairs[n // 2][0]
        return (us, key)

    rows_search = bench(lambda us, k: us.search(k), SIZES, setup=setup_search, reps=10)
    print_table(
        "UserStorage.search  (single lookup in N-node BST)",
        rows_search,
        expected="O(log n)  --  ratio grows slowly (log factor)",
    )

    def setup_range(n):
        pairs = _usernames(n)
        keys  = sorted(p[0] for p in pairs)
        us    = _build(pairs)
        lo    = keys[int(n * 0.45)]
        hi    = keys[int(n * 0.55)]
        return (us, lo, hi)

    rows_range = bench(
        lambda us, lo, hi: us.range_query(lo, hi), SIZES, setup=setup_range, reps=10
    )
    print_table(
        "UserStorage.range_query  (~10% of N-node BST)",
        rows_range,
        expected="O(log n + k)  k ~ 0.1n  --  k term dominates as n grows",
    )

    def setup_inorder(n):
        pairs = _usernames(n)
        us    = _build(pairs)
        return (us,)

    rows_inorder = bench(lambda us: us.inorder(), SIZES, setup=setup_inorder, reps=5)
    print_table(
        "UserStorage.inorder  (full traversal of N-node BST)",
        rows_inorder,
        expected="O(n)  --  visits every node once; ratio ~ N2/N1",
    )

    save_plot(
        "user_storage_build.png",
        "UserStorage (BST) -- build cost: N insertions total",
        [
            {"label": "insert  N keys total  [O(n log n)]", "rows": rows_insert, "complexity": "O(n log n)"},
        ],
    )
    save_plot(
        "user_storage_query.png",
        "UserStorage (BST) -- single-query latency vs. tree size N",
        [
            {"label": "search  single lookup  [O(log n)]",    "rows": rows_search,  "complexity": "O(log n)"},
            {"label": "range_query  ~10% keys  [O(log n+k)]", "rows": rows_range,   "complexity": "O(n)",     "marker": "s"},
            {"label": "inorder  full scan  [O(n)]",           "rows": rows_inorder, "complexity": "O(n)",     "marker": "^"},
        ],
    )


if __name__ == "__main__":
    run()
