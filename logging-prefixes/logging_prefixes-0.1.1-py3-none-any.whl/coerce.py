import logging

from .adapter import PrependAdapter

FALLBACK_LOGGER = logging.getLogger(__name__).getChild("fallback")


def coerce_from_parent_to_prepend_logger(parent, suffix_for_prefix, logger=None):
    if isinstance(logger, PrependAdapter):
        return logger

    if logger is None:
        logger = getattr(parent, "logger", FALLBACK_LOGGER)
    return PrependAdapter.from_parent(logger, suffix_for_prefix)
