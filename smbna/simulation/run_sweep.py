"""
===============================================================================
SMBNA Simulation - Parameter Sweep Runner
===============================================================================

DESCRIPTION
-----------
Performs parameter sweeps to evaluate system sensitivity to configuration
parameters. Tests multiple parameter values across multiple random seeds to
identify optimal settings and parameter sensitivity.

USAGE
-----
    from smbna.simulation.run_sweep import sweep_refusal_thresholds
    
    results = sweep_refusal_thresholds(
        thresholds=(5, 10, 15, 20, 30, 50),
        seeds=range(20)
    )

PARAMETERS
----------
thresholds : tuple
    Parameter values to test
seeds : iterable
    Random seeds for each parameter value

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

def sweep_refusal_thresholds(
    thresholds=(5, 10, 15, 20, 30, 50),
    seeds=range(20),
):
    rows = []

    for th in thresholds:
        for seed in seeds:
            cfg = SimConfig(
                seed=seed,
                refusal_threshold=th,
            )
            logs = run_simulation(cfg)
            row = logs_to_row(logs, seed)
            row["refusal_threshold"] = th
            rows.append(row)

    return write_results(rows, name="refusal_sweep")
