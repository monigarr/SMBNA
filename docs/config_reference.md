# SMBNA Configuration Reference

**Version:** 1.0  
**Last Updated:** 2026

---

## Overview

This document describes configuration parameters available in the SMBNA framework. Parameters are documented with their names, types, units, and high-level purpose. This reference is descriptive, not prescriptive—it documents what parameters exist, not recommended values.

---

## Configuration Files

### File Locations

- **Default**: `smbna/config/default.yaml`
- **User Overrides**: User-specific configuration files

### File Structure

```yaml
# System-wide settings
system:
  ...

# Belief engine settings
beliefs:
  ...

# Invariant settings
invariants:
  ...

# Arbitration settings
arbitration:
  ...

# Sensor settings
sensors:
  ...

# Logging settings
logging:
  ...
```

---

## System Configuration

### System Parameters

```yaml
system:
  update_rate: float        # System update rate (Hz)
  history_length: int       # Maximum history length for temporal invariants
  dt: float                # Time step for simulation (seconds)
  parallel_processing: bool  # Enable/disable parallel belief processing
  max_workers: int         # Maximum number of worker threads/processes
```

**Parameter Descriptions:**

| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `update_rate` | float | Hz | System update rate |
| `history_length` | int | count | Number of historical states to maintain |
| `dt` | float | seconds | Time step for simulation |
| `parallel_processing` | bool | - | Enable parallel belief processing |
| `max_workers` | int | count | Maximum worker threads/processes |

---

## Belief Configuration

### GPS Belief

```yaml
beliefs:
  gps:
    enabled: bool           # Enable GPS belief
    noise_model: str       # Noise model type
    noise_std: float       # GPS noise standard deviation (meters)
    dropout_probability: float  # Probability of GPS dropout
    spoof_probability: float     # Probability of GPS spoofing
    spoof_bias: float      # GPS spoofing bias magnitude (meters)
    initial_confidence: float    # Initial confidence [0, 1]
    confidence_decay: float      # Confidence decay factor [0, 1]
```

**Parameter Descriptions:**

| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `enabled` | bool | - | Enable GPS belief |
| `noise_model` | str | - | Noise model type |
| `noise_std` | float | meters | GPS noise standard deviation |
| `dropout_probability` | float | [0, 1] | Probability of GPS dropout |
| `spoof_probability` | float | [0, 1] | Probability of GPS spoofing |
| `spoof_bias` | float | meters | GPS spoofing bias magnitude |
| `initial_confidence` | float | [0, 1] | Initial confidence |
| `confidence_decay` | float | [0, 1] | Confidence decay factor |

### INS Belief

```yaml
beliefs:
  ins:
    enabled: bool           # Enable INS belief
    noise_std: float       # INS noise standard deviation
    initial_confidence: float    # Initial confidence [0, 1]
    confidence_decay: float      # Confidence decay factor [0, 1]
```

**Parameter Descriptions:**

| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `enabled` | bool | - | Enable INS belief |
| `noise_std` | float | - | INS noise standard deviation |
| `initial_confidence` | float | [0, 1] | Initial confidence |
| `confidence_decay` | float | [0, 1] | Confidence decay factor |

---

## Invariant Configuration

### Temporal Invariant

```yaml
invariants:
  temporal:
    enabled: bool           # Enable temporal invariant
    max_accel: float       # Maximum allowed acceleration (m/s²)
    history_length: int    # History length for temporal checks
```

**Parameter Descriptions:**

| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `enabled` | bool | - | Enable temporal invariant |
| `max_accel` | float | m/s² | Maximum allowed acceleration |
| `history_length` | int | count | History length for temporal checks |

### Physics Invariant

```yaml
invariants:
  physics:
    enabled: bool           # Enable physics invariant
    max_velocity: float     # Maximum allowed velocity (m/s)
    max_accel: float        # Maximum allowed acceleration (m/s²)
```

**Parameter Descriptions:**

| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `enabled` | bool | - | Enable physics invariant |
| `max_velocity` | float | m/s | Maximum allowed velocity |
| `max_accel` | float | m/s² | Maximum allowed acceleration |

---

## Arbitration Configuration

### Trust Engine

```yaml
arbitration:
  trust_engine:
    enabled: bool           # Enable trust arbitration
    trust_min: float       # Minimum trust threshold [0, 1]
    confidence_weight: float  # Weight for confidence in trust score
    consistency_weight: float # Weight for consistency in trust score
```

**Parameter Descriptions:**

| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `enabled` | bool | - | Enable trust arbitration |
| `trust_min` | float | [0, 1] | Minimum trust threshold |
| `confidence_weight` | float | - | Weight for confidence in trust score |
| `consistency_weight` | float | - | Weight for consistency in trust score |

### Refusal Logic

```yaml
arbitration:
  refusal:
    enabled: bool           # Enable refusal logic
    innovation_threshold: float  # Innovation threshold for refusal
```

**Parameter Descriptions:**

| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `enabled` | bool | - | Enable refusal logic |
| `innovation_threshold` | float | - | Innovation threshold for refusal |

---

## Sensor Configuration

### GPS Sensor

```yaml
sensors:
  gps:
    enabled: bool           # Enable GPS sensor
    update_rate: float     # GPS update rate (Hz)
    noise_std: float       # GPS noise standard deviation (meters)
```

**Parameter Descriptions:**

| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `enabled` | bool | - | Enable GPS sensor |
| `update_rate` | float | Hz | GPS update rate |
| `noise_std` | float | meters | GPS noise standard deviation |

### IMU Sensor

```yaml
sensors:
  imu:
    enabled: bool           # Enable IMU sensor
    update_rate: float     # IMU update rate (Hz)
    accel_noise_std: float # Accelerometer noise standard deviation
    gyro_noise_std: float  # Gyroscope noise standard deviation
```

**Parameter Descriptions:**

| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `enabled` | bool | - | Enable IMU sensor |
| `update_rate` | float | Hz | IMU update rate |
| `accel_noise_std` | float | - | Accelerometer noise standard deviation |
| `gyro_noise_std` | float | - | Gyroscope noise standard deviation |

---

## Logging Configuration

### Logging Settings

```yaml
logging:
  level: str               # Logging level (DEBUG, INFO, WARNING, ERROR)
  format: str              # Log message format
  file: str                # Log file path (optional)
  console: bool           # Enable console logging
```

**Parameter Descriptions:**

| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `level` | str | - | Logging level |
| `format` | str | - | Log message format |
| `file` | str | path | Log file path (optional) |
| `console` | bool | - | Enable console logging |

---

## Configuration Loading

### Python API

```python
from smbna.config import load_config

# Load default configuration
config = load_config()

# Load with environment override
config = load_config(env="production")

# Load specific file
config = load_config(path="config/custom.yaml")
```

### Command Line

```bash
# Validate configuration
python -m smbna.config.validate

# Load and print configuration
python -m smbna.config.print_config
```

---

## Configuration Validation

### Validation Rules

- Required fields must be present
- Parameter types must match expected types
- Parameter values must be within valid ranges
- No unknown parameters allowed

### Error Messages

Configuration validation provides clear error messages for:
- Missing required fields
- Type mismatches
- Invalid value ranges
- Unknown parameters

---

## Related Documentation

- [Architecture Overview](./architecture_overview.md) - System architecture
- [API Reference](./api_reference.md) - API documentation
- [Development Guide](./development_guide.md) - Development setup
- [Testing Guide](./testing_guide.md) - Test execution

---

**Note:** This reference documents configuration parameters and their purposes. It does not provide recommended values or tuning guidance. For operational configuration, see internal documentation.

