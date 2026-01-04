# SMBNA API Reference

**Version:** 1.0  
**Last Updated:** 2026

---

## Overview

This document provides a surface-level API reference for the SMBNA framework. It covers public interfaces, function signatures, and intended usage patterns.

---

## Core Data Structures

### `BeliefState`

**Location:** `smbna.core.belief_state`

**Description:** Immutable data structure representing a belief's state estimate at a point in time.

```python
@dataclass
class BeliefState:
    belief_id: str
    position: np.ndarray          # [x, y] or [x, y, z]
    velocity: np.ndarray          # [vx, vy] or [vx, vy, vz]
    covariance: np.ndarray        # State covariance matrix
    internal_confidence: float    # Belief's self-assessed confidence [0, 1]
    timestamp: float              # Unix timestamp or simulation time
    metadata: dict                # Additional belief-specific data
```

**Fields:**
- `belief_id`: Unique identifier for the belief engine (e.g., "gps", "ins", "magnetic")
- `position`: Position estimate as numpy array
- `velocity`: Velocity estimate as numpy array
- `covariance`: Covariance matrix representing uncertainty
- `internal_confidence`: Belief's confidence in its own estimate [0.0, 1.0]
- `timestamp`: Time at which this state was computed
- `metadata`: Dictionary for belief-specific information

**Example:**
```python
from smbna.core.belief_state import BeliefState
import numpy as np

state = BeliefState(
    belief_id="gps",
    position=np.array([10.5, 20.3]),
    velocity=np.array([1.0, 0.5]),
    covariance=np.eye(2) * 2.0,
    internal_confidence=0.95,
    timestamp=1234567890.0,
    metadata={"satellites": 8}
)
```

---

## Belief Engine API

### Base Belief Class

**Location:** `smbna.beliefs.base`

**Description:** Abstract base class for all belief engines.

```python
class Belief:
    def update(self, sensor_data: dict) -> BeliefState:
        """
        Update belief state with new sensor data.
        
        Parameters
        ----------
        sensor_data : dict
            Dictionary containing sensor measurements
            
        Returns
        -------
        BeliefState
            Updated belief state
        """
        raise NotImplementedError
    
    def get_state(self) -> BeliefState:
        """
        Get current belief state without updating.
        
        Returns
        -------
        BeliefState
            Current belief state
        """
        raise NotImplementedError
    
    def reset(self) -> None:
        """
        Reset belief to initial state.
        """
        raise NotImplementedError
```

### GPS Belief

**Location:** `smbna.beliefs.gps`

**Usage:**
```python
from smbna.beliefs.gps import GPSBelief

gps_belief = GPSBelief()
sensor_data = {"gps": {"position": np.array([10.0, 20.0]), "timestamp": 1234.5}}
state = gps_belief.update(sensor_data)
```

### INS Belief

**Location:** `smbna.beliefs.ins`

**Usage:**
```python
from smbna.beliefs.ins import INSBelief

ins_belief = INSBelief()
sensor_data = {"imu": {"accel": np.array([0.1, 0.2]), "gyro": np.array([0.01, 0.02])}}
state = ins_belief.update(sensor_data)
```

---

## Invariant API

### Base Invariant Class

**Location:** `smbna.invariants.base`

**Description:** Abstract base class for all invariant validators.

```python
class Invariant:
    def evaluate(self, belief_state: BeliefState, history: List[BeliefState]) -> float:
        """
        Evaluate invariant and return penalty score.
        
        Parameters
        ----------
        belief_state : BeliefState
            Current belief state to evaluate
        history : List[BeliefState]
            Historical belief states for temporal checks
            
        Returns
        -------
        float
            Penalty score (0.0 = no violation, higher = more violation)
        """
        raise NotImplementedError
```

### Temporal Invariant

**Location:** `smbna.invariants.temporal`

**Purpose:** Checks for unrealistic acceleration between timesteps.

**Usage:**
```python
from smbna.invariants.temporal import TemporalInvariant

invariant = TemporalInvariant()
penalty = invariant.evaluate(belief_state, history)
```

### Physics Invariant

**Location:** `smbna.invariants.physics`

**Purpose:** Validates physical constraints (velocity, acceleration limits).

**Usage:**
```python
from smbna.invariants.physics import PhysicsInvariant

invariant = PhysicsInvariant()
penalty = invariant.evaluate(belief_state, history)
```

---

## Pipeline API

### Pipeline Class

**Location:** `smbna.core.pipeline`

**Description:** Main orchestration component for the SMBNA system.

```python
class Pipeline:
    def __init__(self):
        """Initialize pipeline."""
        pass
    
    def add_belief(self, belief: Belief) -> None:
        """
        Add a belief engine to the pipeline.
        
        Parameters
        ----------
        belief : Belief
            Belief engine instance
        """
        pass
    
    def add_invariant(self, invariant: Invariant) -> None:
        """
        Add an invariant validator to the pipeline.
        
        Parameters
        ----------
        invariant : Invariant
            Invariant validator instance
        """
        pass
    
    def process(self, sensor_data: dict) -> dict:
        """
        Process sensor data and return navigation decision.
        
        Parameters
        ----------
        sensor_data : dict
            Dictionary containing sensor measurements
            
        Returns
        -------
        dict
            Navigation decision with keys:
            - "decision": dict with selected belief, confidence, nav_unsafe flag
            - "beliefs": list of BeliefState objects
            - "invariant_scores": dict of invariant penalty scores
        """
        pass
```

**Usage:**
```python
from smbna.core.pipeline import Pipeline
from smbna.beliefs.gps import GPSBelief
from smbna.beliefs.ins import INSBelief

pipeline = Pipeline()
pipeline.add_belief(GPSBelief())
pipeline.add_belief(INSBelief())

sensor_data = {
    "gps": {"position": np.array([10.0, 20.0])},
    "imu": {"accel": np.array([0.1, 0.2])}
}

result = pipeline.process(sensor_data)
decision = result["decision"]
```

---

## Simulation API

### Run Simulation

**Location:** `smbna.simulation.run_simulation`

**Function:** `run_simulation`

**Description:** Run a single simulation scenario.

```python
def run_simulation(
    time: float = 300.0,
    seed: int = 42,
    scenario: str = "normal"
) -> dict:
    """
    Run a single simulation scenario.
    
    Parameters
    ----------
    time : float
        Simulation duration in seconds
    seed : int
        Random seed for reproducibility
    scenario : str
        Scenario name ("normal", "spoofed_gps", "degraded_gps", etc.)
        
    Returns
    -------
    dict
        Simulation results with trajectory, errors, and metrics
    """
    pass
```

**Usage:**
```python
from smbna.simulation.run_simulation import run_simulation

results = run_simulation(time=300.0, seed=42, scenario="spoofed_gps")
```

### Run Monte Carlo

**Location:** `smbna.simulation.run_monte_carlo`

**Function:** `run_monte_carlo`

**Description:** Run Monte Carlo evaluation across multiple seeds.

```python
def run_monte_carlo(
    runs: int = 50,
    time: float = 300.0,
    scenario: str = "normal"
) -> dict:
    """
    Run Monte Carlo evaluation.
    
    Parameters
    ----------
    runs : int
        Number of Monte Carlo runs
    time : float
        Simulation duration per run
    scenario : str
        Scenario name
        
    Returns
    -------
    dict
        Aggregated results across all runs
    """
    pass
```

---

## Utility Functions

### Refusal Logic

**Location:** `smbna.beliefs.refusal_logic`

**Function:** `should_refuse_navigation`

**Description:** Determines whether navigation should be refused based on innovation magnitude.

```python
def should_refuse_navigation(
    innovation_norm: float,
    threshold: float
) -> bool:
    """
    Determine if navigation should be refused.
    
    Parameters
    ----------
    innovation_norm : float
        Norm of innovation vector
    threshold : float
        Refusal threshold
        
    Returns
    -------
    bool
        True if navigation should be refused
    """
    pass
```

---

## Type Hints

The codebase uses Python type hints for better IDE support and documentation:

```python
from typing import Dict, List, Optional
import numpy as np

def process_sensor_data(
    data: Dict[str, np.ndarray],
    timestamp: float
) -> Optional[BeliefState]:
    """Process sensor data with type hints."""
    pass
```

---

## Error Handling

The API uses standard Python exceptions:

- `ValueError`: Invalid parameter values
- `TypeError`: Type mismatches
- `RuntimeError`: Runtime errors during processing

**Example:**
```python
try:
    state = belief.update(sensor_data)
except ValueError as e:
    print(f"Invalid sensor data: {e}")
```

---

## Related Documentation

- [Architecture Overview](./architecture_overview.md) - System architecture
- [Development Guide](./development_guide.md) - Development setup
- [Testing Guide](./testing_guide.md) - Test execution
- [Configuration Reference](./config_reference.md) - Configuration parameters

---

**Note:** This API reference covers public interfaces only. For detailed implementation information, see the source code and internal documentation.

