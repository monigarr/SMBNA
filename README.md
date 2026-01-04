# SMBNA: Secure Multi-Belief Navigation Arbitration

<div align="center">

**Safe, explainable navigation for autonomous systems in GPS-degraded, GPS-denied, and adversarial environments**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Research%20%26%20Evaluation-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Research%20Ready-orange.svg)](https://github.com/monigarr/SMBNA)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)](CHANGELOG.md)

[Features](#features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Architecture](#architecture) • [Contributing](#contributing)

</div>

---

## Overview

**SMBNA (Secure Multi-Belief Navigation Arbitration)** is a research-grade navigation framework that treats navigation as an *epistemic problem*, not a sensor problem. Unlike traditional systems that can become **confident while wrong**, SMBNA explicitly reasons about **trust**, **consistency**, and **when to refuse** navigation.

> **Core Philosophy**: When the environment lies, the system must know it is being lied to.

### The Problem

Modern navigation systems fail in a dangerous way: they can become **confident while wrong**. Accuracy alone is not sufficient when GPS jamming, spoofing, and signal degradation become routine (not exceptional). Autonomous systems must reason explicitly about trust, consistency, and when to refuse.

### The Solution

SMBNA is a **belief-centric navigation architecture** that:
- Maintains **parallel independent navigation beliefs**
- Evaluates them using **invariant-based consistency checks**
- Dynamically arbitrates trust
- Emits explicit **NAV_UNSAFE** refusal signals when certainty collapses

This design prioritizes **safety, interpretability, and graceful degradation** over brittle accuracy.

### Reproducibility Checklist

All experiments can be reproduced via the provided simulation runners using fixed random seeds and exported CSV/Parquet artifacts.

- **Code Availability**: All source code required to reproduce the experiments is publicly available in this repository under an MIT License.
- **Deterministic Execution**: All simulations and Monte Carlo experiments support fixed random seeds and deterministic execution (`SimConfig.seed`, `np.random.seed()`).
- **Configuration Transparency**: Experiment parameters (sensor noise, spoofing regimes, thresholds, ablations) are explicitly defined in `SimConfig` and version-controlled.
- **Baseline Implementation**: A clearly identified EKF baseline (`smbna/baselines/ekf.py`) is provided for direct comparison against the proposed method.
- **Ablations Provided**: Results include ablations with and without refusal logic (`run_ablation.py`, `compare_variants.py`), enabling attribution of performance gains.
- **Metrics Defined**: Evaluation metrics (final position error, innovation statistics, refusal rate) are formally defined in `experiment_io.py` and consistently reported.
- **Statistical Reporting**: Aggregate statistics are computed over repeated runs (`run_monte_carlo.py`); confidence intervals (`plot_ci.py`) and paired comparisons (`significance.py`) are supported.
- **Artifact Generation**: Scripts are provided to automatically generate tables (`latex_export.py`) and figures (`figure1_architecture.py`, `figure2_failure.py`) used in the paper from raw simulation logs.
- **Environment Specification**: Python version (`>=3.8`) and dependency requirements are documented in `pyproject.toml` to ensure reproducible environments.

---

## Features

### 🎯 Core Capabilities

- **Multi-Belief Architecture**: Parallel, independent belief engines (GPS, INS, Magnetic, LEO, Dead Reckoning)
- **Invariant-Based Validation**: Representation-level consistency checks (temporal, physics, coherence, covariance, earth field)
- **Trust Arbitration**: Dynamic belief selection based on confidence and consistency scores
- **Explicit Refusal**: `NAV_UNSAFE` signaling when confidence collapses
- **Safety-First Design**: Prioritizes safe degradation over false confidence

### 🔬 Research Features

- **Simulation Harness**: GPS degradation, spoofing, and denial scenarios
- **Monte Carlo Evaluation**: Statistical performance analysis
- **Baseline Comparisons**: EKF and classical sensor fusion for fair evaluation
- **Analysis Tools**: Trajectory plotting, error analysis, significance testing
- **Paper-Ready Figures**: Automated figure generation for publications

### 🏗️ Enterprise Features

- **Comprehensive Documentation**: Enterprise-level internal documentation suite
- **Test Infrastructure**: pytest-based test suite with coverage reporting
- **Code Quality**: Enterprise-level code headers and documentation
- **Configuration Management**: YAML-based configuration system
- **Extensible Architecture**: Clean interfaces for adding new beliefs and invariants

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/monigarr/SMBNA.git
cd SMBNA

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install -e .

# Install development dependencies (optional)
pip install -e ".[dev]"
```

### Basic Usage

```python
from smbna.core.pipeline import Pipeline
from smbna.beliefs.gps import GPSBelief
from smbna.beliefs.ins import INSBelief
import numpy as np

# Create pipeline
pipeline = Pipeline()

# Register belief engines
pipeline.add_belief(GPSBelief())
pipeline.add_belief(INSBelief())

# Process sensor data
sensor_data = {
    "gps": {"position": np.array([10.0, 20.0]), "timestamp": 1234.5},
    "imu": {"accel": np.array([0.1, 0.2]), "timestamp": 1234.5}
}

result = pipeline.process(sensor_data)

# Access results
decision = result["decision"]
if not decision["nav_unsafe"]:
    print(f"Selected belief: {decision['selected']}")
    print(f"Confidence: {decision['confidence']:.2f}")
else:
    print("Navigation refused: confidence collapse")
```

### Running Simulations

```bash
# Run a single simulation
python -m smbna.simulation.run_simulation --time 300 --seed 42

# Run Monte Carlo evaluation
python -m smbna.simulation.run_monte_carlo --runs 50

# Run ablation study
python -m smbna.simulation.run_ablation --runs 50
```

---

## Architecture

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

### Key Principles

1. **Beliefs before fusion**: Maintain independent beliefs, never fuse before validating trust
2. **Refusal is valid**: Explicit refusal is preferred over false confidence
3. **Structural explainability**: Decisions include machine-readable explanations
4. **Safety beats accuracy**: Safe degradation over confident failure

---

## Documentation

### Public Documentation

- **[README](README.md)** (this file) - Project overview and quick start
- **[CHANGELOG](CHANGELOG.md)** - Version history and updates
- **[LICENSE](LICENSE)** - License information
- **[Architecture Overview](docs/architecture_overview.md)** - High-level system architecture
- **[API Reference](docs/api_reference.md)** - Public API documentation
- **[Development Guide](docs/development_guide.md)** - Contributor setup and guidelines
- **[Testing Guide](docs/testing_guide.md)** - Test structure and execution
- **[Configuration Reference](docs/config_reference.md)** - Configuration parameters
- **[Troubleshooting Guide](docs/troubleshooting.md)** - Common setup and development issues

### Documentation Scope

**This repository intentionally omits deployment, security, and operational documentation. Those materials are available under controlled access for research, evaluation, and funding purposes.**

**What's Included:**
- How the system works (architecture, API)
- How to reproduce results (development, testing)
- How to extend it safely (development guide, configuration)

**What's Excluded:**
- Deployment procedures
- Security architecture and threat models
- Operational configuration and tuning
- Internal implementation details

---

## Repository Structure

```
SMBNA/
├── smbna/                    # Main package
│   ├── core/                 # Core pipeline and data structures
│   ├── beliefs/              # Independent belief engines
│   ├── invariants/           # Consistency validators
│   ├── arbitration/          # Trust arbitration engine
│   ├── baselines/            # EKF baseline for comparison
│   ├── sensors/              # Sensor interfaces
│   ├── simulation/           # Simulation harness and scenarios
│   ├── analysis/             # Analysis and metrics tools
│   ├── visualization/        # Plotting utilities
│   ├── figures/              # Paper-ready figure generators
│   ├── tests/                # Test suite
│   └── config/               # Configuration files
├── CHANGELOG.md              # Version history
├── LICENSE                   # License file
├── pytest.ini                # Pytest configuration
├── .coveragerc               # Coverage configuration
└── pyproject.toml            # Project metadata
```

---

## Requirements

### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Linux, macOS, or Windows
- **Memory**: 4 GB minimum (8 GB recommended)
- **Storage**: 10 GB minimum

### Dependencies

**Core:**
- `numpy >= 1.20.0`

**Optional:**
- `pandas >= 1.3.0` (for analysis)
- `scipy >= 1.7.0` (for analysis)
- `matplotlib >= 3.5.0` (for visualization)
- `graphviz >= 0.20.0` (for figure generation)

**Development:**
- `pytest >= 7.0.0`
- `pytest-cov >= 4.0.0`
- `black >= 22.0.0`
- `ruff >= 0.1.0`

---

## Research Status

### ✅ Completed

- Architecture complete and validated
- Simulation-validated performance
- Baseline implementations (EKF)
- Paper-ready figures and analysis
- Test infrastructure established
- Enterprise documentation suite

### 🔬 Research Applications

This repository is intended for:
- **Research**: Academic research in navigation and sensor fusion
- **Evaluation**: Performance evaluation in GPS-contested environments
- **Development**: Foundation for further research and development
- **Collaboration**: Grant proposals and research partnerships

### 📊 Use Cases

SMBNA is especially relevant for:
- GPS-contested environments
- Safety-critical autonomous systems
- Long-duration or remote operations
- Future hybrid classical + quantum navigation stacks

---

## What SMBNA Is Not

To set proper expectations:

- ❌ **Not a new GPS signal** - Works with existing GPS infrastructure
- ❌ **Not classified or restricted technology** - Open research framework
- ❌ **Not a hardware or sensor replacement** - Software reasoning layer
- ❌ **Not an autonomy or flight-control stack** - Navigation arbitration only

SMBNA operates strictly at the **navigation reasoning layer** and is compatible with existing and future sensors, including quantum inertial and magnetic systems.

---

## Baselines

For fair comparison, the repository includes:

- **Classical EKF**: Standard Extended Kalman Filter sensor fusion
- **INS + GPS Fallback**: Traditional fallback strategies
- **Best-Single-Sensor**: Single-sensor baseline strategies

These baselines intentionally **lack spoof detection or refusal**, highlighting SMBNA's safety advantage through explicit refusal mechanisms.

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run without coverage (faster)
pytest --no-cov

# Run with coverage
pytest --cov=smbna --cov-report=html

# Run only critical tests (safety-critical components)
pytest -m critical

# Run specific test file
pytest smbna/tests/test_beliefs/test_refusal_logic.py
```

### Test Status

**All Tests Passing: 57/57** ✅

- **Refusal Logic**: 18 tests (safety-critical)
- **Trust Arbitration**: 12 tests (safety-critical)
- **Core Data Structures**: 9 tests
- **Invariants**: 18 tests (9 physics + 9 temporal)

### Coverage

- **Critical Paths**: 100% coverage ✅ (refusal logic, trust arbitration)
- **Core Components**: 93%+ coverage (BeliefState, Temporal invariant)
- **Overall Project**: 24.60% current (85%+ target as project grows)

**Coverage Strategy:**
- Priority on safety-critical components (100% achieved)
- Core data structures and invariants (93%+ achieved)
- Simulation and analysis modules (to be expanded)

## Testing Philosophy
Testing Philosophy

This repository follows a logic-first testing strategy appropriate for research and safety-aware systems.

Unit tests focus on deterministic, decision-critical components, including belief representations, invariant scoring, trust arbitration, and refusal logic. These components directly affect correctness claims and are therefore tested exhaustively across boundary conditions, numerical edge cases (NaN, infinity), and threshold behaviors.

Simulation drivers, Monte Carlo runners, ablation scripts, and experiment orchestration code are intentionally not subjected to line-by-line unit testing. These components are validated through reproducible experiment outputs (tables, plots, and logs) rather than granular assertions, as their correctness is best evaluated at the system and artifact level.

This approach prioritizes scientific validity, interpretability, and long-term maintainability over superficial coverage metrics.

## Coverage Rationale

Reported test coverage reflects a deliberate separation between core logic and experimental orchestration.

High coverage is achieved for modules that encode algorithmic decisions, invariants, and refusal behavior, as faults in these areas would invalidate experimental conclusions. Lower coverage in simulation and experiment modules is expected and intentional, as these components primarily coordinate execution, parameter sweeps, and artifact generation.

Simulation correctness is instead established through:

- deterministic seeds,
- reproducible experiment outputs,
- cross-variant comparisons,
- and statistical validation across repeated runs.

This coverage distribution aligns with best practices for research codebases and safety-oriented autonomy systems, where correctness is demonstrated through reproducibility and controlled experiments rather than exhaustive execution tracing.
---

## Contributing

We welcome contributions! Areas of interest:

- Extending SMBNA to new sensors
- Formal safety guarantees
- Hardware-in-the-loop validation
- Grant or residency collaboration
- Performance optimizations
- Additional invariant validators

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

See the [Development Guide](smbna/docs/DEVELOPMENT_GUIDE.md) for detailed guidelines.

---

## Citation

If you use this framework, ideas, or code in academic work, please cite:

```bibtex
@misc{SMBNA2026,
  title        = {SMBNA: Secure Multi-Belief Navigation Arbitration for Safe Autonomous Systems},
  author       = {MoniGarr},
  year         = {2026},
  howpublished = {\url{https://github.com/monigarr/SMBNA}},
  note         = {Belief-centric navigation with invariant-based trust arbitration and explicit refusal under uncertainty}
}
```

---

## License

This project is released for **research and evaluation purposes**.

- Contains no classified material
- No restricted signal processing
- Open for academic and research use

See [LICENSE](LICENSE) for details.

---

## Contact & Collaboration

**Author**: MoniGarr  
**GitHub**: [github.com/monigarr/SMBNA](https://github.com/monigarr/SMBNA)

### Interested in:

- Extending SMBNA to new sensors
- Formal safety guarantees
- Hardware-in-the-loop validation
- Grant or residency collaboration

**Open an issue** or reach out via the repository to discuss collaboration opportunities.

---

## Philosophy

> **"Robust systems know when they should not act."**

SMBNA is built for environments where:
- Certainty is rare
- Signals lie
- Safety is the top priority

**Knowing when not to trust yourself is the first step toward trustworthy autonomy.**

---

<div align="center">

**Built with ❤️ for safe autonomous systems**

[⬆ Back to Top](#smbna-secure-multi-belief-navigation-arbitration)

</div>
