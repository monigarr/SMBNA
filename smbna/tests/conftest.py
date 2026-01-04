"""
===============================================================================
SMBNA Tests - Shared Test Fixtures
===============================================================================

DESCRIPTION
-----------
Provides shared pytest fixtures for all SMBNA tests, including sample
belief states, sensor data, and test configurations.

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


@pytest.fixture
def sample_belief_state():
    """Create a sample belief state for testing."""
    return BeliefState(
        belief_id="gps",
        position=np.array([10.0, 20.0]),
        velocity=np.array([1.0, 0.5]),
        covariance=np.eye(2) * 2.0,
        internal_confidence=0.95,
        timestamp=1234.5,
        metadata={"satellites": 8, "hdop": 1.2}
    )


@pytest.fixture
def sample_belief_state_ins():
    """Create a sample INS belief state for testing."""
    return BeliefState(
        belief_id="ins",
        position=np.array([10.1, 20.1]),
        velocity=np.array([1.1, 0.6]),
        covariance=np.eye(2) * 1.5,
        internal_confidence=0.85,
        timestamp=1234.5,
        metadata={"drift_rate": 0.001}
    )


@pytest.fixture
def sample_belief_state_magnetic():
    """Create a sample magnetic belief state for testing."""
    return BeliefState(
        belief_id="magnetic",
        position=np.array([10.2, 20.2]),
        velocity=np.array([1.0, 0.5]),
        covariance=np.eye(2) * 3.0,
        internal_confidence=0.70,
        timestamp=1234.5,
        metadata={"field_match_quality": 0.8}
    )


@pytest.fixture
def sample_belief_history(sample_belief_state):
    """Create a sample belief history for temporal invariant testing."""
    # Create history with previous states
    prev_state = BeliefState(
        belief_id="gps",
        position=np.array([9.0, 19.0]),
        velocity=np.array([0.9, 0.4]),
        covariance=np.eye(2) * 2.0,
        internal_confidence=0.95,
        timestamp=1234.4,
        metadata={}
    )
    return [prev_state, sample_belief_state]


@pytest.fixture
def sample_sensor_data():
    """Create sample sensor data dictionary."""
    return {
        "gps": {
            "position": np.array([10.0, 20.0]),
            "timestamp": 1234.5,
            "metadata": {"satellites": 8, "hdop": 1.2}
        },
        "imu": {
            "accel": np.array([0.1, 0.2, 9.8]),
            "gyro": np.array([0.01, 0.02, 0.0]),
            "timestamp": 1234.5
        }
    }


@pytest.fixture
def sample_invariant_scores():
    """Create sample invariant penalty scores."""
    return {
        "gps": 0.5,
        "ins": 0.1,
        "magnetic": 0.3
    }


@pytest.fixture
def multiple_beliefs(sample_belief_state, sample_belief_state_ins, sample_belief_state_magnetic):
    """Create multiple belief states for arbitration testing."""
    return [sample_belief_state, sample_belief_state_ins, sample_belief_state_magnetic]


@pytest.fixture
def sim_config():
    """Create a simulation configuration for testing."""
    from smbna.simulation.run_simulation import SimConfig
    return SimConfig(
        dt=0.1,
        total_time=10.0,  # Short for testing
        gps_noise=2.0,
        imu_noise=0.05,
        gps_dropout_prob=0.2,
        spoof_bias=15.0,
        seed=42
    )


@pytest.fixture
def numpy_random_seed():
    """Set numpy random seed for reproducible tests."""
    np.random.seed(42)
    yield
    # Reset seed after test
    np.random.seed(None)

