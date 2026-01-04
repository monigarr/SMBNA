"""
===============================================================================
SMBNA Plots - Seed-Stratified Analysis
===============================================================================

DESCRIPTION
-----------
Plots performance metrics stratified by random seed to identify seed-dependent
behavior and ensure statistical robustness. Helps identify outliers and
understand performance variability.

USAGE
-----
    from smbna.plots.seed_stratified import plot_error_by_seed, plot_refusal_by_seed
    
    plot_error_by_seed("results/monte_carlo.csv")
    plot_refusal_by_seed("results/monte_carlo.csv")

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

def plot_error_by_seed(csv_path):
    df = pd.read_csv(csv_path)

    plt.figure()
    plt.scatter(df["seed"], df["final_position_error_m"])
    plt.xlabel("Seed")
    plt.ylabel("Final Position Error (m)")
    plt.title("Final Error by Random Seed")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_refusal_by_seed(csv_path):
    df = pd.read_csv(csv_path)

    plt.figure()
    plt.bar(df["seed"], df["refusal_rate"])
    plt.xlabel("Seed")
    plt.ylabel("Refusal Rate")
    plt.title("Refusal Rate by Seed")
    plt.tight_layout()
    plt.show()
