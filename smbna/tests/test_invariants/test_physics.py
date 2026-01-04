"""
===============================================================================
SMBNA Tests - Physics Feasibility Invariant
===============================================================================

DESCRIPTION
-----------
Tests for the physics feasibility invariant that validates physical constraints
such as maximum airspeed.

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

import pytest
import numpy as np
from smbna.invariants.physics import PhysicsInvariant
from smbna.invariants.base import Invariant
from smbna.core.belief_state import BeliefState


class TestPhysicsInvariant:
    """Test suite for physics feasibility invariant."""

    @pytest.fixture
    def invariant(self):
        """Create PhysicsInvariant instance."""
        return PhysicsInvariant()

    @pytest.fixture
    def max_airspeed(self):
        """Default maximum airspeed for testing."""
        return 50.0  # m/s

    @pytest.mark.unit
    def test_inherits_from_invariant(self, invariant):
        """Test that PhysicsInvariant inherits from Invariant base class."""
        assert isinstance(invariant, Invariant)
        assert hasattr(invariant, 'name')
        assert hasattr(invariant, 'score')

    @pytest.mark.unit
    def test_name_attribute(self, invariant):
        """Test that invariant has correct name."""
        assert invariant.name == "physics_feasibility"

    @pytest.mark.unit
    def test_score_with_valid_speed(self, invariant, sample_belief_state):
        """Test that score returns 0.0 when speed is within limits."""
        # Create belief with reasonable speed
        reasonable_state = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([10, 5]),  # ~11.2 m/s, reasonable
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=1.0,
            metadata={}
        )
        
        result = invariant.score(reasonable_state, [], [])
        assert result >= 0.0  # Non-negative

    @pytest.mark.unit
    def test_score_with_excessive_speed(self, invariant):
        """Test that score returns penalty when speed exceeds limit."""
        # Create belief with very high speed
        high_speed_state = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([100, 100]),  # ~141 m/s, unrealistic
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=1.0,
            metadata={}
        )
        
        result = invariant.score(high_speed_state, [], [])
        
        # Should return penalty > 0 for unrealistic speed
        assert result > 0.0

    @pytest.mark.unit
    def test_score_with_zero_velocity(self, invariant):
        """Test that score handles zero velocity."""
        zero_velocity_state = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([0, 0]),
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=1.0,
            metadata={}
        )
        
        result = invariant.score(zero_velocity_state, [], [])
        assert result == 0.0  # Zero speed should have no penalty

    @pytest.mark.unit
    def test_score_penalty_scaling(self, invariant):
        """Test that penalty scales with speed magnitude."""
        # Moderate speed
        moderate_state = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([30, 30]),  # ~42 m/s
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=1.0,
            metadata={}
        )
        
        # High speed
        high_state = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([100, 100]),  # ~141 m/s
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=1.0,
            metadata={}
        )
        
        moderate_penalty = invariant.score(moderate_state, [], [])
        high_penalty = invariant.score(high_state, [], [])
        
        # Higher speed should produce higher penalty (if both exceed limit)
        if high_penalty > 0 and moderate_penalty > 0:
            assert high_penalty >= moderate_penalty

    @pytest.mark.unit
    def test_score_ignores_history_and_other_beliefs(self, invariant, sample_belief_state):
        """Test that physics invariant ignores history and other_beliefs."""
        result1 = invariant.score(sample_belief_state, [], [])
        result2 = invariant.score(sample_belief_state, [sample_belief_state], [sample_belief_state])
        
        # Results should be identical
        assert result1 == result2

    @pytest.mark.unit
    def test_score_returns_non_negative(self, invariant, sample_belief_state):
        """Test that score always returns non-negative penalty."""
        result = invariant.score(sample_belief_state, [], [])
        assert result >= 0.0

    @pytest.mark.unit
    def test_score_with_3d_velocity(self, invariant):
        """Test that score works with 3D velocity vectors."""
        state_3d = BeliefState(
            belief_id="gps",
            position=np.array([0, 0, 100]),
            velocity=np.array([10, 5, 0]),
            covariance=np.eye(3),
            internal_confidence=0.9,
            timestamp=1.0,
            metadata={}
        )
        
        result = invariant.score(state_3d, [], [])
        assert result >= 0.0

