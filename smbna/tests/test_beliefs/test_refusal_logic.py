"""
===============================================================================
SMBNA Tests - Refusal Logic
===============================================================================

DESCRIPTION
-----------
Tests for the navigation refusal logic, a critical safety mechanism that
determines when the system should refuse to provide position estimates.

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
from smbna.beliefs.refusal_logic import should_refuse_navigation


class TestRefusalLogic:
    """Test suite for navigation refusal logic."""

    @pytest.mark.unit
    @pytest.mark.critical
    def test_refusal_below_threshold(self):
        """Test that refusal returns False when innovation is below threshold."""
        result = should_refuse_navigation(15.0, threshold=20.0)
        assert result is False

    @pytest.mark.unit
    @pytest.mark.critical
    def test_refusal_above_threshold(self):
        """Test that refusal returns True when innovation exceeds threshold."""
        result = should_refuse_navigation(25.0, threshold=20.0)
        assert result is True

    @pytest.mark.unit
    @pytest.mark.critical
    def test_refusal_at_threshold(self):
        """Test boundary condition at threshold (should not refuse at exact threshold)."""
        result = should_refuse_navigation(20.0, threshold=20.0)
        assert result is False

    @pytest.mark.unit
    @pytest.mark.critical
    def test_refusal_with_nan(self):
        """Test that NaN innovation returns False (handles missing measurements)."""
        result = should_refuse_navigation(np.nan, threshold=20.0)
        assert result is False

    @pytest.mark.unit
    @pytest.mark.critical
    def test_refusal_with_zero(self):
        """Test that zero innovation does not trigger refusal."""
        result = should_refuse_navigation(0.0, threshold=20.0)
        assert result is False

    @pytest.mark.unit
    @pytest.mark.critical
    def test_refusal_with_very_large_innovation(self):
        """Test that very large innovations trigger refusal."""
        result = should_refuse_navigation(100.0, threshold=20.0)
        assert result is True

    @pytest.mark.unit
    @pytest.mark.critical
    def test_refusal_with_custom_threshold(self):
        """Test refusal with custom threshold values."""
        # Lower threshold
        result = should_refuse_navigation(15.0, threshold=10.0)
        assert result is True
        
        # Higher threshold
        result = should_refuse_navigation(15.0, threshold=30.0)
        assert result is False

    @pytest.mark.unit
    @pytest.mark.critical
    @pytest.mark.parametrize("innovation,threshold,expected", [
        (15.0, 20.0, False),   # Below threshold
        (25.0, 20.0, True),    # Above threshold
        (20.0, 20.0, False),   # At threshold
        (0.0, 20.0, False),    # Zero
        (100.0, 20.0, True),   # Very large
        (19.999, 20.0, False), # Just below
        (20.001, 20.0, True),  # Just above
    ])
    def test_refusal_parametrized(self, innovation, threshold, expected):
        """Parametrized test for refusal logic with various inputs."""
        result = should_refuse_navigation(innovation, threshold)
        assert result == expected, f"Failed for innovation={innovation}, threshold={threshold}"

    @pytest.mark.unit
    @pytest.mark.critical
    def test_refusal_default_threshold(self):
        """Test that default threshold (20.0) is used when not specified."""
        # Should use default threshold of 20.0
        result_below = should_refuse_navigation(15.0)
        result_above = should_refuse_navigation(25.0)
        
        assert result_below is False
        assert result_above is True

    @pytest.mark.unit
    @pytest.mark.critical
    def test_refusal_with_negative_innovation(self):
        """Test that negative innovation values are handled (should not refuse)."""
        # Innovation norm should always be positive, but test edge case
        result = should_refuse_navigation(-5.0, threshold=20.0)
        # Negative values are below threshold, so should not refuse
        assert result is False

    @pytest.mark.unit
    @pytest.mark.critical
    def test_refusal_with_infinity(self):
        """Test that infinity values are handled."""
        result = should_refuse_navigation(np.inf, threshold=20.0)
        assert result is True

    @pytest.mark.unit
    @pytest.mark.critical
    def test_refusal_consistency(self):
        """Test that refusal logic is consistent across multiple calls."""
        innovation = 25.0
        threshold = 20.0
        
        results = [should_refuse_navigation(innovation, threshold) for _ in range(10)]
        
        # All results should be the same
        assert all(r == results[0] for r in results)
        assert results[0] is True

