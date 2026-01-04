"""
===============================================================================
SMBNA Visualization - Confidence Interval Plotting
===============================================================================

DESCRIPTION
-----------
Plots error metrics with confidence intervals computed across multiple Monte
Carlo runs. Visualizes statistical uncertainty in performance metrics.

USAGE
-----
    from smbna.visualization.plot_ci import plot_with_ci, plot_error_ci
    import numpy as np
    
    # Plot with confidence intervals
    errors_over_time = np.array([...])  # Shape: (n_runs, n_timesteps)
    plot_error_ci(errors_over_time)

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

import numpy as np
import matplotlib.pyplot as plt


def plot_with_ci(x, mean, std, label):
    ci = 1.96 * std

    plt.plot(x, mean, label=label)
    plt.fill_between(
        x,
        mean - ci,
        mean + ci,
        alpha=0.2
    )

def plot_error_ci(errors_over_time):
    mean = errors_over_time.mean(axis=0)
    std = errors_over_time.std(axis=0)
    t = np.arange(len(mean))

    plot_with_ci(t, mean, std, "Position Error")
    plt.xlabel("Time Step")
    plt.ylabel("Error (m)")
    plt.legend()
    plt.show()

