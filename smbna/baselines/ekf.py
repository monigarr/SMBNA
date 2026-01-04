"""
===============================================================================
SMBNA Baselines - Extended Kalman Filter (EKF) Baseline
===============================================================================

DESCRIPTION
-----------
Classical Extended Kalman Filter implementation for sensor fusion, used as a
baseline comparison against the SMBNA belief-centric approach. This EKF fuses
GPS and IMU measurements using standard Kalman filtering techniques.

⚠️  CRITICAL: This baseline must remain unchanged to preserve comparison validity.
See ENGINEERING_GUARDRAILS.md for constraints.

USAGE
-----
    from smbna.baselines.ekf import EKFNavigation
    import numpy as np
    
    Q = np.eye(6) * 0.01  # Process noise
    R_gps = np.eye(3) * 4.0  # GPS measurement noise
    
    ekf = EKFNavigation(Q, R_gps)
    
    # Predict step
    accel = np.array([0.1, 0.2, 9.8])
    ekf.predict(accel, dt=0.1)
    
    # Update step
    position = np.array([10.0, 20.0, 100.0])
    ekf.update_gps(position)
    
    # Get state
    x, P = ekf.get_state()

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

import numpy as np

class EKFNavigation:
    def __init__(self, Q, R_gps):
        self.x = np.zeros((6, 1))
        self.P = np.eye(6) * 10.0
        self.Q = Q
        self.R_gps = R_gps

    def predict(self, accel, dt):
        F = np.eye(6)
        F[0:3, 3:6] = np.eye(3) * dt

        B = np.zeros((6, 3))
        B[3:6, :] = np.eye(3) * dt

        self.x = F @ self.x + B @ accel.reshape(3, 1)
        self.P = F @ self.P @ F.T + self.Q

    def update_gps(self, position):
        H = np.zeros((3, 6))
        H[:, 0:3] = np.eye(3)

        y = position.reshape(3, 1) - H @ self.x
        S = H @ self.P @ H.T + self.R_gps
        K = self.P @ H.T @ np.linalg.inv(S)

        self.x = self.x + K @ y
        self.P = (np.eye(6) - K @ H) @ self.P

    def get_state(self):
        return self.x.flatten(), self.P
