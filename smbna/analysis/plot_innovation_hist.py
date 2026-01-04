"""
===============================================================================
SMBNA Analysis - Innovation Histogram Plotting
===============================================================================

DESCRIPTION
-----------
Plots GPS innovation norms over time to visualize belief stress signals.
Shows when innovation exceeds refusal thresholds, indicating potential
spoofing or sensor failures.

USAGE
-----
    from smbna.analysis.plot_innovation_hist import plot_innovation
    from smbna.simulation.run_simulation import run_simulation, SimConfig
    
    config = SimConfig()
    logs = run_simulation(config)
    plot_innovation(logs)

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
import numpy as np

def plot_innovation(logs):
    innov = logs["innovation_norm"]

    plt.figure(figsize=(8, 3))
    plt.plot(innov, label="GPS Innovation Norm")
    plt.axhline(20.0, color="r", linestyle="--", label="Refusal Threshold")
    plt.xlabel("Timestep")
    plt.ylabel("Innovation Magnitude")
    plt.title("Figure 2: Belief Stress Signal (Innovation Norm)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
