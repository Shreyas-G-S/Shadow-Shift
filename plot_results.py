#!/usr/bin/env python3
"""
Plot figures from trials CSV (e.g. results.csv).

Usage:
  python plot_results.py results.csv
  python plot_results.py results.csv --out my_figures

Requires: matplotlib (see requirements.txt)
"""
import argparse
import csv
import os
from collections import Counter
from typing import Any, Dict, List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def read_rows(path: str) -> List[Dict[str, Any]]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def _float(row: Dict[str, str], key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key, default))
    except (TypeError, ValueError):
        return default


def _int(row: Dict[str, str], key: str, default: int = 0) -> int:
    try:
        return int(row.get(key, default))
    except (TypeError, ValueError):
        return default


def plot_outcome_bar(rows: List[Dict[str, Any]], out_dir: str) -> None:
    counts = Counter(r.get("outcome", "").strip() for r in rows)
    labels = [k for k in ("win", "lose", "timeout") if counts.get(k, 0) > 0 or k in counts]
    if not labels:
        labels = sorted(counts.keys())
    values = [counts.get(l, 0) for l in labels]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(labels, values, color=["#4caf50", "#f44336", "#9e9e9e"][: len(labels)])
    ax.set_ylabel("Episodes")
    ax.set_title("Outcomes")
    for i, v in enumerate(values):
        ax.text(i, v + 0.5, str(v), ha="center", fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "outcomes.png"), dpi=150)
    plt.close(fig)


def plot_win_kind(rows: List[Dict[str, Any]], out_dir: str) -> None:
    if not rows or "win_kind" not in rows[0]:
        return
    wins = [r for r in rows if r.get("outcome") == "win"]
    if not wins:
        return
    ck = Counter((r.get("win_kind") or "").strip() or "unknown" for r in wins)
    labels = list(ck.keys())
    values = [ck[k] for k in labels]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(labels, values, color=["#81c784", "#ffd54f", "#90a4ae"][: len(labels)])
    ax.set_ylabel("Wins")
    ax.set_title("Win type (among wins only)")
    for i, v in enumerate(values):
        ax.text(i, v + 0.3, str(v), ha="center", fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "win_kinds.png"), dpi=150)
    plt.close(fig)


def plot_time_histogram(rows: List[Dict[str, Any]], out_dir: str) -> None:
    times = [_float(r, "time_sec") for r in rows]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(times, bins=min(20, max(5, len(set(times)))), color="#5c6bc0", edgecolor="white")
    ax.set_xlabel("time_sec (episode end)")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of episode duration")
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "time_distribution.png"), dpi=150)
    plt.close(fig)


def plot_time_by_outcome(rows: List[Dict[str, Any]], out_dir: str) -> None:
    lose_t = [_float(r, "time_sec") for r in rows if r.get("outcome") == "lose"]
    win_t = [_float(r, "time_sec") for r in rows if r.get("outcome") == "win"]
    fig, ax = plt.subplots(figsize=(7, 4))
    if lose_t:
        ax.hist(
            lose_t,
            bins=min(15, max(4, len(set(lose_t)))),
            alpha=0.75,
            label="lose",
            color="#ef5350",
            edgecolor="white",
        )
    if win_t:
        ax.hist(
            win_t,
            bins=min(15, max(4, len(set(win_t)))),
            alpha=0.65,
            label="win",
            color="#66bb6a",
            edgecolor="white",
        )
    ax.set_xlabel("time_sec")
    ax.set_ylabel("Count")
    ax.set_title("Episode duration by outcome")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "time_by_outcome.png"), dpi=150)
    plt.close(fig)


def plot_episode_timeline(rows: List[Dict[str, Any]], out_dir: str) -> None:
    xs = [_int(r, "episode") for r in rows]
    ts = [_float(r, "time_sec") for r in rows]
    colors = []
    for r in rows:
        o = r.get("outcome", "")
        if o == "win":
            colors.append("#2e7d32")
        elif o == "lose":
            colors.append("#c62828")
        else:
            colors.append("#757575")
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.scatter(xs, ts, c=colors, s=36, alpha=0.85, edgecolors="k", linewidths=0.3)
    ax.set_xlabel("Episode")
    ax.set_ylabel("time_sec")
    ax.set_title("Episode index vs duration")
    from matplotlib.lines import Line2D

    legend_elems = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#2e7d32", markersize=8, label="win"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#c62828", markersize=8, label="lose"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#757575", markersize=8, label="other"),
    ]
    ax.legend(handles=legend_elems, loc="best")
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "episode_timeline.png"), dpi=150)
    plt.close(fig)


def plot_steps(rows: List[Dict[str, Any]], out_dir: str) -> None:
    if not rows or "steps" not in rows[0]:
        return
    steps = [_int(r, "steps") for r in rows]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(steps, bins=min(20, max(5, len(set(steps)))), color="#7e57c2", edgecolor="white")
    ax.set_xlabel("steps")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of simulation steps per episode")
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "steps_distribution.png"), dpi=150)
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser(description="Plot figures from trials CSV")
    p.add_argument("csv", nargs="?", default="results.csv", help="path to CSV")
    p.add_argument("--out", default="figures", help="output directory for PNGs")
    args = p.parse_args()

    if not os.path.isfile(args.csv):
        raise SystemExit(f"File not found: {args.csv}")

    rows = read_rows(args.csv)
    if not rows:
        raise SystemExit("CSV has no data rows")

    os.makedirs(args.out, exist_ok=True)

    plot_outcome_bar(rows, args.out)
    plot_win_kind(rows, args.out)
    plot_time_histogram(rows, args.out)
    plot_time_by_outcome(rows, args.out)
    plot_episode_timeline(rows, args.out)
    plot_steps(rows, args.out)

    print(f"Wrote figures to {os.path.abspath(args.out)}/")
    for name in sorted(os.listdir(args.out)):
        if name.endswith(".png"):
            print(f"  - {name}")


if __name__ == "__main__":
    main()
