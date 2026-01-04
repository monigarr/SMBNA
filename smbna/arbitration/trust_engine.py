"""
===============================================================================
SMBNA Arbitration - Trust Engine
===============================================================================

DESCRIPTION
-----------
Implements the trust arbitration system that selects the most trustworthy belief
or refuses navigation when confidence collapses. Combines belief confidence scores
with invariant penalty scores to compute trust, then selects the highest-trust
belief or emits NAV_UNSAFE if no belief meets minimum trust threshold.

USAGE
-----
    from smbna.arbitration.trust_engine import arbitrate
    from smbna.core.belief_state import BeliefState
    
    beliefs = [gps_state, ins_state, magnetic_state]
    invariant_scores = {
        "gps": 0.5,
        "ins": 0.1,
        "magnetic": 0.3
    }
    
    decision = arbitrate(beliefs, invariant_scores)
    # Returns: {"nav_unsafe": False, "selected": "ins", "confidence": 0.89, ...}

ALGORITHM
---------
1. For each belief: trust = confidence × exp(-λ × penalty)
2. Select belief with highest trust score
3. If max trust < TRUST_MIN: return nav_unsafe=True
4. Otherwise: return selected belief with confidence

PARAMETERS
----------
LAMBDA : float
    Penalty scaling factor (configurable)
TRUST_MIN : float
    Minimum trust threshold for navigation (configurable)

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

# Configuration constants (should be loaded from config in production)
LAMBDA = 1.0  # Penalty scaling factor
TRUST_MIN = 0.3  # Minimum trust threshold for navigation


def arbitrate(beliefs, invariant_scores):
    """
    Arbitrate between multiple beliefs to select the most trustworthy.
    
    Parameters
    ----------
    beliefs : list[BeliefState]
        List of belief states to choose from
    invariant_scores : dict[str, float]
        Dictionary mapping belief_id to invariant penalty score
        
    Returns
    -------
    dict
        Decision dictionary with keys:
        - nav_unsafe: bool - True if navigation should be refused
        - selected: str - Selected belief_id (if nav_unsafe=False)
        - confidence: float - Trust score of selected belief (if nav_unsafe=False)
        - reason: str - Reason for refusal (if nav_unsafe=True)
    """
    trust = {}

    for b in beliefs:
        penalty = invariant_scores.get(b.belief_id, 0.0)
        trust[b.belief_id] = b.internal_confidence * np.exp(-LAMBDA * penalty)

    if not trust:
        return {"nav_unsafe": True, "reason": "no beliefs available"}

    best_id, best_score = max(trust.items(), key=lambda x: x[1])

    if best_score < TRUST_MIN:
        return {"nav_unsafe": True, "reason": "confidence collapse"}

    return {"nav_unsafe": False, "selected": best_id, "confidence": best_score}
