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


def read_config_file(file: Path) -> any:

    file_extension = file.suffix

    if file_extension == "json":
        try:
            with open(file, "r", encoding="utf-8") as cnf_file:
                cnf = json.load(cnf_file)
        except FileNotFoundError:
            cw.print_warn(f"No file {file} found, attempting to use yaml")
        else:
            return cnf
    else:
        try:
            with open(file, "r", encoding="utf-8") as cnf_file:
                cnf = yaml.load(cnf_file, yaml.Loader)
        except FileNotFoundError as err:
            cw.print_error(f'The file "{file}" has no yaml nor json variant')
            raise err

    cw.print_success(f"Using {file}")

    return cnf


def replace_file_extension(file_path, new_extension):
    base_path = os.path.splitext(file_path)[0]  # Extract the base path without the extension
    new_path = base_path + new_extension  # Create the new file path with the desired extension
    # Rename the file object using the new path
    os.rename(file_path, new_path)

    # Update the file object with the new path
    return new_path


def render_files(files: list[Path], cnf: any) -> list[tuple[Path, str]]:

    tpl_loader = Environment(loader=BaseLoader)
    rendered_files: list[tuple[Path, str]] = []
    for file in files:
        tgt_path = create_tgt_path(file,cnf["env"])
        cw.print_info(f"INFO ::: Generating tgt_file_path:  {tgt_path}")

        with open(file, "r", encoding="utf-8") as tpl_file:
            try:
                tpl_str = tpl_file.read()
                tpl_obj = tpl_loader.from_string(tpl_str)
                # TODO Implement file includes
                rendered_file = render_file(tpl_obj, cnf)
                cw.print_info(rendered_file)
            except UnicodeDecodeError:
                print(f"The file {file} is a binary file or its type cannot be determined.")
                rendered_file = "" # will not be used anyways

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
    return render_files(files, cnf)


def render_file(tpl_obj: Template, cnf: any) -> str:
    args = os.environ.copy()
    cnf = eu.override_env(cnf)
    args.update(cnf["env"])

    try:
        rendered = tpl_obj.render(args)
    except UndefinedError as err:
        cw.print_warn(err.message)
        return "There was an error during template generation, check the template"
    except UnicodeDecodeError:
        return ""

    return rendered
