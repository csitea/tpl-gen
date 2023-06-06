"""
This module provides utilities for converting YAML files to JSON format in a given directory.
It uses a specified ignore list to skip certain files during conversion.

Functions:
    convert_dir(src_dir: Path, ignore_list: Optional[list[str]]):
        Converts the YAML files in a given directory and its subdirectories to JSON format.

    convert_yaml_files(dir_path: Path, files: list[str]):
        Converts the YAML files in a list to JSON format.

    convert_file(src_file_path: Path, tgt_file_path: Path):
        Converts a single YAML file to JSON format.

    get_ignored_paths() -> list[str]:
        Gets a list of paths to ignore during the conversion process from a '.tplignore' file.

Modules:
    json, os, pathlib.Path, typing.Optional, utils.console_utils, yaml, config.env_params_tpl, utils
"""

import json
import os
from pathlib import Path
from typing import Optional
import yaml
from utils.console_utils import print_success, print_warn
from config import env_params_tpl as env
import utils
from utils.string_utils import pkey_replace
from utils.env_utils import get_env_as_dict_lower


def convert_dir(src_dir: Path, ignore_list: Optional[list[str]]):
    """
    Iterate over subdirectories and files in the provided directory, skipping directories in the ignore list,
    and convert the YAML files to JSON format.

    Args:
        src_dir (Path): The source directory path.
        ignore_list (list[str], optional): The list of directories to ignore. Defaults to None.
    """
    for subdir, _dirnames, filenames in os.walk(src_dir):
        if utils.string_contains(ignore_list, subdir):
            continue

        convert_yaml_files(Path(subdir), filenames)


def convert_yaml_files(dir_path: Path, files: list[str]):
    """
    Convert all YAML files in a directory to JSON format.

    Args:
        dir_path (Path): The directory path.
        files (list[str]): The list of file names in the directory.
    """
    for file in files:
        if not file.endswith(".yaml"):
            continue

        src_file_path = dir_path.joinpath(file)
        tgt_file_path = Path(env.TGT, dir_path, file.replace(".yaml", ".json"))
        convert_file(src_file_path, tgt_file_path)


def convert_file(src_file_path: Path, tgt_file_path: Path):
    """
    Convert the content of a single YAML file to JSON.

    Args:
        src_file_path (Path): The path of the source YAML file.
        tgt_file_path (Path): The path of the target JSON file.
    """
    with open(src_file_path, "r", encoding="utf-8") as yaml_file:
        data = yaml.load(yaml_file, Loader=yaml.SafeLoader)

    with open(tgt_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print_success(f"rendered yaml into json_file: {tgt_file_path}")


def get_ignored_paths() -> list[str]:
    """
    Retrieve the list of paths to ignore during the conversion process from a '.tplignore' file.
    If the file does not exist, a warning is printed and an empty list is returned.

    Returns:
        list[str]: The list of ignored paths.
    """
    try:
        with open(".tplignore", "r", encoding="UTF8") as ignore_file:
            ignore_list = [line.strip() for line in ignore_file.readlines()]
            print_success("INFO ::: using .tplignore")
            return ignore_list
    except FileNotFoundError:
        print_warn("WARNING ::: .tplignore file not found")
        return []


def create_tgt_path(file: Path):
    str_path = str(file)
    env_dict = get_env_as_dict_lower()
    converted_path = pkey_replace(str_path, env_dict)
    converted_path = converted_path.replace("src/tpl/", "", 1)
    converted_path = Path(converted_path).with_suffix("")
    return converted_path
