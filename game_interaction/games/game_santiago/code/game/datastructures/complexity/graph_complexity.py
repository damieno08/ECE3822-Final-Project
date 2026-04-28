"""
graph_complexity.py - Performance benchmarks for Graph

Author: Santiago Troya
Date:   04/27/2026
Lab:    Lab 7 - NPC Dialog with Graphs

Generates timing tables AND saves PNG charts to:
    code/game/datastructures/complexity/graphs/

Run with:
    cd code/game/datastructures/complexity
    python graph_complexity.py

Requires matplotlib:
    pip install matplotlib
"""

import sys
import os
import time
import random

# Make sure imports work from any working directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.graph import Graph

# -----------------------------------------------------------------------
# Output directory for charts
# -----------------------------------------------------------------------

GRAPHS_DIR = os.path.join(os.path.dirname(__file__), 'graphs')
os.makedirs(GRAPHS_DIR, exist_ok=True)

# -----------------------------------------------------------------------
# Benchmark configuration
# -----------------------------------------------------------------------

SIZES         = [100, 500, 1000]
EDGE_FACTOR   = 3       # directed edges per node
HAS_NODE_Q    = 500     # random has_node queries
SP_QUERIES    = 20      # random shortest_path pairs
REPEAT        = 3       # best-of-N runs

# -----------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------

def make_random_graph(n):
    g = Graph(directed=True)
    for i in range(n):
        g.add_node(i)
    target = n * EDGE_FACTOR
    added  = 0
    while added < target:
        a = random.randint(0, n - 1)
        b = random.randint(0, n - 1)
        if a != b and not g.has_edge(a, b):
            g.add_edge(a, b)
            added += 1
    return g


def time_it(fn):
    best = float('inf')
    for _ in range(REPEAT):
        t0   = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - t0)
    return best * 1000   # milliseconds


# -----------------------------------------------------------------------
# Run benchmarks
# -----------------------------------------------------------------------

print("Running benchmarks...\n")

rows = []
for n in SIZES:
    row = {"n": n}

    # Build
    row["build"]    = time_it(lambda n=n: make_random_graph(n))

    # Use a single graph for the remaining tests
    g     = make_random_graph(n)
    nodes = g.nodes()

    # has_node
    queries = [random.randint(0, n * 2) for _ in range(HAS_NODE_Q)]
    row["has_node"] = time_it(lambda: [g.has_node(q) for q in queries])

    # BFS
    start = nodes[0]
    row["bfs"]      = time_it(lambda: g.bfs(start))

    # DFS
    row["dfs"]      = time_it(lambda: g.dfs(start))

    # shortest_path
    pairs = [(random.choice(nodes), random.choice(nodes)) for _ in range(SP_QUERIES)]
    row["sp"]       = time_it(lambda: [g.shortest_path(a, b) for a, b in pairs])

    rows.append(row)
    print(f"  n={n} done")

# -----------------------------------------------------------------------
# Print results table
# -----------------------------------------------------------------------

COLS   = ["build", "has_node", "bfs", "dfs", "sp"]
LABELS = ["Build", "has_node", "BFS", "DFS", "ShortestPath"]

header = f"{'Nodes':>6} | " + " | ".join(f"{l:>14}" for l in LABELS)
sep    = "-" * len(header)

print("\n" + "=" * len(header))
print("Graph Performance Benchmark  (best of 3 runs, times in ms)")
print(f"Edge factor: {EDGE_FACTOR}x  |  has_node queries: {HAS_NODE_Q}"
      f"  |  shortest_path pairs: {SP_QUERIES}")
print("=" * len(header))
print(header)
print(sep)
for r in rows:
    vals = " | ".join(f"{r[c]:>14.3f}" for c in COLS)
    print(f"{r['n']:>6} | {vals}")
print("=" * len(header))

# -----------------------------------------------------------------------
# Generate charts with matplotlib
# -----------------------------------------------------------------------

try:
    import matplotlib
    matplotlib.use("Agg")   # headless — no display required
    import matplotlib.pyplot as plt

    sizes = [r["n"] for r in rows]

    # --- 1. All operations on one chart ---
    fig, ax = plt.subplots(figsize=(9, 5))
    for col, label in zip(COLS, LABELS):
        ax.plot(sizes, [r[col] for r in rows], marker='o', label=label)
    ax.set_xlabel("Number of nodes")
    ax.set_ylabel("Time (ms)")
    ax.set_title("Graph operations vs. graph size")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    path = os.path.join(GRAPHS_DIR, "all_operations.png")
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nSaved: {path}")

    # --- 2. BFS vs DFS comparison ---
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(sizes, [r["bfs"] for r in rows], marker='o', label="BFS")
    ax.plot(sizes, [r["dfs"] for r in rows], marker='s', label="DFS")
    ax.set_xlabel("Number of nodes")
    ax.set_ylabel("Time (ms)")
    ax.set_title("BFS vs DFS traversal time")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    path = os.path.join(GRAPHS_DIR, "bfs_vs_dfs.png")
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {path}")

    print(f"\nCharts saved to:  {GRAPHS_DIR}/")

except ImportError:
    print("\nmatplotlib not found -- install it to generate charts:")
    print("    pip install matplotlib")
