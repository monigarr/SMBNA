"""
===============================================================================
SMBNA Analysis - Statistical Significance Testing
===============================================================================

DESCRIPTION
-----------
Performs paired statistical significance tests to determine if performance
differences between baseline and SMBNA variants are statistically significant.
Uses paired t-tests for matched-pairs comparison.

USAGE
-----
    from smbna.analysis.significance import paired_significance
    import numpy as np
    
    baseline_errors = np.array([...])  # Baseline position errors
    variant_errors = np.array([...])   # SMBNA position errors
    
    result = paired_significance(baseline_errors, variant_errors)
    print(f"Significant: {result['significant']}")
    print(f"p-value: {result['p_value']:.4f}")

RETURNS
-------
Dictionary with:
- t_stat: t-statistic
- p_value: p-value
- significant: boolean indicating significance at alpha level

DEPENDENCIES
------------
- scipy.stats
- numpy

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
from scipy.stats import ttest_rel


def paired_significance(baseline, variant, alpha=0.05):
    baseline = np.asarray(baseline)
    variant = np.asarray(variant)

    t, p = ttest_rel(baseline, variant, nan_policy="omit")

    return {
        "t_stat": float(t),
        "p_value": float(p),
        "significant": p < alpha,
    }
