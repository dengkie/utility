import json
import os

import utility.logging
from utility.configuring import EnvGetter


CFG_PATH = EnvGetter('MA_CFG_PATH', './')


class JsonConfigError(Exception):
    """raised when cfg file loading fails"""
    def __init__(self, detail_msg):
        msg = 'config file loading failed -- ' + detail_msg
        super().__init__(msg)


class JsonMissingError(JsonConfigError):
    """raised when cfg file can't be found"""


class JsonConfig:
    """subclass & define class attributes to auto-load values from .json file"""

    # override this to achieve same effect as in __init
    __optional__ = False

    def __init__(self, filename=None):
        self.log = utility.logging.get_logger(self)
        # config file name by default equals class name, if not manually set
        fn = filename or '{cls}.json'.format(cls=self.__class__.__name__)
        # search through all paths defined in env
        for dir_path in CFG_PATH().split(':'):
            cfg_path = os.path.join(dir_path, fn)
            if not os.path.exists(cfg_path):
                continue
            else:
                with open(cfg_path) as f:
                    try:
                        cfg = json.load(f)
                    except json.JSONDecodeError:
                        msg = 'failed to decode json file: %s' % cfg_path
                        raise JsonConfigError(msg)
                    else:
                        self.load_from(cfg)
                        msg = '[CFG] %s loaded' % fn
                        self.log.verbose(msg)
                        break
        else:
            # no cfg file found in any path defined
            msg = '[CFG] %s not found' % fn
            if self.__optional__:
                msg += '; using value from class definition'
                self.log.verbose(msg)
            else:
                raise JsonMissingError(msg)

    def load_from(self, cfg):
        """load value from cfg into non-magic class attributes"""
        fields = list(attr for attr in self.__class__.__dict__
                      if not attr.endswith('__'))
        for field in fields:
            try:
                value = cfg[field]
            except KeyError:
                msg = 'missing field [%s]' % field
                raise JsonConfigError(msg)
            value_type = type(self.__class__.__dict__[field])
            if not isinstance(value, value_type):
                msg = 'field "{}={}" should be value type {} (defined in class)'
                raise JsonConfigError(msg.format(field, value, value_type))
            self.__setattr__(field, value)


if __name__ == '__main__':

    # define config data holder by subclassing AutoLoad
    class NetworkConfig(JsonConfig):
        # for config file to be optional, override here
        __optional__ = True
        # class attributes define both value type & default values
        server_ip = '192.168.5.1'
        server_port = 8080
        verify_server_ip = False

    # init a instance to load cfg from json file
    net_cfg = NetworkConfig()

    # notice instance carries configured value while Class still holds defaults
    print('"server_ip" in cfg instance = ', net_cfg.server_ip)
    print('"server_ip" in cfg class (default) = ', NetworkConfig.server_ip)
