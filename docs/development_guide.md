# SMBNA Development Guide

**Version:** 1.0  
**Last Updated:** 2026

---

## Getting Started

### Prerequisites

- **Python**: 3.8 or higher
- **Package Manager**: pip, poetry, or uv
- **Version Control**: Git
- **IDE**: VS Code, PyCharm, or similar
- **Operating System**: Linux, macOS, or Windows

### Quick Start

```bash
# Clone repository
git clone https://github.com/monigarr/SMBNA.git
cd SMBNA

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Run tests
pytest

# Run simulation
python -m smbna.simulation.run_simulation
```

---

## Development Environment Setup

### Virtual Environment

**Recommended:** Use a virtual environment for isolation.

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### IDE Configuration

#### VS Code

**Recommended Extensions:**
- Python
- Pylance
- Python Test Explorer
- Ruff (linter)

**.vscode/settings.json:**
```json
{
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.testing.pytestEnabled": true
}
```

---

## Project Structure

```
smbna/
├── beliefs/          # Belief engines
├── invariants/       # Invariant checks
├── arbitration/      # Trust arbitration
├── core/            # Core pipeline
├── sensors/         # Sensor interfaces
├── simulation/      # Simulation harness
├── analysis/        # Analysis tools
├── visualization/   # Plotting
├── tests/           # Test suite
└── config/          # Configuration files
```

---

## Coding Standards

### Python Style Guide

Follow **PEP 8** with project-specific modifications:

#### Naming Conventions

- **Classes**: `PascalCase` (e.g., `BeliefState`, `GPSBelief`)
- **Functions/Methods**: `snake_case` (e.g., `should_refuse_navigation`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_ACCEL`, `TRUST_MIN`)
- **Private**: Prefix with `_` (e.g., `_internal_method`)

#### Code Formatting

**Use Black** for automatic formatting:
```bash
black smbna/
```

**Line Length**: 100 characters (Black default)

**Import Organization:**
```python
# Standard library
import os
from typing import Dict, List

# Third-party
import numpy as np

# Local
from smbna.core.belief_state import BeliefState
```

---

## Development Workflow

### Making Changes

1. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes:**
   - Write code following coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests:**
   ```bash
   # Run all tests
   pytest
   
   # Run without coverage (faster)
   pytest --no-cov
   
   # Run only critical tests
   pytest -m critical
   ```

4. **Format code:**
   ```bash
   black smbna/
   ruff check smbna/
   ```

5. **Commit changes:**
   ```bash
   git add .
   git commit -m "feat: Add new feature"
   ```

6. **Push and create pull request:**
   ```bash
   git push origin feature/your-feature-name
   ```

### Adding a New Experiment

1. Create a new script in `smbna/simulation/` or `scripts/`
2. Use the simulation harness for consistency
3. Document the experiment purpose
4. Add results to `results/` directory
5. Update documentation if needed

**Example:**
```python
# scripts/my_experiment.py
from smbna.simulation.run_simulation import run_simulation

def main():
    results = run_simulation(time=300.0, seed=42, scenario="normal")
    # Process and save results
    ...

if __name__ == "__main__":
    main()
```

---

## Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest

# Run all tests without coverage (faster)
pytest --no-cov

# Run specific test file
pytest smbna/tests/test_beliefs/test_refusal_logic.py

# Run with coverage
pytest --cov=smbna --cov-report=html

# Run only fast tests
pytest -m "not slow"

# Run only critical tests (safety-critical)
pytest -m critical
```

**Current Test Status:**
- All 57 tests passing ✅
- 32 critical path tests passing
- 100% coverage on safety-critical components

### Writing Tests

**Test Structure (AAA Pattern):**
```python
def test_feature_name():
    # Arrange: Set up test data
    belief = GPSBelief()
    sensor_data = {"gps": {"position": np.array([10.0, 20.0])}}
    
    # Act: Execute functionality
    state = belief.update(sensor_data)
    
    # Assert: Verify results
    assert isinstance(state, BeliefState)
    assert state.belief_id == "gps"
```

See [Testing Guide](./testing_guide.md) for more details.

---

## Code Review Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] No linter errors

### Review Checklist

- Code quality and style
- Test coverage
- Documentation completeness
- Performance considerations
- Security implications

---

## Documentation Requirements

### Code Documentation

All public functions and classes should have docstrings:

```python
def process_sensor_data(data: dict) -> BeliefState:
    """
    Process sensor data and return belief state.
    
    Parameters
    ----------
    data : dict
        Dictionary containing sensor measurements
        
    Returns
    -------
    BeliefState
        Updated belief state
    """
    pass
```

### Module Documentation

Each module should have a module-level docstring describing its purpose.

---

## Debugging

### Using Python Debugger

```python
import pdb

def my_function():
    pdb.set_trace()  # Breakpoint
    # Your code here
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

---

## Performance Optimization

### Profiling

```bash
# Profile a script
python -m cProfile -o profile.stats scripts/my_script.py

# Analyze profile
python -m pstats profile.stats
```

### Optimization Guidelines

- Profile before optimizing
- Focus on bottlenecks
- Maintain code readability
- Document performance improvements

---

## Contributing

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Contribution Guidelines

- Follow coding standards
- Write clear commit messages
- Add tests for new features
- Update documentation
- Be respectful in discussions

---

## Related Documentation

- [Architecture Overview](./architecture_overview.md) - System architecture
- [API Reference](./api_reference.md) - API documentation
- [Testing Guide](./testing_guide.md) - Test execution
- [Configuration Reference](./config_reference.md) - Configuration parameters

---

**Note:** This guide focuses on contributor setup and workflows. For operational procedures, see internal documentation.

