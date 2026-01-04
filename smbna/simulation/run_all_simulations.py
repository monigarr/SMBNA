"""
===============================================================================
SMBNA Simulation - Run All Batch Simulations
===============================================================================

DESCRIPTION
-----------
Runs all batch simulations (Monte Carlo, ablation study, parameter sweep) in
sequence to generate a complete evaluation suite. This is useful for generating
all results files at once for comprehensive analysis.

USAGE
-----
    # Command line (default parameters)
    python -m smbna.simulation.run_all_simulations
    
    # Custom parameters
    python -m smbna.simulation.run_all_simulations --monte-carlo-runs 100 --ablation-runs 100
    
    # Skip specific simulations
    python -m smbna.simulation.run_all_simulations --skip-monte-carlo --skip-sweep

OUTPUT
------
Generates all batch simulation results:
- results/monte_carlo.csv and .parquet
- results/ablation_refusal.csv and .parquet
- results/refusal_sweep.csv and .parquet

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

import argparse
import sys

from smbna.simulation.run_monte_carlo import monte_carlo
from smbna.simulation.run_ablation import run_ablation
from smbna.simulation.run_sweep import sweep_refusal_thresholds


def run_all(
    monte_carlo_runs=50,
    ablation_runs=50,
    sweep_thresholds=(5, 10, 15, 20, 30, 50),
    sweep_seeds=20,
    skip_monte_carlo=False,
    skip_ablation=False,
    skip_sweep=False,
):
    """
    Run all batch simulations in sequence.
    
    Parameters
    ----------
    monte_carlo_runs : int
        Number of runs for Monte Carlo evaluation (default: 50)
    ablation_runs : int
        Number of runs per variant for ablation study (default: 50)
    sweep_thresholds : tuple
        Refusal threshold values to test in parameter sweep (default: (5, 10, 15, 20, 30, 50))
    sweep_seeds : int
        Number of random seeds per threshold in parameter sweep (default: 20)
    skip_monte_carlo : bool
        Skip Monte Carlo evaluation (default: False)
    skip_ablation : bool
        Skip ablation study (default: False)
    skip_sweep : bool
        Skip parameter sweep (default: False)
    
    Returns
    -------
    dict
        Dictionary with keys: 'monte_carlo', 'ablation', 'sweep'
        Contains DataFrames or None if skipped
    """
    results = {}
    
    print("="*70)
    print("RUNNING ALL BATCH SIMULATIONS")
    print("="*70)
    print("\nThis will run:")
    if not skip_monte_carlo:
        print(f"  1. Monte Carlo evaluation ({monte_carlo_runs} runs)")
    if not skip_ablation:
        print(f"  2. Ablation study ({ablation_runs} runs per variant)")
    if not skip_sweep:
        print(f"  3. Parameter sweep ({len(sweep_thresholds)} thresholds, {sweep_seeds} seeds each)")
    print("\nThis may take several minutes to hours depending on parameters.")
    print("="*70 + "\n")
    
    # 1. Monte Carlo Evaluation
    if not skip_monte_carlo:
        print("\n" + "="*70)
        print("RUNNING MONTE CARLO EVALUATION")
        print("="*70)
        try:
            stats = monte_carlo(num_runs=monte_carlo_runs, out_name="monte_carlo")
            results['monte_carlo'] = stats
            print("\n✓ Monte Carlo evaluation complete")
        except Exception as e:
            print(f"\n✗ Monte Carlo evaluation failed: {e}")
            results['monte_carlo'] = None
            sys.exit(1)
    else:
        print("\n⏭ Skipping Monte Carlo evaluation")
        results['monte_carlo'] = None
    
    # 2. Ablation Study
    if not skip_ablation:
        print("\n" + "="*70)
        print("RUNNING ABLATION STUDY")
        print("="*70)
        try:
            df_ablation = run_ablation(num_runs=ablation_runs)
            results['ablation'] = df_ablation
            print("\n✓ Ablation study complete")
        except Exception as e:
            print(f"\n✗ Ablation study failed: {e}")
            results['ablation'] = None
            sys.exit(1)
    else:
        print("\n⏭ Skipping ablation study")
        results['ablation'] = None
    
    # 3. Parameter Sweep
    if not skip_sweep:
        print("\n" + "="*70)
        print("RUNNING PARAMETER SWEEP")
        print("="*70)
        try:
            df_sweep = sweep_refusal_thresholds(
                thresholds=sweep_thresholds,
                seeds=range(sweep_seeds)
            )
            results['sweep'] = df_sweep
            print("\n✓ Parameter sweep complete")
        except Exception as e:
            print(f"\n✗ Parameter sweep failed: {e}")
            results['sweep'] = None
            sys.exit(1)
    else:
        print("\n⏭ Skipping parameter sweep")
        results['sweep'] = None
    
    # Summary
    print("\n" + "="*70)
    print("ALL SIMULATIONS COMPLETE")
    print("="*70)
    print("\nGenerated results files:")
    
    if results['monte_carlo'] is not None:
        print(f"  ✓ results/monte_carlo.csv")
        print(f"  ✓ results/monte_carlo.parquet")
    
    if results['ablation'] is not None:
        print(f"  ✓ results/ablation_refusal.csv")
        print(f"  ✓ results/ablation_refusal.parquet")
    
    if results['sweep'] is not None:
        print(f"  ✓ results/refusal_sweep.csv")
        print(f"  ✓ results/refusal_sweep.parquet")
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("\nTo analyze results:")
    print("  import pandas as pd")
    print("  ")
    if results['monte_carlo'] is not None:
        print("  # Load Monte Carlo results")
        print("  mc_df = pd.read_csv('results/monte_carlo.csv')")
        print("  ")
    if results['ablation'] is not None:
        print("  # Load ablation results")
        print("  ablation_df = pd.read_csv('results/ablation_refusal.csv')")
        print("  ekf_errors = ablation_df[ablation_df['variant'] == 'ekf']['final_position_error_m']")
        print("  smbna_errors = ablation_df[ablation_df['variant'] == 'smbna']['final_position_error_m']")
        print("  ")
    if results['sweep'] is not None:
        print("  # Load parameter sweep results")
        print("  sweep_df = pd.read_csv('results/refusal_sweep.csv')")
        print("  grouped = sweep_df.groupby('refusal_threshold')['final_position_error_m'].agg(['mean', 'std'])")
        print("  ")
    if results['ablation'] is not None:
        print("\nTo perform statistical significance testing:")
        print("  from smbna.analysis.significance import paired_significance")
        print("  result = paired_significance(ekf_errors, smbna_errors)")
        print("  print(f\"Significant: {result['significant']}, p-value: {result['p_value']:.4f}\")")
        print("  ")
    print("\nTo export to LaTeX tables:")
    print("  from smbna.analysis.latex_export import dataframe_to_latex")
    if results['monte_carlo'] is not None:
        print("  dataframe_to_latex(mc_df, 'monte_carlo')")
    if results['ablation'] is not None:
        print("  dataframe_to_latex(ablation_df, 'ablation_refusal')")
    if results['sweep'] is not None:
        print("  dataframe_to_latex(sweep_df, 'refusal_sweep')")
    print("="*70 + "\n")
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run all batch simulations (Monte Carlo, ablation, parameter sweep).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all simulations with default parameters
  python -m smbna.simulation.run_all_simulations
  
  # Run with custom number of runs
  python -m smbna.simulation.run_all_simulations --monte-carlo-runs 100 --ablation-runs 100
  
  # Skip specific simulations
  python -m smbna.simulation.run_all_simulations --skip-monte-carlo --skip-sweep
  
  # Custom parameter sweep thresholds
  python -m smbna.simulation.run_all_simulations --sweep-thresholds 10 20 30 40 50
        """
    )
    
    parser.add_argument("--monte-carlo-runs", type=int, default=50,
                        help="Number of runs for Monte Carlo evaluation (default: 50)")
    parser.add_argument("--ablation-runs", type=int, default=50,
                        help="Number of runs per variant for ablation study (default: 50)")
    parser.add_argument("--sweep-thresholds", type=float, nargs="+",
                        default=[5, 10, 15, 20, 30, 50],
                        help="Refusal threshold values for parameter sweep (default: 5 10 15 20 30 50)")
    parser.add_argument("--sweep-seeds", type=int, default=20,
                        help="Number of random seeds per threshold in parameter sweep (default: 20)")
    parser.add_argument("--skip-monte-carlo", action="store_true",
                        help="Skip Monte Carlo evaluation")
    parser.add_argument("--skip-ablation", action="store_true",
                        help="Skip ablation study")
    parser.add_argument("--skip-sweep", action="store_true",
                        help="Skip parameter sweep")
    
    args = parser.parse_args()
    
    run_all(
        monte_carlo_runs=args.monte_carlo_runs,
        ablation_runs=args.ablation_runs,
        sweep_thresholds=tuple(args.sweep_thresholds),
        sweep_seeds=args.sweep_seeds,
        skip_monte_carlo=args.skip_monte_carlo,
        skip_ablation=args.skip_ablation,
        skip_sweep=args.skip_sweep,
    )

