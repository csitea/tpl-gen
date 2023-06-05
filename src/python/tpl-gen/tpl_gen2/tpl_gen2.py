import os
from pathlib import Path
from config import env_params_tpl as env
from utils import tpl_utils as tpl
from utils import convert_utils as convert


def main():
    json_cnf_file = Path(env.CNF_SRC, env.APP, f"{env.ENV}.env.json")
    cnf = tpl.read_json_file(json_cnf_file)

    for subdir, _dirs, files in os.walk(Path(env.TPL_SRC, "src", "tpl")):
        print(subdir)
        print(files)
