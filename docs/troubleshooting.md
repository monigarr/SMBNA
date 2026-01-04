# SMBNA Troubleshooting Guide

**Version:** 1.0  
**Last Updated:** 2026

---

## Overview

This guide helps resolve common issues encountered when using the SMBNA framework. It focuses on setup, installation, and benign errors that users may encounter during development and experimentation.

---

## Common Issues

### Issue: Import Errors

**Symptoms:**
- `ModuleNotFoundError` when importing SMBNA
- `ImportError` for dependencies

**Diagnosis:**
```bash
# Check if package is installed
python -c "import smbna; print(smbna.__version__)"

# Check Python path
python -c "import sys; print(sys.path)"
```

**Solutions:**

1. **Package Not Installed:**
   ```bash
   pip install -e .
   ```

2. **Virtual Environment Not Activated:**
   ```bash
   # Activate virtual environment
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. **Missing Dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

---

### Issue: Environment Setup Problems

**Symptoms:**
- Python version mismatch
- Package installation failures
- Virtual environment issues

**Diagnosis:**
```bash
# Check Python version
python --version  # Should be 3.8+

# Check pip version
pip --version

# Check virtual environment
which python  # Should point to venv
```

**Solutions:**

1. **Python Version Too Old:**
   ```bash
   # Upgrade Python to 3.8 or higher
   # Use pyenv or system package manager
   ```

2. **Virtual Environment Issues:**
   ```bash
   # Recreate virtual environment
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

3. **Package Installation Failures:**
   ```bash
   # Upgrade pip
   pip install --upgrade pip
   
   # Clear pip cache
   pip cache purge
   
   # Reinstall
   pip install -e .
   ```

---

### Issue: Test Failures

**Symptoms:**
- Tests fail with assertion errors
- Tests fail with import errors
- Tests fail with timeout errors
- Pytest plugin errors (e.g., `pytest_dash`)

**Diagnosis:**
```bash
# Run tests with verbose output
pytest -v

# Run specific test
pytest smbna/tests/test_core/test_belief_state.py -v

# Check test output
pytest --tb=short

# Run without coverage (faster, fewer dependencies)
pytest --no-cov
```

**Solutions:**

1. **Missing Test Dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

2. **Pytest Plugin Conflicts:**
   ```bash
   # Run with plugin disabled (if needed)
   pytest -p no:dash
   
   # Or use --no-cov to avoid coverage-related issues
   pytest --no-cov
   ```

3. **Test Data Issues:**
   ```bash
   # Clear test cache
   pytest --cache-clear
   ```

4. **Environment Issues:**
   ```bash
   # Check environment variables
   env | grep SMBNA
   ```

**Note:** The project configuration automatically disables problematic plugins.
If you encounter plugin errors, ensure you're using the latest configuration files.

---

### Issue: NaN or Inf Values

**Symptoms:**
- NaN values in results
- Inf values in calculations
- Division by zero warnings

**Diagnosis:**
```python
import numpy as np

# Check for NaN
if np.any(np.isnan(array)):
    print("NaN detected")

# Check for Inf
if np.any(np.isinf(array)):
    print("Inf detected")
```

**Solutions:**

1. **Invalid Input Data:**
   ```python
   # Validate input data
   assert np.all(np.isfinite(sensor_data))
   ```

2. **Numerical Instability:**
   ```python
   # Add small epsilon to prevent division by zero
   result = numerator / (denominator + 1e-10)
   ```

3. **Covariance Issues:**
   ```python
   # Ensure covariance is positive definite
   covariance = np.linalg.cholesky(covariance)
   ```

---

### Issue: Configuration Errors

**Symptoms:**
- Configuration file not found
- Invalid YAML syntax
- Missing required fields

**Diagnosis:**
```bash
# Validate configuration
python -m smbna.config.validate

# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('config/default.yaml'))"
```

**Solutions:**

1. **Invalid YAML Syntax:**
   ```bash
   # Use YAML validator
   # Fix syntax errors in configuration file
   ```

2. **Missing Required Fields:**
   ```bash
   # Check configuration against schema
   # Add missing required fields
   ```

3. **Type Mismatches:**
   ```bash
   # Ensure parameter types match expected types
   # Fix type errors in configuration
   ```

---

### Issue: Simulation Errors

**Symptoms:**
- Simulation fails to start
- Simulation produces unexpected results
- Simulation hangs or times out

**Diagnosis:**
```python
# Run simulation with debug output
from smbna.simulation.run_simulation import run_simulation
import logging
logging.basicConfig(level=logging.DEBUG)

results = run_simulation(time=300.0, seed=42)
```

**Solutions:**

1. **Invalid Simulation Parameters:**
   ```python
   # Check parameter ranges
   assert time > 0
   assert seed >= 0
   ```

2. **Memory Issues:**
   ```python
   # Reduce simulation time or history length
   results = run_simulation(time=100.0)  # Shorter simulation
   ```

3. **Numerical Issues:**
   ```python
   # Use fixed seed for reproducibility
   results = run_simulation(seed=42)
   ```

---

### Issue: Plotting/Visualization Errors

**Symptoms:**
- Matplotlib errors
- Figure generation fails
- Display issues

**Diagnosis:**
```python
# Check matplotlib backend
import matplotlib
print(matplotlib.get_backend())

# Test basic plotting
import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
plt.show()
```

**Solutions:**

1. **Missing Matplotlib:**
   ```bash
   pip install matplotlib
   ```

2. **Backend Issues:**
   ```python
   # Set non-interactive backend
   import matplotlib
   matplotlib.use('Agg')
   ```

3. **Display Issues:**
   ```python
   # Use non-interactive backend for headless systems
   import matplotlib
   matplotlib.use('Agg')
   ```

---

### Issue: Performance Problems

**Symptoms:**
- Slow execution
- High memory usage
- CPU usage spikes

**Diagnosis:**
```python
# Profile code
import cProfile
cProfile.run('your_function()')

# Check memory usage
import tracemalloc
tracemalloc.start()
# Your code here
current, peak = tracemalloc.get_traced_memory()
```

**Solutions:**

1. **Optimize Loops:**
   ```python
   # Use vectorized operations
   result = np.sum(array)  # Instead of loop
   ```

2. **Reduce History Length:**
   ```python
   # Limit history size
   config.history_length = 50  # Instead of 100
   ```

3. **Disable Parallel Processing:**
   ```python
   # Disable if causing issues
   config.parallel_processing = False
   ```

---

## Getting Help

### Documentation

- [Architecture Overview](./architecture_overview.md)
- [API Reference](./api_reference.md)
- [Development Guide](./development_guide.md)
- [Testing Guide](./testing_guide.md)

### Community

- GitHub Issues: Report bugs and ask questions
- Discussions: Community discussions and Q&A

### Debugging Tips

1. **Enable Debug Logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Use Print Statements:**
   ```python
   print(f"Variable value: {variable}")
   ```

3. **Use Debugger:**
   ```python
   import pdb
   pdb.set_trace()  # Breakpoint
   ```

---

## Related Documentation

- [Architecture Overview](./architecture_overview.md) - System architecture
- [API Reference](./api_reference.md) - API documentation
- [Development Guide](./development_guide.md) - Development setup
- [Configuration Reference](./config_reference.md) - Configuration parameters

---

**Note:** This guide focuses on benign errors and setup issues. For operational issues, see internal documentation.

