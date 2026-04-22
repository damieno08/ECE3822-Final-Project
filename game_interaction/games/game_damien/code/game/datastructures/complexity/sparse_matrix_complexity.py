import time
import random
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import sys

from scipy.sparse import csr_matrix

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from datastructures.sparse_matrix import SparseMatrix


def generate_sparse_data(n, density=0.05):
    nnz = int(n * n * density)
    data = set()

    while len(data) < nnz:
        r = random.randint(0, n - 1)
        c = random.randint(0, n - 1)
        v = random.randint(1, 100)
        data.add((r, c, v))

    return list(data)


# ---------------- SPACE ESTIMATION ----------------
def estimate_sparse_size(sm):
    size = sys.getsizeof(sm)
    items = sm.items()

    for i in range(len(items)):
        key, val = items[i]
        size += sys.getsizeof(key)
        size += sys.getsizeof(val)

    return size


def estimate_numpy_size(arr):
    return arr.nbytes


def estimate_scipy_size(sp):
    return sp.data.nbytes + sp.indices.nbytes + sp.indptr.nbytes


# ---------------- BENCHMARK ----------------
def benchmark_once(n):
    data = generate_sparse_data(n)

    # -------- Custom Sparse --------
    sm1 = SparseMatrix(n, n)
    sm2 = SparseMatrix(n, n)

    for r, c, v in data:
        sm1.set(r, c, v)
        sm2.set(c, r, v)

    start = time.perf_counter()
    sm1.multiply(sm2)
    sm_time = time.perf_counter() - start

    sm_space = estimate_sparse_size(sm1)

    # -------- NumPy Dense --------
    np1 = np.zeros((n, n))
    np2 = np.zeros((n, n))

    for r, c, v in data:
        np1[r][c] = v
        np2[c][r] = v

    start = time.perf_counter()
    np.dot(np1, np2)
    np_time = time.perf_counter() - start

    np_space = estimate_numpy_size(np1)

    # -------- SciPy CSR --------
    rows, cols, vals = zip(*data)
    sp1 = csr_matrix((vals, (rows, cols)), shape=(n, n))
    sp2 = csr_matrix((vals, (cols, rows)), shape=(n, n))

    start = time.perf_counter()
    sp1 @ sp2
    sp_time = time.perf_counter() - start

    sp_space = estimate_scipy_size(sp1)

    return sm_time, np_time, sp_time, sm_space, np_space, sp_space


def run_benchmarks():
    sizes = [50, 100, 150, 200]
    trials = 3

    time_results = {"sm": [], "np": [], "sp": []}
    space_results = {"sm": [], "np": [], "sp": []}

    print("\n=== TIME COMPLEXITY ===")
    print(f"{'Size':<10}{'Custom':<15}{'NumPy':<15}{'SciPy':<15}")

    for n in sizes:
        sm_t = np_t = sp_t = 0
        sm_s = np_s = sp_s = 0

        for _ in range(trials):
            sm_time, np_time, sp_time, sm_space, np_space, sp_space = benchmark_once(n)

            sm_t += sm_time
            np_t += np_time
            sp_t += sp_time

            sm_s += sm_space
            np_s += np_space
            sp_s += sp_space

        sm_t /= trials
        np_t /= trials
        sp_t /= trials

        sm_s /= trials
        np_s /= trials
        sp_s /= trials

        time_results["sm"].append(sm_t)
        time_results["np"].append(np_t)
        time_results["sp"].append(sp_t)

        space_results["sm"].append(sm_s)
        space_results["np"].append(np_s)
        space_results["sp"].append(sp_s)

        print(f"{n:<10}{sm_t:<15.6f}{np_t:<15.6f}{sp_t:<15.6f}")

    # ---------------- SPACE TABLE ----------------
    print("\n=== SPACE COMPLEXITY (bytes) ===")
    print(f"{'Size':<10}{'Custom':<15}{'NumPy':<15}{'SciPy':<15}")

    for i, n in enumerate(sizes):
        print(f"{n:<10}{space_results['sm'][i]:<15.0f}{space_results['np'][i]:<15.0f}{space_results['sp'][i]:<15.0f}")

    # ---------------- TIME GRAPH ----------------
    plt.figure()
    plt.plot(sizes, time_results["sm"], marker='o', label="Custom Sparse")
    plt.plot(sizes, time_results["np"], marker='s', label="NumPy Dense")
    plt.plot(sizes, time_results["sp"], marker='^', label="SciPy CSR")

    plt.xlabel("Matrix Size (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Time Complexity Comparison")
    plt.yscale("log")
    plt.legend()
    plt.grid(True)
    plt.savefig("time_complexity.png")

    # ---------------- SPACE GRAPH ----------------
    plt.figure()
    plt.plot(sizes, space_results["sm"], marker='o', label="Custom Sparse")
    plt.plot(sizes, space_results["np"], marker='s', label="NumPy Dense")
    plt.plot(sizes, space_results["sp"], marker='^', label="SciPy CSR")

    plt.xlabel("Matrix Size (n)")
    plt.ylabel("Memory (bytes)")
    plt.title("Space Complexity Comparison")
    plt.legend()
    plt.grid(True)
    plt.savefig("space_complexity.png")

    print("\nGraphs saved as:")
    print("- time_complexity.png")
    print("- space_complexity.png")


if __name__ == "__main__":
    run_benchmarks()