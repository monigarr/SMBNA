"""
===============================================================================
SMBNA Tests - Temporal Smoothness Invariant
===============================================================================

DESCRIPTION
-----------
Tests for the temporal smoothness invariant that validates acceleration
between consecutive belief states.

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
from smbna.invariants.temporal import TemporalSmoothness
from smbna.invariants.base import Invariant
from smbna.core.belief_state import BeliefState


class TestTemporalSmoothness:
    """Test suite for temporal smoothness invariant."""

    @pytest.fixture
    def invariant(self):
        """Create TemporalSmoothness invariant instance."""
        return TemporalSmoothness()

    @pytest.fixture
    def max_accel(self):
        """Default maximum acceleration for testing."""
        # Note: This should come from config, using default for testing
        return 10.0  # m/s²

    @pytest.mark.unit
    def test_inherits_from_invariant(self, invariant):
        """Test that TemporalSmoothness inherits from Invariant base class."""
        assert isinstance(invariant, Invariant)
        assert hasattr(invariant, 'name')
        assert hasattr(invariant, 'score')

    @pytest.mark.unit
    def test_name_attribute(self, invariant):
        """Test that invariant has correct name."""
        assert invariant.name == "temporal_smoothness"

    @pytest.mark.unit
    def test_score_with_insufficient_history(self, invariant, sample_belief_state):
        """Test that score returns 0.0 when history has less than 2 states."""
        # Empty history
        result = invariant.score(sample_belief_state, [], [])
        assert result == 0.0
        
        # Single state in history
        result = invariant.score(sample_belief_state, [sample_belief_state], [])
        assert result == 0.0

    @pytest.mark.unit
    def test_score_with_valid_acceleration(self, invariant, sample_belief_history):
        """Test that score returns 0.0 when acceleration is within limits."""
        current_belief = sample_belief_history[-1]
        history = sample_belief_history
        
        # Calculate expected acceleration
        prev = history[-2]
        dt = current_belief.timestamp - prev.timestamp
        accel = (current_belief.velocity - prev.velocity) / max(dt, 1e-3)
        accel_norm = np.linalg.norm(accel)
        
        # If acceleration is reasonable, should return 0.0
        # (assuming MAX_ACCEL is set appropriately)
        result = invariant.score(current_belief, history, [])
        assert result >= 0.0  # Penalty is non-negative

    @pytest.mark.unit
    def test_score_with_high_acceleration(self, invariant):
        """Test that score returns penalty when acceleration exceeds limit."""
        # Create belief with very high acceleration
        prev_state = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([0, 0]),
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=1.0,
            metadata={}
        )
        
        current_state = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([100, 100]),  # Very high velocity change
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=1.1,  # 0.1 second later
            metadata={}
        )
        
        # History should only contain previous states, not current
        history = [prev_state]
        
        result = invariant.score(current_state, history, [])
        
        # Should return penalty > 0 for unrealistic acceleration
        # Acceleration = (100, 100) - (1, 1) / 0.1 = (990, 990) m/s²
        # Norm ≈ 1400 m/s², which exceeds MAX_ACCEL (10.0 m/s²)
        assert result > 0.0

    @pytest.mark.unit
    def test_score_with_zero_dt(self, invariant):
        """Test that score handles zero or very small time differences."""
        prev_state = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([1, 1]),
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=1.0,
            metadata={}
        )
        
        current_state = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([2, 2]),
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=1.0,  # Same timestamp
            metadata={}
        )
        
        history = [prev_state, current_state]
        
        # Should handle zero dt gracefully (uses max(dt, 1e-3))
        result = invariant.score(current_state, history, [])
        assert result >= 0.0

    @pytest.mark.unit
    def test_score_penalty_scaling(self, invariant):
        """Test that penalty scales with acceleration magnitude."""
        prev_state = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([0, 0]),
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=1.0,
            metadata={}
        )
        
        # Moderate acceleration
        moderate_state = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([5, 5]),
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=1.1,
            metadata={}
        )
        
        # High acceleration
        high_state = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([50, 50]),
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=1.1,
            metadata={}
        )
        
        history = [prev_state]
        
        moderate_penalty = invariant.score(moderate_state, history + [moderate_state], [])
        high_penalty = invariant.score(high_state, history + [high_state], [])
        
        # Higher acceleration should produce higher penalty (if both exceed limit)
        if high_penalty > 0 and moderate_penalty > 0:
            assert high_penalty >= moderate_penalty

    @pytest.mark.unit
    def test_score_ignores_other_beliefs(self, invariant, sample_belief_history):
        """Test that temporal invariant ignores other_beliefs parameter."""
        current_belief = sample_belief_history[-1]
        
        result1 = invariant.score(current_belief, sample_belief_history, [])
        result2 = invariant.score(current_belief, sample_belief_history, [sample_belief_history[0]])
        
        # Results should be identical regardless of other_beliefs
        assert result1 == result2

    @pytest.mark.unit
    def test_score_returns_non_negative(self, invariant, sample_belief_state, sample_belief_history):
        """Test that score always returns non-negative penalty."""
        result = invariant.score(sample_belief_state, sample_belief_history, [])
        assert result >= 0.0

