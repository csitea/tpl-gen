import os, errno, yaml, json
from pathlib import Path
from jq import jq
from libs.utils.console_utils import *


class ConfigDataLoader:

    def __init__(self):
        pass

    def read_yaml_files(self, config_point, data_key_path=None):
        data = {}

        # if config_point is a file
        if os.path.isfile(config_point) and filename.endswith('.yaml'):
            with open(filepath, 'r') as file:
                yaml_data = yaml.safe_load(file)

                # Add the YAML data to the .env data structure path
                data.setdefault('conf', {}).update(yaml_data)
        elif os.path.isdir(config_point): # Iterate over all files in the directory
            for filename in os.listdir(config_point): # for each yaml file loads it up
                filepath = os.path.join(config_point, filename)

                # Check if the file is a YAML file
                if os.path.isfile(filepath) and filename.endswith('.yaml'):
                    # Read the YAML file
                    with open(filepath, 'r') as file:
                        yaml_data = yaml.safe_load(file)

                        # Add the YAML data to the .env data structure path
                        data.setdefault('conf', {}).update(yaml_data)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_point)

        if data_key_path:
            # Convert data to JSON
            json_data = json.dumps(data)
            # Execute jq query using jq.py library
            query_result = jq(data_key_path).transform(data)
            self.data = query_result
        else:
            self.data = data

        return self.data


    def read_config_file(file: Path) -> any:
        """
        Reads a configuration file and returns its contents as a dictionary.
        Supports both JSON and YAML files.

        The function first tries to load the file as JSON. If the file is not
        found, it prints a warning message and attempts to load it as a YAML file.
        If the file is not found again, it raises a FileNotFoundError and prints
        an error message. If the file is loaded successfully, a success message
        is printed.

        Args:
            file (Path): The path to the configuration file.

        Returns:
            dict: The contents of the configuration file.

        Raises:
            FileNotFoundError: If neither a JSON nor a YAML file is found at the
                provided path.
        """

        try:
            with open(file, "r", encoding="utf-8") as cnf_file:
                cnf = json.load(cnf_file)
        except FileNotFoundError:
            print_warn(f"No file {file} found, attempting to use yaml")
        except JSONDecodeError:
            print_warn(
                "A yaml file has been passed to read_config_file() it is\
                    encouraged to pass .json files if none exist the\
                        function will fallback to searching for an yaml variant by itself"
            )
        else:
            return cnf

        try:
            with open(file, "r", encoding="utf-8") as cnf_file:
                cnf = yaml.load(cnf_file, yaml.Loader)
        except FileNotFoundError as err:
            print_error(f'The file "{file}" has no yaml nor json variant')
            raise err

        print_success(f"Using {file}")

        return cnf