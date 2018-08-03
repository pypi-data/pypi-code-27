config = {
    'regindexer.consumer.enabled': False,
    'regindexer.config_file': '/etc/regindexer/config.yaml',
    'logging': {
        'loggers': {
            'regindexer': {
                "level": "INFO",
                "propagate": False,
                "handlers": ["console"],
            },
            'regindexer.consumer': {
                "level": "INFO",
                "propagate": False,
                "handlers": ["console"],
            }
        }
    }
}
