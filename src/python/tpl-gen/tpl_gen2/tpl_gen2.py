import os
from pathlib import Path
from config import env_params_tpl as env
from utils import tpl_utils as tpl
from utils import console_utils as cw


def main():
    cw.print_info_heading("STARTING TPL GEN")
    mode = get_tpl_render_mode()

    json_cnf_file = Path(env.CNF_SRC, env.APP, f"{env.ENV}.env.json")
    cnf = tpl.read_json_file(json_cnf_file)

    for subdir, _dirs, files in os.walk(Path(env.TPL_SRC, "src", "tpl")):
        files = sorted(files)
        files = [Path(subdir, file) for file in files]

        files = mode(files, cnf)

        write_output_files(files)


def get_tpl_render_mode():
    """This is for backwards compatibility, if a step is specified tpl
    will enter into step mode which will only render files related to
    the exported step otherwise it will exhibit normal behavior and
    render all files in the directory based on the configuration.
    """
    if os.environ.get("STEP"):
        cw.print_info_heading("RENDERING FILES IN STEP MODE")
        return tpl.render_files_step

    cw.print_info_heading("RENDERING FILES IN NORMAL MODE")
    return tpl.render_files


def write_output_files(files: list[tuple[Path, str]]):
    for file_path, content in files:
        with open(file_path, "w", encoding="utf-8") as output_file:
            output_file.write(content + os.linesep)

        cw.print_success(f"Wrote file {file_path}")
