"""
sparse_matrix_complexity.py - Performance analysis for SparseMatrix

Compare your SparseMatrix implementation to:
  - scipy.sparse (CSR format)
  - numpy dense matrix (numpy.ndarray)

Measure and report wall-clock time for:
  1. Building the matrix (set() calls)
  2. Random get() accesses
  3. items() full iteration
  4. multiply()

Run with:
    cd code/game/datastructures/complexity
    python sparse_matrix_complexity.py

Install dependencies if needed:
    pip install scipy numpy

Author: [Your Name]
Date:   [Date]
Lab:    Lab 6 - Sparse World Map
"""

import time
import random
import sys
import os

try:
    from scipy.sparse import csr_matrix
    import numpy as np
except ImportError:
    return {'error': 'scipy/numpy not installed — run: pip install scipy numpy'}

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.sparse_matrix import SparseMatrix
