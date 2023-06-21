import os
from jq import jq
from json import JSONDecodeError
from pathlib import Path
from jinja2 import Environment, BaseLoader, Template
from .console_utils import *
from .env_utils import override_env
from jinja2.exceptions import UndefinedError



def render_file(tpl_obj: Template, cnf: any,data_key_path:str) -> str:

    args = os.environ.copy()
    override_env(cnf,data_key_path)
    args.update(cnf["env"])
    # print(args)
    # print("eof env from render_file")
    try:
        # undefined=StrictUndefined

        rendered = tpl_obj.render(args)
    except UndefinedError as err:
        print_warn(err.message)
        return "There was an error during template generation, check the template"
    except UnicodeDecodeError:
        return ""

    return rendered


