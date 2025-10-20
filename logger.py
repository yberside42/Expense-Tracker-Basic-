# logger.py

import logging

logging.basicConfig(
    filename= "tracker.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True
)

logger = logging.getLogger("ExpenseTracker")
