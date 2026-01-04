"""
===============================================================================
SMBNA Simulation - Test Scenarios
===============================================================================

DESCRIPTION
-----------
Defines standard test scenarios for evaluating SMBNA performance under various
conditions including GPS degradation, GPS denial, spoofing attacks, and
nominal operation. Provides reproducible scenario configurations.

USAGE
-----
    from smbna.simulation.scenarios import get_scenario
    
    scenario = get_scenario("gps_spoofing")
    config = scenario.get_config()

AVAILABLE SCENARIOS
-------------------
- gps_degraded: GPS with high noise and dropouts
- gps_denied: Complete GPS unavailability
- gps_spoofing: GPS spoofing attacks
- nominal: Normal operating conditions

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

