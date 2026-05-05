"""
test_profanity_filter.py - Complexity test for
    user_interaction.chat_moderation.ProfanityFilter
    user_interaction.chat_moderation.PrimeHashTable

Processes tested:
  ProfanityFilter.contains_profanity(text)  -- O(w): scans every word in text
  ProfanityFilter.censor(text)              -- O(w): scans + replaces every word
  ProfanityFilter.add_word(word)            -- O(1) amortized: PrimeHashTable.set

Two graphs are produced:
  profanity_scan.png  -- contains_profanity and censor vs. text length (O(w))
  profanity_add.png   -- add_word total cost vs. N words added (O(n) amortized)

Revision History:
    (ST) 05/05/2026 Create initial file
"""

import sys
import os
import random
import time
import statistics

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_interaction.chat_moderation import ProfanityFilter, PrimeHashTable
from complexity._timer import bench, print_table, save_plot

SIZES_TEXT = [10, 50, 100, 500, 1_000, 5_000]
SIZES_ADD  = [100, 500, 1_000, 5_000, 10_000, 50_000]

_CLEAN = [
    "hello", "world", "game", "player", "score", "level", "jump",
    "run", "fight", "castle", "sword", "shield", "magic", "quest",
    "dragon", "hero", "victory", "defeat", "arena", "tower",
]
_PROFANE_SAMPLE = ["damn", "crap", "ass"]


def _make_text(n_words, profanity_rate=0.05, seed=0):
    random.seed(seed)
    words = []
    for _ in range(n_words):
        if random.random() < profanity_rate:
            words.append(random.choice(_PROFANE_SAMPLE))
        else:
            words.append(random.choice(_CLEAN))
    return " ".join(words)


def run():
    print("\n=== ProfanityFilter / PrimeHashTable Complexity ===")

    pf = ProfanityFilter()

    def setup_contains(n):
        return (_make_text(n),)

    rows_contains = bench(pf.contains_profanity, SIZES_TEXT, setup=setup_contains, reps=10)
    print_table(
        "ProfanityFilter.contains_profanity(text)  (N-word text)",
        rows_contains,
        expected="O(w) where w = words in text  --  ratio ~ N2/N1",
    )

    def setup_censor(n):
        return (_make_text(n, profanity_rate=0.1),)

    rows_censor = bench(pf.censor, SIZES_TEXT, setup=setup_censor, reps=10)
    print_table(
        "ProfanityFilter.censor(text)  (N-word text, 10% profane)",
        rows_censor,
        expected="O(w)  --  same scan + regex sub; ratio ~ N2/N1",
    )

    rows_add = []
    for n in SIZES_ADD:
        words = [f"zword_{i}" for i in range(n)]
        times = []
        for _ in range(3):
            pf2 = ProfanityFilter()
            start = time.perf_counter()
            for w in words:
                pf2.add_word(w)
            times.append(time.perf_counter() - start)
        rows_add.append((n, statistics.median(times)))

    print_table(
        "ProfanityFilter.add_word  (N words added total)",
        rows_add,
        expected=(
            "O(n) total  --  O(1) amortized per add (PrimeHashTable); "
            "periodic resizes are O(n) but amortized"
        ),
    )

    print("  PrimeHashTable resize sanity check:")
    pht = PrimeHashTable(initial_capacity=10)
    for i in range(300):
        pht.set(f"key_{i}", i)
    is_prime = all(
        pht.capacity % d != 0 for d in range(2, int(pht.capacity ** 0.5) + 1)
    )
    print(f"  Capacity after 300 inserts: {pht.capacity}  (prime: {is_prime})\n")

    save_plot(
        "profanity_scan.png",
        "ProfanityFilter -- scan cost vs. text length (words)",
        [
            {"label": "contains_profanity  [O(w)]", "rows": rows_contains, "complexity": "O(n)"},
            {"label": "censor  [O(w)]",             "rows": rows_censor,   "complexity": "O(n)", "marker": "s"},
        ],
    )
    save_plot(
        "profanity_add.png",
        "ProfanityFilter.add_word -- N words added to PrimeHashTable",
        [
            {"label": "add_word  N words total  [O(n) amortized]", "rows": rows_add, "complexity": "O(n)"},
        ],
    )


if __name__ == "__main__":
    run()
