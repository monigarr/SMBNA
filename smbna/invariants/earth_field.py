"""
===============================================================================
SMBNA Invariants - Earth Magnetic Field Consistency Invariant
===============================================================================

DESCRIPTION
-----------
Validates that measured magnetic field values are consistent with the expected
Earth magnetic field at the estimated position. Detects magnetic anomalies,
sensor failures, or position errors by comparing measured field against
geophysical models (e.g., IGRF).

USAGE
-----
    from smbna.invariants.earth_field import EarthFieldInvariant
    
    invariant = EarthFieldInvariant()
    penalty = invariant.score(belief, belief_history, other_beliefs)
    
    # penalty = 0.0 if field is consistent
    # penalty > 0.0 if field deviation exceeds threshold

PARAMETERS
----------
MAX_FIELD_ANGLE : float
    Maximum allowed angle between expected and measured field (radians)

DEPENDENCIES
------------
- Magnetic field model (e.g., IGRF)
- smbna.invariants.base
- smbna.core.belief_state

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

class EarthFieldInvariant(Invariant):
    name = "earth_field_structure"

    def score(self, belief, history, _):
        expected_field = lookup_magnetic_field(belief.position)

        measured_field = belief.metadata.get("mag_vector")
        if measured_field is None:
            return 0.0

        angle = angle_between(expected_field, measured_field)

        if angle > MAX_FIELD_ANGLE:
            return angle / MAX_FIELD_ANGLE

        return 0.0
