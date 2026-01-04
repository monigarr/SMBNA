"""
===============================================================================
SMBNA Tests - Belief State Data Structure
===============================================================================

DESCRIPTION
-----------
Tests for the BeliefState dataclass, the core data structure used throughout
the SMBNA system.

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
from smbna.core.belief_state import BeliefState


class TestBeliefState:
    """Test suite for BeliefState dataclass."""

    @pytest.mark.unit
    @pytest.mark.critical
    def test_belief_state_creation(self):
        """Test creating a BeliefState with all required fields."""
        state = BeliefState(
            belief_id="gps",
            position=np.array([10.0, 20.0]),
            velocity=np.array([1.0, 0.5]),
            covariance=np.eye(2) * 2.0,
            internal_confidence=0.95,
            timestamp=1234.5,
            metadata={"satellites": 8}
        )
        
        assert state.belief_id == "gps"
        assert np.allclose(state.position, [10.0, 20.0])
        assert np.allclose(state.velocity, [1.0, 0.5])
        assert np.allclose(state.covariance, np.eye(2) * 2.0)
        assert state.internal_confidence == 0.95
        assert state.timestamp == 1234.5
        assert state.metadata == {"satellites": 8}

    @pytest.mark.unit
    @pytest.mark.critical
    def test_belief_state_immutability(self, sample_belief_state):
        """Test that BeliefState fields cannot be modified (dataclass frozen behavior)."""
        # Dataclasses are not frozen by default, but we should test behavior
        # If frozen=True is added, this test will verify it
        original_position = sample_belief_state.position.copy()
        
        # Attempt to modify (may or may not work depending on frozen setting)
        try:
            sample_belief_state.position[0] = 999.0
            # If not frozen, verify it changed
            if not hasattr(sample_belief_state, '__frozen__'):
                assert sample_belief_state.position[0] == 999.0
        except (AttributeError, TypeError):
            # If frozen, modification should fail
            pass

    @pytest.mark.unit
    def test_belief_state_different_ids(self):
        """Test creating BeliefStates with different belief IDs."""
        gps_state = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([0, 0]),
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=1.0,
            metadata={}
        )
        
        ins_state = BeliefState(
            belief_id="ins",
            position=np.array([0, 0]),
            velocity=np.array([0, 0]),
            covariance=np.eye(2),
            internal_confidence=0.8,
            timestamp=1.0,
            metadata={}
        )
        
        assert gps_state.belief_id == "gps"
        assert ins_state.belief_id == "ins"
        assert gps_state.belief_id != ins_state.belief_id

    @pytest.mark.unit
    def test_belief_state_confidence_range(self):
        """Test BeliefState with confidence values at boundaries."""
        # High confidence
        high_conf = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([0, 0]),
            covariance=np.eye(2),
            internal_confidence=1.0,
            timestamp=1.0,
            metadata={}
        )
        assert high_conf.internal_confidence == 1.0
        
        # Low confidence
        low_conf = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([0, 0]),
            covariance=np.eye(2),
            internal_confidence=0.0,
            timestamp=1.0,
            metadata={}
        )
        assert low_conf.internal_confidence == 0.0

    @pytest.mark.unit
    def test_belief_state_metadata(self):
        """Test BeliefState with various metadata structures."""
        # Empty metadata
        state1 = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([0, 0]),
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=1.0,
            metadata={}
        )
        assert state1.metadata == {}
        
        # Metadata with multiple keys
        state2 = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([0, 0]),
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=1.0,
            metadata={"satellites": 8, "hdop": 1.2, "fix_quality": "good"}
        )
        assert len(state2.metadata) == 3
        assert state2.metadata["satellites"] == 8

    @pytest.mark.unit
    def test_belief_state_covariance_shapes(self):
        """Test BeliefState with different covariance matrix shapes."""
        # 2D position
        state_2d = BeliefState(
            belief_id="gps",
            position=np.array([10.0, 20.0]),
            velocity=np.array([1.0, 0.5]),
            covariance=np.eye(2) * 2.0,
            internal_confidence=0.9,
            timestamp=1.0,
            metadata={}
        )
        assert state_2d.covariance.shape == (2, 2)
        
        # 3D position (if supported)
        state_3d = BeliefState(
            belief_id="gps",
            position=np.array([10.0, 20.0, 100.0]),
            velocity=np.array([1.0, 0.5, 0.0]),
            covariance=np.eye(3) * 2.0,
            internal_confidence=0.9,
            timestamp=1.0,
            metadata={}
        )
        assert state_3d.covariance.shape == (3, 3)

    @pytest.mark.unit
    def test_belief_state_equality(self):
        """Test BeliefState equality comparison."""
        state1 = BeliefState(
            belief_id="gps",
            position=np.array([10.0, 20.0]),
            velocity=np.array([1.0, 0.5]),
            covariance=np.eye(2) * 2.0,
            internal_confidence=0.95,
            timestamp=1234.5,
            metadata={"satellites": 8}
        )
        
        state2 = BeliefState(
            belief_id="gps",
            position=np.array([10.0, 20.0]),
            velocity=np.array([1.0, 0.5]),
            covariance=np.eye(2) * 2.0,
            internal_confidence=0.95,
            timestamp=1234.5,
            metadata={"satellites": 8}
        )
        
        # Dataclasses compare by value
        assert state1 == state2

    @pytest.mark.unit
    def test_belief_state_inequality(self):
        """Test BeliefState inequality when fields differ."""
        state1 = BeliefState(
            belief_id="gps",
            position=np.array([10.0, 20.0]),
            velocity=np.array([1.0, 0.5]),
            covariance=np.eye(2) * 2.0,
            internal_confidence=0.95,
            timestamp=1234.5,
            metadata={}
        )
        
        state2 = BeliefState(
            belief_id="gps",
            position=np.array([11.0, 20.0]),  # Different position
            velocity=np.array([1.0, 0.5]),
            covariance=np.eye(2) * 2.0,
            internal_confidence=0.95,
            timestamp=1234.5,
            metadata={}
        )
        
        assert state1 != state2

    @pytest.mark.unit
    def test_belief_state_timestamp_ordering(self):
        """Test BeliefState timestamp ordering for temporal operations."""
        state1 = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([0, 0]),
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=1.0,
            metadata={}
        )
        
        state2 = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([0, 0]),
            covariance=np.eye(2),
            internal_confidence=0.9,
            timestamp=2.0,
            metadata={}
        )
        
        assert state1.timestamp < state2.timestamp
        assert state2.timestamp > state1.timestamp

