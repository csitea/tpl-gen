import os, json
from jq import jq
from .console_utils import print_error, print_info, print_warn


def get_env_var(name: str) -> str:
    """Gets a required environment variable from the os

    Args:
        name (str): the name of the environment variable

    Raises:
        KeyError: when the variable doesn't exist

    Returns:
        str: the value of the variable
    """
    try:
        var_value = os.environ[name]
    except KeyError as err:
        print_warn("Make sure to call init_env() before your main() function")
        print_error(f"env var {name} has no value")
        raise err

    return var_value


def get_optional_env_var(name: str, fallback_value: str) -> str:
    """Gets an optional environment variable from the os

    Args:
        name (str): the name of the environment variable
        fallback_value (str): will be returned if no variable is found in the environment

    Returns:
        str: variable_value
    """
    try:
        var_value = os.environ[name]
    except KeyError:
        print_info(f"using generated value for {name}={fallback_value}")
        return fallback_value

    return var_value


def get_env_as_dict_lower() -> "dict[str, str]":

    environment: dict[str, str] = {}

    for key, value in os.environ.items():
        environment[key.lower()] = value.lower()

    return environment


#  passing by reference for cnf
def override_env(cnf:any,data_key_path:str):

    try:
        # Execute jq query using jq.py library
        sub_data = jq(data_key_path).transform(cnf)
        overridable_dict = get_scalar_key_vals(sub_data)

        for key, val in overridable_dict.items():
            env_val = get_optional_env_var(key,sub_data[key])
            sub_data[key] = env_val

        replace_data_substructure(cnf, data_key_path, sub_data)

    except KeyError as e:
        print_error("could not override_env: " + str(e))
        return cnf
    except TypeError as e:
        print_error("could not override_env: " + str(e))



def get_scalar_key_vals(dictionary):
    scalar_dict = {}
    try:
        for key, value in dictionary.items():
            if isinstance(value, (int, float, str, bool)):
                scalar_dict[key] = value
    except AttributeError as e:
        print_error("could not override_env: " + str(e))
        return scalar_dict
    return scalar_dict


def replace_data_substructure(data, path , value):
    keys = path.split('.')
    _start = data
    for i in keys[:-1]:
        if i == "": # skip the root level
            continue
        _start = _start[i]

    _start[keys[-1]] = value