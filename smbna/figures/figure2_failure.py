"""
===============================================================================
SMBNA Figures - Failure Mode Comparison Diagram Generator
===============================================================================

DESCRIPTION
-----------
Generates Figure 2: Comparison of EKF baseline (confident but wrong) vs. SMBNA
(refusal) behavior during GPS spoofing attacks. Demonstrates SMBNA's safety
advantage through explicit refusal.

USAGE
-----
    from smbna.figures.figure2_failure import generate_failure_plot
    import numpy as np
    
    t = np.linspace(0, 300, 3000)
    ekf_errors = ...  # EKF position errors
    smbna_errors = ...  # SMBNA position errors
    
    generate_failure_plot(t, ekf_errors, smbna_errors)
    # Generates figure2_failure.pdf

OUTPUT
------
PDF file: figure2_failure.pdf
Shows: Error trajectories comparing EKF vs. SMBNA during spoofing

DEPENDENCIES
------------
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

import matplotlib.pyplot as plt

def generate_failure_plot(t, ekf, smbna):
    plt.figure()
    plt.plot(t, ekf, label="EKF (confident wrong)")
    plt.plot(t, smbna, label="SMBNA (refusal)")
    plt.axvline(x=spoof_time, linestyle="--")
    plt.xlabel("Time")
    plt.ylabel("Error")
    plt.legend()
    plt.savefig("figure2_failure.pdf")
