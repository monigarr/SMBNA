"""
===============================================================================
SMBNA Simulation - Monte Carlo Evaluation Runner
===============================================================================

DESCRIPTION
-----------
Runs Monte Carlo simulations across multiple random seeds to generate
statistical performance metrics. Aggregates results across runs to compute
mean, standard deviation, and maximum position errors.

USAGE
-----
    from smbna.simulation.run_monte_carlo import monte_carlo
    
    results = monte_carlo(num_runs=50, out_name="monte_carlo")
    print(f"Mean error: {results['mean_error']:.2f} m")
    print(f"Max error: {results['max_error']:.2f} m")

OUTPUT
------
Generates CSV and Parquet files with aggregated statistics:
- mean_error: Mean final position error
- std_error: Standard deviation of errors
- max_error: Maximum position error

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
from smbna.simulation.run_simulation import run_simulation, SimConfig
from smbna.simulation.experiment_io import logs_to_row, write_results

# -----------------------------
# Guard for module execution
# -----------------------------
if __name__ == "__main__" and __package__ is None:
    raise RuntimeError(
        "This module must be run as a package:\n"
        "python -m smbna.simulation.simulation.run_monte_carlo"
    )

def monte_carlo(num_runs=50, out_name="monte_carlo"):
    rows = []

    for seed in range(num_runs):
        cfg = SimConfig(seed=seed)
        logs = run_simulation(cfg)
        rows.append(logs_to_row(logs, seed))

    df = write_results(rows, name=out_name)

    return {
        "mean_error": df["final_position_error_m"].mean(),
        "std_error": df["final_position_error_m"].std(),
        "max_error": df["final_position_error_m"].max(),
    }

if __name__ == "__main__":
    stats = monte_carlo()
    for k, v in stats.items():
        print(f"{k}: {v:.2f}")
