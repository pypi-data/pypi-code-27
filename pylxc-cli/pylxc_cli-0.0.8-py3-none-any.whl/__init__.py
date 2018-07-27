__version__ = '0.0.8'
__all__ = ["__main__.py", 'liblxc']

import logging
import logging.config

DEFAULT_LOGGING = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },

    "handlers": {
        # "console": {
        #     "class": "logging.StreamHandler",
        #     "level": "DEBUG",
        #     "formatter": "simple",
        #     "stream": "ext://sys.stdout"
        # },

        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": "info.log",
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        },

        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "simple",
            "filename": "errors.log",
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        }
    },

    "loggers": {
        "my_module": {
            "level": "ERROR",
            # "handlers": ["console"],
            "propagate": "no"
        }
    },

    "root": {
        "level": "INFO",
        "handlers": ["info_file_handler", "error_file_handler"]
        # "handlers": ["console", "info_file_handler", "error_file_handler"]
    }
}

logging.config.dictConfig(DEFAULT_LOGGING)
