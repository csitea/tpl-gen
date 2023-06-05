import json
from pathlib import Path

import yaml
from utils import console_utils as cw
from utils.convert_utils import create_tgt_path
from jinja2 import Environment, BaseLoader, exceptions


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

    return cnf


def render_files(files: list[Path], cnf: any):
    tpl_loader = Environment(loader=BaseLoader)
    for file in files:
        tgt_path = create_tgt_path(file)

        with open(file, "r", encoding="utf-8") as tpl_file:
            tpl_str = tpl_file.read()
            tpl_obj = tpl_loader.from_string()
