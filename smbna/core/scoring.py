"""
===============================================================================
SMBNA Core - Invariant Scoring System
===============================================================================

DESCRIPTION
-----------
Orchestrates invariant evaluation across all registered invariants and beliefs.
Computes penalty scores for each belief based on consistency checks including
temporal smoothness, physics feasibility, cross-belief coherence, and other
invariant validations.

USAGE
-----
    from smbna.core.scoring import InvariantScorer
    from smbna.invariants.temporal import TemporalSmoothness
    
    scorer = InvariantScorer()
    scorer.add_invariant(TemporalSmoothness())
    
    # Score beliefs
    scores = scorer.evaluate(beliefs, belief_histories)

DEPENDENCIES
------------
- smbna.invariants.base
- smbna.core.belief_state

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

