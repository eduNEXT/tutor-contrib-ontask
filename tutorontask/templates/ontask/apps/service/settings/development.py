"""Configuration for development."""
import logging.config

from settings.base import *  # NOQA


def get_logger_config(
    debug=False,
):
    """
    Return the appropriate logging config dictionary.

    You should assign the result of this to the LOGGING var in your settings.
    """
    syslog_format = (
        "[%(name)s] %(levelname)s "
        "[user %(userid)s] [%(filename)s:%(lineno)d] "
        "- %(message)s"
    )

    handlers = ['console']

    logger_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(levelname)s %(process)d '
                          '[%(name)s] %(filename)s:%(lineno)d - %(message)s',
            },
            'syslog_format': {'format': syslog_format},
            'raw': {'format': '%(message)s'},
        },
        'handlers': {
            'console': {
                'level': 'DEBUG' if debug else 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'stream': sys.stdout,
            },
        },
        'loggers': {
            'django': {
                'handlers': handlers,
                'propagate': True,
                'level': 'INFO'
            },
            'requests': {
                'handlers': handlers,
                'propagate': True,
                'level': 'WARNING'
            },
            'factory': {
                'handlers': handlers,
                'propagate': True,
                'level': 'WARNING'
            },
            'django.request': {
                'handlers': handlers,
                'propagate': True,
                'level': 'WARNING'
            },
            '': {
                'handlers': handlers,
                'level': 'DEBUG',
                'propagate': False
            },
        }
    }

    return logger_config


logging.config.dictConfig(get_logger_config(debug=DEBUG))

{{ ONTASK_EXTRA_DEV_SETTINGS }}
