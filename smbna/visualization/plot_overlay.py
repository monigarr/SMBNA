"""
===============================================================================
SMBNA Visualization - Trajectory Overlay Plotting
===============================================================================

DESCRIPTION
-----------
Creates overlay plots comparing EKF and SMBNA trajectories against ground
truth. Visualizes the safety benefits of SMBNA's refusal mechanism during
GPS spoofing attacks.

USAGE
-----
    from smbna.visualization.plot_overlay import plot_ekf_vs_smbna
    from smbna.simulation.run_simulation import run_simulation, SimConfig
    
    config = SimConfig()
    logs = run_simulation(config)
    plot_ekf_vs_smbna(logs)

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


def plot_ekf_vs_smbna(logs):
    truth = logs["truth"][:, :2]
    ekf = logs["estimate"][:, :2]
    smbna = logs.get("estimate_smbna", None)

    plt.figure(figsize=(6, 6))
    plt.plot(truth[:, 0], truth[:, 1], "k-", label="Ground Truth")
    plt.plot(ekf[:, 0], ekf[:, 1], "r--", label="EKF")

    if smbna is not None:
        plt.plot(smbna[:, 0], smbna[:, 1], "b-", label="SMBNA (Refusal)")

    plt.legend()
    plt.axis("equal")
    plt.title("Trajectory Overlay: EKF vs SMBNA")
    plt.show()
