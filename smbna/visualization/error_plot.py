"""
===============================================================================
SMBNA Visualization - Error Plotting Utilities
===============================================================================

DESCRIPTION
-----------
Visualization utilities for plotting position errors, belief trust scores,
and other error metrics over time. Provides publication-ready plots for
analyzing system performance and failure modes.

USAGE
-----
    from smbna.visualization.error_plot import plot_position_error, plot_belief_trust
    import numpy as np
    
    time = np.linspace(0, 300, 3000)
    ekf_errors = ...
    smbna_errors = ...
    
    plot_position_error(time, ekf_errors, smbna_errors)
    plot_belief_trust(time, trust_scores)

DEPENDENCIES
------------
- matplotlib
- numpy

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

import matplotlib.pyplot as plt

def plot_position_error(time, ekf_err, smbna_err):
    plt.figure()
    plt.plot(time, ekf_err, label="EKF")
    plt.plot(time, smbna_err, label="SMBNA")
    plt.axvline(x=time[spoof_index], linestyle="--", label="Spoof Onset")
    plt.xlabel("Time (s)")
    plt.ylabel("Position Error (m)")
    plt.legend()
    plt.title("Position Error Under GPS Spoofing")
    plt.show()

def plot_belief_trust(time, trust_dict):
    plt.figure()
    for belief, scores in trust_dict.items():
        plt.plot(time, scores, label=belief)
    plt.axhline(y=TRUST_MIN, linestyle="--")
    plt.xlabel("Time (s)")
    plt.ylabel("Trust Score")
    plt.legend()
    plt.title("Belief Trust Evolution")
    plt.show()

import seaborn as sns

def plot_invariant_heatmap(violations):
    sns.heatmap(violations, cmap="Reds")
    plt.xlabel("Invariant")
    plt.ylabel("Time")
    plt.title("Invariant Violation Intensity")
    plt.show()
