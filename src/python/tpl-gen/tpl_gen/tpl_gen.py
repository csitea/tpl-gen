import os
from pathlib import Path
from config import run_env
from config import config_data_loader
from config import config_data_loader
from data import generic_data_service
from libs.utils.console_utils import *
from libs.utils.io_utils import *
from libs.utils.tpl_utils import render_files
from data.data_provider_type import DataProviderType
import mimetypes
import shutil


def main():

    print_info_heading("START ::: infra conf generator")
    env = run_env.RunEnv()

    config_dir = env.CNF_SRC
    data_key_path = env.DATA_KEY_PATH or '.'
    obj_config_data_loader = config_data_loader.ConfigDataLoader()
    cnf = obj_config_data_loader.read_yaml_files(config_dir, data_key_path=data_key_path)
    # obj_generic_data_service = generic_data_service.GenericDataService(env,cnf,DataProviderType.aws)
    data = cnf

    tpl_files = list_files_and_dirs(env.TPL_SRC)
    # Here we could remove the src/tpl logic. Whenever we call this from cli
    # we could specify what is the TPL_SRC. We just walk down it.
    for subdir, _dirs, files in os.walk(Path(env.TPL_SRC)):
        tpl_files = [Path(subdir, file) for file in files]
        tpl_files = sorted(tpl_files)
        #print(cnf)
        files_and_contents = render_files(env, data, tpl_files, '.conf.aws-services-data')
        print(files_and_contents)
        # write_output_files(tpl_files, files_and_contents)



def is_text_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith("text/")


def write_output_files(
    tpl_files: "list[str]", files_and_contents: "list[tuple[Path, str]]"
):

    counter = 0
    for file_path, content in files_and_contents:
        directory = file_path.parent  # Get the directory path
        # create the directory if it doesn't exist
        directory.mkdir(parents=True, exist_ok=True)
        # resolve the tpl_file for the copy file if needed
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


if __name__ == "__main__":
    main()



    # # Read the YAML file
    # with open(env.PRODUCT_DIR + '/cnf/yaml/aws/aws-services.yaml', 'r') as f:
    #     data = yaml.safe_load(f)