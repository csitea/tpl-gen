import os
from jq import jq
from json import JSONDecodeError
from pathlib import Path
from .env_utils import *
from config import run_env
from jinja2 import Environment, BaseLoader, Template
from .console_utils import *
from jinja2.exceptions import UndefinedError





def render_file(tpl_obj: Template, cnf: any,data_key_path:str) -> str:
    args = os.environ.copy()
    override_env(cnf,data_key_path)
    try:
        args.update(cnf)
    except AttributeError as e:
        print_warn("could not update args in render_file: " + str(e))

    try:
        rendered = tpl_obj.render(args)
    except UndefinedError as err:
        print_warn(err.message)
        return "There was an error during template generation, check the template"
    except UnicodeDecodeError:
        return ""

    return rendered
