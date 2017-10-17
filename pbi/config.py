import yaml

f = open('config.yaml', 'r')
_config = yaml.load(f)
f.close()


class Config():
    def __init__(self):
        f = open('config.yaml', 'r')
        self._config = yaml.load(f)
        f.close()

    @staticmethod
    def get(section='main', key=''):
        if section not in _config:
            raise KeyError("Section '{0}' is not in config".format(section))
        try:
            return _config[section][key]
        except KeyError:
            raise KeyError(
                "Key '{0}' not found in config section '{1}'".format(
                    key, section)
            )



