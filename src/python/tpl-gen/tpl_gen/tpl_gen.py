import os, mimetypes,shutil
from jq import jq
from pathlib import Path
from jinja2 import Environment, BaseLoader
from config import run_env
from config import config_data_loader
from config import config_data_loader
from data import generic_data_service
from libs.utils.console_utils import *
from libs.utils.io_utils import *
from data.data_provider_type import DataProviderType
from json import JSONDecodeError
from pathlib import Path
from libs.utils.env_utils import *
from config import run_env
from libs.utils.console_utils import *
from libs.utils.convert_utils import  create_tgt_path
from libs.utils.tpl_utils import render_file



def main():

    print_info_heading("START ::: infra conf generator")
    env = run_env.RunEnv()

    config_end_point = env.CNF_SRC

    data_key_path = env.DATA_KEY_PATH or '.'

    obj_config_data_loader = config_data_loader.ConfigDataLoader()
    cnf = obj_config_data_loader.read_yaml_files(config_end_point, data_key_path=data_key_path)
    # optionally enrich the cnf with data from data services
    # obj_generic_data_service = generic_data_service.GenericDataService(env,cnf,DataProviderType.aws)
    # data = sub_cnf
    tpl_paths = list_files_and_dirs(env.TPL_SRC)
    tpl_loader = Environment(loader=BaseLoader)

    rendered_files_and_contents: list[tuple[Path, str]] = []
    for tpl_path in tpl_paths:
        tgt_path = create_tgt_path(env,cnf,data_key_path,tpl_path )
        rendered_file_content = ''
        print_info(f"INFO ::: Generating tgt_file_path:  {tgt_path}")

        if os.path.isdir(tpl_path):
            if not os.path.exists(tgt_path):
                os.mkdir(tgt_path)
        elif os.path.isfile(tpl_path):
            with open(tpl_path, "r", encoding="utf-8") as tgt_file_fh:
                try:
                    tpl_str = tgt_file_fh.read()
                    tpl_obj = tpl_loader.from_string(tpl_str)
                    rendered_file_content = render_file(tpl_obj, cnf,data_key_path)
                    # print_code(rendered_file_content)
                except UnicodeDecodeError:
                    print(
                        f"The file {tpl_path} is a binary file or its type cannot be determined."
                    )
                    rendered_file_content = ""  # will not be used anyways
        else:
             print(f"The file {tpl_path} is a binary file or its type cannot be determined.")
        # print(rendered_files_and_contents)
        # print("eof rendered_files_and_contents")


        rendered_files_and_contents.append((tgt_path, rendered_file_content))

    write_output_files(tpl_paths,rendered_files_and_contents)


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


if __name__ == "__main__":
    main()



    # # Read the YAML file
    # with open(env.PRODUCT_DIR + '/cnf/yaml/aws/aws-services.yaml', 'r') as f:
    #     data = yaml.safe_load(f)