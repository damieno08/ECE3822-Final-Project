"""
_timer.py - Shared timing and space-complexity utilities for complexity tests.

Revision History:
    (ST) 05/05/2026 Create initial file
"""

import math
import os
import statistics
import time
import tracemalloc

GRAPHS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphs")

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    _HAS_MPL = True
except ImportError:
    _HAS_MPL = False

_PALETTE = [
    "#1f77b4", "#d62728", "#2ca02c", "#ff7f0e",
    "#9467bd", "#8c564b", "#e377c2", "#17becf",
]

_THEORY = {
    "O(1)":       lambda n: 1.0,
    "O(log n)":   lambda n: math.log2(max(n, 2)),
    "O(n)":       lambda n: float(n),
    "O(n log n)": lambda n: n * math.log2(max(n, 2)),
    "O(n^2)":     lambda n: float(n * n),
}


# ── timing ────────────────────────────────────────────────────────────────────

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


def bench_space(func, sizes, *, setup=None):
    """
    Measure peak heap allocation (bytes) for func at each N.
    setup(N) -> tuple of args forwarded to func.
    Returns [(N, peak_bytes), ...].
    """
    results = []
    for n in sizes:
        args = setup(n) if setup else ()
        tracemalloc.start()
        func(*args)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        results.append((n, peak))
    return results


# ── display ───────────────────────────────────────────────────────────────────

def print_table(title, rows, expected="", unit="Time (s)"):
    print(f"\n{'-' * 60}")
    print(f"  {title}")
    if expected:
        print(f"  Expected: {expected}")
    print(f"{'-' * 60}")
    print(f"  {'N':>10}  {unit:>14}  {'Ratio vs prev':>14}")
    print(f"  {'-'*10}  {'-'*14}  {'-'*14}")
    prev = None
    for n, t in rows:
        ratio = f"{t / prev:.2f}x" if prev else "         -"
        print(f"  {n:>10,}  {t:>14.6f}  {ratio:>14}")
        prev = t
    print()


def print_space_table(title, rows, expected=""):
    kb_rows = [(n, b / 1024) for n, b in rows]
    print_table(title, kb_rows, expected=expected, unit="Peak mem (KB)")


# ── graphing ──────────────────────────────────────────────────────────────────

def save_plot(filename, title, series):
    """
    Save a log-log complexity graph to complexity/graphs/<filename>.

    series : list[dict] with keys:
        "label"      : str
        "rows"       : [(N, value), ...]
        "complexity" : str or None   -- draws a scaled theoretical overlay
        "marker"     : str           -- optional (default "o")
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

        ax.plot(ns, ts, marker=mark, color=color, label=s["label"],
                linewidth=2.2, markersize=7, zorder=3)

        cname = s.get("complexity")
        if cname and cname in _THEORY and len(ns) > 1:
            fn    = _THEORY[cname]
            mid   = len(ns) // 2
            f_mid = fn(ns[mid])
            if f_mid != 0:
                scale  = ts[mid] / f_mid
                theory = [fn(n) * scale for n in ns]
                ax.plot(ns, theory, linestyle="--", color=color, alpha=0.5,
                        linewidth=1.6, label=f"{cname} fit", zorder=2)

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


def save_space_plot(filename, title, series):
    """Same as save_plot but y-axis is labelled in KB."""
    kb_series = [
        {**s, "rows": [(n, b / 1024) for n, b in s["rows"]]}
        for s in series
    ]
    if not _HAS_MPL:
        print("  [matplotlib not installed -- skipping graph]")
        return

    os.makedirs(GRAPHS_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#fafafa")
    ax.set_facecolor("#ffffff")

    all_positive = any(t > 0 for s in kb_series for _, t in s["rows"])

    for i, s in enumerate(kb_series):
        rows  = s["rows"]
        ns    = [r[0] for r in rows]
        ts    = [r[1] for r in rows]
        color = _PALETTE[i % len(_PALETTE)]
        mark  = s.get("marker", "o")

        ax.plot(ns, ts, marker=mark, color=color, label=s["label"],
                linewidth=2.2, markersize=7, zorder=3)

        if all_positive:
            cname = s.get("complexity")
            if cname and cname in _THEORY and len(ns) > 1:
                fn    = _THEORY[cname]
                mid   = len(ns) // 2
                f_mid = fn(ns[mid])
                if f_mid != 0:
                    scale  = ts[mid] / f_mid
                    theory = [fn(n) * scale for n in ns]
                    ax.plot(ns, theory, linestyle="--", color=color, alpha=0.5,
                            linewidth=1.6, label=f"{cname} fit", zorder=2)

    ax.set_xscale("log")
    if all_positive:
        ax.set_yscale("log")
    else:
        ax.set_ylim(-0.5, 2)
        ax.axhline(y=0, color="#888", linestyle="--", linewidth=1, alpha=0.6)
        ax.text(0.5, 0.5, "O(1) -- no heap allocation measured\n(stack space not tracked by tracemalloc)",
                transform=ax.transAxes, ha="center", va="center",
                fontsize=11, color="#555555",
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#f0f0f0", alpha=0.8))
    ax.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"{int(x):,}" if x >= 1 else f"{x:.2g}")
    )
    ax.set_xlabel("Input Size  N", fontsize=12, labelpad=8)
    ax.set_ylabel("Peak Memory  (KB)", fontsize=12, labelpad=8)
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
