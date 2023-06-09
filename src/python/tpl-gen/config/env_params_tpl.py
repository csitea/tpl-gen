"""
This module contains the init_env() function, which initializes several
global environment variables: ORG, APP, ENV, TPL_SRC, CNF_SRC, HOME,
PRODUCT_DIR, BASE_DIR, and TGT. These variables are used across the application
and are set from the system's environment variables.

The init_env() function is intended to be called only once during the execution
of the program, typically at startup. It should not be used during testing.
Instead, to control the environment during testing, use pytest's monkeypatch
feature to temporarily change the environment as needed for each test.

Please note:
- ORG, APP, ENV, TPL_SRC, CNF_SRC, and HOME are mandatory\
    environment variables and the program will raise an error if they are not set.
- PRODUCT_DIR, BASE_DIR, and TGT are optional environment\
    variables. If they are not set, they will be given default values.
  PRODUCT_DIR defaults to three directories above the current working directory.
  BASE_DIR defaults to two directories above the PRODUCT_DIR.
  TGT defaults to the value of CNF_SRC.

Functions:
    init_env() -> None:
        Initializes global environment variables from the system's environment variables.
"""
from pathlib import Path
from utils.env_utils import get_env_var, get_optional_env_var

ORG: str
APP: str
ENV: str
TPL_SRC: str
CNF_SRC: str
HOME: str
PRODUCT_DIR: str
BASE_DIR: str
TGT: str


def init_env():
    """
    Initializes several global environment variables from the system's environment variables.

    This function is intended to be called only once during the execution
    of the program, typically at startup. It should not be used during testing.
    Instead, use pytest's monkeypatch feature to temporarily change the
    environment as needed for each test.

    The function sets the following global variables:
    ORG, APP, ENV, TPL_SRC, CNF_SRC, HOME, PRODUCT_DIR, BASE_DIR, TGT

    Raises:
        KeyError: If a mandatory environment variable is not set.
    """
    global ORG
    global APP
    global ENV
    global TPL_SRC
    global CNF_SRC
    global HOME
    global PRODUCT_DIR
    global BASE_DIR
    global TGT

    ORG = get_env_var("ORG")
    APP = get_env_var("APP")
    ENV = get_env_var("ENV")
    TPL_SRC = get_env_var("TPL_SRC")
    CNF_SRC = get_env_var("CNF_SRC")
    HOME = get_env_var("HOME")
    PRODUCT_DIR = get_optional_env_var("PRODUCT_DIR", Path.cwd().parent.parent.parent)
    BASE_DIR = get_optional_env_var("BASE_DIR", Path(PRODUCT_DIR).parent.parent)
    TGT = get_optional_env_var("TGT", CNF_SRC)
