"""
test_load_play_history.py - Complexity test for ArcadeClient.load_play_history()

Source: client_test.py lines 466-481
    def load_play_history(self, user_obj, ranks_data):
        ...renders game-filter buttons...

The button-render itself is O(1) (5 fixed games).
The real complexity work happens when a game button is clicked, triggering
show_game_history() (lines 483-521), which:

    history_list  = [user_obj.get_history('game', i) for i in range(N)]  # O(n)
    sorted_history = self.sorter.heap_sort(history_list, mode=...)        # O(n log n)

Total end-to-end complexity (button render + sort + display):

Time Complexity
    load_play_history render:  O(1)        -- 5 game buttons, constant
    show_game_history:         O(n log n)  -- history retrieval O(n) + heap_sort O(n log n)
    Combined (user-visible):   O(n log n)

Space Complexity
    history_list:  O(n)       -- holds all N session references
    heap_sort:     O(log n)   -- in-place recursion stack
    Combined:      O(n)

Revision History:
    (ST) 05/05/2026 Create initial file
"""

import sys
import os
import random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.heap_sort import HeapSortGames
from user_interaction.history import History
from game_interaction.game_session import GameSession
from complexity._timer import (
    bench, bench_space, print_table, print_space_table,
    save_plot, save_space_plot,
)

SIZES  = [100, 500, 1_000, 5_000, 10_000, 50_000]
SORTER = HeapSortGames()
BASE   = datetime(2025, 1, 1)
GAMES  = ["LUAIANID", "JAG", "VERMIS", "RICHARD", "TOM"]


class _FakeUser:
    """Stand-in for User with get_history() and get_total_games()."""
    def __init__(self, sessions):
        self._sessions = sessions

    def get_total_games(self):
        return len(self._sessions)

    def get_history(self, kind, idx):
        if kind == "game":
            return self._sessions[idx]
        return None

    def update_history(self, *_):
        pass


class _Session:
    __slots__ = ("game_name", "start_time", "score")
    def __init__(self, game_name, start_time, score):
        self.game_name  = game_name
        self.start_time = start_time
        self.score      = score


def _make_user(n, seed=0):
    random.seed(seed)
    sessions = [
        _Session(
            random.choice(GAMES),
            BASE + timedelta(seconds=random.randint(0, 10_000_000)),
            random.randint(0, 500),
        )
        for _ in range(n)
    ]
    return _FakeUser(sessions)


def _show_game_history(user_obj, mode="time"):
    """
    Core data operations of show_game_history, without tkinter rendering.
    Matches lines 503-504 of client_test.py exactly.
    """
    history_list   = [user_obj.get_history("game", i)
                      for i in range(user_obj.get_total_games())]
    sorted_history = SORTER.heap_sort(history_list, mode=mode)
    return sorted_history


def run():
    print("\n=== load_play_history() / show_game_history() ===")

    # ── Time: history retrieval + sort ────────────────────────────────────────
    rows_time = bench(
        lambda user: _show_game_history(user, mode="time"),
        SIZES,
        setup=lambda n: (_make_user(n),),
        reps=5,
    )
    print_table(
        "show_game_history  (retrieve N sessions + heap_sort by time)",
        rows_time,
        expected="O(n log n)  --  O(n) retrieval + O(n log n) sort",
    )

    rows_score = bench(
        lambda user: _show_game_history(user, mode="score"),
        SIZES,
        setup=lambda n: (_make_user(n),),
        reps=5,
    )
    print_table(
        "show_game_history  (retrieve N sessions + heap_sort by score)",
        rows_score,
        expected="O(n log n)  --  same asymptotic, different comparator",
    )

    # ── Space ─────────────────────────────────────────────────────────────────
    rows_space = bench_space(
        lambda user: _show_game_history(user, mode="time"),
        SIZES,
        setup=lambda n: (_make_user(n),),
    )
    print_space_table(
        "show_game_history  peak heap allocation",
        rows_space,
        expected="O(n)  --  history_list holds N session references",
    )

    # ── Graphs ────────────────────────────────────────────────────────────────
    save_plot(
        "load_play_history_time.png",
        "load_play_history() -> show_game_history() -- Time Complexity",
        [
            {"label": "sort by time   [O(n log n)]",  "rows": rows_time,  "complexity": "O(n log n)"},
            {"label": "sort by score  [O(n log n)]",  "rows": rows_score, "complexity": "O(n log n)", "marker": "s"},
        ],
    )
    save_space_plot(
        "load_play_history_space.png",
        "load_play_history() -> show_game_history() -- Space Complexity",
        [
            {"label": "peak heap allocation  [O(n)]", "rows": rows_space, "complexity": "O(n)"},
        ],
    )


if __name__ == "__main__":
    run()
