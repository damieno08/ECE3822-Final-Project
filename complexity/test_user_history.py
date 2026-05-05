"""
test_user_history.py - Complexity tests for user_interaction history classes

Processes tested:
  History.set_history(session)      -- O(1): Stack.push onto an ArrayList
  History.get_history(idx)          -- O(1): Stack.peek by index (ArrayList lookup)
  History.pop()                     -- O(1): Stack.pop (ArrayList pop at end)
  Play_history.get_total_time()     -- O(n): iterates all n sessions summing playtime

Two graphs are produced:
  user_history_total.png  -- N-total costs (set_history N times, get_total_time)
  user_history_single.png -- single-call latency vs. history depth

Revision History:
    (ST) 05/05/2026 Create initial file
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_interaction.history import History
from user_interaction.play_history import Play_history
from game_interaction.game_session import GameSession
from complexity._timer import bench, print_table, save_plot

SIZES        = [100, 500, 1_000, 5_000, 10_000, 50_000]
SIZES_LINEAR = [100, 500, 1_000, 5_000, 10_000]


class _FakeUser:
    def update_history(self, *args):
        pass


def _make_session():
    s = GameSession(_FakeUser(), "test_game")
    s.start_time = datetime(2026, 1, 1, 0, 0, 0)
    s.end_time   = datetime(2026, 1, 1, 0, 1, 0)
    return s


def run():
    print("\n=== User History Complexity ===")

    def setup_push(n):
        h   = History()
        ses = _make_session()
        def _push_n():
            for _ in range(n):
                h.set_history(ses)
        return (_push_n,)

    rows_push = bench(lambda fn: fn(), SIZES, setup=setup_push, reps=3)
    print_table(
        "History.set_history  (N pushes total)",
        rows_push,
        expected="O(n) total  --  O(1) amortized per push (ArrayList); ratio ~ N2/N1",
    )

    def setup_peek(n):
        h   = History()
        ses = _make_session()
        for _ in range(n):
            h.set_history(ses)
        return (h,)

    rows_peek = bench(lambda h: h.get_history(-1), SIZES, setup=setup_peek, reps=10)
    print_table(
        "History.get_history(-1)  (peek top after N pushes)",
        rows_peek,
        expected="O(1)  --  ArrayList index lookup; ratio stays near 1x",
    )

    def setup_pop(n):
        h   = History()
        ses = _make_session()
        for _ in range(n):
            h.set_history(ses)
        return (h,)

    rows_pop = bench(lambda h: h.pop(), SIZES, setup=setup_pop, reps=10)
    print_table(
        "History.pop()  (pop from a history of size N)",
        rows_pop,
        expected="O(1)  --  ArrayList pop from end; ratio stays near 1x",
    )

    def setup_total_time(n):
        ph  = Play_history()
        ses = _make_session()
        for _ in range(n):
            ph.set_history(ses)
        return (ph,)

    rows_total = bench(
        lambda ph: ph.get_total_time(), SIZES_LINEAR, setup=setup_total_time, reps=5
    )
    print_table(
        "Play_history.get_total_time()  (sum over N sessions)",
        rows_total,
        expected="O(n)  --  full iteration of the Stack's array; ratio ~ N2/N1",
    )

    save_plot(
        "user_history_total.png",
        "User History -- O(n) total-cost operations",
        [
            {"label": "set_history  N pushes total  [O(n)]",       "rows": rows_push,  "complexity": "O(n)"},
            {"label": "get_total_time()  scan N sessions  [O(n)]", "rows": rows_total, "complexity": "O(n)", "marker": "s"},
        ],
    )
    save_plot(
        "user_history_single.png",
        "User History -- single-call latency vs. history depth N",
        [
            {"label": "get_history(-1)  single peek  [O(1)]", "rows": rows_peek, "complexity": "O(1)"},
            {"label": "pop()  single pop  [O(1)]",            "rows": rows_pop,  "complexity": "O(1)", "marker": "s"},
        ],
    )


if __name__ == "__main__":
    run()
