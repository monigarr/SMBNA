"""
===============================================================================
SMBNA Core - Belief State Data Structure
===============================================================================

DESCRIPTION
-----------
Defines the BeliefState data structure used throughout the SMBNA system to
represent a belief engine's state estimate at a point in time. This immutable
data structure contains position, velocity, covariance, confidence, and metadata
for a single belief's navigation estimate.

USAGE
-----
    from smbna.core.belief_state import BeliefState
    import numpy as np
    
    state = BeliefState(
        belief_id="gps",
        position=np.array([10.0, 20.0]),
        velocity=np.array([1.0, 0.5]),
        covariance=np.eye(2) * 2.0,
        internal_confidence=0.95,
        timestamp=1234.5,
        metadata={"satellites": 8}
    )

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

from dataclasses import dataclass
import numpy as np

@dataclass
class BeliefState:
    belief_id: str
    position: np.ndarray
    velocity: np.ndarray
    covariance: np.ndarray
    internal_confidence: float
    timestamp: float
    metadata: dict
    
    def __eq__(self, other):
        """Equality comparison that handles numpy arrays properly."""
        if not isinstance(other, BeliefState):
            return False
        
        return (
            self.belief_id == other.belief_id
            and np.array_equal(self.position, other.position)
            and np.array_equal(self.velocity, other.velocity)
            and np.array_equal(self.covariance, other.covariance)
            and self.internal_confidence == other.internal_confidence
            and self.timestamp == other.timestamp
            and self.metadata == other.metadata
        )
