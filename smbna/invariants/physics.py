"""
===============================================================================
SMBNA Invariants - Physics Feasibility Invariant
===============================================================================

DESCRIPTION
-----------
Validates that belief states satisfy physical constraints, such as maximum
airspeed limits. Detects physically impossible states that indicate sensor
failures, spoofing, or belief errors.

USAGE
-----
    from smbna.invariants.physics import PhysicsInvariant
    
    invariant = PhysicsInvariant()
    penalty = invariant.score(belief, belief_history, other_beliefs)
    
    # penalty = 0.0 if speed is within limits
    # penalty > 0.0 if speed exceeds MAX_AIRSPEED

PARAMETERS
----------
MAX_AIRSPEED : float
    Maximum physically feasible airspeed (m/s), configurable via configuration

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
MAX_AIRSPEED = 100.0  # m/s, typical maximum airspeed for small UAVs


class PhysicsInvariant(Invariant):
    name = "physics_feasibility"

    def score(self, belief, belief_history, other_beliefs):
        """Score physics feasibility based on velocity magnitude."""
        speed = norm(belief.velocity)

        if speed > MAX_AIRSPEED:
            return (speed - MAX_AIRSPEED) / MAX_AIRSPEED

        return 0.0
