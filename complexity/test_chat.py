"""
test_chat.py - Complexity test for game_interaction.chat.Chat

Processes tested:
  send(user, message)  -- O(1): CircularBuffer.write wraps the fixed-size ring
  recent()             -- O(capacity): always iterates at most MAX_MESSAGES=20 slots

Both are O(1) with respect to total messages ever sent.
The graph confirms that per-call time stays flat as N grows from 100 to 1 000 000.

Revision History:
    (ST) 05/05/2026 Create initial file
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_interaction.chat import Chat
from complexity._timer import bench, print_table, save_plot

SIZES = [100, 1_000, 10_000, 100_000, 1_000_000]


def run():
    print("\n=== Chat (CircularBuffer) Complexity ===")

    # send: N messages total — O(n) total, O(1) per send
    def setup_send(n):
        chat = Chat()
        msgs = [f"msg_{i}" for i in range(n)]
        def _send_all():
            for m in msgs:
                chat.send("player", m)
        return (_send_all,)

    rows_send = bench(lambda fn: fn(), SIZES, setup=setup_send, reps=3)
    print_table(
        "Chat.send  (N total messages into a 20-slot buffer)",
        rows_send,
        expected="O(n) total  --  O(1) per send; ratio ~ N2/N1",
    )

    # recent: single call after N messages — O(20) = O(1) always
    def setup_recent(n):
        chat = Chat()
        for i in range(n):
            chat.send("player", f"msg_{i}")
        return (chat,)

    rows_recent = bench(lambda c: c.recent(), SIZES, setup=setup_recent, reps=10)
    print_table(
        "Chat.recent()  (after N total sends; always <= 20 stored messages)",
        rows_recent,
        expected="O(capacity) = O(20) = O(1)  --  ratio stays near 1x regardless of N",
    )

    save_plot(
        "chat.png",
        "Chat (CircularBuffer) -- scaling with total messages sent",
        [
            {"label": "send  N messages total  [O(n)]",     "rows": rows_send,   "complexity": "O(n)"},
            {"label": "recent()  single call  [O(1) = O(20)]", "rows": rows_recent, "complexity": "O(1)", "marker": "s"},
        ],
    )


if __name__ == "__main__":
    run()
