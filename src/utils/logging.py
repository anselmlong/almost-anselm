"""Project logging helpers.
"""

import logging


def setup_logging(level: str = "INFO"):
    logging.basicConfig(level=getattr(logging, level))
    return logging.getLogger("almost-anselm")


logger = setup_logging()
