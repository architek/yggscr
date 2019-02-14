import configparser


class Config(dict):

    def __init__(self):
        pass

    def load_config(self, filename, **options):
        """Load config and default values and return config as a dict"""
        options.setdefault('allow_no_value', True)
        options.setdefault('interpolation', None)
        options.setdefault('strict', True)
        options.setdefault('defaults', {
            'proxy': '',
            'debug': 'False',
            'if.host': '127.0.0.1',
            'if.port': 8333,
            'transmission.host': '',
            'rtorrent.rpc_url': '',
            'deluge.host': '',
        })
        self.conf = configparser.ConfigParser(**options)

        if not self.conf.read(filename):
            raise FileNotFoundError("Can't find filename <{}>".format(filename))

        for section in self.conf.sections():
            for key in self.conf.options(section):
                value = self.conf.get(section, key)
                if section != 'base':
                    key = section + '.' + key
                self[key.lower()] = value

        return self

    def bool(self, key):
        """Convert string config to boolean"""
        if "." in key:
            section, key = key.split('.')
        else:
            section = 'base'
        return self.conf.getboolean(section, key)
