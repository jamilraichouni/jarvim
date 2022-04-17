"""Enhance loguru logger."""

# Standard library:
import functools

# 3rd party:
from loguru import logger

try:
    logger.level("NOTICE")
except ValueError:
    # introduce NOTICE level when not already existing:
    logger.level("NOTICE", no=25, color="<green><bold>")
    logger.__class__.notice = functools.partialmethod(  # type: ignore
        logger.__class__.log, "NOTICE"
    )
# format output for some of the default levels:
logger.level("CRITICAL", color="<bg red><fg black><bold>")
logger.level("INFO", color="<white>")
logger.level("DEBUG", color="<cyan>")
logger.level("TRACE", color="<magenta>")
