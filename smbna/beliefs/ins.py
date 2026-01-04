"""
===============================================================================
SMBNA Beliefs - Inertial Navigation System (INS) Belief Engine
===============================================================================

DESCRIPTION
-----------
INS belief engine that maintains navigation state estimates based on inertial
measurement unit (IMU) data. Processes accelerometer and gyroscope
measurements to estimate position, velocity, and attitude through dead
reckoning.

USAGE
-----
    from smbna.beliefs.ins import INSBelief
    
    belief = INSBelief()
    sensor_data = {
        "imu": {
            "accel": np.array([0.1, 0.2, 9.8]),
            "gyro": np.array([0.01, 0.02, 0.0]),
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

