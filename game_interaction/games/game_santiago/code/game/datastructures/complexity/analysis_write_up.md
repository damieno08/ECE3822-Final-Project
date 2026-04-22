# Sparse Matrix Complexity Analysis

**Name:** Santiago Troya
**Date:** 04/10/2026
**Implementation:** [(DOK) / COO / CSR — circle one]

---

## Overview

Describe your implementation choice and why you chose it.  For example:
- What backing data structure does it use?
- Why is it appropriate for the tile-map use case?
- What trade-offs does it make compared to the other options?

I chose the DOK representation. Each of the non-default entries are stored as a (row,col) tuple key mapped to its value inside of a the implemented hashtable datastructure. 

it is appropiate to use this datastructure for this case becuase most of the map is not going to be occupied, which means that we can represent it as a sparse matrix. 

Compared to the CSR for bulk operations, DOK is slower. But as a tradeoff for these bulk cases, the computation of the multiplication of matrices is faster.

---

## Time Complexity

Fill in the `?` cells after analysing your implementation.

| Operation | Your SparseMatrix | scipy sparse (CSR) | numpy dense |
|-----------|-------------------|--------------------|-------------|
| `set(r, c, v)` | O(1) avg | O(nnz) amortised | O(1) |
| `get(r, c)` | O(1) avg | O(log nnz) | O(1) |
| `items()` iteration | O(nnz) | O(nnz) | O(n^2) |
| `multiply(other)` | O(nnz^2) | O(nnz^2/n) | O(n^3) |

*nnz = number of non-zero entries, n = matrix dimension side length*

Explain your reasoning for each `?` in a sentence or two.

For set, ammortized O(1) because it computes a bucket index in O(1) and appends or updates in the chain. It occasionally resizes, but it is O(1) ammortized.

For get, O(1) The same hash lookup ends up in the same bucket. 

For items() O(nnz) iterating the hashtable in only the occupied chain entries.

multiply() O(nnz^2) the implementation computes all of the non zero elements.
 
---

## Benchmark Results

Run `sparse_matrix_complexity.py` and paste the output here:

```

=== Build ===
       N      DOK (ours)       scipy CSR     numpy dense
     400        0.014887        0.001330        0.000634
     800        0.076229        0.004350        0.002180
    1600        0.196061        0.009850        0.006727
    3200        0.955093        0.033019        0.023033
    6400        3.382979        0.182041        0.140945
 
=== Get ===
       N      DOK (ours)       scipy CSR     numpy dense
     400        0.000558        0.007543        0.000106
     800        0.000452        0.010191        0.000118
    1600        0.001285        0.017255        0.000282
    3200        0.001154        0.009753        0.000179
    6400        0.001389        0.008083        0.000180
 
=== Iteration ===
       N      DOK (ours)       scipy CSR     numpy dense
     400        0.001683        0.000742        0.001022
     800        0.005607        0.001995        0.003248
    1600        0.028574        0.003922        0.008424
    3200        0.062654        0.018958        0.062288
    6400        0.335116        0.103408        0.259203
 
=== Multiply ===
       N      DOK (ours)       scipy CSR     numpy dense
      10        0.000045        0.000625        0.000060
      20        0.000090        0.000401        0.000029
      30        0.000204        0.000422        0.000067
      40        0.000398        0.000447        0.000127
      50        0.000852        0.000548        0.000188

```

---

## Space Complexity

| Representation | Space Used |
|----------------|-----------|
| Dense n×n      | O(n²)     |
| Your sparse    | O(nnz)      |

At what density (percentage of non-zero entries) does your sparse matrix
use *more* memory than a dense matrix?  Show your reasoning.

---

## Observations

1. How does your implementation compare to scipy in terms of speed?
2. When is a sparse representation faster than a dense one?
3. Was the overhead per entry (your structure vs. numpy array) noticeable?

My implementation is 10-20x slower for build, and 3-10x slower for iteration, for get is 5-12x faster.

For Build and Iteration at 1 % density, both DOK and scipy avoid touching the ~99 % empty cells, so they scale with nnz rather than n^2.

Yes, it is very noticeable. At N=6400 DOK Build takes 3.38 s versus 0.18 s for scipy.

---

## Conclusions

Write 2–3 sentences summarising what you learned about sparse data structures
from this experiment.

DOK is great for the implementation of sparse matrices, it has a O(1) ammortized hash table lookup. However, the results demonstrates that the overhead is significant in comparison to the python level datastructure.

---

## References

List any resources (textbooks, websites, papers) you used.
https://docs.scipy.org/doc/scipy/reference/sparse.html
