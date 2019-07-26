import os

import utility.logging


class EnvGetterError(Exception):
    """raised on errors during env value extracting & parsing"""


class EnvGetter:
    """instance to create a os environment value getter with parsing"""

    def __init__(self, name, default=None, parser=None):
        self.log = utility.logging.get_logger(self)
        self.name = name
        self.default = default
        self.parser = parser
        self.last_value = None
        # safe check happens on init phase to allow max security
        self.safe_check()

    def __call__(self, *args, **kwargs):
        """call to retrieve env value, parsed if necessary"""
        self.safe_check()
        value = os.environ.get(self.name, self.default)
        parsed = value if self.parser is None else self.parser(value)
        if parsed != self.last_value:
            self.log.verbose('[ENV] %s = %s' % (self.name, parsed))
            self.last_value = parsed
        return parsed

    def safe_check(self):
        # make sure setting exists if default wasn't set
        if self.default is None and not self.env_exist():
            msg = 'missing mandatory environment setting key $%s' % self.name
            raise EnvGetterError(msg)
        # make sure value to be retrieved can be parsed
        if self.parser is not None:
            value = os.environ.get(self.name, self.default)
            try:
                self.parser(value)
            except ValueError:
                msg = 'failed to parse env ${}="{}" to <{}>'
                raise EnvGetterError(msg.format(self.name, value,
                                                self.parser.__name__))

    def env_exist(self):
        return self.name in os.environ.keys()


def boolish(value):
    """parse value into bool, tolerating texts ('yes', 'no', etc.)"""
    if str(value).lower() in {'true', 'yes'}:
        return True
    elif str(value).lower() in {'false', 'no'}:
        return False
    else:
        msg = 'failed to parse %s as boolish string to <bool>' % repr(value)
        raise ValueError(msg)


if __name__ == '__main__':

    utility.logging.setup_loggers()

    # manually set env value for testing purposing
    os.environ['MA_ENV_HAPPY'] = 'yes'

    # set up environment setting getter by instancing from EnvGetter
    HAPPY = EnvGetter(name='MA_ENV_HAPPY', parser=boolish)
    RATING = EnvGetter(name='MA_ENV_RATING', parser=int, default='10')

    # retrieve env setting by calling
    print('Rate this module: %s/10' % RATING())
    print("Happy now? %s" % HAPPY())
