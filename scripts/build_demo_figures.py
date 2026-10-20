#!/usr/bin/env python3
"""Rebuild synthetic visual fixtures. Optional development dependency: matplotlib.

These charts intentionally contain disclosed validation-case defects. They are
not research results or examples of recommended scientific presentation.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1] / "tests/fixtures"
plt.rcParams.update({"font.size": 13, "svg.fonttype": "none"})

fig, ax = plt.subplots(figsize=(7.2, 4.6), layout="constrained")
ax.bar(["Baseline", "RouteMind"], [80, 88], color=["#64748b", "#2563eb"], width=.55)
ax.set(ylim=(79, 90), ylabel="Mean accuracy (%)", title="Figure 1. TaskBench-Q")
for i, value in enumerate([80, 88]):
    ax.text(i, value + .2, f"{value:.1f}", ha="center", weight="bold")
ax.spines[["top", "right"]].set_visible(False)
fig.text(.5, .005, "SYNTHETIC VALIDATION FIXTURE", ha="center", fontsize=8, color="#64748b")
fig.savefig(ROOT / "en_agent/figure1.png", dpi=160)
fig.savefig(ROOT / "en_agent/figure1.svg")
plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 3.4), layout="constrained")
data = np.array([[1, 1, 1, 1], [2, 3, 4, 2]])
im = ax.imshow(data, vmin=0, vmax=4, cmap="Blues")
ax.set_xticks(range(4), labels=["Q1", "Q2", "Q3", "Q4"])
ax.set_yticks(range(2), labels=["Baseline", "RouteMind"])
for row in range(2):
    for col in range(4):
        ax.text(col, row, str(data[row,col]), ha="center", va="center", color="white" if data[row,col] >= 3 else "black")
ax.set_title("Figure 2. Illustrative retrieval calls")
fig.colorbar(im, ax=ax, ticks=[0,1,2,3,4], label="Calls per query")
fig.text(.5, .005, "SYNTHETIC TRACE; FOUR ILLUSTRATIVE QUERIES", ha="center", fontsize=8, color="#64748b")
fig.savefig(ROOT / "en_agent/figure2.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(7.2, 4.6), layout="constrained")
ax.bar(["Single agent", "Full system"], [.80, .84], color=["#64748b", "#0d9488"], width=.55)
ax.set(ylim=(0, 1), ylabel="Accuracy (%)", title="Figure 1. Synthetic Chinese QA")
for i, value in enumerate([.80, .84]):
    ax.text(i, value + .02, f"{value:.2f}", ha="center", weight="bold")
ax.spines[["top", "right"]].set_visible(False)
fig.text(.5, .005, "SYNTHETIC VALIDATION FIXTURE", ha="center", fontsize=8, color="#64748b")
fig.savefig(ROOT / "zh_agent/figure1.png", dpi=160)
fig.savefig(ROOT / "zh_agent/figure1.svg")
plt.close(fig)
print("Rebuilt 3 synthetic figures (2 SVG sources, 3 PNG images).")
