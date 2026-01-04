"""
===============================================================================
SMBNA Beliefs - Navigation Refusal Logic
===============================================================================

DESCRIPTION
-----------
Implements the refusal logic that determines when the navigation system should
explicitly refuse to provide a position estimate. This is a key safety mechanism
that prevents false confidence when belief inconsistency is detected.

The refusal decision is based on innovation magnitude (residual between
measurement and prediction), with configurable thresholds.

USAGE
-----
    from smbna.beliefs.refusal_logic import should_refuse_navigation
    
    innovation_norm = 25.0  # meters
    threshold = 20.0  # meters
    
    should_refuse = should_refuse_navigation(innovation_norm, threshold)
    # Returns: True (innovation exceeds threshold)

PARAMETERS
----------
innovation_norm : float
    Norm of the innovation residual (measurement - prediction)
threshold : float, optional
    Maximum tolerated innovation magnitude (default: 20.0 meters)

RETURNS
-------
bool
    True if navigation should be refused, False otherwise

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

def should_refuse_navigation(innovation_norm: float,
                             threshold: float = 20.0) -> bool:
    """
    Determines whether the navigation system should refuse to provide
    a position estimate based on belief inconsistency.

    Parameters
    ----------
    innovation_norm : float
        Norm of the GPS innovation residual.
    threshold : float
        Maximum tolerated innovation magnitude.

    Returns
    -------
    bool
        True if navigation should refuse, False otherwise.
    """
    if np.isnan(innovation_norm):
        return False
    return innovation_norm > threshold
