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


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run parameter sweep to evaluate system sensitivity to refusal thresholds."
    )
    parser.add_argument("--thresholds", type=float, nargs="+", 
                        default=[5, 10, 15, 20, 30, 50],
                        help="Refusal threshold values to test (default: 5 10 15 20 30 50)")
    parser.add_argument("--seeds", type=int, default=20,
                        help="Number of random seeds per threshold (default: 20)")
    args = parser.parse_args()
    
    thresholds = tuple(args.thresholds)
    seeds = range(args.seeds)
    
    total_runs = len(thresholds) * args.seeds
    
    print(f"\nRunning parameter sweep...")
    print(f"  Thresholds to test: {thresholds}")
    print(f"  Seeds per threshold: {args.seeds}")
    print(f"  Total runs: {total_runs}")
    print("This may take several minutes depending on the number of runs.\n")
    
    df = sweep_refusal_thresholds(thresholds=thresholds, seeds=seeds)
    
    print("\n" + "="*70)
    print("PARAMETER SWEEP COMPLETE")
    print("="*70)
    print(f"\nSummary Statistics:")
    for th in thresholds:
        th_df = df[df['refusal_threshold'] == th]
        print(f"\nRefusal threshold = {th:.1f} m:")
        print(f"  Mean final position error: {th_df['final_position_error_m'].mean():.2f} m")
        print(f"  Std final position error: {th_df['final_position_error_m'].std():.2f} m")
        print(f"  Mean refusal rate: {th_df['refusal_rate'].mean():.2%}")
    
    print("\n" + "="*70)
    print("RESULTS SAVED TO:")
    print("="*70)
    print("  CSV: results/refusal_sweep.csv")
    print("  Parquet: results/refusal_sweep.parquet")
    print("\nThese files contain per-run metrics for all threshold values:")
    print("  - seed: Random seed for each run")
    print("  - refusal_threshold: Refusal threshold value tested")
    print("  - final_position_error_m: Final position error (meters)")
    print("  - mean_innovation: Mean GPS innovation magnitude")
    print("  - max_innovation: Maximum GPS innovation magnitude")
    print("  - refusal_rate: Fraction of timesteps where navigation was refused")
    print("\nTo load and analyze results:")
    print("  import pandas as pd")
    print("  df = pd.read_csv('results/refusal_sweep.csv')")
    print("  # Group by threshold:")
    print("  grouped = df.groupby('refusal_threshold')['final_position_error_m'].agg(['mean', 'std'])")
    print("\nTo export to LaTeX tables:")
    print("  from smbna.analysis.latex_export import dataframe_to_latex")
    print("  dataframe_to_latex(df, 'refusal_sweep')")
    print("="*70 + "\n")
