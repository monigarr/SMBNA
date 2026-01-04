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

class TemporalSmoothness(Invariant):
    name = "temporal_smoothness"

    def score(self, belief, history, _):
        if len(history) < 2:
            return 0.0

        prev = history[-1]
        dt = belief.timestamp - prev.timestamp

        accel = (belief.velocity - prev.velocity) / max(dt, 1e-3)

        if norm(accel) > MAX_ACCEL:
            return (norm(accel) - MAX_ACCEL) / MAX_ACCEL

        return 0.0
