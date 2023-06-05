import os
from utils.console_utils import print_error, print_info


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


def get_env_as_dict() -> dict[str, str]:
    environment: dict[str, str] = {}

    for key, value in os.environ.items():
        environment[key.lower()] = value.lower()

    return environment
