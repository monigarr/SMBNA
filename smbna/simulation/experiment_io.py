"""
===============================================================================
SMBNA Simulation - Experiment I/O Utilities
===============================================================================

DESCRIPTION
-----------
Utilities for converting simulation logs to tabular format and writing results
to CSV/Parquet files. Enables aggregation, analysis, and comparison of
simulation results across multiple runs.

USAGE
-----
    from smbna.simulation.experiment_io import logs_to_row, write_results
    
    # Convert logs to row
    row = logs_to_row(logs, seed=42, variant="smbna")
    
    # Write results
    df = write_results([row1, row2, ...], name="experiment_results")

OUTPUT FORMATS
--------------
- CSV: Human-readable tabular format
- Parquet: Efficient binary format for large datasets

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
from pathlib import Path

def logs_to_row(logs: dict, seed: int, variant: str = "baseline") -> dict:
    """
    Reduce a single simulation run to scalar metrics
    suitable for tables and aggregation.
    """
    final_error = (
        (logs["truth"][-1][:2] - logs["estimate"][-1][:2]) ** 2
    ).sum() ** 0.5

    refused = logs.get("refused", None)

    if refused is None:
        refusal_rate = 0.0
    else:
        refused = list(refused)
        refusal_rate = sum(refused) / max(1, len(refused))

    return {
        "seed": seed,
        "final_position_error_m": final_error,
        "mean_innovation": float(sum(logs["innovation_norm"]) / len(logs["innovation_norm"])),
        "max_innovation": float(max(logs["innovation_norm"])),
        "refusal_rate": refusal_rate,
        "variant": variant,
    }


def write_results(rows, out_dir="results", name="monte_carlo"):
    """
    Write results in CSV and Parquet formats.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(rows)

    df.to_csv(out / f"{name}.csv", index=False)
    df.to_parquet(out / f"{name}.parquet")

    return df


