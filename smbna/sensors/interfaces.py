"""
===============================================================================
SMBNA Sensors - Sensor Interface Definitions
===============================================================================

DESCRIPTION
-----------
Defines abstract interfaces for sensor data acquisition in the SMBNA system.
Provides standardized interfaces for GPS, IMU, magnetic, and other sensors
to ensure consistent data formats and health monitoring across sensor types.

USAGE
-----
    from smbna.sensors.interfaces import SensorInterface, GPSInterface
    
    class CustomSensor(SensorInterface):
        def read(self) -> dict:
            # Implementation
            return {"position": np.array([10.0, 20.0])}
        
        def is_healthy(self) -> bool:
            # Implementation
            return True

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

