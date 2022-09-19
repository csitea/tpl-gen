#!/usr/bin/env python3

import time
import os
import json
import yaml
from jinja2 import Environment, BaseLoader, exceptions
from pprintjson import pprintjson
from colorama import Fore, Style


def main():
    ORG_, ENV_, APP_, cnf, src_proj_dir, tgt_proj_dir = set_vars()
    print(ORG_, APP_, ENV_, src_proj_dir, tgt_proj_dir)
    # 2209060034 ::: support for early credentials
    do_generate_early_credentials(ORG_)
    do_generate(ORG_, ENV_ , APP_ , cnf, src_proj_dir, tgt_proj_dir)


def print_warn(msg):
    print(f"{Fore.YELLOW}{msg}{Style.RESET_ALL}")


def print_error(msg):
    print(f"{Fore.RED}{msg}{Style.RESET_ALL}")


def print_success(msg):
    print(f"{Fore.GREEN}{msg}{Style.RESET_ALL}")

def do_generate_early_credentials(org):
    
    # This path is enforced, not configurable. It is mounted when docker starts.
    early_credentials_yaml = f"/home/appusr/.aws/.{org}/early-credentials.yaml"
    early_credentials_json = early_credentials_yaml.replace("yaml", "json")  # to allow the use of jq tool later when needed
    print_warn(f"Early credentials path: {early_credentials_yaml}")

    if os.path.exists(early_credentials_yaml):
        print_success(f"Early credentials file does exist: {early_credentials_yaml}")

        # render variables from yaml file
        with open(early_credentials_yaml, encoding="utf-8") as file:
            cnf = yaml.load(file, Loader=yaml.Loader)

        # dump into json to be bash/jq friendly
        with open(early_credentials_json, 'w', encoding="utf-8") as file:
           json.dump(cnf, file, indent=4)
    else:
        print_error(f"Early credentials file does not exist: {early_credentials_yaml}")
        exit(1)

def set_vars():
    try:
        ENV_ = os.getenv("ENV")
        ORG_ = os.getenv("ORG")
        APP_ = os.getenv("APP")

        product_dir = os.path.join(__file__, "..", "..", "..", "..", "..")
        product_dir = os.path.abspath(product_dir)
        
        # the tpl-gen and the target project MUST be in the same directory !!!
        SRC_ = os.getenv("SRC")
        TGT_ = os.getenv("TGT")
        
        if SRC_ == "": SRC_ = "infra"
        
        src_proj_dir = os.path.join("/var", SRC_)

        json_cnf_file = f"{src_proj_dir}/cnf/env/{ORG_}/{APP_}/{ENV_}.env.json"
        yaml_cnf_file = json_cnf_file.replace('json', 'yaml')

        print(f"tpl_gen.py ::: using config json file: {json_cnf_file}")
        time.sleep(1)

        # If YAML exists, dump it into JSON and use it.
        if os.path.exists(yaml_cnf_file):
            with open(yaml_cnf_file, encoding="utf-8") as file:
                cnf = yaml.load(file, Loader=yaml.Loader)

            with open(json_cnf_file, 'w') as file:
                json.dump(cnf, file, indent=4)
        else:  # otherwise use json
            with open(json_cnf_file, encoding="utf-8") as file:
                cnf = json.load(file)
        
        #pprintjson(cnf)

    except IndexError as error:
        raise Exception("ERROR in set_vars: ", str(error)) from error

    return ORG_, ENV_, APP_, cnf, src_proj_dir, TGT_


def do_generate(ORG_, ENV_, APP_, cnf, src_proj_dir, tgt_proj_dir):
    pathnames = [os.path.join(src_proj_dir, "src", "tpl", "cnf")]

    for pathname in pathnames:
        for subdir, _dirs, files in os.walk(pathname):
            for file in files:
                current_file_path = os.path.join(subdir, file)
                if current_file_path.endswith(".tpl"):
                    try:
                        print (f"START ::: working on tpl file: {current_file_path}")
                        with open(current_file_path, "r", encoding="utf-8") as current_file:
                            str_tpl = current_file.read()
                            obj_tpl = Environment(loader=BaseLoader) \
                                .from_string(str_tpl)
                            args = os.environ.copy()
                            args.update(cnf["env"])
                            rendered = obj_tpl.render(args)

                            current_file = current_file_path.split('/')[-1].replace(".tpl", "")  # name of the file
                            if tgt_proj_dir == "":
                                tgt_file_path = current_file_path.replace(".tpl", "")\
                                    .replace(r"%org%", ORG_) \
                                    .replace(r"%app%", APP_) \
                                    .replace(r"%env%", ENV_)
                            else:
                                tgt_file_path = os.path.join(os.path.join("/var", tgt_proj_dir), current_file)

                            if not os.path.exists(os.path.dirname(tgt_file_path)):
                                os.makedirs(os.path.dirname(tgt_file_path))

                            with open(tgt_file_path, "w", encoding="utf-8") as tgt_file:
                                tgt_file.write(rendered + os.linesep)
                                msg = f"File \"{tgt_file_path}\" rendered with success."
                                print_success(msg)

                    except exceptions.UndefinedError as error:
                        msg = "WARNING: Missing variable in json config in file: " + \
                            f"\"{current_file_path}\" - {error}"
                        print_warn(msg)

                    except Exception as error:
                        print_error(f"RENDERING EXCEPTION: \n{error}")
                        raise error

    print("STOP generating templates")


if __name__ == "__main__":
    main()
