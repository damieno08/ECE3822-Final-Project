"""
_timer.py - Shared timing and graphing utilities for complexity tests.
Revision History:
    (ST) 05/05/2026 Create initial file
"""

import math
import os
import statistics
import time

GRAPHS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphs")

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    _HAS_MPL = True
except ImportError:
    _HAS_MPL = False

# Palette — colour-blind-friendly tones
_PALETTE = [
    "#1f77b4", "#d62728", "#2ca02c", "#ff7f0e",
    "#9467bd", "#8c564b", "#e377c2", "#17becf",
]

# Theoretical complexity functions (unnormalised)
_THEORY = {
    "O(1)":       lambda n: 1.0,
    "O(log n)":   lambda n: math.log2(max(n, 2)),
    "O(n)":       lambda n: float(n),
    "O(n log n)": lambda n: n * math.log2(max(n, 2)),
    "O(n^2)":     lambda n: float(n * n),
}


# ── core helpers ──────────────────────────────────────────────────────────────

def bench(func, sizes, *, setup=None, reps=5):
    """
    Time func for each N in sizes.
    setup(N) -> tuple of args forwarded to func.
    Returns [(N, median_seconds), ...].
    """
    results = []
    for n in sizes:
        args = setup(n) if setup else ()
        times = []
        for _ in range(reps):
            start = time.perf_counter()
            func(*args)
            times.append(time.perf_counter() - start)
        results.append((n, statistics.median(times)))
    return results


def print_table(title, rows, expected=""):
    """Print a timing table with a ratio column showing empirical scaling."""
    print(f"\n{'-' * 58}")
    print(f"  {title}")
    if expected:
        print(f"  Expected complexity: {expected}")
    print(f"{'-' * 58}")
    print(f"  {'N':>10}  {'Time (s)':>12}  {'Ratio vs prev':>14}")
    print(f"  {'-'*10}  {'-'*12}  {'-'*14}")
    prev = None
    for n, t in rows:
        ratio = f"{t / prev:.2f}x" if prev else "         -"
        print(f"  {n:>10,}  {t:>12.6f}  {ratio:>14}")
        prev = t
    print()


# ── graphing ──────────────────────────────────────────────────────────────────

def save_plot(filename, title, series):
    """
    Render and save a complexity graph to complexity/graphs/<filename>.

    Parameters
    ----------
    filename : str
        Output PNG filename (e.g. "merge_sort.png").
    title : str
        Graph title shown at the top.
    series : list[dict]
        Each dict describes one curve:
          "label"      : str            -- legend entry
          "rows"       : [(N, t), ...]  -- measured data
          "complexity" : str or None    -- e.g. "O(n log n)"; draws a scaled
                                           theoretical dashed overlay
          "marker"     : str            -- optional matplotlib marker (default "o")
    """
    if not _HAS_MPL:
        print("  [matplotlib not installed -- skipping graph]")
        return

    os.makedirs(GRAPHS_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#fafafa")
    ax.set_facecolor("#ffffff")

    for i, s in enumerate(series):
        rows  = s["rows"]
        ns    = [r[0] for r in rows]
        ts    = [r[1] for r in rows]
        color = _PALETTE[i % len(_PALETTE)]
        mark  = s.get("marker", "o")

        # Measured data
        ax.plot(ns, ts, marker=mark, color=color, label=s["label"],
                linewidth=2.2, markersize=7, zorder=3)

        # Theoretical overlay — scale so the curve passes through the median point
        cname = s.get("complexity")
        if cname and cname in _THEORY and len(ns) > 1:
            fn  = _THEORY[cname]
            mid = len(ns) // 2
            f_mid = fn(ns[mid])
            if f_mid != 0:
                scale   = ts[mid] / f_mid
                theory  = [fn(n) * scale for n in ns]
                ax.plot(ns, theory, linestyle="--", color=color, alpha=0.5,
                        linewidth=1.6, label=f"{cname} fit", zorder=2)

    # Axes — log-log shows complexity class as slope
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"{int(x):,}" if x >= 1 else f"{x:.2g}")
    )

    ax.set_xlabel("Input Size  N", fontsize=12, labelpad=8)
    ax.set_ylabel("Time  (seconds)", fontsize=12, labelpad=8)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=14)
    ax.legend(fontsize=9, loc="upper left", framealpha=0.85)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.4, color="#888")
    for spine in ax.spines.values():
        spine.set_linewidth(0.8)
        spine.set_color("#cccccc")

    plt.tight_layout()
    outpath = os.path.join(GRAPHS_DIR, filename)
    plt.savefig(outpath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Graph -> graphs/{filename}")
