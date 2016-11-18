"""Python Cookbook

Chapter 13, recipe 4
"""
from pathlib import Path
import platform

def load_config_file(config_file, classname='Configuration') -> dict:
    code = compile(config_file.read(), config_file.name, 'exec')
    globals = {'__builtins__':__builtins__,
               'Path': Path,
               'platform': platform}
    locals = {}
    exec(code, globals, locals)
    return locals[classname]

import importlib
def load_config_module(name):
    module_name, _, class_name = name.rpartition('.')
    settings_module = importlib.import_module(module_name)
    return vars(settings_module)[class_name]

class ConfigMetaclass(type):
    def __repr__(self):
        name = super().__name__ + '(' + ', '.join(b.__name__ for b in super().__bases__) + ')'
        base_values = {n:v
            for base in reversed(super().__mro__)
                for n, v in vars(base).items()
                    if not n.startswith('_')}
        values_text = ['    {0} = {1!r}'.format(name, value) for name, value in base_values.items()]
        return '\n'.join(["class {}:".format(name)] + values_text)

class Configuration(metaclass=ConfigMetaclass):
    unchanged = 'default'
    override = 'default'
    feature_override = 'default'
    feature = 'default'

class Customized(Configuration):
    override = 'customized'
    feature_override = 'customized'

class Feature_On(Configuration):
    feature = 'enabled'
    feature_override = 'enabled'

class Config_Feature(Feature_On, Customized):
    local = 'local'

__test__ = {
    'load_config_file':
'''
>>> settings_path = Path('settings.py')
>>> with settings_path.open() as settings_file:
...     configuration = load_config_file(settings_file, 'Chesapeake')
>>> configuration.__doc__.strip()
'Weather for Cheaspeake Bay'
>>> configuration.query
{'mz': ['ANZ532']}
>>> configuration.url['netloc']
'forecast.weather.gov'
''',

    'load_config':
'''
>>> configuration = load_config_module('settings.Chesapeake')
>>> configuration.__doc__.strip()
'Weather for Cheaspeake Bay'
>>> print(configuration)  # doctest: +ELLIPSIS
<class 'settings.Chesapeake'>
>>> from pprint import pprint
>>> pprint(vars(configuration))
mappingproxy({'__doc__': '\\n    Weather for Cheaspeake Bay\\n    ',
              '__module__': 'settings',
              'query': {'mz': ['ANZ532']}})
'''
}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=0)
