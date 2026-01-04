"""
===============================================================================
SMBNA Utils - Logging Utilities
===============================================================================

DESCRIPTION
-----------
Logging configuration and utilities for the SMBNA system. Provides structured
logging setup, log formatting, and log level management for consistent
logging across all modules.

USAGE
-----
    from smbna.utils.logging import setup_logging, get_logger
    
    # Setup logging
    setup_logging(level="INFO", log_file="/var/log/smbna/smbna.log")
    
    # Get logger
    logger = get_logger(__name__)
    logger.info("System initialized")
    logger.error("Error occurred", exc_info=True)

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

