# Sparse Matrix Complexity Analysis

**Name:** [Your Name]
**Date:** [Date]
**Implementation:** [DOK / COO / CSR — circle one]

---

## Overview

Describe your implementation choice and why you chose it.  For example:
- What backing data structure does it use?
- Why is it appropriate for the tile-map use case?
- What trade-offs does it make compared to the other options?

---

## Time Complexity

Fill in the `?` cells after analysing your implementation.

| Operation | Your SparseMatrix | scipy sparse (CSR) | numpy dense |
|-----------|-------------------|--------------------|-------------|
| `set(r, c, v)` | O(?) | O(nnz) amortised | O(1) |
| `get(r, c)` | O(?) | O(log nnz) | O(1) |
| `items()` iteration | O(?) | O(nnz) | O(n²) |
| `multiply(other)` | O(?) | O(nnz²/n) | O(n³) |

*nnz = number of non-zero entries, n = matrix dimension side length*

Explain your reasoning for each `?` in a sentence or two.

---

## Benchmark Results

Run `sparse_matrix_complexity.py` and paste the output here:

```
(paste timing table here)
```

---

## Space Complexity

| Representation | Space Used |
|----------------|-----------|
| Dense n×n      | O(n²)     |
| Your sparse    | O(?)      |

At what density (percentage of non-zero entries) does your sparse matrix
use *more* memory than a dense matrix?  Show your reasoning.

---

## Observations

1. How does your implementation compare to scipy in terms of speed?
2. When is a sparse representation faster than a dense one?
3. Was the overhead per entry (your structure vs. numpy array) noticeable?

---

## Conclusions

Write 2–3 sentences summarising what you learned about sparse data structures
from this experiment.

---

## References

List any resources (textbooks, websites, papers) you used.
