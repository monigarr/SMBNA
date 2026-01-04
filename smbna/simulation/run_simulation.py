"""
===============================================================================
SMBNA Simulation - Navigation Simulation Runner (Baseline EKF)
===============================================================================

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0

===============================================================================
SMBNA — Navigation Simulation Runner (Baseline EKF)
===============================================================================

PURPOSE
-------
This script provides a reference-grade simulation harness for evaluating
autonomous drone navigation under GPS-degraded, denied, or adversarial
conditions. It is intended to serve as a stable baseline against which
belief-centric arbitration, invariant checks, and explicit refusal logic
can be introduced and evaluated.

The implementation prioritizes clarity, reproducibility, and extensibility
over performance or hardware fidelity.

-------------------------------------------------------------------------------
WHAT THIS SCRIPT DOES
-------------------------------------------------------------------------------

• Runs a time-stepped planar drone navigation simulation
• Maintains a ground-truth state for evaluation
• Estimates state using an Extended Kalman Filter (EKF) baseline:
    - Position (x, y)
    - Velocity (vx, vy)
    - Heading (θ placeholder)
• Simulates realistic sensor conditions:
    - GPS noise
    - GPS dropout
    - Intermittent GPS spoofing / bias injection
    - IMU noise
• Logs internal metrics required for:
    - Trajectory plots
    - Innovation (residual) analysis
    - Failure mode characterization
    - Paper figures and tables
• Exposes clean insertion points for:
    - Invariant validation
    - Belief arbitration
    - Trust scoring
    - Explicit refusal / safe-degrade behavior

-------------------------------------------------------------------------------
WHAT THIS SCRIPT INTENTIONALLY DOES NOT DO
-------------------------------------------------------------------------------

• No advanced motion model (simple kinematics only)
• No nonlinear attitude dynamics or aerodynamics
• No hardware-specific sensor timing
• No learning-based components
• No automatic failure correction or rejection logic

These omissions are deliberate to ensure:
    (1) Reviewer trust
    (2) Auditability
    (3) Clear attribution of improvements in downstream work

-------------------------------------------------------------------------------
STATE REPRESENTATION
-------------------------------------------------------------------------------

State vector (5D):
    x = [pos_x, pos_y, vel_x, vel_y, heading]

Measurement models:
    • GPS: position only (x, y)
    • IMU: velocity proxy (vx, vy) with noise

-------------------------------------------------------------------------------
PRIMARY OUTPUTS
-------------------------------------------------------------------------------

The simulation returns a dictionary of NumPy arrays containing:

    logs["truth"]            → Ground-truth state over time
    logs["estimate"]         → EKF state estimate over time
    logs["gps_used"]         → Binary flag indicating GPS availability
    logs["innovation_norm"]  → GPS residual norm (critical for invariants)

These logs are designed to map directly to:
    • Paper figures (trajectory, error, residuals)
    • Evaluation tables
    • Monte Carlo aggregation scripts

-------------------------------------------------------------------------------
USAGE
-------------------------------------------------------------------------------

Command line:
    python run_simulation.py
    python run_simulation.py --time 600 --seed 123
    python -m smbna.simulation.run_simulation


Programmatic:
    from run_simulation import run_simulation, SimConfig
    logs = run_simulation(SimConfig())

-------------------------------------------------------------------------------
EXTENSION POINTS (DO NOT MODIFY CORE LOGIC)
-------------------------------------------------------------------------------

Future work should extend this script by ADDITION, not modification:

    • Insert invariant checks after EKF update
    • Gate GPS usage via trust arbitration
    • Trigger refusal modes when invariants are violated
    • Compare baseline vs belief-centric variants via wrapper scripts

Core EKF logic should remain untouched to preserve baseline validity.

-------------------------------------------------------------------------------
INTENDED AUDIENCE
-------------------------------------------------------------------------------

• Autonomy engineers
• Applied ML / robotics researchers
• Safety and assurance reviewers
• Defense / critical-infrastructure stakeholders

-------------------------------------------------------------------------------
LICENSE / ATTRIBUTION
-------------------------------------------------------------------------------

Part of the SMBNA (Secure Multi-Belief Navigation Arbitration) project.

Author: MoniGarr
Github: github.com/MoniGarr/SMBNA
Year: 2026

This file is designed to remain usable as a long-lived reference artifact.
===============================================================================
"""


import numpy as np
import argparse
from dataclasses import dataclass
from typing import Dict, Tuple
from smbna.beliefs.refusal_logic import should_refuse_navigation

# -----------------------------
# Guard for module execution
# -----------------------------
if __name__ == "__main__" and __package__ is None:
    raise RuntimeError(
        "This module must be run as a package:\n"
        "python -m smbna.simulation.run_simulation"
    )


# -----------------------------
# Configuration
# -----------------------------

@dataclass
class SimConfig:
    dt: float = 0.1
    total_time: float = 300.0  # seconds
    gps_noise: float = 2.0     # meters
    imu_noise: float = 0.05
    gps_dropout_prob: float = 0.2
    spoof_bias: float = 15.0   # meters
    seed: int = 42


# -----------------------------
# Ground Truth Dynamics
# -----------------------------

def propagate_truth(state: np.ndarray, dt: float) -> np.ndarray:
    """
    Simple planar drone dynamics:
    state = [x, y, vx, vy, heading]
    """
    x, y, vx, vy, theta = state
    x += vx * dt
    y += vy * dt
    return np.array([x, y, vx, vy, theta])


# -----------------------------
# Sensors
# -----------------------------

def simulate_gps(state: np.ndarray, cfg: SimConfig) -> Tuple[bool, np.ndarray]:
    """
    Returns (valid, measurement)
    """
    if np.random.rand() < cfg.gps_dropout_prob:
        return False, None

    noise = np.random.randn(2) * cfg.gps_noise
    measurement = state[:2] + noise

    # occasional spoofing
    if np.random.rand() < 0.05:
        measurement += cfg.spoof_bias * np.random.randn(2)

    return True, measurement


def simulate_imu(state: np.ndarray, cfg: SimConfig) -> np.ndarray:
    accel_noise = np.random.randn(2) * cfg.imu_noise
    return state[2:4] + accel_noise


# -----------------------------
# EKF
# -----------------------------

def ekf_predict(x, P, u, Q, dt):
    F = np.eye(5)
    F[0, 2] = dt
    F[1, 3] = dt

    B = np.zeros((5, 2))
    B[2, 0] = dt
    B[3, 1] = dt

    x = F @ x + B @ u
    P = F @ P @ F.T + Q
    return x, P


def ekf_update(x, P, z, R):
    H = np.zeros((2, 5))
    H[0, 0] = 1
    H[1, 1] = 1

    y = z - H @ x
    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)

    x = x + K @ y
    P = (np.eye(len(x)) - K @ H) @ P
    return x, P, np.linalg.norm(y)


# -----------------------------
# Simulation Loop
# -----------------------------

def run_simulation(cfg: SimConfig) -> Dict:
    np.random.seed(cfg.seed)

    steps = int(cfg.total_time / cfg.dt)

    truth = np.array([0, 0, 1.0, 0.5, 0])
    x = truth + np.random.randn(5)
    P = np.eye(5)

    Q = np.eye(5) * 0.01
    R = np.eye(2) * cfg.gps_noise**2

    logs = {
        "truth": [],
        "estimate": [],
        "gps_used": [],
        "innovation_norm": [],
        "refusal":  [],
    }

    for _ in range(steps):
        truth = propagate_truth(truth, cfg.dt)
        imu = simulate_imu(truth, cfg)

        x, P = ekf_predict(x, P, imu, Q, cfg.dt)

        gps_valid, gps_meas = simulate_gps(truth, cfg)
        if gps_valid:
            x, P, innov = ekf_update(x, P, gps_meas, R)

            # Belief-level refusal signal (NO gating, NO correction)
            refuse = should_refuse_navigation(innov)

            logs["gps_used"].append(1)
            logs["innovation_norm"].append(innov)
            logs["refusal"].append(refuse)
        else:
            logs["gps_used"].append(0)
            logs["innovation_norm"].append(np.nan)
            logs["refusal"].append(False)

        logs["truth"].append(truth.copy())
        logs["estimate"].append(x.copy())

    for k in logs:
        logs[k] = np.array(logs[k])

    return logs


# -----------------------------
# Entry Point
# -----------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--time", type=float, default=300)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    cfg = SimConfig(total_time=args.time, seed=args.seed)
    logs = run_simulation(cfg)

    print("Simulation complete.")
    print(f"Final position error: "
          f"{np.linalg.norm(logs['truth'][-1][:2] - logs['estimate'][-1][:2]):.2f} m")


if __name__ == "__main__":
    main()
