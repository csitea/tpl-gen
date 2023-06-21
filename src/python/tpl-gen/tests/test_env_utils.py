import os
import pytest


from tpl_gen.libs.utils.env_utils import *

# def test_get_env_var(monkeypatch):
#     monkeypatch.setenv("TEST_VAR", "TEST_VALUE")

#     assert get_env_var("TEST_VAR") == "TEST_VALUE"

#     with pytest.raises(KeyError):
#         get_env_var("NON_EXISTING_VAR")


# def test_get_optional_env_var(monkeypatch):
#     monkeypatch.setenv("TEST_VAR_OPTIONAL", "TEST_VALUE_OPTIONAL")

#     assert (
#         get_optional_env_var("TEST_VAR_OPTIONAL", "FALLBACK_VALUE")
#         == "TEST_VALUE_OPTIONAL"
#     )
#     assert (
#         get_optional_env_var("NON_EXISTING_VAR_OPTIONAL", "FALLBACK_VALUE")
#         == "FALLBACK_VALUE"
#     )


# def test_get_env_as_dict_lower(monkeypatch):
#     monkeypatch.setenv("TEST_VAR_LOWERCASE", "TEST_VALUE_LOWERCASE")

#     env_dict_lower = get_env_as_dict_lower()

#     assert env_dict_lower.get("test_var_lowercase") == "test_value_lowercase"


# def test_override_env(monkeypatch):
#     cnf = {"env": {"steps": {"001-step-name": {"AWS_PROFILE": "initial_value"}}}}

#     monkeypatch.setenv("AWS_PROFILE", "overridden_value")

#     cnf_overridden = override_env(cnf)

#     assert (
#         cnf_overridden["env"]["steps"]["001-step-name"]["AWS_PROFILE"]
#         == "overridden_value"
#     )



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
