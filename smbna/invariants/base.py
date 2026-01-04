"""
===============================================================================
SMBNA Invariants - Base Invariant Class
===============================================================================

DESCRIPTION
-----------
Abstract base class for all invariant validators in the SMBNA system. Invariants
evaluate belief states for consistency, plausibility, and physical feasibility.
Each invariant returns a penalty score where 0 indicates full consistency and
higher values indicate greater inconsistency.

USAGE
-----
    from smbna.invariants.base import Invariant
    from smbna.core.belief_state import BeliefState
    
    class CustomInvariant(Invariant):
        name = "custom_invariant"
        
        def score(self, belief, belief_history, other_beliefs) -> float:
            # Implementation
            return penalty  # ∈ [0, +∞)

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

class Invariant:
    name: str

    def score(self, belief, belief_history, other_beliefs) -> float:
        """
        Returns penalty ∈ [0, +∞)
        0 = fully consistent
        """
        raise NotImplementedError
