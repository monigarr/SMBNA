# SMBNA Test Suite

## Overview

This directory contains the test suite for the SMBNA (Secure Multi-Belief Navigation Arbitration) system.

## Test Structure

```
smbna/tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_core/              # Core module tests
│   └── test_belief_state.py
├── test_beliefs/           # Belief engine tests
│   └── test_refusal_logic.py
├── test_invariants/        # Invariant validator tests
│   ├── test_temporal.py
│   └── test_physics.py
├── test_arbitration/       # Arbitration tests
│   └── test_trust_engine.py
└── test_scenarios/         # Scenario tests
```

## Running Tests

### Install Test Dependencies

```bash
pip install -e ".[dev]"
```

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest smbna/tests/test_beliefs/test_refusal_logic.py
```

### Run with Coverage

```bash
pytest --cov=smbna --cov-report=html
```

### Run Only Critical Tests

```bash
pytest -m critical
```

### Run Fast Tests Only

```bash
pytest -m "not slow"
```

## Test Markers

- `@pytest.mark.unit` - Unit tests (fast, isolated)
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow running tests
- `@pytest.mark.critical` - Critical path tests (safety-critical)

## Coverage Targets

- **Critical paths**: 100% coverage required
- **Core navigation logic**: 95%+ coverage
- **Overall project**: 85%+ coverage

## Test Fixtures

Common fixtures are defined in `conftest.py`:
- `sample_belief_state` - Sample GPS belief state
- `sample_belief_state_ins` - Sample INS belief state
- `sample_belief_state_magnetic` - Sample magnetic belief state
- `sample_belief_history` - Belief history for temporal tests
- `sample_sensor_data` - Sample sensor data dictionary
- `sample_invariant_scores` - Sample invariant penalty scores
- `multiple_beliefs` - Multiple belief states
- `sim_config` - Simulation configuration

## Writing New Tests

1. Create test file in appropriate directory
2. Use fixtures from `conftest.py`
3. Mark tests appropriately (`@pytest.mark.unit`, etc.)
4. Follow naming convention: `test_*.py`, `Test*`, `test_*`
5. Aim for 100% coverage on critical paths

## Continuous Integration

Tests are run automatically in CI/CD pipeline with:
- Coverage reporting
- Coverage threshold enforcement (85% minimum)
- Test result publishing

