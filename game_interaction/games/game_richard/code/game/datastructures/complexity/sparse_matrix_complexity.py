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

Author: Richard Lin
Date:   4/15/26
Lab:    Lab 6 - Sparse World Map
"""

import time
import random
import sys
import os
import tracemalloc

from scipy.sparse import csr_matrix
import numpy as np


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.sparse_matrix import SparseMatrix
import matplotlib.pyplot as plt

SIZE = 100
ENTRIES = 1000
GETS = 3000

def test_custom():
    m = SparseMatrix()

    start = time.perf_counter()
    for _ in range(ENTRIES):
        r = random.randint(0, SIZE - 1)
        c = random.randint(0, SIZE - 1)
        m.set(r, c, 1)
    build = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(GETS):
        r = random.randint(0, SIZE - 1)
        c = random.randint(0, SIZE - 1)
        m.get(r, c)
    get = time.perf_counter() - start

    start = time.perf_counter()
    list(m.items())
    items = time.perf_counter() - start

    start = time.perf_counter()
    m.multiply(m)
    mult = time.perf_counter() - start

    print("\nCUSTOM")
    print("Build:", build)
    print("Get:", get)
    print("Items:", items)
    print("Multiply:", mult)

    return build, get, items, mult

def test_scipy():
    rows, cols, data = [], [], []

    start = time.perf_counter()
    for _ in range(ENTRIES):
        rows.append(random.randint(0, SIZE - 1))
        cols.append(random.randint(0, SIZE - 1))
        data.append(1)

    m = csr_matrix((data, (rows, cols)), shape=(SIZE, SIZE))
    build = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(GETS):
        r = random.randint(0, SIZE - 1)
        c = random.randint(0, SIZE - 1)
        _ = m[r, c]
    get = time.perf_counter() - start

    start = time.perf_counter()
    m.nonzero()
    items = time.perf_counter() - start

    start = time.perf_counter()
    m @ m
    mult = time.perf_counter() - start

    print("\nSCIPY")
    print("Build:", build)
    print("Get:", get)
    print("Items:", items)
    print("Multiply:", mult)

    return build, get, items, mult

def test_numpy():
    start = time.perf_counter()
    m = np.zeros((SIZE, SIZE))

    for _ in range(ENTRIES):
        r = random.randint(0, SIZE - 1)
        c = random.randint(0, SIZE - 1)
        m[r][c] = 1

    build = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(GETS):
        r = random.randint(0, SIZE - 1)
        c = random.randint(0, SIZE - 1)
        _ = m[r][c]
    get = time.perf_counter() - start

    start = time.perf_counter()
    np.nonzero(m)
    items = time.perf_counter() - start

    start = time.perf_counter()
    m @ m
    mult = time.perf_counter() - start

    print("\nNUMPY")
    print("Build:", build)
    print("Get:", get)
    print("Items:", items)
    print("Multiply:", mult)

    return build, get, items, mult

def test_space_custom():
    m = SparseMatrix()

    tracemalloc.start()

    for _ in range(ENTRIES):
        m.set(random.randint(0, SIZE - 1), random.randint(0, SIZE - 1), 1)

    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\nCUSTOM MEMORY:", peak)
    return peak


def test_space_scipy():
    tracemalloc.start()

    rows, cols, data = [], [], []

    for _ in range(ENTRIES):
        rows.append(random.randint(0, SIZE - 1))
        cols.append(random.randint(0, SIZE - 1))
        data.append(1)

    m = csr_matrix((data, (rows, cols)), shape=(SIZE, SIZE))

    _ = m.nnz

    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("SCIPY MEMORY:", peak)
    return peak


def test_space_numpy():
    tracemalloc.start()

    m = np.zeros((SIZE, SIZE))

    for _ in range(ENTRIES):
        m[random.randint(0, SIZE - 1)][random.randint(0, SIZE - 1)] = 1

    _ = m.shape

    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("NUMPY MEMORY:", peak)
    return peak

def plot_times(custom, scipy, numpy):
    labels = ["Build", "Get", "Items", "Multiply"]
    x = range(len(labels))

    plt.figure()
    plt.plot(x, custom, "o-", label="Custom")
    plt.plot(x, scipy, "o-", label="SciPy")
    plt.plot(x, numpy, "o-", label="NumPy")

    plt.xticks(x, labels)
    plt.ylabel("Time (s)")
    plt.title("Time Complexity Comparison")
    plt.legend()
    plt.grid()
    plt.show()


def plot_memory(mem):
    labels = ["Custom", "SciPy", "NumPy"]

    plt.figure()
    plt.bar(labels, mem)
    plt.title("Memory Usage Comparison")
    plt.ylabel("Peak Memory (bytes)")
    plt.grid()
    plt.show()

def main():

    custom = test_custom()
    scipy = test_scipy()
    numpy = test_numpy()

    mem_custom = test_space_custom()
    mem_scipy = test_space_scipy()
    mem_numpy = test_space_numpy()

    plot_times(custom, scipy, numpy)
    plot_memory([mem_custom, mem_scipy, mem_numpy])


if __name__ == "__main__":
    main()