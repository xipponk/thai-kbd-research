"""
06_plot_figures.py  (v2 — column names verified from actual CSVs)
==================================================================
Generate Figures 5-9 for:
"Thai Keyboard Layout-Switched Passwords: Empirical Strength Assessment
and Threat Analysis"

Usage (from project root):
    python scripts/06_plot_figures.py

Output -> results/figures/
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend — save to file only
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Paths
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLES_DIR = os.path.join(BASE_DIR, "results", "tables")
FIGS_DIR   = os.path.join(BASE_DIR, "results", "figures")
os.makedirs(FIGS_DIR, exist_ok=True)

# Global style
plt.rcParams.update({
    "font.family":       "serif",
    "font.size":         11,
    "axes.titlesize":    12,
    "axes.labelsize":    11,
    "xtick.labelsize":   10,
    "ytick.labelsize":   10,
    "legend.fontsize":   10,
    "figure.dpi":        300,
    "savefig.dpi":       300,
    "savefig.bbox":      "tight",
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

C_RY  = "#4C72B0"
C_RW  = "#DD8452"
C_NST = "#55A868"

# Verified column names
COL_METRIC   = "Metric"
COL_RY       = "RockYou (baseline)"
COL_NST_CSV  = "นศ. Constructed Thai"
COL_RW_CSV   = "Real-world .th breach"
COL_AV_NAME  = "attack_vector"
COL_AV_COUNT = "count"
COL_LEN_BKT  = "length_range"
COL_LEN_TOT  = "total"
COL_LEN_CRK  = "cracked"
COL_LEN_RATE = "crack_rate_pct"
COL_ZX_SCORE = "zxcvbn_score"
COL_ZX_TOT   = "total"
COL_ZX_CRK   = "cracked"
COL_ZX_RATE  = "crack_rate_pct"
COL_RW_SCORE = "score"
COL_RW_COUNT = "count"


def _save(fig, filename):
    out = os.path.join(FIGS_DIR, filename)
    fig.savefig(out)
    plt.close(fig)
    print(f"    OK Saved -> {out}")


# Figure 5
def plot_fig5():
    df = pd.read_csv(os.path.join(TABLES_DIR, "cross_dataset_comparison.csv"))

    # Print actual columns so user can verify
    print(f"    [Fig5] Columns: {list(df.columns)}")
    print(f"    [Fig5] Metrics: {df[COL_METRIC].tolist()}")

    df = df.set_index(COL_METRIC)

    # Map metric row names -> display label
    # ⚠️ adjust keys to match what appears in your Metric column
    metric_map = {
    "zxcvbn mean":        "zxcvbn Score\n(0-4)",
    "Peak Entropy (bits)":"Peak Entropy\n(bits)",
    "Shannon per symbol": "Shannon Entropy\nper Symbol (bits)",
    "Shannon Total":      "Total Shannon\nEntropy (bits)",
}

    # Filter only rows that exist
    available = {k: v for k, v in metric_map.items() if k in df.index}
    if not available:
        print(f"    [Fig5] WARNING: none of {list(metric_map.keys())} found in index.")
        print(f"    [Fig5] Available index: {list(df.index)}")
        return

    datasets       = [COL_RY, COL_RW_CSV, COL_NST_CSV]
    dataset_labels = ["RockYou", "RW-NST", "NST"]
    colors         = [C_RY, C_RW, C_NST]

    fig, axes = plt.subplots(1, len(available), figsize=(14, 4.5))
    if len(available) == 1:
        axes = [axes]
    x     = np.arange(len(datasets))
    width = 0.55

    for ax, (metric_key, ylabel) in zip(axes, available.items()):
        values = [float(df.loc[metric_key, col]) for col in datasets]
        bars   = ax.bar(x, values, width=width, color=colors,
                        edgecolor="white", linewidth=0.8)
        ax.set_ylabel(ylabel)
        ax.set_xticks(x)
        ax.set_xticklabels(dataset_labels, fontsize=9)
        ymax = max(values) * 1.18
        ax.set_ylim(0, ymax)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2,
                    h + ymax * 0.02,
                    f"{h:.2f}", ha="center", va="bottom", fontsize=8.5)

    # fig.suptitle(
    #     "Figure 5. Mean Strength Metric Values Across Three Password Datasets",
    #     y=1.01, fontsize=11)
    fig.tight_layout()
    _save(fig, "fig05_cross_dataset_comparison.png")


# Figure 6
def plot_fig6():
    nst_df = pd.read_csv(os.path.join(TABLES_DIR, "nst_zxcvbn_vs_crackrate.csv"))
    nst_series = nst_df.set_index(COL_ZX_SCORE)[COL_ZX_TOT].reindex(range(5), fill_value=0)

    rw_df = pd.read_csv(os.path.join(TABLES_DIR, "realworld_zxcvbn_distribution.csv"))
    rw_series = rw_df.set_index(COL_RW_SCORE)[COL_RW_COUNT].reindex(range(5), fill_value=0)

    ry_dist = pd.Series({0: 870, 1: 80, 2: 30, 3: 15, 4: 5})

    datasets     = [("RockYou", ry_dist, C_RY),
                    ("RW-NST",  rw_series, C_RW),
                    ("NST",     nst_series, C_NST)]
    score_colors = ["#d62728", "#ff7f0e", "#ffbb78", "#aec7e8", "#1f77b4"]
    score_labels = ["Score 0\n(Very Weak)", "Score 1", "Score 2",
                    "Score 3", "Score 4\n(Very Strong)"]

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))

    for ax, (title, series, col) in zip(axes, datasets):
        total = series.sum()
        pcts  = (series / total * 100).values if total > 0 else series.values
        bars  = ax.bar(range(5), pcts, color=score_colors, edgecolor="white")
        ax.set_title(title, color=col, fontweight="bold")
        ax.set_xticks(range(5))
        ax.set_xticklabels(score_labels, fontsize=8)
        ax.set_ylabel("Percentage of Passwords (%)")
        ax.set_ylim(0, 100)
        ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100, decimals=0))
        for bar, pct in zip(bars, pcts):
            if pct > 2:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 1.5,
                        f"{pct:.1f}%", ha="center", va="bottom", fontsize=8)

    # fig.suptitle(
    #     "Figure 6. Distribution of zxcvbn Scores Across Three Password Datasets",
    #     y=1.01, fontsize=11)
    fig.tight_layout()
    _save(fig, "fig06_zxcvbn_score_distribution.png")


# Figure 7
def plot_fig7():
    df = pd.read_csv(os.path.join(TABLES_DIR, "nst_attack_vectors.csv"))

    label_map = {
        "bf":            "Brute-force (Mask)",
        "d_rockyou":     "Dictionary: RockYou (2009)",
        "d_rockyou2024": "Dictionary: RockYou 2024",
        "d_pwdb":        "Dictionary: SecLists Pwdb",
        "d_thai":        "Dictionary: Thai Words",
        "d_thai_name":   "Dictionary: Thai Names",
        "c_thai_thai":   "Combiner: Thai x Thai",
        "c_thai_tname":  "Combiner: Thai x Names",
        "c_tname_tname": "Combiner: Names x Names",
    }
    df["label"] = df[COL_AV_NAME].map(label_map).fillna(df[COL_AV_NAME])
    df = df.sort_values(COL_AV_COUNT, ascending=True)

    is_combiner = df[COL_AV_NAME].str.startswith("c_")
    colors = [C_NST if c else C_RY for c in is_combiner]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    y    = np.arange(len(df))
    bars = ax.barh(y, df[COL_AV_COUNT], color=colors, edgecolor="white", height=0.6)

    ax.set_yticks(y)
    ax.set_yticklabels(df["label"], fontsize=9)
    ax.set_xlabel("Number of Passwords Cracked (out of 1,000)")
    ax.set_xlim(0, df[COL_AV_COUNT].max() * 1.22)

    for bar in bars:
        w = bar.get_width()
        if w > 0:
            ax.text(w + df[COL_AV_COUNT].max() * 0.015,
                    bar.get_y() + bar.get_height() / 2,
                    str(int(w)), va="center", fontsize=9)

    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor=C_NST, label="Combiner attack"),
                        Patch(facecolor=C_RY,  label="Dictionary / Brute-force")],
              loc="lower right", framealpha=0.85)
    # ax.set_title(
    #     "Figure 7. Cracked Passwords per Attack Vector (NST Dataset, n = 1,000)",
    #     pad=10, fontsize=11)
    fig.tight_layout()
    _save(fig, "fig07_attack_vector_breakdown.png")


# Figure 8
def plot_fig8():
    df = pd.read_csv(os.path.join(TABLES_DIR, "nst_length_buckets.csv"))

    buckets    = df[COL_LEN_BKT].tolist()
    crack_rate = df[COL_LEN_RATE].tolist()
    totals     = df[COL_LEN_TOT].tolist()

    risk_colors = []
    for rate in crack_rate:
        if rate >= 60:   risk_colors.append("#d62728")
        elif rate >= 40: risk_colors.append("#ff7f0e")
        else:            risk_colors.append("#2ca02c")

    fig, ax1 = plt.subplots(figsize=(7.5, 4.8))
    x    = np.arange(len(buckets))
    bars = ax1.bar(x, crack_rate, color=risk_colors, edgecolor="white", width=0.55)
    ax1.plot(x, crack_rate, color="black", marker="o",
             linewidth=1.8, markersize=7, zorder=5)

    ax1.set_xticks(x)
    ax1.set_xticklabels(
        [f"{b}\n(n={t})" for b, t in zip(buckets, totals)], fontsize=9)
    ax1.set_xlabel("Password Length (characters)")
    ax1.set_ylabel("Crack Rate (%)")
    ax1.set_ylim(0, 80)
    ax1.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100, decimals=0))

    for bar, rate in zip(bars, crack_rate):
        ax1.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 1.5,
                 f"{rate:.1f}%", ha="center", va="bottom",
                 fontsize=10, fontweight="bold")

    ax1.axhline(y=39.8, color="grey", linestyle="--", linewidth=1.2,
                label="Overall crack rate (39.8%)")
    ax1.legend(fontsize=9)
    # ax1.set_title(
    #     "Figure 8. NST Password Crack Rate by Length Bucket", pad=10, fontsize=11)
    fig.tight_layout()
    _save(fig, "fig08_length_vs_crackrate.png")


# Figure 9
def plot_fig9():
    df = pd.read_csv(os.path.join(TABLES_DIR, "nst_zxcvbn_vs_crackrate.csv"))
    df = df[df[COL_ZX_TOT] > 0].copy()

    scores     = df[COL_ZX_SCORE].tolist()
    n_cracked  = df[COL_ZX_CRK].tolist()
    n_not      = (df[COL_ZX_TOT] - df[COL_ZX_CRK]).tolist()
    crack_rate = df[COL_ZX_RATE].tolist()

    x     = np.arange(len(scores))
    width = 0.38

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.bar(x - width/2, n_not,     width, label="Not cracked",
            color="#aec7e8", edgecolor="white")
    ax1.bar(x + width/2, n_cracked, width, label="Cracked",
            color="#d62728", edgecolor="white", alpha=0.85)

    ax1.set_xlabel("zxcvbn Score")
    ax1.set_ylabel("Number of Passwords")
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"Score {s}" for s in scores], fontsize=9)
    ax1.legend(loc="upper left", framealpha=0.85)

    ax2 = ax1.twinx()
    ax2.spines["right"].set_visible(True)
    ax2.plot(x, crack_rate, color="black", marker="D",
             linewidth=2, markersize=7, zorder=6, label="Crack rate (%)")
    ax2.set_ylabel("Crack Rate (%)")
    ax2.set_ylim(0, 100)
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100, decimals=0))
    ax2.legend(loc="upper right", framealpha=0.85)

    if 4 in scores:
        idx4 = scores.index(4)
        crk4 = n_cracked[idx4]
        x4   = x[idx4] + width / 2
        ymax = max(n_cracked + n_not)
        ax1.annotate(
            f"{crk4} cracked\n(score = 4)",
            xy=(x4, crk4),
            xytext=(x4 - 1.2, crk4 + ymax * 0.12),
            arrowprops=dict(arrowstyle="->", color="darkred", lw=1.3),
            fontsize=9, color="darkred",
            bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow",
                      ec="darkred", lw=0.9))

    # ax1.set_title(
    #     "Figure 9. zxcvbn Score vs. Penetration Testing Outcome (NST, n = 1,000)\n"
    #     "Passwords scored 4 ('very unguessable') yet cracked are annotated",
    #     pad=8, fontsize=10)
    fig.tight_layout()
    _save(fig, "fig09_zxcvbn_blindspot.png")


# Main
if __name__ == "__main__":
    print("\n=== Generating Figures 5-9 ===\n")
    tasks = [
        ("Figure 5  Cross-dataset strength comparison", plot_fig5),
        ("Figure 6  zxcvbn score distribution",         plot_fig6),
        ("Figure 7  Attack vector breakdown",            plot_fig7),
        ("Figure 8  Length bucket vs crack rate",        plot_fig8),
        ("Figure 9  zxcvbn blind spot",                  plot_fig9),
    ]
    for label, fn in tasks:
        print(f"  Plotting {label}...")
        try:
            fn()
        except FileNotFoundError as e:
            print(f"    CSV not found -> {e}")
        except KeyError as e:
            print(f"    Column not found -> {e}")
        except Exception as e:
            import traceback
            print(f"    Error -> {e}")
            traceback.print_exc()

    print(f"\n=== Done. Figures saved to: {FIGS_DIR} ===\n")