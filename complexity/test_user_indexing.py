"""
test_user_indexing.py - Complexity test for user_interaction.user_indexing.UserIndexing

UserIndexing extends HashTable and maps user IDs to storage indices.

Processes tested:
  map_user(user_id, idx)  -- O(1) amortized: HashTable.set with quadratic probing
  get_index(user_id)      -- O(1) amortized: HashTable.get
  remove_user(user_id)    -- O(1) amortized: HashTable.delete

Two graphs are produced:
  user_indexing_total.png  -- N-total costs (O(n) total, O(1) per op)
  user_indexing_single.png -- single-call latency (should be flat O(1))

Revision History:
    (ST) 05/05/2026 Create initial file
"""

import sys
import os
import random
import time
import statistics

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_interaction.user_indexing import UserIndexing
from complexity._timer import bench, print_table, save_plot

SIZES = [500, 1_000, 5_000, 10_000, 50_000, 100_000]


def run():
    print("\n=== UserIndexing (HashTable) Complexity ===")

    # ── map_user: N insertions total ─────────────────────────────────────────
    rows_map = []
    for n in SIZES:
        ids = [f"user_{i}" for i in range(n)]
        times = []
        for _ in range(3):
            ui = UserIndexing()
            start = time.perf_counter()
            for i, uid in enumerate(ids):
                ui.map_user(uid, i)
            times.append(time.perf_counter() - start)
        rows_map.append((n, statistics.median(times)))

    print_table(
        "UserIndexing.map_user  (N insertions total)",
        rows_map,
        expected="O(n) total  --  O(1) amortized per insert; ratio ~ N2/N1",
    )

    # ── get_index: single lookup in N-entry table ────────────────────────────
    def setup_get(n):
        ui  = UserIndexing()
        ids = [f"user_{i}" for i in range(n)]
        for i, uid in enumerate(ids):
            ui.map_user(uid, i)
        target = ids[n // 2]
        return (ui, target)

    rows_get = bench(lambda ui, t: ui.get_index(t), SIZES, setup=setup_get, reps=20)
    print_table(
        "UserIndexing.get_index  (single lookup in N-entry table)",
        rows_get,
        expected="O(1)  --  direct hash probe; ratio stays near 1x",
    )

    # ── remove_user: single delete in N-entry table ──────────────────────────
    def setup_del(n):
        ui  = UserIndexing()
        ids = [f"user_{i}" for i in range(n)]
        for i, uid in enumerate(ids):
            ui.map_user(uid, i)
        return (ui, ids[n // 2])

    rows_del = bench(lambda ui, t: ui.remove_user(t), SIZES, setup=setup_del, reps=20)
    print_table(
        "UserIndexing.remove_user  (single delete in N-entry table)",
        rows_del,
        expected="O(1)  --  tombstone / rehash probe; ratio stays near 1x",
    )

    # ── N get_index calls (aggregate) ────────────────────────────────────────
    def setup_n_gets(n):
        ui  = UserIndexing()
        ids = [f"user_{i}" for i in range(n)]
        for i, uid in enumerate(ids):
            ui.map_user(uid, i)
        def _get_all():
            for uid in ids:
                ui.get_index(uid)
        return (_get_all,)

    rows_n_gets = bench(lambda fn: fn(), SIZES, setup=setup_n_gets, reps=3)
    print_table(
        "UserIndexing.get_index  (N lookups total)",
        rows_n_gets,
        expected="O(n) total  --  O(1) per lookup; ratio ~ N2/N1",
    )

    # Graph 1: O(n) total-cost operations
    save_plot(
        "user_indexing_total.png",
        "UserIndexing (HashTable) -- N-total operation cost",
        [
            {"label": "map_user    N insertions  [O(n)]", "rows": rows_map,    "complexity": "O(n)"},
            {"label": "get_index   N lookups     [O(n)]", "rows": rows_n_gets, "complexity": "O(n)", "marker": "s"},
        ],
    )

    # Graph 2: single-call latency -- should be flat O(1)
    save_plot(
        "user_indexing_single.png",
        "UserIndexing (HashTable) -- single-call latency vs. table size N",
        [
            {"label": "get_index    single lookup  [O(1)]", "rows": rows_get, "complexity": "O(1)"},
            {"label": "remove_user  single delete  [O(1)]", "rows": rows_del, "complexity": "O(1)", "marker": "s"},
        ],
    )


if __name__ == "__main__":
    run()
