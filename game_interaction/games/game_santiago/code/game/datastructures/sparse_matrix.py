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

Implementation chosen: Option A — DOK backed by HashTable.

Author: Santiago Troya
Date:   04/10/2026
Lab:    Lab 6 - Sparse World Map
"""

from game_interaction.games.game_santiago.code.game.datastructures.hash_table import HashTable


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

class SparseMatrix(SparseMatrixBase):
    """
    Sparse matrix using the DOK (Dictionary of Keys) representation.

    """

    def __init__(self, rows=None, cols=None, default=0):
        """
        Initialize an empty sparse matrix.

        Args:
            rows: Row bound, or None for unbounded.
            cols: Column bound, or None for unbounded.
            default: Value for cells that have not been set.
        """
        super().__init__(rows, cols, default)
        # DOK backing store: maps (row, col) -> value via HashTable
        self._data = HashTable(initial_capacity=64)

    def set(self, row, col, value):
        """
        Store value at position (row, col).

        Args:
            row   (int): Row index.
            col   (int): Column index.
            value (any): Value to store.
        """
        key = (row, col)
        if value == self.default:
            # Removing a stored entry keeps the matrix consistent
            if key in self._data:
                self._data.delete(key)
        else:
            self._data.set(key, value)

    def get(self, row, col):
        """
        Return the value at (row, col), or the default if not set.

        Args:
            row (int): Row index.
            col (int): Column index.

        Returns:
            The stored value, or self.default if the cell is empty.
        """
        return self._data.get((row, col), self.default)

    def items(self):
        """
        Yield all explicitly stored (position, value) pairs.

        """
        for key, value in self._data.items():
            yield key, value

    def __len__(self):
        """
        Return the number of non-default entries stored in the matrix.

        """
        return len(self._data)

    def multiply(self, other):
        """
        Compute and return the matrix product self * other.

        Args:
            other (SparseMatrix): Right-hand operand.

        Returns:
            SparseMatrix: A new sparse matrix representing self * other.
        """
        result = SparseMatrix(self.rows, other.cols, default=0)

        for (i, j), a in self.items():
            for (r, k), b in other.items():
                if r == j:  # inner indices must match
                    current = result.get(i, k)
                    result.set(i, k, current + a * b)

        return result

    def __str__(self):
        """
        Returns:
            str: A one-line summary string.
        """
        rows_str = str(self.rows) if self.rows is not None else "?"
        cols_str = str(self.cols) if self.cols is not None else "?"
        return (
            f"SparseMatrix(DOK) [{rows_str} x {cols_str}]  "
            f"nnz={len(self)}  default={self.default!r}"
        )
