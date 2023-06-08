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


def get_env_as_dict_lower() -> dict[str, str]:
    """_summary_

    Returns:
        dict[str, str]: _description_
    """
    environment: dict[str, str] = {}

    for key, value in os.environ.items():
        environment[key.lower()] = value.lower()

    return environment


# allow environment variables to override configuration
# Warning: this is an important feature, users now need
# to be aware of their environment.
def override_env(cnf):
    """overrides the cnf with environment variables
        this function is mainly kept for backwards compatibility
        we should move away from specifics like STEP

    Args:
        cnf (Any): The configuration

    Returns:
        Any: The configuration overriden with env variables
    """
    # it only makes sense to talk about overriding variables on step level
    # since nested variables within steps are flattened to environment level
    # variables, i.e. :
    #     cnf["steps"]["001-step-name"]["AWS_PROFILE"]
    #     becomes AWS_PROFILE, thus no need to override
    #     cnf["aws"]["AWS_PROFILE"], since it won't be considered
    try:
        if cnf["env"] == None or cnf["env"]["steps"] == None:
            return cnf
    except KeyError:
        return cnf

    for step in cnf["env"]["steps"]:
        for step_var in cnf["env"]["steps"][step]:
            # checks if it is defined as environment variable
            # if it's not, preserves the value of itself.
            cnf["env"]["steps"][step][step_var] = os.getenv(
                step_var, cnf["env"]["steps"][step][step_var]
            )

    return cnf
