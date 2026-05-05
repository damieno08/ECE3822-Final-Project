"""
test_find_user.py - Complexity test for ArcadeServer.find_user_by_name()

Source: main_server.py lines 105-109
    def find_user_by_name(self, name):
        for i in range(len(self.main_array)):
            if self.main_array[i].name == name:
                return self.main_array[i]
        return None

Called on every LOGIN_REQUEST, SAVE_SESSION, SAVE_CHAT, and GET_HISTORY
to locate a user in the server's in-memory ArrayList.

Time Complexity
    O(n)  -- single linear scan through main_array of n users.
    Worst case: user not found or at end of array.

Space Complexity
    O(1)  -- only a loop index variable; no extra allocation.

Revision History:
    (ST) 05/05/2026 Create initial file
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datastructures.array import ArrayList
from complexity._timer import (
    bench, bench_space, print_table, print_space_table,
    save_plot, save_space_plot,
)

SIZES = [100, 500, 1_000, 5_000, 10_000, 50_000, 100_000]


class _User:
    """Minimal stand-in for User -- only .name is needed."""
    __slots__ = ("name",)
    def __init__(self, name):
        self.name = name


def _find_user_by_name(main_array, name):
    """Exact copy of ArcadeServer.find_user_by_name (no socket needed)."""
    for i in range(len(main_array)):
        if main_array[i].name == name:
            return main_array[i]
    return None


def _make_array(n):
    arr = ArrayList()
    for i in range(n):
        arr.append(_User(f"user_{i}"))
    return arr


def run():
    print("\n=== find_user_by_name() ===")

    # ── Time: worst-case (target not present) ─────────────────────────────────
    rows_miss = bench(
        lambda arr, name: _find_user_by_name(arr, name),
        SIZES,
        setup=lambda n: (_make_array(n), "ghost"),
        reps=5,
    )
    print_table(
        "find_user_by_name  (worst case: user not found)",
        rows_miss,
        expected="O(n)  --  full scan; ratio ~ N2/N1",
    )

    # ── Time: hit at midpoint ─────────────────────────────────────────────────
    rows_mid = bench(
        lambda arr, name: _find_user_by_name(arr, name),
        SIZES,
        setup=lambda n: (_make_array(n), f"user_{n // 2}"),
        reps=5,
    )
    print_table(
        "find_user_by_name  (average case: hit at midpoint)",
        rows_mid,
        expected="O(n)  --  half scan on average; same slope, ~0.5x constant",
    )

    # ── Space ─────────────────────────────────────────────────────────────────
    rows_space = bench_space(
        lambda arr, name: _find_user_by_name(arr, name),
        SIZES,
        setup=lambda n: (_make_array(n), "ghost"),
    )
    print_space_table(
        "find_user_by_name  peak heap allocation",
        rows_space,
        expected="O(1)  --  only a loop variable; allocation stays flat",
    )

    # ── Graphs ────────────────────────────────────────────────────────────────
    save_plot(
        "find_user_time.png",
        "find_user_by_name() -- Time Complexity",
        [
            {"label": "worst case (miss)      [O(n)]", "rows": rows_miss, "complexity": "O(n)"},
            {"label": "average case (mid hit) [O(n)]", "rows": rows_mid,  "complexity": "O(n)", "marker": "s"},
        ],
    )
    save_space_plot(
        "find_user_space.png",
        "find_user_by_name() -- Space Complexity",
        [
            {"label": "peak heap allocation  [O(1)]", "rows": rows_space, "complexity": "O(1)"},
        ],
    )


if __name__ == "__main__":
    run()
