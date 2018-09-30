import configparser


class Config(dict):

    def __init__(self):
        pass

    def load_config(self, filename, **options):
        options.setdefault('allow_no_value', True)
        options.setdefault('interpolation', None)
        self.conf = configparser.ConfigParser(**options)
        if not self.conf.read(filename):
            raise FileNotFoundError
        for section in self.conf.sections():
            for key in self.conf.options(section):
                value = self.conf.get(section, key)
                if section != 'base':
                    key = section + '.' + key
                self[key.lower()] = value

        return self

    def bool(self, key):
        if "." in key:
            section, key = key.split('.')
        else:
            section = 'base'
        return self.conf.getboolean(section, key)
