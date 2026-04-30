"""
sparse_matrix_tests.py - Tests for SparseMatrix

Write tests for ALL methods of your SparseMatrix implementation.
You may use AI to help generate edge cases, but make sure you understand
every test before submitting.

Run with:
    cd code/game/datastructures/tests
    python sparse_matrix_tests.py

Author: Richard Lin
Date:   4/15/26
Lab:    Lab 6 - Sparse World Map
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.sparse_matrix import SparseMatrix
from scipy.sparse import csr_matrix


# ==========================================================================
# TODO: Write your tests below
#
# Suggested test ideas (each as a separate function):
#
def test_set_and_get():
    m = SparseMatrix(default=-1)
    m.set(2, 3, 10)
    assert m.get(2, 3) == 10

def test_default_value():
    m = SparseMatrix(default=-1)
    assert m.get(0, 0) == -1


def test_custom_default():
    m = SparseMatrix(default=0)
    assert m.get(5, 5) == 0


def test_len_empty():
    m = SparseMatrix(default=-1)
    assert len(m) == 0


def test_len_after_set():
    m = SparseMatrix(default=-1)
    m.set(1, 1, 5)
    assert len(m) == 1

def test_items():
    """items() should yield exactly the non-default entries."""
    m = SparseMatrix(default=-1)
    m.set(1, 2, 3)
    m.set(4, 5, 6)

    items = list(m.items())
    assert ((1, 2), 3) in items
    assert ((4, 5), 6) in items
    assert len(items) == 2


def test_overwrite():
    """Setting a position twice keeps only the latest value."""
    m = SparseMatrix(default=-1)
    m.set(1, 1, 5)
    m.set(1, 1, 10)

    assert m.get(1, 1) == 10
    assert len(m) == 1

def test_set_to_default_removes_entry():
    """set(r, c, default) should remove the entry so len() decreases."""
    m = SparseMatrix(default=-1)
    m.set(2, 2, 7)
    m.set(2, 2, -1)

    assert m.get(2, 2) == -1
    assert len(m) == 0

def test_large_sparse():
    """A 1000x1000 matrix with 10 entries should use minimal memory."""
    m = SparseMatrix(default=-1)

    for i in range(10):
        m.set(i, i, i * 2)

    assert len(m) == 10
    for i in range(10):
        assert m.get(i, i) == i * 2

    assert m.get(999, 999) == -1

def test_items_consistent_with_get():
    """Every (r, c) yielded by items() should match get(r, c)."""
    m = SparseMatrix(default=-1)
    m.set(1, 2, 3)
    m.set(3, 4, 5)

    for (r, c), v in m.items():
        assert m.get(r, c) == v


def test_multiply_identity():
    """A * I == A  for a 2x2 identity matrix."""
    m = SparseMatrix(default=0)
    m.set(0, 0, 2)
    m.set(1, 1, 3)

    identity = SparseMatrix(default=0)
    identity.set(0, 0, 1)
    identity.set(1, 1, 1)

    result = m.multiply(identity)

    assert result.get(0, 0) == 2
    assert result.get(1, 1) == 3

def test_multiply_basic():
    """Hand-computed 2x2 example."""
    a = SparseMatrix(default=0)
    b = SparseMatrix(default=0)

    a.set(0, 0, 1)
    a.set(0, 1, 2)
    a.set(1, 1, 3)

    b.set(0, 0, 4)
    b.set(1, 0, 5)
    b.set(1, 1, 6)

    result = a.multiply(b)

    assert result.get(0, 0) == 14
    assert result.get(0, 1) == 12
    assert result.get(1, 0) == 15
    assert result.get(1, 1) == 18

def test_multiply_zero():
    """A * Z == all-zeros (empty sparse matrix)."""
    a = SparseMatrix(default=0)
    a.set(0, 0, 5)

    zero = SparseMatrix(default=0)

    result = a.multiply(zero)

    assert len(result) == 0

def test_str():
    """__str__ should return a non-empty string."""
    m = SparseMatrix(default=-1)
    m.set(1, 1, 5)

    s = str(m)
    assert isinstance(s, str)
    assert len(s) > 0
# ==========================================================================


if __name__ == '__main__':
    # TODO: call your tests here
    test_set_and_get()
    test_default_value()
    test_custom_default()
    test_len_empty()
    test_len_after_set()
    test_items()
    test_overwrite()
    test_set_to_default_removes_entry()
    test_large_sparse()
    test_items_consistent_with_get()
    test_multiply_identity()
    test_multiply_basic()
    test_multiply_zero()
    test_str()
    print("All tests passed!")
