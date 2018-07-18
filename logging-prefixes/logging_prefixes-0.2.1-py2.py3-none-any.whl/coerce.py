import logging

from .adapter import PrependAdapter

FALLBACK_LOGGER = logging.getLogger(__name__).getChild("fallback")


def context_to_path_logger(
    parent, suffix_for_prefix, given_logger=None, fallback_logger=FALLBACK_LOGGER
):
    """
    helper to get a logger with a prefix path for a given object and/or parent
    if a PrependAdapter is given its assumed to be preconfigured
    if no logger is given it tries to get the logger of the parent
    and falls back to the fallback logger
    """
    if isinstance(given_logger, PrependAdapter):
        return given_logger
    if given_logger is None:
        given_logger = getattr(parent, "logger", fallback_logger)
    return PrependAdapter.from_parent(given_logger, suffix_for_prefix)
