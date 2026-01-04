"""
===============================================================================
SMBNA Analysis - Trajectory Plotting
===============================================================================

DESCRIPTION
-----------
Generates trajectory plots comparing ground truth paths with estimated paths.
Visualizes navigation performance and divergence under GPS-degraded conditions.

USAGE
-----
    from smbna.analysis.plot_trajectory import plot_trajectory
    from smbna.simulation.run_simulation import run_simulation, SimConfig
    
    config = SimConfig()
    logs = run_simulation(config)
    plot_trajectory(logs)

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

def plot_trajectory(logs):
    truth = logs["truth"]
    est = logs["estimate"]

    plt.figure(figsize=(6, 6))
    plt.plot(truth[:, 0], truth[:, 1], label="Ground Truth")
    plt.plot(est[:, 0], est[:, 1], label="EKF Estimate", linestyle="--")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.title("Figure 1: Trajectory Under GPS-Degraded Conditions")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
