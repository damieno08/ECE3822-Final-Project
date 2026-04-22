"""
sparse_matrix_tests.py - Tests for SparseMatrix

Write tests for ALL methods of your SparseMatrix implementation.
You may use AI to help generate edge cases, but make sure you understand
every test before submitting.

Run with:
    cd code/game/datastructures/tests
    python sparse_matrix_tests.py

Author: Santiago Troya
Date:   04/10/2026
Lab:    Lab 6 - Sparse World Map
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.sparse_matrix import SparseMatrix
from scipy.sparse import csr_matrix
import numpy as np


def test_set_and_get():
    m = SparseMatrix()
    m.set(0, 0, 5)
    m.set(2, 3, 7)
    assert m.get(0, 0) == 5, "Expected 5 at (0,0)"
    assert m.get(2, 3) == 7, "Expected 7 at (2,3)"


def test_default_value():
    m = SparseMatrix()
    assert m.get(10, 10) == 0, "Unset cell should return default 0"
    assert m.get(0, 0) == 0


def test_custom_default():
    m = SparseMatrix(default=-1)
    assert m.get(5, 5) == -1, "Unset cell should return custom default -1"
    m.set(1, 1, 42)
    assert m.get(1, 1) == 42
    assert m.get(1, 2) == -1


def test_len_empty():
    m = SparseMatrix()
    assert len(m) == 0, "Empty matrix should have len 0"


def test_len_after_set():
    m = SparseMatrix()
    m.set(0, 0, 1)
    m.set(1, 1, 2)
    m.set(2, 2, 3)
    assert len(m) == 3, "Expected 3 stored entries"


def test_items():
    """items() should yield exactly the non-default entries."""
    m = SparseMatrix()
    m.set(0, 1, 10)
    m.set(3, 3, 20)
    entries = {pos: val for pos, val in m.items()}
    assert (0, 1) in entries and entries[(0, 1)] == 10
    assert (3, 3) in entries and entries[(3, 3)] == 20
    assert len(entries) == 2, "items() should yield exactly 2 entries"


def test_overwrite():
    """Setting a position twice keeps only the latest value."""
    m = SparseMatrix()
    m.set(1, 1, 99)
    m.set(1, 1, 42)
    assert m.get(1, 1) == 42, "Second set should overwrite first"
    assert len(m) == 1, "Overwrite should not increase len"


def test_set_to_default_removes_entry():
    """set(r, c, default) should remove the entry so len() decreases."""
    m = SparseMatrix(default=0)
    m.set(2, 2, 5)
    assert len(m) == 1
    m.set(2, 2, 0)  # set back to default
    assert len(m) == 0, "Setting to default should remove the entry"
    assert m.get(2, 2) == 0


def test_large_sparse():
    """A 1000x1000 matrix with 10 entries should use minimal memory."""
    m = SparseMatrix(rows=1000, cols=1000, default=0)
    coords = [(i * 100, i * 99) for i in range(10)]
    for r, c in coords:
        m.set(r, c, r + c + 1)  # +1 ensures value is never the default (0)
    assert len(m) == 10
    for r, c in coords:
        assert m.get(r, c) == r + c + 1
    # All other cells return the default
    assert m.get(500, 501) == 0


def test_items_consistent_with_get():
    """Every (r, c) yielded by items() should match get(r, c)."""
    m = SparseMatrix()
    for i in range(15):
        m.set(i, i * 2, i * 3)
    for (r, c), val in m.items():
        assert m.get(r, c) == val, f"items() and get() disagree at ({r},{c})"


def test_multiply_identity():
    """A * I == A for a 2x2 identity matrix."""
    A = SparseMatrix(rows=2, cols=2)
    A.set(0, 0, 3)
    A.set(0, 1, 4)
    A.set(1, 0, 5)
    A.set(1, 1, 6)

    I = SparseMatrix(rows=2, cols=2)
    I.set(0, 0, 1)
    I.set(1, 1, 1)

    result = A.multiply(I)
    assert result.get(0, 0) == 3
    assert result.get(0, 1) == 4
    assert result.get(1, 0) == 5
    assert result.get(1, 1) == 6


def test_multiply_basic():
    """Hand-computed 2x2 example verified against scipy."""
    # A = [[1, 2], [3, 4]]   B = [[5, 6], [7, 8]]
    # A*B = [[1*5+2*7, 1*6+2*8], [3*5+4*7, 3*6+4*8]]
    #     = [[19, 22], [43, 50]]
    A = SparseMatrix(rows=2, cols=2)
    for r, c, v in [(0,0,1),(0,1,2),(1,0,3),(1,1,4)]:
        A.set(r, c, v)

    B = SparseMatrix(rows=2, cols=2)
    for r, c, v in [(0,0,5),(0,1,6),(1,0,7),(1,1,8)]:
        B.set(r, c, v)

    result = A.multiply(B)

    # Verify with scipy
    sa = csr_matrix(np.array([[1,2],[3,4]]))
    sb = csr_matrix(np.array([[5,6],[7,8]]))
    expected = (sa * sb).toarray()

    assert result.get(0, 0) == expected[0][0]
    assert result.get(0, 1) == expected[0][1]
    assert result.get(1, 0) == expected[1][0]
    assert result.get(1, 1) == expected[1][1]


def test_multiply_zero():
    """A * Z == all-zeros (empty sparse matrix)."""
    A = SparseMatrix(rows=2, cols=2)
    A.set(0, 0, 9)
    A.set(1, 1, 3)

    Z = SparseMatrix(rows=2, cols=2)  # all default=0

    result = A.multiply(Z)
    assert len(result) == 0, "Product with zero matrix should have no stored entries"
    assert result.get(0, 0) == 0
    assert result.get(1, 1) == 0


def test_str():
    """__str__ should return a non-empty, informative string."""
    m = SparseMatrix(rows=5, cols=5, default=-1)
    m.set(1, 2, 10)
    s = str(m)
    assert isinstance(s, str) and len(s) > 0
    assert "5" in s, "String should include dimension info"
    assert "1" in s, "String should reflect nnz count"


if __name__ == '__main__':
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
