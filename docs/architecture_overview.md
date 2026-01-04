# SMBNA Architecture Overview

**Version:** 1.0  
**Last Updated:** 2026

---

## Overview

SMBNA (Secure Multi-Belief Navigation Arbitration) is a belief-centric navigation framework designed for autonomous systems operating in GPS-degraded, GPS-denied, and adversarial environments. The system treats navigation as an epistemic problem, maintaining parallel independent beliefs and using invariant-based consistency checks to arbitrate trust.

### Core Philosophy

**"Never fuse before you trust."**

The system prioritizes:
- **Safety over accuracy**: Explicit refusal is preferred over false confidence
- **Belief independence**: No belief consumes another's output
- **Structural explainability**: Decisions include machine-readable explanations
- **Graceful degradation**: System degrades safely when certainty collapses

---

## High-Level Architecture

### System Flow

```
┌─────────────┐
│   Sensors   │  (GPS, IMU, Magnetic, etc.)
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│  Belief Engines      │  (Parallel, Independent)
│  • GPS               │
│  • INS               │
│  • Magnetic          │
│  • LEO               │
│  • Dead Reckoning    │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Invariant Scoring   │  (Consistency Checks)
│  • Temporal          │
│  • Physics           │
│  • Coherence         │
│  • Covariance        │
│  • Earth Field       │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Trust Arbitration   │  (Belief Selection)
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Navigation Decision  │
│  • Pose              │
│  • Confidence        │
│  • NAV_UNSAFE        │
│  • Explanation       │
└──────────────────────┘
```

---

## Architecture Layers

The system is organized into five primary layers:

### 1. Sensor Interface Layer

**Purpose:** Abstract sensor data acquisition and normalization

**Components:**
- Sensor interface definitions
- Standardized data formats
- Sensor health monitoring

### 2. Belief Layer

**Purpose:** Independent belief engines producing state estimates

**Components:**
- GPS-only belief
- Inertial navigation system belief
- Magnetic map-matching belief
- Low Earth Orbit ranging belief (optional)
- Dead-reckoning fallback

**Key Principle:** Each belief engine operates independently with no cross-dependencies.

### 3. Invariant Layer

**Purpose:** Evaluate belief consistency using representation-level invariants

**Invariant Types:**
- Temporal smoothness: Checks for unrealistic acceleration
- Physics feasibility: Validates physical constraints
- Cross-belief coherence: Compares consistency across beliefs
- Covariance honesty: Validates uncertainty estimates
- Earth-field consistency: Validates magnetic field consistency

### 4. Arbitration Layer

**Purpose:** Dynamically select the most trustworthy belief or refuse navigation

**Components:**
- Trust scoring based on confidence and consistency
- Belief selection logic
- Explicit refusal mechanism (`NAV_UNSAFE`)

### 5. Core Pipeline Layer

**Purpose:** Orchestrate belief updates, invariant evaluation, and arbitration

**Components:**
- `BeliefState`: Immutable data structure for state estimates
- `Pipeline`: Main orchestration component
- `Scoring`: Trust and consistency scoring

---

## Key Design Principles

### 1. Belief Independence

Each belief engine operates independently:
- No cross-belief dependencies
- Parallel execution capability
- Independent failure modes
- Isolated state management

### 2. Invariant-Based Validation

Beliefs are evaluated using representation-level invariants that check:
- Temporal consistency
- Physical feasibility
- Cross-belief coherence
- Uncertainty honesty
- Environmental consistency

### 3. Explicit Refusal

The system can explicitly refuse navigation:
- `NAV_UNSAFE` signal when confidence collapses
- Machine-readable refusal reasons
- No silent failures or degraded modes

### 4. Auditability

All decisions are traceable:
- Complete belief history
- Invariant scores at each timestep
- Arbitration decisions with explanations
- Reproducible evaluation

---

## Component Interactions

### Belief Update Flow

1. **Sensor Data Acquisition**: Sensors provide measurements
2. **Belief Updates**: Each belief engine independently processes sensor data
3. **State Estimation**: Each belief produces a `BeliefState` with position, velocity, covariance, and confidence
4. **Invariant Evaluation**: All beliefs are evaluated against invariants
5. **Trust Scoring**: Beliefs receive trust scores based on confidence and consistency
6. **Arbitration**: Most trustworthy belief is selected, or navigation is refused
7. **Decision Output**: Final navigation decision with explanation

### Data Structures

**BeliefState:**
- `belief_id`: Unique identifier
- `position`: Position estimate
- `velocity`: Velocity estimate
- `covariance`: Uncertainty matrix
- `internal_confidence`: Belief's self-assessed confidence
- `timestamp`: Time of estimate
- `metadata`: Additional belief-specific data

---

## Extension Points

The architecture is designed for extensibility:

### Adding New Belief Engines

1. Implement the `Belief` base class interface
2. Provide `update()` method that returns `BeliefState`
3. Register with the pipeline

### Adding New Invariants

1. Implement the `Invariant` base class interface
2. Provide `evaluate()` method that returns a penalty score
3. Register with the invariant evaluator

### Custom Arbitration Logic

1. Implement custom trust scoring
2. Implement custom selection logic
3. Configure in the pipeline

---

## Research Applications

This architecture supports:
- **Reproducible Research**: All components are modular and testable
- **Baseline Comparisons**: EKF and other baselines included
- **Simulation Validation**: Comprehensive simulation harness
- **Academic Research**: Clean interfaces for research extensions

---

## Related Documentation

- [API Reference](./api_reference.md) - Detailed API documentation
- [Development Guide](./development_guide.md) - Contributor setup and guidelines
- [Testing Guide](./testing_guide.md) - Test structure and execution
- [Configuration Reference](./config_reference.md) - Configuration parameters

---

**Note:** This document provides a high-level architectural overview. For detailed implementation information, see the API reference and source code.

