import os, errno, yaml, json
from pathlib import Path
from jq import jq



class ConfigDataLoader:

    def __init__(self):
        pass

    def read_yaml_files(self, config_point, data_key_path=None):
        data = {}

        # if config_point is a file
        if os.path.isfile(config_point):
            if config_point.endswith('.yaml') or config_point.endswith('.yml'):
                load_method = yaml.safe_load
                # todo:
                # Add the YAML data to the .env data structure path
                #data.setdefault('env', {}).update(yaml_data)
            elif config_point.endswith('.json'):
                load_method = json.load
            with open(config_point, 'r') as file_handle:
                data = load_method(file_handle)
        elif os.path.isdir(config_point): # Iterate over all files in the directory
            for filename in os.listdir(config_point): # for each yaml file loads it up
                file_path = os.path.join(config_point, filename)
                print(file_path)
                print("eof file_path")

                # Check if the file is a YAML file
                if os.path.isfile(file_path) and filename.endswith('.yaml'):
                    # Read the YAML file
                    with open(file_path, 'r') as file_handle:
                        data = yaml.safe_load(file_handle)

        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_point)

        # Add the YAML data to the .env data structure path
        # add .env unless does not exist as the root element of the tree
        # data.setdefault('.env', {}).update(yaml_data)


        # if data_key_path:
        #     # Convert data to JSON
        #     #json_data_str = json.dumps(data)
        #     # json_obj = json.loads(json_data_str)
        #     # Execute jq query using jq.py library
        #     # query_result = jq(data_key_path).transform(data)
        #     self.data = query_result
        # else:
        #     self.data = data

        return data


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
