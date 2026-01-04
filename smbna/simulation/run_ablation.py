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
