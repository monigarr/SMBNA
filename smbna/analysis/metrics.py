"""
===============================================================================
SMBNA Analysis - Performance Metrics
===============================================================================

DESCRIPTION
-----------
Computes statistical metrics from simulation logs, handling NaN values
appropriately. Provides functions for analyzing position errors, innovation
statistics, and other performance measures.

USAGE
-----
    from smbna.analysis.metrics import nan_safe_stats
    import numpy as np
    
    # Compute statistics on innovation norms
    innov_stats = nan_safe_stats(logs["innovation_norm"])
    print(f"Mean: {innov_stats['mean']:.2f}")
    print(f"Std: {innov_stats['std']:.2f}")
    print(f"Max: {innov_stats['max']:.2f}")

RETURNS
-------
Dictionary with keys:
- mean: Mean value (NaN-safe)
- std: Standard deviation (NaN-safe)
- max: Maximum value (NaN-safe)
- median: Median value (NaN-safe)
- count_valid: Number of valid (non-NaN) values

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


def nan_safe_stats(x: np.ndarray):
    x = np.asarray(x, dtype=float)

    return {
        "mean": float(np.nanmean(x)),
        "std": float(np.nanstd(x)),
        "max": float(np.nanmax(x)),
        "median": float(np.nanmedian(x)),
        "count_valid": int(np.sum(~np.isnan(x))),
    }
