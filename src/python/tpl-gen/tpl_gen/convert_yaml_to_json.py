import os, mimetypes,shutil
from jq import jq
from pathlib import Path
from jinja2 import Environment, BaseLoader, StrictUndefined
from config import run_env
from config import config_data_loader
from config import config_data_loader
from libs.utils.console_utils import *
from libs.utils.io_utils import *
from json import JSONDecodeError
from pathlib import Path
from libs.utils.env_utils import *
from libs.utils.tpl_utils import render_file
from libs.utils.string_utils import string_contains
from libs.utils.convert_utils import *



def main():

    env = run_env.RunEnv()

    print_info_heading(" ::: CONVERT YAML TO JSON ::: ")

    paths_to_iterate = [
        # Path(env.HOME, ".aws"),
        # Path(env.HOME, ".ssh"),
        Path(env.CNF_SRC),
    ]
    ignore_list = get_ignored_paths()

    for cur_path in paths_to_iterate:
        convert_yaml_to_json_dir(cur_path, ignore_list,env)



def is_text_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith("text/")


def write_output_files(
    tpl_paths: "list[str]", rendered_files_and_contents: "list[tuple[Path, str]]"
):

    counter = 0
    for file_path, content in rendered_files_and_contents:
        # print(content)
        # print("eof content")

        # print(file_path)
        # print("eof file_path")
        directory = file_path.parent  # Get the directory path
        # create the directory if it doesn't exist
        directory.mkdir(parents=True, exist_ok=True)
        # resolve the tpl_file for the copy file if needed
        tpl_file = tpl_paths[counter]

        if os.path.isdir(file_path):
            continue

        try:
            with open(file_path, "w", encoding="utf-8") as output_file:
                output_file.write(content + os.linesep)
        except UnicodeDecodeError:
            print(
                f"The file {file_path} is a binary file or its type cannot be determined."
            )
            shutil.copy(tpl_file, file_path)
        counter += 1


# (env,sub_cnf, tpl_path,data_key_path )
# create_tgt_path(env,cnf,data_key_path,tpl_path )
def create_tgt_path(env: run_env,
                    cnf: dict,
                    data_key_path:str,
                    tpl_file: Path,
                    opt_dict=None) -> Path:

    ignore_list = get_ignored_paths()
    if string_contains(ignore_list, tpl_file):
        return ""

    if opt_dict is None:
        opt_dict = {}

    str_path = str(tpl_file)
    env_dict = get_env_as_dict_lower()


    # Convert data to JSON
    # todo: remove ?!
    # json_data_str = json.dumps(cnf)
    #json_obj = json.loads(json_data_str)
    #Execute jq query using jq.py library
    print (f"data_key_path: {data_key_path}")
    
    opt_dict = jq(data_key_path).transform(cnf)

    opt_dict.update(env_dict)
    converted_path = pkey_replace(str_path, opt_dict)
    converted_path = replace_path(converted_path, env.TGT)
    converted_path = converted_path.replace(env.SRC_PRF, env.TGT_PRF, 1) # optional from 4.0
    converted_path = Path(converted_path.replace(env.SRC_EXT, env.TGT_EXT)) # optional from 4.0
    return converted_path


if __name__ == "__main__":
    main()



    # # Read the YAML file
    # with open(env.PROJ_PATH + '/cnf/yaml/aws/aws-services.yaml', 'r') as f:
    #     data = yaml.safe_load(f)
