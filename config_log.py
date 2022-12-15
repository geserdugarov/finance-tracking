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
        'processing':     {'handlers': ['stream_handler'], 'level': 'INFO', 'propagate': False}
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
