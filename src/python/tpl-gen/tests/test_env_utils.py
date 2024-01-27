import os
import pytest


from tpl_gen.libs.utils.env_utils import *


# Assume your functions are in a file called `your_module.py`
from tpl_gen.libs.utils.env_utils import override_env

def test_override_env_level_01():
    # Set environment variables
    os.environ['TEST_ENV_VAR'] = '1234'
    os.environ['ANOTHER_TEST_ENV_VAR'] = 'abcd'

    # Dictionary to be modified
    cnf = {
        'key1': {
            'TEST_ENV_VAR': 0,
            'ANOTHER_TEST_ENV_VAR': 'xyz',
            'NON_ENV_VAR': 5678
        },
        "key2": "dummy_data"
    }

    # Call function with data_key_path to 'key1'
    override_env(cnf, '.key1')

    # Check that the environment variables were correctly used to override the values in the dictionary
    assert cnf['key1']['TEST_ENV_VAR'] == '1234'
    assert cnf['key1']['ANOTHER_TEST_ENV_VAR'] == 'abcd'

    # # Check that the value not corresponding to an environment variable remained the same
    assert cnf['key1']['NON_ENV_VAR'] == 5678

    # # Check that other parts of the dictionary were not modified
    assert cnf['key2'] == 'dummy_data'

    # # Clean up environment variables
    del os.environ['TEST_ENV_VAR']
    del os.environ['ANOTHER_TEST_ENV_VAR']



def test_override_env_level_02():
    # Set environment variables
    os.environ['TEST_ENV_VAR'] = '1234'
    os.environ['ANOTHER_TEST_ENV_VAR'] = 'abcd'

    # Dictionary to be modified
    cnf = {
        'key_level_01': {
            'TEST_ENV_VAR': 0,
            'ANOTHER_TEST_ENV_VAR': 'xyz',
            'NON_ENV_VAR': 5678,
            'key_level_02': {
                'TEST_ENV_VAR': 0,
                'ANOTHER_TEST_ENV_VAR': 'xyz',
                'NON_ENV_VAR': 5678
            },
        },
        "key2": "dummy_data"
    }

    # Call function with data_key_path to 'key1'
    override_env(cnf, '.key_level_01.key_level_02')

    # Check that the environment variables were correctly used to override the values in the dictionary
    assert cnf['key_level_01']['key_level_02']['TEST_ENV_VAR'] == '1234'
    assert cnf['key_level_01']['key_level_02']['ANOTHER_TEST_ENV_VAR'] == 'abcd'

    # # Check that the value not corresponding to an environment variable remained the same
    assert cnf['key_level_01']['key_level_02']['NON_ENV_VAR'] == 5678

    # # Check that other parts of the dictionary were not modified
    assert cnf['key2'] == 'dummy_data'

    # # Clean up environment variables
    del os.environ['TEST_ENV_VAR']
    del os.environ['ANOTHER_TEST_ENV_VAR']
