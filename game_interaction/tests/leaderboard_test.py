"""
Tests for "leaderboard.py"
Date: 4/30/26
Author: Paul Garrison
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from leaderboard import Leaderboard


def assert_equal(a, b, msg=""):
    if a != b:
        raise AssertionError(f"{msg} | Expected {b}, got {a}")


def assert_true(cond, msg=""):
    if not cond:
        raise AssertionError(msg)


# ---------------------------------------------------------
# TEST 1 — Basic insertion + lookup
# ---------------------------------------------------------
def test_basic_add_and_lookup():
    print("TEST 1: Basic add + score lookup")

    lb = Leaderboard()

    lb.add_score("Alice", 50)
    lb.add_score("Bob", 30)
    lb.add_score("Charlie", 70)

    assert_equal(lb.score_of("Alice"), 50, "Alice score wrong")
    assert_equal(lb.score_of("Bob"), 30, "Bob score wrong")
    assert_equal(lb.score_of("Charlie"), 70, "Charlie score wrong")

    print("PASS")


# ---------------------------------------------------------
# TEST 2 — Reject worse scores
# ---------------------------------------------------------
def test_reject_worse_score():
    print("TEST 2: Reject worse score")

    lb = Leaderboard()

    assert_true(lb.add_score("Alice", 50))
    assert_true(not lb.add_score("Alice", 40))   # should be ignored
    assert_true(not lb.add_score("Alice", 50))   # equal ignored

    assert_equal(lb.score_of("Alice"), 50)

    print("PASS")


# ---------------------------------------------------------
# TEST 3 — Score update (delete + reinsert)
# ---------------------------------------------------------
def test_score_update():
    print("TEST 3: Score update")

    lb = Leaderboard()

    lb.add_score("Alice", 50)
    lb.add_score("Bob", 30)

    lb.add_score("Alice", 80)   # upgrade

    assert_equal(lb.score_of("Alice"), 80)
    assert_equal(lb.rank_of("Alice"), 1)

    print("PASS")


# ---------------------------------------------------------
# TEST 4 — Rank correctness
# ---------------------------------------------------------
def test_rankings():
    print("TEST 4: Rankings")

    lb = Leaderboard()

    lb.add_score("Alice", 100)
    lb.add_score("Bob", 80)
    lb.add_score("Charlie", 60)
    lb.add_score("Dave", 40)

    assert_equal(lb.rank_of("Alice"), 1)
    assert_equal(lb.rank_of("Bob"), 2)
    assert_equal(lb.rank_of("Charlie"), 3)
    assert_equal(lb.rank_of("Dave"), 4)

    print("PASS")


# ---------------------------------------------------------
# TEST 5 — Ties handling
# ---------------------------------------------------------
def test_ties():
    print("TEST 5: Ties")

    lb = Leaderboard()

    lb.add_score("Alice", 100)
    lb.add_score("Bob", 100)
    lb.add_score("Charlie", 90)

    players = lb.players_with_score(100)
    assert_equal(players, ["Alice", "Bob"])

    # both tied players share rank 1 or 2 (tree ranks by insertion order inside tie)
    assert_true(lb.rank_of("Alice") in [1, 2])
    assert_true(lb.rank_of("Bob") in [1, 2])

    print("PASS")


# ---------------------------------------------------------
# TEST 6 — top_n()
# ---------------------------------------------------------
def test_top_n():
    print("TEST 6: Top N")

    lb = Leaderboard()

    lb.add_score("A", 10)
    lb.add_score("B", 20)
    lb.add_score("C", 30)
    lb.add_score("D", 40)

    top3 = lb.top_n(3)

    assert_equal(top3, [("D", 40), ("C", 30), ("B", 20)])

    print("PASS")
# ---------------------------------------------------------
# TEST 7 - example leaderboard
# ---------------------------------------------------------
def test_display_full_leaderboard_with_ties():
    print("TEST 7: Display leaderboard with ties")

    lb = Leaderboard()

    # 10 players, with a tie in the top 5
    players = [
        ("Alice", 95),
        ("Bob", 88),
        ("Charlie", 88),   # ← tie
        ("Dave", 70),
        ("Eve", 65),
        ("Frank", 60),
        ("Grace", 55),
        ("Heidi", 50),
        ("Ivan", 45),
        ("Judy", 40),
    ]

    for user, score in players:
        lb.add_score(user, score)

    # ---- Print Top 5 ----
    print("\nTop 5 Players:")
    top5 = lb.top_n(5)
    for i, (user, score) in enumerate(top5, start=1):
        print(f"{i}. {user} - {score}")

    # Ensure both tied players are inside top 5
    top5_users = [u for u, _ in top5]
    assert_true("Bob" in top5_users, "Bob missing from top 5")
    assert_true("Charlie" in top5_users, "Charlie missing from top 5")

    # ---- Print Remaining Leaderboard ----
    print("\nRest of Leaderboard:")
    total_players = len(lb)

    for rank in range(6, total_players + 1):
        score, user = lb.kth_largest(rank)
        print(f"{rank}. {user} - {score}")
    
# ---------------------------------------------------------
# Run all tests
# ---------------------------------------------------------
if __name__ == "__main__":
    test_basic_add_and_lookup()
    test_reject_worse_score()
    test_score_update()
    test_rankings()
    test_ties()
    test_top_n()
    test_display_full_leaderboard_with_ties()

    print("\nALL LEADERBOARD TESTS PASSED")
