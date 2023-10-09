# -*- coding: utf-8 -*-

import logging.config

log_settings = {
    'version': 1,
    'formatters': {
        'file_formatter': {
            'format': '%(asctime)s-%(name)s-%(levelname)s-%(message)s'
        },
        'stream_formatter': {
            'format': '%(asctime)s-%(message)s'
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'file_formatter',
            'filename': 'vk_bot.log',
            'encoding': 'UTF-8',
        },
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'stream_formatter',
        },
    },
    'loggers': {
        'main_log': {
            'handlers': ['file_handler', 'stream_handler'],
            'level': 'INFO',
        },
    },
}

logging.config.dictConfig(log_settings)
main_log = logging.getLogger('main_log')
