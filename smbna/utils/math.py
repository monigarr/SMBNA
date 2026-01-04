"""
===============================================================================
SMBNA Utils - Mathematical Utilities
===============================================================================

DESCRIPTION
-----------
Mathematical utility functions used throughout the SMBNA system, including
vector operations, matrix computations, statistical functions, and numerical
helpers.

USAGE
-----
    from smbna.utils.math import norm, trace, angle_between
    import numpy as np
    
    # Vector norm
    v = np.array([1.0, 2.0, 3.0])
    magnitude = norm(v)
    
    # Matrix trace
    M = np.eye(3)
    tr = trace(M)
    
    # Angle between vectors
    v1 = np.array([1.0, 0.0])
    v2 = np.array([0.0, 1.0])
    angle = angle_between(v1, v2)

DEPENDENCIES
------------
- numpy

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

