"""
===============================================================================
SMBNA Beliefs - Dead Reckoning Fallback Belief Engine
===============================================================================

DESCRIPTION
-----------
Dead reckoning belief engine that provides a fallback navigation estimate
based on simple kinematic propagation. Used when other belief sources are
unavailable or unreliable.

USAGE
-----
    from smbna.beliefs.dead_reckoning import DeadReckoningBelief
    
    belief = DeadReckoningBelief()
    sensor_data = {
        "velocity": np.array([1.0, 0.5]),
        "timestamp": 1234.5
    }
    state = belief.update(sensor_data)

DEPENDENCIES
------------
- smbna.beliefs.base
- smbna.core.belief_state
- numpy

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

