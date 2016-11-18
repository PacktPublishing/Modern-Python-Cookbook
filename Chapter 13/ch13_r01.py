"""Python Cookbook

Chapter 13, recipe 1.
"""
from pathlib import Path
from collections import ChainMap

def load_config_file(config_file):
    '''Loads a configuration mapping object with contents
    of a given file.

    :param config_file: File-like object that can be read.
    :returns: mapping with configuration parameter values
    '''
    # Details omitted.

def get_config():
    system_path = Path('/etc/profile')
    home_path = Path('~').expanduser()
    local_paths = [home_path/'.bash_profile',
        home_path/'.bash_login',
        home_path/'.profile']

    configuration_items = [
        dict(
            some_setting = 'Default Value',
            another_setting = 'Another Default',
            some_option = 'Built-In Choice',
        )
    ]


    if system_path.exists():
        with system_path.open() as config_file:
            configuration_items.append(load_config_file(config_file))
    for config_path in local_paths:
        if config_path.exists():
            with config_path.open() as config_file:
                configuration_items.append(load_config_file(config_file))
            break

    configuration = ChainMap(*reversed(configuration_items))
    return configuration

import unittest

class GIVEN_get_config_WHEN_load_THEN_overrides(unittest.TestCase):
    def setUp(self):
        self.mock_system_path = Mock(
            exists = Mock(return_value=True),
            open = mock_open()
        )
        self.exist = Mock(
            exists = Mock(return_value=True),
            open = mock_open()
        )
        self.not_exist = Mock(
            exists = Mock(return_value=False)
        )

        self.mock_expanded_home_path = MagicMock(
            __truediv__ = Mock(
                side_effect = [self.not_exist, self.exist, self.exist]
            )
        )
        self.mock_home_path = Mock(
            expanduser = Mock(
                return_value = self.mock_expanded_home_path
            )
        )
        self.mock_path = Mock(
            side_effect = [self.mock_system_path, self.mock_home_path]
        )

        self.mock_load = Mock(
            side_effect = [{'some_setting': 1}, {'another_setting': 2}]
        )

    def runTest(self):
        with patch('__main__.Path', self.mock_path), patch('__main__.load_config_file', self.mock_load):
            config = get_config()
        # print(config)
        self.assertEqual(2, config['another_setting'])
        self.assertEqual(1, config['some_setting'])
        self.assertEqual('Built-In Choice', config['some_option'])

        # print(self.mock_load.mock_calls)
        self.mock_load.assert_has_calls(
            [
                call(self.mock_system_path.open.return_value.__enter__.return_value),
                call(self.exist.open.return_value.__enter__.return_value)
            ]
        )

        # print(self.mock_expanded_home_path.mock_calls)
        self.mock_expanded_home_path.assert_has_calls(
            [call.__truediv__('.bash_profile'),
            call.__truediv__('.bash_login'),
            call.__truediv__('.profile')]
        )

        # print(self.mock_path.mock_calls)
        self.mock_path.assert_has_calls(
            [call('/etc/profile'), call('~')]
        )

        # print(self.exist.mock_calls)
        self.exist.assert_has_calls( [call.exists()] )

        # print(self.exist.open.mock_calls)
        self.exist.open.assert_has_calls(
            [call(), call().__enter__(), call().__exit__(None, None, None)]
        )

if __name__ == "__main__":
    from unittest.mock import *
    unittest.main(exit=False)
