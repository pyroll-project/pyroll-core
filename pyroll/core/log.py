import logging

LOG_PREFIX = "pyroll.core"

__all__ = ["LOG_PREFIX", "LogMixin"]


class LogMixin:
    def __init_subclass__(cls, logger_prefix: str = LOG_PREFIX, **kwargs):
        cls.logger = logging.getLogger(f"{logger_prefix}.{cls.__qualname__}")
        super().__init_subclass__(**kwargs)


global_logger = logging.getLogger(LOG_PREFIX)
