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

def arbitrate(beliefs, invariant_scores):
    trust = {}

    for b in beliefs:
        penalty = invariant_scores[b.belief_id]
        trust[b.belief_id] = b.internal_confidence * np.exp(-LAMBDA * penalty)

    best_id, best_score = max(trust.items(), key=lambda x: x[1])

    if best_score < TRUST_MIN:
        return {"nav_unsafe": True, "reason": "confidence collapse"}

    return {"nav_unsafe": False, "selected": best_id, "confidence": best_score}
