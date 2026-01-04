"""
===============================================================================
SMBNA Simulation - Variant Comparison
===============================================================================

DESCRIPTION
-----------
Compares different system variants (e.g., EKF baseline vs. SMBNA with refusal)
on identical scenarios. Enables fair comparison by running variants with the
same random seeds and conditions.

USAGE
-----
    from smbna.simulation.compare_variants import run_variant
    from smbna.simulation.run_simulation import SimConfig
    
    config = SimConfig(seed=42)
    
    # Run baseline (no refusal)
    logs_baseline = run_variant(config, enable_refusal=False)
    
    # Run SMBNA (with refusal)
    logs_smbna = run_variant(config, enable_refusal=True)

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

from smbna.simulation.run_simulation import run_simulation, SimConfig
from smbna.beliefs.refusal_logic import should_refuse_navigation
import numpy as np


def run_variant(cfg: SimConfig, enable_refusal: bool):
    logs = run_simulation(cfg)

    if not enable_refusal:
        return logs

    # SMBNA overlay: mask estimates after refusal triggers
    refused = logs["innovation_norm"] > 20.0
    refused = np.nan_to_num(refused, nan=False)

    smbna_est = logs["estimate"].copy()
    smbna_est[refused] = np.nan

    logs["estimate_smbna"] = smbna_est
    logs["refused"] = refused

    return logs
