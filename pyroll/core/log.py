import logging


class LogMixin:
    def __init_subclass__(cls, logger_prefix: str = "pyroll.core", **kwargs):
        cls.logger = logging.getLogger(f"{logger_prefix}.{cls.__qualname__}")
        super().__init_subclass__(**kwargs)
