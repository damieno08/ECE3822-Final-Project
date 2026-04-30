# Sparse Matrix Complexity Analysis

**Name:** Richard Lin
**Date:** 4/15/26
**Implementation:** COO

---

## Overview

I implemented the sparse matrix using the COO (Coordinate List) representation backed by the ArrayList

Each non-default entry is stored as (row, col, value)

This design was chosen because:
- It was simple and works nicely with the ArrayList Class
- It stores only non-default values, saving a lot of memory compared to a dense matrix
- It doesn't require to implement a hash table or CSR pointer

The tradeoff is that all the operation rely on linear scanning of the internal list, making operations slower than optimized.

---

## Time Complexity

Fill in the `?` cells after analysing your implementation.

| Operation | Your SparseMatrix | scipy sparse (CSR) | numpy dense |
|-----------|-------------------|--------------------|-------------|
| `set(r, c, v)` | O(nnz) | O(nnz) amortised | O(1) |
| `get(r, c)` | O(nnz) | O(log nnz) | O(1) |
| `items()` iteration | O(nnz) | O(nnz) | O(n²) |
| `multiply(other)` | O(nnz²) | O(nnz²/n) | O(n³) |

*nnz = number of non-zero entries, n = matrix dimension side length*

- set: must scan ArrayList to find exisiting entry
- get: linear search through stored entries
- item: loops through all stored values
- multiply: nested loop over both sparse list

---

## Benchmark Results

Run `sparse_matrix_complexity.py` and paste the output here:

```
CUSTOM
Build: 0.11823009999352507
Get: 0.364336300001014
Items: 0.00044010000419802964
Multiply: 10.813771300003282

SCIPY
Build: 0.00166680000256747
Get: 0.04741900000226451
Items: 0.00015050000365590677
Multiply: 0.00024510000366717577

NUMPY
Build: 0.0011510000040289015
Get: 0.0030019000041647814
Items: 0.00012549999519251287
Multiply: 0.00014229999942472205

```

---

## Space Complexity

| Representation | Space Used |
|----------------|-----------|
| Dense n×n      | O(n²)     |
| Your sparse    | O(nnz)      |

### Measured Memory Usage
CUSTOM MEMORY: 15664
SCIPY MEMORY: 56972
NUMPY MEMORY: 80328

### Explanation
My sparse only store non-default values, so the memory would be linear with the number of stored entries (O(nnz)).
Dense NumPy matrices allocate full n×n memory regardless of sparsity, which makes them much heavier in memory.
SciPy uses optimized CSR structures, but still has more overhead per entry than my simple tuple-based COO design.

---

## Observations

1. SciPy is much faster than my implementation, especially for multiply
2. My implementation is slow because it uses nested loop and linear search.
3. Sparse matrices save a lot more memory compared to dense Numpy arrays

---

## Conclusions
This experiment demonstrates the trade-off between time and space complexity. My COO implementation is memory efficient and easy to build, but significantly slower than the Python libraries. SciPy achieves the best performance using CSR format and low-level optimizations, while NumPy is fastest for dense operations but not suitable for sparse data.
---

## References
- SciPy CSR document
- Numpy document
