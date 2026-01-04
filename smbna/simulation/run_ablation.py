"""
===============================================================================
SMBNA Simulation - Ablation Study Runner
===============================================================================

DESCRIPTION
-----------
Runs ablation studies to isolate the impact of specific components (e.g., refusal
logic) on system performance. Compares baseline and augmented variants across
multiple runs to quantify component contributions.

USAGE
-----
    from smbna.simulation.run_ablation import run_ablation
    
    results = run_ablation(num_runs=50)
    # Results saved to CSV/Parquet for analysis

OUTPUT
------
Generates comparison data with metrics for:
- Baseline (EKF only)
- SMBNA (with refusal logic)
- Performance differences

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

from smbna.simulation.compare_variants import run_variant
from smbna.simulation.run_simulation import SimConfig
from smbna.simulation.experiment_io import logs_to_row, write_results


def run_ablation(num_runs=50):
    rows = []

    for seed in range(num_runs):
        cfg = SimConfig(seed=seed)

        logs_ekf = run_variant(cfg, enable_refusal=False)
        logs_smbna = run_variant(cfg, enable_refusal=True)

        rows.append(logs_to_row(logs_ekf, seed, "ekf"))
        rows.append(logs_to_row(logs_smbna, seed, "smbna"))

    return write_results(rows, name="ablation_refusal")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run ablation study comparing baseline (EKF) vs. SMBNA (with refusal)."
    )
    parser.add_argument("--runs", type=int, default=50,
                        help="Number of simulation runs per variant (default: 50)")
    args = parser.parse_args()
    
    print(f"\nRunning ablation study with {args.runs} runs per variant...")
    print("Comparing:")
    print("  - Baseline (EKF only, no refusal)")
    print("  - SMBNA (with refusal logic)")
    print("This may take several minutes depending on the number of runs.\n")
    
    df = run_ablation(num_runs=args.runs)
    
    # Compute summary statistics
    ekf_df = df[df['variant'] == 'ekf']
    smbna_df = df[df['variant'] == 'smbna']
    
    print("\n" + "="*70)
    print("ABLATION STUDY COMPLETE")
    print("="*70)
    print(f"\nSummary Statistics ({args.runs} runs per variant):")
    print(f"\nBaseline (EKF):")
    print(f"  Mean final position error: {ekf_df['final_position_error_m'].mean():.2f} m")
    print(f"  Std final position error: {ekf_df['final_position_error_m'].std():.2f} m")
    print(f"  Mean refusal rate: {ekf_df['refusal_rate'].mean():.2%}")
    
    print(f"\nSMBNA (with refusal):")
    print(f"  Mean final position error: {smbna_df['final_position_error_m'].mean():.2f} m")
    print(f"  Std final position error: {smbna_df['final_position_error_m'].std():.2f} m")
    print(f"  Mean refusal rate: {smbna_df['refusal_rate'].mean():.2%}")
    
    print("\n" + "="*70)
    print("RESULTS SAVED TO:")
    print("="*70)
    print("  CSV: results/ablation_refusal.csv")
    print("  Parquet: results/ablation_refusal.parquet")
    print("\nThese files contain per-run metrics for both variants:")
    print("  - seed: Random seed for each run")
    print("  - variant: 'ekf' or 'smbna'")
    print("  - final_position_error_m: Final position error (meters)")
    print("  - mean_innovation: Mean GPS innovation magnitude")
    print("  - max_innovation: Maximum GPS innovation magnitude")
    print("  - refusal_rate: Fraction of timesteps where navigation was refused")
    print("\nTo load and analyze results:")
    print("  import pandas as pd")
    print("  df = pd.read_csv('results/ablation_refusal.csv')")
    print("  # Compare variants:")
    print("  ekf_errors = df[df['variant'] == 'ekf']['final_position_error_m']")
    print("  smbna_errors = df[df['variant'] == 'smbna']['final_position_error_m']")
    print("\nTo perform statistical significance testing:")
    print("  from smbna.analysis.significance import paired_significance")
    print("  result = paired_significance(ekf_errors, smbna_errors)")
    print("\nTo export to LaTeX tables:")
    print("  from smbna.analysis.latex_export import dataframe_to_latex")
    print("  dataframe_to_latex(df, 'ablation_refusal')")
    print("="*70 + "\n")
