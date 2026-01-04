"""
===============================================================================
SMBNA Plots - Refusal Tradeoff Analysis
===============================================================================

DESCRIPTION
-----------
Plots the safety-accuracy tradeoff curve showing how refusal rate affects
position error. Visualizes the relationship between conservative refusal
thresholds and navigation accuracy.

USAGE
-----
    from smbna.plots.refusal_tradeoff import plot_tradeoff
    
    plot_tradeoff("results/refusal_sweep.csv")
    # Shows tradeoff between refusal rate and position error

DEPENDENCIES
------------
- pandas
- matplotlib

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

import pandas as pd
import matplotlib.pyplot as plt

def plot_tradeoff(csv_path):
    df = pd.read_csv(csv_path)

    grouped = df.groupby("refusal_threshold").mean()

    plt.figure()
    plt.plot(
        grouped["refusal_rate"],
        grouped["final_position_error_m"],
        marker="o",
    )

    plt.xlabel("Refusal Rate")
    plt.ylabel("Mean Final Position Error (m)")
    plt.title("Safety–Accuracy Tradeoff")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
