"""
===============================================================================
SMBNA Beliefs - GPS-Only Belief Engine
===============================================================================

DESCRIPTION
-----------
GPS-only belief engine that maintains navigation state estimates based solely
on GPS measurements. This belief engine processes GPS position measurements and
maintains its own state estimate with associated confidence and covariance.

USAGE
-----
    from smbna.beliefs.gps import GPSBelief
    
    belief = GPSBelief()
    sensor_data = {
        "gps": {
            "position": np.array([10.0, 20.0]),
            "timestamp": 1234.5,
            "metadata": {"satellites": 8, "hdop": 1.2}
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

