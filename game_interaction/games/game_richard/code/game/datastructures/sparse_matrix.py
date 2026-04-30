"""
sparse_matrix.py - Sparse Matrix implementation

A sparse matrix stores only non-default entries, saving memory when most
cells share the same value (like -1 in a tile map).

Choose one of three backing representations:

  Option A — DOK (Dictionary of Keys): {(row, col): value}
    Requires implementing HashTable in hash_table.py.
    Do not use Python's built-in dict or set.

  Option B — COO (Coordinate List): list of (row, col, value) triples
    Use your ArrayList from Lab 3. Do not use Python's built-in list.

  Option C — CSR (Compressed Sparse Row): three parallel arrays
    row_ptr, col_idx, values. Most efficient for row-wise access.

All three options must satisfy the same interface.

Author: Richard Lin
Date:   4/12/26
Lab:    Lab 6 - Sparse World Map
"""


# =============================================================================
# Do not modify SparseMatrixBase.
# =============================================================================

class SparseMatrixBase:
    """Interface definition. Your SparseMatrix must inherit from this."""

    def __init__(self, rows=None, cols=None, default=0):
        self.rows    = rows
        self.cols    = cols
        self.default = default

    def set(self, row, col, value):
        raise NotImplementedError

    def get(self, row, col):
        raise NotImplementedError

    def items(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def multiply(self, other):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


# =============================================================================
# Your implementation goes here.
# =============================================================================

from datastructures.array import ArrayList

class SparseMatrix(SparseMatrixBase):

    def __init__(self, rows=None, cols=None, default=0):
        super().__init__(rows, cols, default)
        # TODO: initialize your backing data structure
        self.data = ArrayList()

    def set(self, row, col, value):
        # TODO
        i = 0
        while i < len(self.data):
            r, c, v = self.data[i]

            if r == row and c == col:
                if value == self.default:
                    self.data.pop(i)
                    return
                else:
                    self.data[i] = (row, col, value)
                    return

            i += 1

        if value != self.default:
            self.data.append((row, col, value))


    def get(self, row, col):
        # TODO
        for i in range(len(self.data)):
            r, c, v = self.data[i]
            if r == row and c == col:
                return v
            
        return self.default

    def items(self):
        # TODO
        for i in range(len(self.data)):
            r, c, v = self.data[i]
            yield ((r, c), v)

    def __len__(self):
        # TODO
        return len(self.data)

    def multiply(self, other):
        # TODO
        result = SparseMatrix(self.rows, other.cols, self.default)

        for i in range(len(self.data)):
            r1, c1, v1 = self.data[i]

            for j in range(len(other.data)):
                r2, c2, v2 = other.data[j]

                if c1 == r2:
                    current = result.get(r1, c2)
                    result.set(r1, c2, current + (v1 * v2))

        return result

    def __str__(self):
        # TODO
        return f"SparseMatrix(nnz={len(self)}, default={self.default})"
