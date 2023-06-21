import os
from jq import jq
from json import JSONDecodeError
from pathlib import Path
from .env_utils import *
from config import run_env
from jinja2 import Environment, BaseLoader, Template
from .console_utils import *
from .convert_utils import create_tgt_path
from jinja2.exceptions import UndefinedError


def render_files(env:run_env, data:any, files: "list[Path]", data_key_path:str) -> "list[tuple[Path, str]]":
    tpl_loader = Environment(loader=BaseLoader)
    rendered_files: list[tuple[Path, str]] = []
    for file in files:
        data_substructure = jq(data_key_path).transform(data)
        tgt_path = create_tgt_path(env, file, data_substructure )
        print_info(f"INFO ::: Generating tgt_file_path:  {tgt_path}")

        with open(file, "r", encoding="utf-8") as tpl_file:
            try:
                tpl_str = tpl_file.read()
                tpl_obj = tpl_loader.from_string(tpl_str)
                # TODO Implement file includes
                rendered_file = render_file(tpl_obj, data,data_key_path)
                print_info(rendered_file)
            except UnicodeDecodeError:
                print(
                    f"The file {file} is a binary file or its type cannot be determined."
                )
                rendered_file = ""  # will not be used anyways

        rendered_files.append((tgt_path, rendered_file))

    return rendered_files


def render_file(tpl_obj: Template, cnf: any,data_key_path:str) -> str:
    args = os.environ.copy()
    override_env(cnf,data_key_path)
    args.update(cnf)

    try:
        rendered = tpl_obj.render(args)
    except UndefinedError as err:
        print_warn(err.message)
        return "There was an error during template generation, check the template"
    except UnicodeDecodeError:
        return ""

    return rendered
