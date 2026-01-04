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
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run Monte Carlo evaluation across multiple random seeds."
    )
    parser.add_argument("--runs", type=int, default=50,
                        help="Number of simulation runs (default: 50)")
    parser.add_argument("--name", type=str, default="monte_carlo",
                        help="Output file name (default: monte_carlo)")
    args = parser.parse_args()
    
    print(f"\nRunning Monte Carlo evaluation with {args.runs} runs...")
    print("This may take several minutes depending on the number of runs.\n")
    
    stats = monte_carlo(num_runs=args.runs, out_name=args.name)
    
    print("\n" + "="*70)
    print("MONTE CARLO EVALUATION COMPLETE")
    print("="*70)
    print(f"\nAggregate Statistics ({args.runs} runs):")
    for k, v in stats.items():
        print(f"  {k.replace('_', ' ').title()}: {v:.2f} m")
    
    print("\n" + "="*70)
    print("RESULTS SAVED TO:")
    print("="*70)
    print(f"  CSV: results/{args.name}.csv")
    print(f"  Parquet: results/{args.name}.parquet")
    print("\nThese files contain per-run metrics:")
    print("  - seed: Random seed for each run")
    print("  - final_position_error_m: Final position error (meters)")
    print("  - mean_innovation: Mean GPS innovation magnitude")
    print("  - max_innovation: Maximum GPS innovation magnitude")
    print("  - refusal_rate: Fraction of timesteps where navigation was refused")
    print("\nTo load and analyze results:")
    print("  import pandas as pd")
    print(f"  df = pd.read_csv('results/{args.name}.csv')")
    print("  # or")
    print(f"  df = pd.read_parquet('results/{args.name}.parquet')")
    print("\nTo export to LaTeX tables:")
    print("  from smbna.analysis.latex_export import dataframe_to_latex")
    print(f"  dataframe_to_latex(df, '{args.name}')")
    print("="*70 + "\n")
