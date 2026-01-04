"""
===============================================================================
SMBNA Simulation - GPS Spoofing Models
===============================================================================

DESCRIPTION
-----------
Implements GPS spoofing attack models for simulation and evaluation. Provides
various spoofing strategies including bias injection, gradual drift, and
coordinated attacks to test SMBNA's detection and refusal capabilities.

USAGE
-----
    from smbna.simulation.spoofing import apply_spoofing
    
    spoofed_position = apply_spoofing(
        true_position,
        spoof_type="bias",
        bias_magnitude=15.0
    )

SPOOFING TYPES
--------------
- bias: Constant bias injection
- drift: Gradual position drift
- coordinated: Coordinated multi-satellite attack

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

