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

Author: Tom Lipski
Date:   4/12/2026
Lab:    Lab 6 - Sparse World Map
"""

import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(parent_dir)  # Add parent directory to path
sys.path.insert(0, parent_dir)

from datastructures.hash_table import HashTable


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

    def __init__(self, rows=None, cols=None, default=0):
        super().__init__(rows, cols, default)
        # initialize sparse matrix
        self.sparse_matrix = HashTable()
        
        # DONE: initialize your backing data structure

    def set(self, row, col, value):
        # set value in sparse matrix if value is not equal to default
        if(value == self.default):
            self.sparse_matrix.delete((row, col))
        else:
            self.sparse_matrix.set((row,col),value)
        
        # DONE

    def get(self, row, col):
        # return value based on tuple passed in
        #return self.sparse_matrix.get((row,col))

        val = self.sparse_matrix.get((row, col))

        return val if val is not None else self.default
        
        # DONE

    def items(self):
        # return items of sparse matrix
        return self.sparse_matrix.items()
        # DONE

    def __len__(self):
        # return length of sparse matrix
        return self.sparse_matrix.__len__()
        # DONE

    def multiply(self, other):
        """
        Multiply sparse matrix by other matrix, using only entries where ones are present. 
        """
        # check dimensions
        if(self.cols != other.rows):
            raise ValueError("Dimensions don't match.")

        # Create matrix to store result
        result = SparseMatrix(rows=self.rows, cols=other.cols, default=self.default)

        b_rows = {}
        for entry in other.items():
            # Based on your previous code, entry is likely [(row, col), value]
            (k_row, j_col), val = entry[0], entry[1]
            if k_row not in b_rows:
                b_rows[k_row] = []
            b_rows[k_row].append((j_col, val))

        # 2. Iterate through Matrix A
        for entry_a in self.items():
            (i, k), val1 = entry_a[0], entry_a[1]
            
            # 3. Only look at the specific rows in B that match our current column 'k'
            if k in b_rows:
                for j, val2 in b_rows[k]:
                    current = result.get(i, j)
                    result.set(i, j, current + (val1 * val2))        

        return result
        
        # DONE

    def __str__(self):
        """
        Return string representation of sparse matrix.
        """

        output = ""
        for r in range(self.rows):
            row_str = "|"
            for c in range(self.cols):
                val = self.get(r, c)
                if val is None:
                    val = self.default
                row_str += f" {val:>4} "
            output += row_str + "|\n"
        return output
        
        # DONE
