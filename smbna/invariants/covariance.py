"""
===============================================================================
SMBNA Invariants - Covariance Honesty Invariant
===============================================================================

DESCRIPTION
-----------
Validates that belief covariance matrices accurately represent uncertainty.
Detects cases where beliefs claim high confidence (low covariance) but should
have higher uncertainty, indicating overconfident or dishonest uncertainty
estimates.

USAGE
-----
    from smbna.invariants.covariance import CovarianceHonesty
    
    invariant = CovarianceHonesty()
    penalty = invariant.score(belief, belief_history, other_beliefs)
    
    # penalty = 0.0 if covariance is honest
    # penalty = 1.0 if covariance is dishonest (hard penalty)

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

class CovarianceHonesty(Invariant):
    name = "covariance_honesty"

    def score(self, belief, history, _):
        if belief.internal_confidence > CONF_HIGH and trace(belief.covariance) < SIGMA_MIN:
            return 1.0  # hard penalty

        return 0.0
