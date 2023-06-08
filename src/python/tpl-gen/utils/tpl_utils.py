import json
import os
from pathlib import Path
from utils import env_utils as eu
import yaml
from jinja2 import Environment, BaseLoader, Template
from utils import console_utils as cw
from utils.convert_utils import create_tgt_path
from jinja2.exceptions import UndefinedError
from rich.padding import Padding


def read_json_file(file: Path) -> any:
    try:
        with open(file, "r", encoding="utf-8") as cnf_file:
            cnf = json.load(cnf_file)
    except FileNotFoundError:
        cw.print_warn(f"No file {file} found, attempting to use yaml")
    else:
        return cnf

    try:
        yaml_file = file.with_suffix(".yaml")
        with open(yaml_file, "r", encoding="utf-8") as cnf_file:
            cnf = yaml.load(cnf_file, yaml.SafeLoader)
    except FileNotFoundError as err:
        cw.print_error(f'The file "{yaml_file}" has no yaml nor json variant')
        raise err

    cw.print_success(f"Using {yaml_file}")

    return cnf


def render_files(files: list[Path], cnf: any) -> list[tuple[Path, str]]:
    tpl_loader = Environment(loader=BaseLoader)
    rendered_files: list[tuple[Path, str]] = []
    for file in files:
        tgt_path = create_tgt_path(file)
        cw.print_info(f"INFO ::: Generating tgt_file_path:  {tgt_path}")

        with open(file, "r", encoding="utf-8") as tpl_file:
            tpl_str = tpl_file.read()
            tpl_obj = tpl_loader.from_string(tpl_str)

        # TODO Implement file includes
        rendered_file = render_file(tpl_obj, cnf)
        cw.print_info(rendered_file)

        rendered_files.append((tgt_path, rendered_file))

    return rendered_files


def render_files_step(files: list[Path], cnf: any) -> list[tuple[Path, str]]:
    tpl_loader = Environment(loader=BaseLoader)
    rendered_files: list[tuple[Path, str]] = []
    for file in files:
        if not eu.get_env_var("STEP") in str(file):
            continue

        tgt_path = create_tgt_path(file)
        cw.print_info(f"generating tgt_file_path:  {tgt_path}")

        with open(file, "r", encoding="utf-8") as tpl_file:
            tpl_str = tpl_file.read()
            tpl_obj = tpl_loader.from_string(tpl_str)

        # TODO Implement file includes
        rendered_file = render_file(tpl_obj, cnf)
        cw.print_yaml(rendered_file)
        rendered_files.append((tgt_path, rendered_file))

    return rendered_files


def render_files_multi(files: list[Path], cnf: any) -> list[tuple[Path, str]]:
    rendered_files: list[tuple[Path, str]] = []
    for step, data in cnf["env"]["steps"].items():
        cw.print_info(f"Iterating step {step}")
        rendered_files.append(render_files(files, data))

    return rendered_files


def render_file(tpl_obj: Template, cnf: any) -> str:
    args = os.environ.copy()
    cnf = eu.override_env(cnf)
    args.update(cnf["env"])
    try:
        rendered = tpl_obj.render(args)
    except UndefinedError as err:
        cw.print_warn(err.message)
        return "There was an error during template generation, check the template"

    return rendered
