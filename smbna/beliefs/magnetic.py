"""
===============================================================================
SMBNA Beliefs - Magnetic Map-Matching Belief Engine
===============================================================================

DESCRIPTION
-----------
Magnetic map-matching belief engine that estimates position by matching
measured magnetic field values against a magnetic field map. Uses the Earth's
magnetic field variations for navigation in GPS-denied environments.

USAGE
-----
    from smbna.beliefs.magnetic import MagneticBelief
    
    belief = MagneticBelief(map_file="data/magnetic_map.npy")
    sensor_data = {
        "magnetic": {
            "field": np.array([20000.0, 5000.0, 45000.0]),  # nT
            "timestamp": 1234.5
        }
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

