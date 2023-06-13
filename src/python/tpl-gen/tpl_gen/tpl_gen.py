import os
import time
from pathlib import Path
from .config.env_params_tpl import Environment
from utils import tpl_utils as tpl
from utils import console_utils as cw
import mimetypes
import shutil


env = Environment()


def main():
    """
    Entry point function for infra conf generator.

    This function executes the infra conf generation process by performing the following steps:
    1. Prints an information heading to indicate the start of the process.
    2. Retrieves the template render mode action and configuration.
    3. Walks through the source template directory, collecting template file paths.
    4. Sorts the template files.
    5. Executes the mode action on the template files and configuration to generate file contents.
    6. Writes the generated file contents to the output files.

    Returns:
        None
    """
    cw.print_info_heading("START ::: infra conf generator")
    mode_action, cnf = get_tpl_render_mode_action()

    for subdir, _dirs, files in os.walk(Path(env.TPL_SRC, "src", "tpl")):
        tpl_files = [Path(subdir, file) for file in files]
        tpl_files = sorted(tpl_files)
        # tpl_files = array("str",tpl_files)
        files_and_contents = mode_action(tpl_files, cnf)
        write_output_files(tpl_files, files_and_contents)
    cw.print_info_heading("STOP  ::: infra conf generator")


def get_tpl_render_mode_action():
    """This is for backwards compatibility, if a step is specified tpl
    will enter into step mode which will only render files related to
    the exported step otherwise it will exhibit normal behavior and
    render all files in the directory based on the configuration.
    """
    if os.environ.get("STEP"):
        cw.print_info_heading("START ::: rendering files for STEP")
        json_cnf_file = Path(env.CNF_SRC, env.APP, f"{env.ENV}.env.json")
        cnf = tpl.read_config_file(json_cnf_file)
        cw.print_code(cnf)
        return tpl.render_files_step, cnf
    else:
        cw.print_info_heading("START ::: rendering for full configuration")
        return tpl.render_files, cnf


def is_text_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith("text/")


def write_output_files(
    tpl_files: list[str], files_and_contents: list[tuple[Path, str]]
):
    """
    Write or update output files based on the provided content.

    Args:
        tpl_files (list[str]): List of template file paths.
        files_and_contents (list[tuple[Path, str]]): List of tuples containing file paths and their corresponding content.

    Returns:
        None
    """
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
