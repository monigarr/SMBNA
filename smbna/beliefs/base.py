"""
===============================================================================
SMBNA Beliefs - Base Belief Engine Class
===============================================================================

DESCRIPTION
-----------
Abstract base class for all belief engines in the SMBNA system. Defines the
interface that all belief engines must implement, including state updates,
state retrieval, and reset functionality.

Belief engines operate independently and maintain their own navigation state
estimates without consuming outputs from other beliefs.

USAGE
-----
    from smbna.beliefs.base import Belief
    from smbna.core.belief_state import BeliefState
    
    class CustomBelief(Belief):
        def update(self, sensor_data: dict) -> BeliefState:
            # Implementation
            return BeliefState(...)
        
        def get_state(self) -> BeliefState:
            # Implementation
            return BeliefState(...)
        
        def reset(self) -> None:
            # Implementation
            pass

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

