# SMBNA Testing Guide

**Version:** 1.0  
**Last Updated:** 2026

---

## Overview

This guide explains how to run tests, understand test structure, and contribute tests to the SMBNA project. The test suite ensures correctness, stability, and reproducibility of the navigation framework.

---

## Testing Philosophy

SMBNA follows a comprehensive testing strategy emphasizing:
- **Reproducibility**: All tests use fixed seeds
- **Isolation**: Tests are independent and can run in any order
- **Speed**: Fast feedback for developers
- **Maintainability**: Clear, readable test code

---

## Test Organization

### Directory Structure

```
smbna/tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_beliefs/
│   ├── test_gps.py
│   ├── test_ins.py
│   └── test_magnetic.py
├── test_invariants/
│   ├── test_temporal.py
│   ├── test_physics.py
│   └── test_coherence.py
├── test_arbitration/
│   └── test_trust_engine.py
├── test_core/
│   ├── test_belief_state.py
│   └── test_pipeline.py
└── test_scenarios/
    └── test_spoofing.py
```

### Test Naming Conventions

**File Names:**
- Prefix with `test_`
- Match module name: `test_gps.py` for `gps.py`

**Test Function Names:**
- Prefix with `test_`
- Descriptive: `test_gps_belief_updates_position_correctly`
- Use underscores, not camelCase

---

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest smbna/tests/test_beliefs/test_gps.py

# Run specific test function
pytest smbna/tests/test_beliefs/test_gps.py::test_gps_belief_update

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=smbna --cov-report=html

# Run only fast tests
pytest -m "not slow"
```

### Test Markers

Tests can be marked for selective execution:

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run critical tests
pytest -m critical

# Skip slow tests
pytest -m "not slow"
```

---

## Test Types

### Unit Tests

**Purpose:** Test individual components in isolation

**Characteristics:**
- Fast execution (< 1 second each)
- No external dependencies
- Mock external components
- Test single responsibility

**Example:**
```python
def test_gps_belief_update():
    """Test GPS belief updates position correctly."""
    belief = GPSBelief()
    sensor_data = {
        "gps": {
            "position": np.array([10.0, 20.0]),
            "timestamp": 1234.5
        }
    }
    
    state = belief.update(sensor_data)
    
    assert isinstance(state, BeliefState)
    assert state.belief_id == "gps"
    assert np.allclose(state.position, [10.0, 20.0])
```

### Integration Tests

**Purpose:** Test component interactions

**Characteristics:**
- Test multiple components together
- May use real dependencies
- Test data flow between components
- Verify interfaces

**Example:**
```python
def test_pipeline_with_gps_and_ins():
    """Test pipeline processes GPS and INS beliefs."""
    pipeline = Pipeline()
    pipeline.add_belief(GPSBelief())
    pipeline.add_belief(INSBelief())
    
    sensor_data = {
        "gps": {"position": np.array([10.0, 20.0])},
        "imu": {"accel": np.array([0.1, 0.2])}
    }
    
    result = pipeline.process(sensor_data)
    
    assert "decision" in result
    assert len(result["beliefs"]) == 2
```

### Scenario Tests

**Purpose:** Test specific use cases and failure modes

**Characteristics:**
- Test realistic scenarios
- Include edge cases
- Test failure modes
- Verify safety behavior

**Example:**
```python
def test_gps_spoofing_detection():
    """Test system detects GPS spoofing."""
    config = SimConfig(spoof_bias=50.0, seed=42)
    logs = run_simulation(config)
    
    # Check that refusal was triggered
    assert np.any(logs["refusal"])
    
    # Check that position error is bounded
    errors = np.linalg.norm(
        logs["truth"][:, :2] - logs["estimate"][:, :2],
        axis=1
    )
    assert np.max(errors) < 100.0
```

---

## Writing Tests

### Test Structure

**AAA Pattern (Arrange-Act-Assert):**

```python
def test_feature_name():
    # Arrange: Set up test data and objects
    belief = GPSBelief()
    sensor_data = {"gps": {"position": np.array([10.0, 20.0])}}
    
    # Act: Execute the functionality being tested
    state = belief.update(sensor_data)
    
    # Assert: Verify the results
    assert isinstance(state, BeliefState)
    assert state.belief_id == "gps"
```

### Using Fixtures

**Shared fixtures** are defined in `conftest.py`:

```python
# In conftest.py
@pytest.fixture
def sample_gps_state():
    return BeliefState(
        belief_id="gps",
        position=np.array([10.0, 20.0]),
        velocity=np.array([1.0, 0.5]),
        covariance=np.eye(2) * 2.0,
        internal_confidence=0.95,
        timestamp=1234.5,
        metadata={}
    )

# In test file
def test_with_fixture(sample_gps_state):
    assert sample_gps_state.belief_id == "gps"
```

### Test Data

**Use fixed seeds** for reproducibility:

```python
def test_reproducible_simulation():
    """Test that simulation is reproducible with fixed seed."""
    results1 = run_simulation(seed=42)
    results2 = run_simulation(seed=42)
    
    np.testing.assert_array_equal(
        results1["trajectory"],
        results2["trajectory"]
    )
```

---

## Test Coverage

### Coverage Requirements

- **Critical paths**: 100% coverage (refusal logic, trust arbitration)
- **Core components**: 95%+ coverage
- **Overall project**: 85%+ coverage target

### Viewing Coverage

```bash
# Generate HTML coverage report
pytest --cov=smbna --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

### Coverage Reports

Coverage reports show:
- Which lines are covered
- Which lines are missing
- Branch coverage
- Function coverage

---

## Continuous Integration

Tests run automatically on:
- Pull requests
- Commits to main branch
- Scheduled runs

**CI checks:**
- All tests pass
- Code coverage meets thresholds
- Linting passes
- Code formatting is correct

---

## Debugging Tests

### Running Tests in Debug Mode

```bash
# Run with Python debugger
pytest --pdb

# Drop into debugger on failure
pytest --pdb --pdbcls=IPython.terminal.debugger:Pdb
```

### Verbose Output

```bash
# Show print statements
pytest -s

# Show local variables on failure
pytest -l

# Show test names
pytest -v
```

---

## Best Practices

### Do's

- ✅ Write tests before fixing bugs
- ✅ Use descriptive test names
- ✅ Keep tests independent
- ✅ Use fixtures for shared setup
- ✅ Test edge cases
- ✅ Use fixed seeds for reproducibility

### Don'ts

- ❌ Don't test implementation details
- ❌ Don't make tests depend on each other
- ❌ Don't use random data without seeds
- ❌ Don't skip assertions
- ❌ Don't test external libraries

---

## Related Documentation

- [Architecture Overview](./architecture_overview.md) - System architecture
- [API Reference](./api_reference.md) - API documentation
- [Development Guide](./development_guide.md) - Development setup
- [Configuration Reference](./config_reference.md) - Configuration parameters

---

**Note:** This guide focuses on test execution and structure. For detailed test implementation, see the test source code.

