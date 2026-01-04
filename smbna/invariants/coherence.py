"""
===============================================================================
SMBNA Invariants - Cross-Belief Coherence Invariant
===============================================================================

DESCRIPTION
-----------
Validates coherence between different belief estimates by comparing their
position estimates. Detects when beliefs disagree beyond what can be explained
by their stated uncertainties, indicating potential spoofing or sensor failures.

USAGE
-----
    from smbna.invariants.coherence import CrossBeliefCoherence
    
    invariant = CrossBeliefCoherence()
    penalty = invariant.score(belief, belief_history, other_beliefs)
    
    # penalty = 0.0 if beliefs are coherent
    # penalty > 0.0 if beliefs disagree beyond uncertainty bounds

PARAMETERS
----------
K : float
    Coherence threshold multiplier (typically 2-3 sigma)

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

class CrossBeliefCoherence(Invariant):
    name = "cross_belief_coherence"

    def score(self, belief, _, other_beliefs):
        penalties = []

        for other in other_beliefs:
            delta = norm(belief.position - other.position)
            combined_sigma = trace(belief.covariance + other.covariance)

            if delta > K * sqrt(combined_sigma):
                penalties.append(delta / combined_sigma)

        return max(penalties, default=0.0)
