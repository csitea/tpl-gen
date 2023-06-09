import os
import time
from pathlib import Path
from config import env_params_tpl as env
from utils import tpl_utils as tpl
from utils import console_utils as cw
import mimetypes
import shutil
import array

env.init_env()


def main():
    cw.print_info_heading("STARTING TPL GEN")
    mode_action, cnf = get_tpl_render_mode_action()

    for subdir, _dirs, files in os.walk(Path(env.TPL_SRC, "src", "tpl")):
        tpl_files = [Path(subdir, file) for file in files]
        tpl_files = sorted(tpl_files)
        # tpl_files = array("str",tpl_files)
        files_and_contents = mode_action(tpl_files, cnf)
        write_output_files(tpl_files, files_and_contents)


def get_tpl_render_mode_action():
    """This is for backwards compatibility, if a step is specified tpl
    will enter into step mode which will only render files related to
    the exported step otherwise it will exhibit normal behavior and
    render all files in the directory based on the configuration.
    """
    if os.environ.get("STEP"):
        cw.print_info_heading("RENDERING FILES IN STEP MODE")
        json_cnf_file = Path(env.CNF_SRC, env.APP, f"{env.ENV}.env.json")
        cnf = tpl.read_config_file(json_cnf_file)
        cw.print_code(cnf)
        return tpl.render_files_step, cnf

    if os.environ.get("MULTI"):
        cw.print_info_heading("RENDERING FILES IN MULTI MODE")
        json_cnf_file = Path(env.CNF_SRC)  # no naming convention just the conf file
        cnf = tpl.read_config_file(json_cnf_file)
        cw.print_code(cnf)
        return tpl.render_files, cnf

    cw.print_info_heading("RENDERING FILES IN NORMAL MODE")
    return tpl.render_files, cnf


def is_text_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith("text/")


def write_output_files(
    tpl_files: list[str], files_and_contents: list[tuple[Path, str]]
):
    counter = 0
    for file_path, content in files_and_contents:
        directory = file_path.parent  # Get the directory path
        directory.mkdir(
            parents=True, exist_ok=True
        )  # Create the directory if it doesn't exist

        tpl_file = tpl_files[counter]

        try:
            with open(file_path, "w", encoding="utf-8") as output_file:
                output_file.write(content + os.linesep)
        except UnicodeDecodeError:
            print(
                f"The file {file_path} is a binary file or its type cannot be determined."
            )
            shutil.copy(tpl_file, file_path)
        counter += 1
