"""
This module loads configuration data for the application from environment variables.

Attributes:
    ORG (str): Name of the organization. Loaded from the ORG environment variable.
    APP (str): Name of the application. Loaded from the APP environment variable.
    ENV (str): Current environment (e.g., "dev", "prd"). Loaded from the ENV environment variable.

    PRODUCT_DIR (str): Path to the product directory. Loaded from the PRODUCT_DIR environment variable.
    BASE_DIR (str): Path to the base directory. Loaded from the BASE_DIR environment variable.

    TPL_SRC (str): Path to the template source. Loaded from the TPL_SRC environment variable.
    CNF_SRC (str): Path to the configuration source. Loaded from the CNF_SRC environment variable.
    TGT (str): Path to the target. Loaded from the TGT environment variable.

Functions:
    get_env_var(var_name: str) -> str: Utility function imported from utils.env_utils to fetch environment variables.
    Raises an error if the environment variable is not set.
"""
from pathlib import Path
from utils.env_utils import get_env_var, get_optional_env_var


ORG = get_env_var("ORG")
APP = get_env_var("APP")
ENV = get_env_var("ENV")

TPL_SRC = get_env_var("TPL_SRC")
CNF_SRC = get_env_var("CNF_SRC")
HOME = get_env_var("HOME")

PRODUCT_DIR = get_optional_env_var("PRODUCT_DIR", Path.cwd().parent.parent.parent)
BASE_DIR = get_optional_env_var("BASE_DIR", Path(PRODUCT_DIR).parent.parent)

TGT = get_optional_env_var("TGT", CNF_SRC)
