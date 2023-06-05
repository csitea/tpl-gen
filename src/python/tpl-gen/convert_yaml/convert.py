"""
This module provides functionality to convert YAML files to JSON format.
It looks for YAML files in specified directories, converts the contents to JSON,
and saves the results to a new file.

Functions:
    main: The primary function of the script, which manages the conversion process.
"""
from pathlib import Path
from utils.console_utils import print_info, print_info_heading
from config import env_params_tpl as env
import utils

ignore_list = utils.get_ignored_paths()


def main():
    print_info_heading("CONVERT YAML TO JSON")

    dirs_to_iterate = [
        Path(env.HOME, ".aws"),
        Path(env.HOME, ".ssh"),
        Path(env.CNF_SRC),
    ]

    for cur_path in dirs_to_iterate:
        utils.convert_dir(cur_path, ignore_list)

    print_info("STOP ::: render_yaml")
