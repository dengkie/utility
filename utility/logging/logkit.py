import os
import logging
import logging.handlers
import verboselogs
import coloredlogs


LOG_LEVEL = os.environ.get('MA_LOG_LEVEL', 'INFO')

# a name for all loggers to be registered under
DEFAULT_ROOT = ' '

# log path & format setting for rotating file
DEFAULT_LOG_PATH = '.ma/logkit/debug.log'
ROT_FILE_SIZE = 1024 * 1024
ROT_FILE_BAK_COUNT = 5
FMT_FILE = '%(asctime)s [%(levelname)-8s|%(name)16s] %(message)s'

# format setting for coloredlogs with verboselogs
FMT_CONS = '%(name)16s | %(levelname)8s | %(message)s'
FIELD_STYLE = {
    'asctime': {'color': 'green'},
    'hostname': {'color': 'magenta'},
    'levelname': {'color': 'white', 'faint': True, 'bold': True},
    'name': {'color': 8, 'faint': True},
    'programname': {'color': 'cyan'}
}
LEVEL_STYLE = {
    'critical': {'background': 'red', 'color': 'white', 'bright': True},
    'error': {'background': 'red', 'color': 208},
    'success': {'background': 'green', 'color': 255},
    'warning': {'color': 'yellow', 'bright': True},
    'notice': {'color': 'cyan'},
    'info': {'color': 'green'},
    'verbose': {'color': 63},
    'debug': {'color': 'white'},
    'spam': {'color': 'white', 'faint': True}
}


def get_logger(target=None) -> verboselogs.VerboseLogger:
    """return a verbose logger auto-registered under a root"""
    if target is None:
        rooted_name = DEFAULT_ROOT
    else:
        name = target if isinstance(target, str) else target.__class__.__name__
        rooted_name = '%s.%s' % (DEFAULT_ROOT, name)
    return verboselogs.VerboseLogger(rooted_name)


def setup_loggers(logfile_path=None):
    """direct all loggers under root_name to rotating file & console"""
    root_logger = logging.getLogger(name=DEFAULT_ROOT)
    if root_logger.hasHandlers():
        return
    # setup rotating file handler if file path exists
    if logfile_path is not None:
        rotating_file_handler = logging.handlers.RotatingFileHandler(
            logfile_path,
            maxBytes=ROT_FILE_SIZE,
            backupCount=ROT_FILE_BAK_COUNT)
        rotating_file_handler.setFormatter(logging.Formatter(FMT_FILE))
        root_logger.addHandler(rotating_file_handler)
    # setup console handler using coloredlogs
    coloredlogs.install(level=LOG_LEVEL,
                        fmt=FMT_CONS,
                        level_styles=LEVEL_STYLE,
                        field_styles=FIELD_STYLE)


if __name__ == '__main__':
    log = get_logger('logkit')
    setup_loggers()

    log.critical('program may be unable to continue running')
    log.error('certain function has not been able to perform')
    log.success('a explicit confirmation of success')
    log.warning('indication of unexpected event occurred')
    log.notice('auditing info for multiple success path')
    log.info('confirmation of things working')
    log.verbose('provide insight for user on behavior')
    log.debug('detailed info for diagnosing problems')
    log.spam('a desperate measure for late night debugging')
