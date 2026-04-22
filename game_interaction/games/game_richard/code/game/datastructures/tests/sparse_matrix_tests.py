"""
sparse_matrix_tests.py - Tests for SparseMatrix

Write tests for ALL methods of your SparseMatrix implementation.
You may use AI to help generate edge cases, but make sure you understand
every test before submitting.

Run with:
    cd code/game/datastructures/tests
    python sparse_matrix_tests.py

Author: [Your Name]
Date:   [Date]
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
# def test_set_and_get():
#
# def test_default_value():
#
# def test_custom_default():
#
# def test_len_empty():
#
# def test_len_after_set():
#
# def test_items():
#     """items() should yield exactly the non-default entries."""
#
# def test_overwrite():
#     """Setting a position twice keeps only the latest value."""
#
# def test_set_to_default_removes_entry():
#     """set(r, c, default) should remove the entry so len() decreases."""
#
# def test_large_sparse():
#     """A 1000x1000 matrix with 10 entries should use minimal memory."""
#
# def test_items_consistent_with_get():
#     """Every (r, c) yielded by items() should match get(r, c)."""
#
# def test_multiply_identity():
#     """A * I == A  for a 2x2 identity matrix."""
#
# def test_multiply_basic():
#     """Hand-computed 2x2 example."""
#
# def test_multiply_zero():
#     """A * Z == all-zeros (empty sparse matrix)."""
#
# def test_str():
#     """__str__ should return a non-empty string."""
# ==========================================================================


if __name__ == '__main__':
    # TODO: call your tests here
    print("All tests passed!")
