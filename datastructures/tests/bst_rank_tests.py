"""
bst_rank tests
Author: Paul Garrison
Date: 4/25/26
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from datastructures.bst_rank import BST

def assert_equal(actual, expected, msg):
    if actual != expected:
        raise AssertionError(f"{msg}\nExpected: {expected}, Got: {actual}")


def assert_true(cond, msg):
    if not cond:
        raise AssertionError(msg)


def test_insert_and_ties():
    print("TEST 1: Insert + Ties")

    t = BST()

    t.insert((50, "Alice"))
    t.insert((30, "Bob"))
    t.insert((50, "Charlie"))
    t.insert((70, "Dave"))
    t.insert((50, "Eve"))

    # total users
    assert_equal(len(t), 5, "Total user count mismatch")

    # tie group check
    root = t._root
    assert_true(50 in [root.value, root.left.value, root.right.value],
                "50 score node missing")

    print("PASS: Insert + ties")


def test_rank():
    print("TEST 2: Rank correctness")

    t = BST()

    t.insert((100, "A"))
    t.insert((90, "B"))
    t.insert((90, "C"))
    t.insert((80, "D"))

    assert_equal(t.find_rank((100, "A")), 0, "A rank wrong")
    assert_equal(t.find_rank((90, "B")), 1, "B rank wrong")
    assert_equal(t.find_rank((90, "C")), 1, "C tie rank wrong")
    assert_equal(t.find_rank((80, "D")), 3, "D rank wrong")

    print("PASS: Rank correctness")


def test_kth_smallest():
    print("TEST 3: kth smallest")

    t = BST()

    data = [
        (100, "A"),
        (90, "B"),
        (90, "C"),
        (80, "D"),
        (70, "E"),
    ]

    for x in data:
        t.insert(x)

    # expected ordering (by score desc → but kth_smallest is asc)
    # 70, 80, 90, 90, 100

    assert_equal(t.kth_smallest(1)[0], 70, "k=1 wrong")
    assert_equal(t.kth_smallest(2)[0], 80, "k=2 wrong")
    assert_equal(t.kth_smallest(3)[0], 90, "k=3 wrong")

    print("PASS: kth smallest")


def test_kth_largest():
    print("TEST 4: kth largest")

    t = BST()

    t.insert((100, "A"))
    t.insert((90, "B"))
    t.insert((80, "C"))

    assert_equal(t.kth_largest(1)[0], 100, "k=1 largest wrong")
    assert_equal(t.kth_largest(2)[0], 90, "k=2 largest wrong")
    assert_equal(t.kth_largest(3)[0], 80, "k=3 largest wrong")

    print("PASS: kth largest")


def test_delete():
    print("TEST 5: Delete correctness")

    t = BST()

    t.insert((50, "A"))
    t.insert((50, "B"))
    t.insert((50, "C"))

    assert_equal(len(t), 3, "initial insert failed")

    t.delete((50, "B"))
    assert_equal(len(t), 2, "delete B failed")

    t.delete((50, "A"))
    assert_equal(len(t), 1, "delete A failed")

    t.delete((50, "C"))
    assert_equal(len(t), 0, "final delete failed")

    print("PASS: Delete correctness")


def test_mixed():
    print("TEST 6: Mixed operations")

    t = BST()

    t.insert((10, "A"))
    t.insert((20, "B"))
    t.insert((20, "C"))
    t.insert((30, "D"))

    assert_equal(len(t), 4, "size mismatch")

    # rank sanity
    assert_true(t.find_rank((30, "D")) == 0, "top rank wrong")

    # kth consistency
    top = t.kth_largest(1)
    assert_equal(top[0], 30, "top element wrong")

    print("PASS: Mixed operations")


if __name__ == "__main__":
    test_insert_and_ties()
    test_rank()
    test_kth_smallest()
    test_kth_largest()
    test_delete()
    test_mixed()

    print("\nALL TESTS PASSED")
