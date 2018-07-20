import logging
from pathlib import Path
import sys

import coloredlogs

from munch import munchify

import yaml

cfg = munchify(yaml.safe_load(open(Path(__file__).parent / "config.yaml")))


def configure_logging():
    logging.root.handlers = []
    coloredlogs.install(stream=sys.stderr, **cfg.logging.config)
    for logger, level in cfg.logging.loggers.items():
        logging.getLogger(logger).setLevel(getattr(logging, level.upper()))
    logging.captureWarnings(True)
