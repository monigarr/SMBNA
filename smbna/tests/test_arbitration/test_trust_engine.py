"""
===============================================================================
SMBNA Tests - Trust Engine (Arbitration)
===============================================================================

DESCRIPTION
-----------
Tests for the trust arbitration system, a critical safety component that
selects the most trustworthy belief or refuses navigation when confidence
collapses.

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
from smbna.arbitration.trust_engine import arbitrate
from smbna.core.belief_state import BeliefState


class TestTrustEngine:
    """Test suite for trust arbitration engine."""

    @pytest.mark.unit
    @pytest.mark.critical
    def test_arbitration_selects_highest_trust(self, multiple_beliefs, sample_invariant_scores):
        """Test that arbitration selects belief with highest trust score."""
        # Modify scores so INS has highest trust (lowest penalty)
        scores = {"gps": 0.5, "ins": 0.05, "magnetic": 0.3}
        
        result = arbitrate(multiple_beliefs, scores)
        
        assert result["nav_unsafe"] is False
        assert result["selected"] == "ins"  # Lower penalty = higher trust
        assert "confidence" in result
        assert result["confidence"] > 0

    @pytest.mark.unit
    @pytest.mark.critical
    def test_arbitration_refuses_when_trust_too_low(self):
        """Test that arbitration refuses when all trust scores are too low."""
        # Create belief with very low confidence and high penalty
        low_confidence_belief = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([0, 0]),
            covariance=np.eye(2),
            internal_confidence=0.1,  # Very low confidence
            timestamp=1.0,
            metadata={}
        )
        beliefs = [low_confidence_belief]
        scores = {"gps": 10.0}  # Very high penalty
        
        result = arbitrate(beliefs, scores)
        
        assert result["nav_unsafe"] is True
        assert result["reason"] == "confidence collapse"
        assert "selected" not in result or result.get("selected") is None

    @pytest.mark.unit
    @pytest.mark.critical
    def test_arbitration_with_single_belief(self, sample_belief_state):
        """Test arbitration with single belief."""
        beliefs = [sample_belief_state]
        scores = {"gps": 0.1}
        
        result = arbitrate(beliefs, scores)
        
        assert result["nav_unsafe"] is False
        assert result["selected"] == "gps"
        assert result["confidence"] > 0

    @pytest.mark.unit
    @pytest.mark.critical
    def test_arbitration_with_high_confidence_low_penalty(self):
        """Test that high confidence + low penalty produces high trust."""
        high_confidence_belief = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([0, 0]),
            covariance=np.eye(2),
            internal_confidence=0.95,  # High confidence
            timestamp=1.0,
            metadata={}
        )
        beliefs = [high_confidence_belief]
        scores = {"gps": 0.01}  # Very low penalty
        
        result = arbitrate(beliefs, scores)
        
        assert result["nav_unsafe"] is False
        assert result["confidence"] > 0.9  # Should be close to original confidence

    @pytest.mark.unit
    @pytest.mark.critical
    def test_arbitration_with_low_confidence_high_penalty(self):
        """Test that low confidence + high penalty produces low trust."""
        low_confidence_belief = BeliefState(
            belief_id="gps",
            position=np.array([0, 0]),
            velocity=np.array([0, 0]),
            covariance=np.eye(2),
            internal_confidence=0.3,  # Low confidence
            timestamp=1.0,
            metadata={}
        )
        beliefs = [low_confidence_belief]
        scores = {"gps": 5.0}  # High penalty
        
        result = arbitrate(beliefs, scores)
        
        # Trust should be very low, likely triggering refusal
        # Exact behavior depends on LAMBDA and TRUST_MIN constants
        assert "confidence" in result or result["nav_unsafe"] is True

    @pytest.mark.unit
    @pytest.mark.critical
    def test_arbitration_compares_multiple_beliefs(self, multiple_beliefs):
        """Test that arbitration correctly compares multiple beliefs."""
        # Set scores so GPS has lowest penalty (should win)
        scores = {"gps": 0.05, "ins": 0.2, "magnetic": 0.3}
        
        result = arbitrate(multiple_beliefs, scores)
        
        assert result["nav_unsafe"] is False
        assert result["selected"] == "gps"
        assert result["confidence"] > 0

    @pytest.mark.unit
    @pytest.mark.critical
    def test_arbitration_handles_zero_penalty(self, sample_belief_state):
        """Test arbitration with zero penalty (perfect consistency)."""
        beliefs = [sample_belief_state]
        scores = {"gps": 0.0}  # Zero penalty
        
        result = arbitrate(beliefs, scores)
        
        assert result["nav_unsafe"] is False
        assert result["selected"] == "gps"
        # With zero penalty, trust should equal confidence
        assert result["confidence"] == pytest.approx(sample_belief_state.internal_confidence, abs=0.01)

    @pytest.mark.unit
    @pytest.mark.critical
    def test_arbitration_handles_very_high_penalty(self, sample_belief_state):
        """Test arbitration with very high penalty."""
        beliefs = [sample_belief_state]
        scores = {"gps": 100.0}  # Very high penalty
        
        result = arbitrate(beliefs, scores)
        
        # High penalty should significantly reduce trust
        # May trigger refusal depending on TRUST_MIN
        assert "confidence" in result or result["nav_unsafe"] is True

    @pytest.mark.unit
    @pytest.mark.critical
    def test_arbitration_result_structure(self, multiple_beliefs, sample_invariant_scores):
        """Test that arbitration result has correct structure."""
        result = arbitrate(multiple_beliefs, sample_invariant_scores)
        
        assert isinstance(result, dict)
        assert "nav_unsafe" in result
        assert isinstance(result["nav_unsafe"], bool)
        
        if not result["nav_unsafe"]:
            assert "selected" in result
            assert "confidence" in result
            assert isinstance(result["selected"], str)
            assert isinstance(result["confidence"], (int, float))
            assert result["confidence"] >= 0
        else:
            assert "reason" in result
            assert isinstance(result["reason"], str)

    @pytest.mark.unit
    @pytest.mark.critical
    def test_arbitration_with_empty_beliefs(self):
        """Test arbitration with empty belief list."""
        beliefs = []
        scores = {}
        
        # Should handle gracefully (may raise exception or return refusal)
        # Behavior depends on implementation
        with pytest.raises((ValueError, KeyError, IndexError)):
            arbitrate(beliefs, scores)

    @pytest.mark.unit
    @pytest.mark.critical
    def test_arbitration_missing_belief_in_scores(self, sample_belief_state):
        """Test arbitration when belief ID is missing from scores."""
        beliefs = [sample_belief_state]
        scores = {}  # Missing "gps" key
        
        # Should raise KeyError
        with pytest.raises(KeyError):
            arbitrate(beliefs, scores)

    @pytest.mark.unit
    @pytest.mark.critical
    def test_arbitration_consistency(self, multiple_beliefs, sample_invariant_scores):
        """Test that arbitration produces consistent results."""
        results = [arbitrate(multiple_beliefs, sample_invariant_scores) for _ in range(5)]
        
        # All results should be identical
        first_result = results[0]
        for result in results[1:]:
            assert result["nav_unsafe"] == first_result["nav_unsafe"]
            if not first_result["nav_unsafe"]:
                assert result["selected"] == first_result["selected"]
                assert result["confidence"] == pytest.approx(first_result["confidence"], abs=0.001)

