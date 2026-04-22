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

Author: Santiago Troya
Date:   04/10/2026
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
    print("scipy/numpy not installed — run: pip install scipy numpy")
    sys.exit(1)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.sparse_matrix import SparseMatrix
import matplotlib.pyplot as plt


def _random_entries(size, nnz, seed=42):
    """Return a list of (row, col, value) tuples with no duplicate positions."""
    rng = random.Random(seed)
    entries = set()
    while len(entries) < nnz:
        entries.add((rng.randint(0, size - 1), rng.randint(0, size - 1)))
    return [(r, c, rng.randint(1, 100)) for r, c in entries]


def _sp(entries, size):
    """Build a scipy CSR matrix from a list of (row, col, value) entries."""
    r, c, v = zip(*entries) if entries else ([], [], [])
    return csr_matrix((np.array(v), (np.array(r), np.array(c))), shape=(size, size))


def _np(entries, size, default=0):
    """Build a numpy dense matrix from a list of (row, col, value) entries."""
    m = np.full((size, size), default, dtype=np.int32)
    for r, c, v in entries:
        m[r, c] = v
    return m


def _time(fn):
    """Return the wall-clock time (seconds) to run fn()."""
    t0 = time.perf_counter()
    fn()
    return time.perf_counter() - t0


def measure_build(sizes, density=0.01):
    """Time building each matrix type via repeated set() / constructor calls."""
    dok_t, sci_t, np_t = [], [], []
    for size in sizes:
        entries = _random_entries(size, max(1, int(size * size * density)))
        sm = SparseMatrix(rows=size, cols=size, default=-1)
        dok_t.append(_time(lambda: [sm.set(r, c, v) for r, c, v in entries]))
        sci_t.append(_time(lambda: _sp(entries, size)))
        np_t.append(_time(lambda: _np(entries, size, default=-1)))
    return dok_t, sci_t, np_t


def measure_get(sizes, density=0.01, num_queries=1000):
    """Time 1000 random get() / index lookups on each matrix type."""
    dok_t, sci_t, np_t = [], [], []
    rng = random.Random(0)
    for size in sizes:
        entries = _random_entries(size, max(1, int(size * size * density)))
        queries = [(rng.randint(0, size - 1), rng.randint(0, size - 1)) for _ in range(num_queries)]
        sm = SparseMatrix(rows=size, cols=size, default=-1)
        for r, c, v in entries:
            sm.set(r, c, v)
        sp  = _sp(entries, size)
        mat = _np(entries, size, default=-1)
        dok_t.append(_time(lambda: [sm.get(r, c) for r, c in queries]))
        sci_t.append(_time(lambda: [sp[r, c]     for r, c in queries]))
        np_t.append(_time(lambda: [mat[r, c]     for r, c in queries]))
    return dok_t, sci_t, np_t


def measure_iteration(sizes, density=0.01):
    """Time a full iteration over all stored entries."""
    dok_t, sci_t, np_t = [], [], []
    for size in sizes:
        entries = _random_entries(size, max(1, int(size * size * density)))
        sm = SparseMatrix(rows=size, cols=size, default=-1)
        for r, c, v in entries:
            sm.set(r, c, v)
        sp  = _sp(entries, size)
        mat = _np(entries, size, default=-1)
        dok_t.append(_time(lambda: list(sm.items())))
        sci_t.append(_time(lambda: list(zip(sp.tocoo().row, sp.tocoo().col, sp.tocoo().data))))
        np_t.append(_time(lambda: list(zip(*np.where(mat != -1)))))
    return dok_t, sci_t, np_t


def measure_multiply(sizes, density=0.01):
    """Time matrix multiplication for each implementation."""
    dok_t, sci_t, np_t = [], [], []
    for size in sizes:
        ea = _random_entries(size, max(1, int(size * size * density)), seed=1)
        eb = _random_entries(size, max(1, int(size * size * density)), seed=2)
        a = SparseMatrix(rows=size, cols=size, default=0)
        b = SparseMatrix(rows=size, cols=size, default=0)
        for r, c, v in ea:
            a.set(r, c, v)
        for r, c, v in eb:
            b.set(r, c, v)
        dok_t.append(_time(lambda: a.multiply(b)))
        sci_t.append(_time(lambda: _sp(ea, size).dot(_sp(eb, size))))
        np_t.append(_time(lambda: np.dot(_np(ea, size), _np(eb, size))))
    return dok_t, sci_t, np_t


def _print_table(op, sizes, dok, sci, npy):
    """Print timing results as a plain-text table (paste into the write-up)."""
    print(f"\n=== {op} ===")
    print(f"{'N':>8}  {'DOK (ours)':>14}  {'scipy CSR':>14}  {'numpy dense':>14}")
    for n, d, s, np_ in zip(sizes, dok, sci, npy):
        print(f"{n:>8}  {d:>14.6f}  {s:>14.6f}  {np_:>14.6f}")


def run_complexity_analysis():
    sizes     = [400, 800, 1600, 3200, 6400]
    mul_sizes = [10, 20, 30, 40, 50]

    results = {
        "Build":     (sizes,     measure_build(sizes)),
        "Get":       (sizes,     measure_get(sizes)),
        "Iteration": (sizes,     measure_iteration(sizes)),
        "Multiply":  (mul_sizes, measure_multiply(mul_sizes)),
    }

    for op, (sz, (dok, sci, npy)) in results.items():
        _print_table(op, sz, dok, sci, npy)

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle("SparseMatrix: DOK vs scipy vs numpy")
    for ax, (op, (sz, (dok, sci, npy))) in zip(axes.flat, results.items()):
        ax.plot(sz, dok, 'o-', label="DOK (ours)")
        ax.plot(sz, sci, 's-', label="scipy CSR")
        ax.plot(sz, npy, '^-', label="numpy dense")
        ax.set_title(op)
        ax.set_xlabel("N")
        ax.set_ylabel("time (s)")
        ax.legend(fontsize=9)
        ax.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig('complexity.png')
    plt.show()


if __name__ == "__main__":
    run_complexity_analysis()
