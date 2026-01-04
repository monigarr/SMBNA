"""
===============================================================================
SMBNA - Secure Multi-Belief Navigation Arbitration
===============================================================================

DESCRIPTION
-----------
SMBNA is a belief-centric navigation framework for autonomous systems operating
in GPS-degraded, GPS-denied, and adversarial environments. The system maintains
parallel independent navigation beliefs and uses invariant-based consistency
checks to arbitrate trust and make safe navigation decisions.

This package provides the core navigation arbitration system with support for
multiple belief engines, invariant validation, and explicit refusal mechanisms.

USAGE
-----
    from smbna.core.pipeline import Pipeline
    from smbna.beliefs.gps import GPSBelief
    from smbna.beliefs.ins import INSBelief
    
    # Create pipeline
    pipeline = Pipeline()
    pipeline.add_belief(GPSBelief())
    pipeline.add_belief(INSBelief())
    
    # Process sensor data
    sensor_data = {"gps": {...}, "imu": {...}}
    result = pipeline.process(sensor_data)

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

LICENSE
-------
This project is released for research and evaluation purposes.
Contains no classified material and no restricted signal processing.

VERSION
-------
1.0.0
===============================================================================
"""

