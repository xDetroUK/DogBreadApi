import structlog
import logging

def configure_logging(log_level: str = "INFO"):
    """Configure structured logging with structlog."""
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    logging.basicConfig(level=log_level.upper())
    logger = structlog.get_logger()
    logger.info("Logging configured", level=log_level)
