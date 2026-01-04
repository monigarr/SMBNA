"""
===============================================================================
SMBNA Invariants - Temporal Smoothness Invariant
===============================================================================

DESCRIPTION
-----------
Validates temporal smoothness by checking for unrealistic acceleration between
consecutive belief states. Detects sudden jumps or discontinuities that
indicate sensor failures, spoofing, or belief inconsistencies.

USAGE
-----
    from smbna.invariants.temporal import TemporalSmoothness
    
    invariant = TemporalSmoothness()
    penalty = invariant.score(belief, belief_history, other_beliefs)
    
    # penalty = 0.0 if acceleration is within limits
    # penalty > 0.0 if acceleration exceeds MAX_ACCEL

PARAMETERS
----------
MAX_ACCEL : float
    Maximum allowed acceleration (m/s²), configurable via configuration

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""
from smbna.invariants.base import Invariant
from numpy.linalg import norm

# Configuration constants (should be loaded from config in production)
MAX_ACCEL = 10.0  # m/s², typical maximum acceleration for small UAVs


class TemporalSmoothness(Invariant):
    name = "temporal_smoothness"

    def score(self, belief, belief_history, other_beliefs):
        """Score temporal smoothness based on acceleration."""
        if len(belief_history) < 1:
            return 0.0

        prev = belief_history[-1]
        dt = belief.timestamp - prev.timestamp

        if dt <= 0:
            return 0.0

        accel = (belief.velocity - prev.velocity) / dt

        if norm(accel) > MAX_ACCEL:
            return (norm(accel) - MAX_ACCEL) / MAX_ACCEL

        return 0.0
