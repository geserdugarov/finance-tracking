import logging.config


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {'format': '[%(levelname)s | %(name)s | %(asctime)s] %(message)s'},
    },

    'handlers': {
        'stream_handler': { 'class': 'logging.StreamHandler', 'formatter': 'default_formatter'},
    },

    'loggers': {
        '': {'handlers': ['stream_handler'], 'level': 'INFO', 'propagate': True},
        'processing.balance':  {'handlers': ['stream_handler'], 'level': 'INFO', 'propagate': False},
        'processing.currency': {'handlers': ['stream_handler'], 'level': 'INFO', 'propagate': False},
        'processing.export':   {'handlers': ['stream_handler'], 'level': 'INFO', 'propagate': False},
        'processing.wallet':   {'handlers': ['stream_handler'], 'level': 'INFO', 'propagate': False}
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
