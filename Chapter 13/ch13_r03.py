"""Python Cookbook

Chapter 13, recipe 3.
"""

def load_config_file(config_file) -> dict:
    '''Loads a configuration mapping object with contents
    of a given file.

    :param config_file: File-like object that can be read.
    :returns: mapping with configuration parameter values
    '''
    code = compile(config_file.read(), config_file.name, 'exec')
    locals = {}
    exec(code, {'__builtins__':__builtins__}, locals)
    return locals

from pathlib import Path
import platform

def load_config_file_path(config_file) -> dict:
    code = compile(config_file.read(), config_file.name, 'exec')
    globals = {'__builtins__':__builtins__,
               'Path': Path,
               'platform': platform}
    locals = {}
    exec(code, globals, locals)
    return locals

import io
settings_file = io.StringIO("""
'''Weather forecast for Offshore including the Bahamas
'''
query = {'mz': ['ANZ532', 'AMZ117', 'AMZ080']}
url = {
  'scheme': 'http',
  'netloc': 'forecast.weather.gov',
  'path': '/shmrn.php'
}
""")
# Add a ``name`` attribute to mimic a file
settings_file.name = 'settings.py'

settings_file_2 = io.StringIO(
'''
base = Path('/var/app/')
log = base/'log'
out = base/'out'
'''
)
# Add a ``name`` attribute to mimic a file
settings_file_2.name = 'settings.py'

__test__ = {
    'load_config_file':
'''
>>> from pprint import pprint
>>> pprint(load_config_file(settings_file))
{'__doc__': 'Weather forecast for Offshore including the Bahamas\\n',
 'query': {'mz': ['ANZ532', 'AMZ117', 'AMZ080']},
 'url': {'netloc': 'forecast.weather.gov',
         'path': '/shmrn.php',
         'scheme': 'http'}}
''',

    'load_config_file_path':
'''
>>> from pprint import pprint
>>> settings = load_config_file_path(settings_file_2)
>>> pprint(settings)
{'base': PosixPath('/var/app'),
 'log': PosixPath('/var/app/log'),
 'out': PosixPath('/var/app/out')}

'''
}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
