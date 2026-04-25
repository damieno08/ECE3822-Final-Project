"""
sparse_matrix_tests.py - Tests for SparseMatrix

Write tests for ALL methods of your SparseMatrix implementation.
You may use AI to help generate edge cases, but make sure you understand
every test before submitting.

Run with:
    cd code/game/datastructures/tests
n    python sparse_matrix_tests.py

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

# Suggested test ideas (each as a separate function):

def test_set_and_get():
    """ Test the get and set methods of the sparse matrix."""

    print("Testing Sparse Matrix Get and Set methods...")
    
    # Initialize matrix
    sparse = SparseMatrix()

    sparse.set(1, 2, 10)
    assert sparse.get(1, 2) == 10
    assert sparse.get(0, 0) == 0

    print("✓ Sparse Matrix Get and Set methods work!")

def test_default_value():
    """ Tests the default value when calling the sparse matrix constructor."""

    print("Testing Sparse Matrix default value...")
    
    # Initialize matrix
    sparse = SparseMatrix(rows = 5, cols = 5)
    assert sparse.default == 0

    print("✓ Sparse Matrix Get and Set methods work!")
    

def test_custom_default():
    """ Test the custom default value when calling the sparse matrix constructor."""

    print("Testing Sparse Matrix custom default value...")
    # Initialize matrix
    sparse = SparseMatrix(rows = 5, cols = 5, default = 5)

    # Assert default value
    assert sparse.default == 5
    
    print("✓ Sparse Matrix custom default value works!")
    
def test_len_empty():
    """ Test if the sparse matrix is empty. """

    print("Testing if Sparse Matrix is empty ...")
    
    # Initialize matrix
    sparse = SparseMatrix(rows = 5, cols = 5)

    assert len(sparse) == 0

    print("✓ Sparse Matrix length check works!")
    

def test_len_after_set():
    """ Check the length of the sparse matrix after setting an element.  """
    
    print("Testing if Sparse Matrix after element set increases size...")

    # Initialize matrix
    sparse = SparseMatrix(rows = 5, cols = 5)

    sparse.set(1, 2, 10)
    assert sparse.get(1, 2) == 10
    assert len(sparse) == 1
    
    print("✓ Sparse Matrix length after element set works!")
    
def test_items():
    """items() should yield exactly the non-default entries."""

    print("Testing items of Sparse Matrix...")

    # Initialize matrix
    sparse = SparseMatrix(rows = 5, cols = 5)

    # Set non-default entries
    sparse.set(1, 2, 10)
    sparse.set(3, 4, 20)
    sparse.set(0, 0, 5)

    # Get values
    retrieved_values = list(sparse.items())

    # assert count
    assert len(retrieved_values) == 3

    found = False
    for key, value in retrieved_values:
        if key == (1, 2) and value == 10:
            found = True

    assert found

    print("Testing items of Sparse Matrix works!")
    

def test_overwrite():
    """Setting a position twice keeps only the latest value."""

    print("Testing Sparse Matrix Overwrite...")

    # Initialize matrix
    sparse = SparseMatrix(rows = 2, cols = 2)
    sparse.set(0, 0, 10)
    assert sparse.__len__() == 1
    sparse.set(0, 0, 20)
    assert sparse.__len__() == 1
    assert sparse.get(0, 0) == 20
    assert len(sparse) == 1

    print("Testing Sparse Matrix Overwrite works!")

def test_set_to_default_removes_entry():
    """set(r, c, default) should remove the entry so len() decreases."""

    print("Testing Sparse Matrix default removes entry...")
    
    # Initialize matrix
    sparse = SparseMatrix(rows = 3, cols = 3, default = 0)
    sparse.set(1, 1, 10)
    #print(sparse.__len__())
    assert sparse.__len__() == 1
    
    sparse.set(1, 1, 0)
    #print(sparse.__len__())
    assert sparse.__len__() == 0

    print("Testing Sparse Matrix default removes entry works!")

def test_large_sparse():
    """A 1000x1000 matrix with 10 entries should use minimal memory."""

    print("Testing large Sparse Matrix....")

    # Initialize matrix
    sparse = SparseMatrix(1000, 1000)
    sparse.set(999, 999, 1)
    sparse.set(0, 0, 1)
    assert len(sparse) == 2
    
    print("Testing large Sparse Matrix works!")
    

def test_items_consistent_with_get():
    """Every (r, c) yielded by items() should match get(r, c)."""

    print("Testing Sparse Matrix consitency with get....") 

    # Initialize matrix
    sparse = SparseMatrix(rows = 10, cols = 10)
    sparse.set(1, 1, 5)
    sparse.set(2, 2, 10)

    for(r, c), val in sparse.items():
        assert sparse.get(r, c) == val
    
    print("Testing Sparse Matrix consitency with get works!")
    

def test_multiply_identity():
    """A * I == A  for a 2x2 identity matrix."""

    print("Testing Sparse Matrix multiplication identity...")
    
    A = SparseMatrix(2, 2)
    A.set(0, 1, 5)
    A.set(1, 0, 10)
    
    identity = SparseMatrix(2, 2)
    identity.set(0, 0, 1)
    identity.set(1, 1, 1)

    result = A.multiply(identity)
    assert result.get(0, 1) == 5
    assert result.get(1, 0) == 10
    assert len(result) == 2

    print("Testing Sparse Matrix multiplication identity works!") 
    

def test_multiply_basic():
    """Hand-computed 2x2 example."""

    print("Testing Sparse Matrix basic multiplication...")

    # Set elements of A
    A = SparseMatrix(2, 2)
    A.set(0, 0, 1)
    A.set(0, 1, 2)
    A.set(1, 0, 3)
    A.set(1, 1, 4)

    # Set elements of B
    B = SparseMatrix(2, 2)
    B.set(0, 0, 5)
    B.set(0, 1, 6)
    B.set(1, 0, 7)
    B.set(1, 1, 8)

    result = A.multiply(B)
    assert result.get(0, 0) == 19
    assert result.get(0, 1) == 22
    assert result.get(1, 0) == 43
    assert result.get(1, 1) == 50

    print("Testing Sparse Matrix basic multiplication works!")
    

def test_multiply_zero():
    """A * Z == all-zeros (empty sparse matrix)."""

    print("Testing Sparse Matrix multiplication by zero...")

    # Initialize zero matrix
    A = SparseMatrix(2, 2)
    A.set(0, 0, 5)
    zero = SparseMatrix(2, 2)

    # Multiply
    result = A.multiply(zero)
    assert len(result) == 0

    print("Testing Sparse Matrix multiplication by zero works!")
    
    

def test_str():
    """__str__ should return a non-empty string."""

    print("Testing Sparse Matrix __str__()....")

    # Initialize matrix
    sparse = SparseMatrix(2, 2)
    sparse.set(0, 0, 1)
    output = str(sparse)
    assert isinstance(output, str)
    assert len(output) > 0

    print("Testing Sparse Matrix __str__() works!")
    
    
# ==========================================================================


if __name__ == '__main__':

    test_set_and_get()
    test_default_value()
    test_custom_default()
    test_len_empty()
    test_len_after_set()
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
