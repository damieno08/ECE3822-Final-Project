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

Author: Damien Ortiz
Date:   04/10/2026
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

from datastructures.hash_table import HashTable

class SparseMatrix(SparseMatrixBase):

    def __init__(self, rows=None, cols=None, default=0):
        super().__init__(rows, cols, default)
        # Dictionary of Keys: HashTable maps (row, col) -> value
        self._data = HashTable()

    def set(self, row, col, value):
        """Sets the value at (row, col). Removes entry if value is default."""
        if value == self.default:
            self._data.delete((row, col))
        else:
            self._data.set((row, col), value)

    def get(self, row, col):
        """Returns the value at (row, col) or the default if not stored."""
        return self._data.get((row, col), self.default)

    def items(self):
        """Returns the internal HashTable's items (key-value pairs)."""
        return self._data.items()

    def __len__(self):
        """Returns the number of non-default elements stored."""
        return len(self._data)

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Dimensions mismatch for matrix multiplication.")

        result = SparseMatrix(rows=self.rows, cols=other.cols, default=self.default)

        # Better iteration for custom ArrayLists
        a_items = self.items()
        b_items = other.items()

        for item_a in a_items:
            (r1, c1), val_a = item_a
            
            for item_b in b_items:
                (r2, c2), val_b = item_b
                
                if c1 == r2:
                    current_val = result.get(r1, c2)
                    result.set(r1, c2, current_val + (val_a * val_b))

        return result

    def __str__(self):
        """Returns a string representation of the non-default elements."""
        out = f"SparseMatrix({self.rows}x{self.cols}, default={self.default})\n"
        stored_items = self.items()
        for i in range(len(stored_items)):
            key, val = stored_items[i]
            out += f"  {key}: {val}\n"
        return out