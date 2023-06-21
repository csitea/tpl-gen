import json, os,yaml
from pathlib import Path
from typing import Optional
from .console_utils import print_success, print_warn

from .string_utils import pkey_replace, string_contains
from .io_utils import replace_path




def convert_yaml_to_json_dir(config_end_point: Path, ignore_list: "Optional[list[str]]",env:any):
    """
    Iterate over subdirectories and files in the provided directory, skipping directories in the ignore list,
    and convert the YAML files to JSON format.

    Args:
        src_dir (Path): The source directory path.
        ignore_list (list[str], optional): The list of directories to ignore. Defaults to None.
    """
    if config_end_point.is_file():
        tgt_file_path = Path(str(config_end_point).replace(".yaml", ".json"))
        convert_file(config_end_point,tgt_file_path)

    for subdir, _dirnames, filenames in os.walk(config_end_point):
        if string_contains(ignore_list, subdir):
            continue

        convert_yaml_files(Path(subdir), filenames,env)


def convert_yaml_files(dir_path: Path, files: "list[str]",env:any):
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


def get_ignored_paths() -> "list[str]":
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

