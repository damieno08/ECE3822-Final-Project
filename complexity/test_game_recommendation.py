"""
test_game_recommendation.py - Complexity test for
    user_interaction.game_recommendation.GameRecommendation

Processes tested:
  record_play(genre, game_name, seconds)  -- O(1): SparseMatrix.get + set via HashTable
  recommend()                             -- O(k log k), k <= 5 games -> O(1) in practice

Revision History:
    (ST) 05/05/2026 Create initial file
"""

import sys
import os
import random
import time
import statistics

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_interaction.game_recommendation import GameRecommendation, GAMES, GENRES
from complexity._timer import bench, print_table, save_plot

SIZES = [100, 500, 1_000, 5_000, 10_000, 100_000]

GAME_NAMES  = list(GAMES.keys())
GENRE_NAMES = list(GENRES.keys())


def run():
    print("\n=== GameRecommendation (SparseMatrix) Complexity ===")

    # ── record_play: N calls ──────────────────────────────────────────────────
    rows_record = []
    for n in SIZES:
        random.seed(0)
        calls = [
            (random.choice(GENRE_NAMES), random.choice(GAME_NAMES), random.uniform(60, 3600))
            for _ in range(n)
        ]
        times = []
        for _ in range(3):
            gr = GameRecommendation()
            start = time.perf_counter()
            for genre, game, secs in calls:
                gr.record_play(genre, game, secs)
            times.append(time.perf_counter() - start)
        rows_record.append((n, statistics.median(times)))

    print_table(
        "GameRecommendation.record_play  (N calls total)",
        rows_record,
        expected="O(n) total  --  O(1) per call (SparseMatrix.set via HashTable); ratio ~ N2/N1",
    )

    # ── recommend: single call after N record_play calls ─────────────────────
    def setup_recommend(n):
        random.seed(0)
        gr = GameRecommendation()
        for _ in range(n):
            gr.record_play(
                random.choice(GENRE_NAMES),
                random.choice(GAME_NAMES),
                random.uniform(60, 3600),
            )
        return (gr,)

    rows_recommend = bench(lambda gr: gr.recommend(), SIZES, setup=setup_recommend, reps=10)
    print_table(
        "GameRecommendation.recommend()  (after N record_play calls)",
        rows_recommend,
        expected=(
            "O(k log k) where k <= 5 games -> O(1) in practice; "
            "time stays constant regardless of N"
        ),
    )

    # ── correctness check ─────────────────────────────────────────────────────
    print("  Correctness check:")
    gr = GameRecommendation()
    gr.record_play("RPG",    "Luaianid", 100)
    gr.record_play("Action", "JAG",      500)
    gr.record_play("Action", "JAG",      200)
    result  = gr.recommend()
    top     = result[0][0] if result else None
    status  = "PASS" if top == "JAG" else f"FAIL (got {top!r})"
    print(f"  Most-played game ranks first: {status}")
    print(f"  Full ranking: {result}\n")

    save_plot(
        "game_recommendation.png",
        "GameRecommendation -- record_play vs. recommend scaling",
        [
            {"label": "record_play  N calls total  [O(n)]",          "rows": rows_record,    "complexity": "O(n)"},
            {"label": "recommend()  single call  [O(1) in practice]", "rows": rows_recommend, "complexity": "O(1)", "marker": "s"},
        ],
    )


if __name__ == "__main__":
    run()
