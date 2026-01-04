"""
===============================================================================
SMBNA Core - Main Processing Pipeline
===============================================================================

DESCRIPTION
-----------
Orchestrates the complete SMBNA navigation pipeline, coordinating belief
updates, invariant evaluation, and trust arbitration. This is the primary
interface for processing sensor data through the multi-belief navigation
system.

The pipeline maintains belief engines, invariant validators, and coordinates
the flow from sensor data acquisition through to navigation decision output.

USAGE
-----
    from smbna.core.pipeline import Pipeline
    from smbna.beliefs.gps import GPSBelief
    from smbna.beliefs.ins import INSBelief
    
    # Initialize pipeline
    pipeline = Pipeline()
    
    # Register belief engines
    pipeline.add_belief(GPSBelief())
    pipeline.add_belief(INSBelief())
    
    # Process sensor data
    sensor_data = {
        "gps": {"position": np.array([10.0, 20.0])},
        "imu": {"accel": np.array([0.1, 0.2])}
    }
    result = pipeline.process(sensor_data)
    
    # Access results
    decision = result["decision"]
    beliefs = result["beliefs"]

DEPENDENCIES
------------
- smbna.core.belief_state
- smbna.beliefs.base
- smbna.invariants.base
- smbna.arbitration.trust_engine

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

