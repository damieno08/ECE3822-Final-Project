"""
test_rate_limiter.py - Complexity test for
    user_interaction.chat_moderation.RateLimiter

Processes tested:
  RateLimiter.is_allowed(player)       -- O(m), m capped at max_messages -> O(1) per call
  RateLimiter.seconds_until_allowed(p) -- O(m) same -> O(1) per call

Revision History:
    (ST) 05/05/2026 Create initial file
"""

import sys
import os
import time
import statistics

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_interaction.chat_moderation import RateLimiter
from complexity._timer import bench, print_table, save_plot

SIZES     = [100, 500, 1_000, 5_000, 10_000, 50_000]
MSG_SIZES = [10,  50,  100,   500,   1_000,  5_000]


def run():
    print("\n=== RateLimiter Complexity ===")

    rows_distinct = []
    for n in SIZES:
        players = [f"player_{i}" for i in range(n)]
        times = []
        for _ in range(3):
            rl = RateLimiter(max_messages=5, window_seconds=10)
            start = time.perf_counter()
            for p in players:
                rl.is_allowed(p)
            times.append(time.perf_counter() - start)
        rows_distinct.append((n, statistics.median(times)))

    print_table(
        "RateLimiter.is_allowed  (N distinct players, 1 call each)",
        rows_distinct,
        expected="O(n) total  --  O(1) per call (window capped at max_messages=5)",
    )

    rows_same = []
    for n in MSG_SIZES:
        times = []
        for _ in range(5):
            rl = RateLimiter(max_messages=5, window_seconds=10)
            start = time.perf_counter()
            for _ in range(n):
                rl.is_allowed("spammer")
            times.append(time.perf_counter() - start)
        rows_same.append((n, statistics.median(times)))

    print_table(
        "RateLimiter.is_allowed  (same player, N calls)",
        rows_same,
        expected="O(n) total  --  O(5) per call -> O(1); ratio ~ N2/N1",
    )

    def setup_wait(n):
        rl = RateLimiter(max_messages=5, window_seconds=10)
        players = [f"player_{i}" for i in range(n)]
        for p in players:
            for _ in range(6):
                rl.is_allowed(p)
        return (rl, players)

    def call_wait(rl, players):
        for p in players:
            rl.seconds_until_allowed(p)

    rows_wait = bench(call_wait, SIZES, setup=setup_wait, reps=3)
    print_table(
        "RateLimiter.seconds_until_allowed  (N players over limit)",
        rows_wait,
        expected="O(n) total  --  O(1) per call (scans <= max_messages timestamps)",
    )

    save_plot(
        "rate_limiter.png",
        "RateLimiter -- total cost scaling with N",
        [
            {"label": "is_allowed  N distinct players  [O(n)]",  "rows": rows_distinct, "complexity": "O(n)"},
            {"label": "seconds_until_allowed  N players  [O(n)]","rows": rows_wait,     "complexity": "O(n)", "marker": "s"},
        ],
    )


if __name__ == "__main__":
    run()
