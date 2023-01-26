#!/usr/bin/env python3

import time
import os
import json
import yaml
from jinja2 import Environment, BaseLoader, exceptions
from pprintjson import pprintjson
from colorama import Fore, Style


def main():
    ORG_, ENV_, APP_, env_config_dir, tgt_proj_dir  = set_vars()
    cnf = get_cnf(env_config_dir,ENV_)
    do_generate(ORG_, ENV_ , APP_ , cnf, tgt_proj_dir)


def print_warn(msg):
    print(f"{Fore.YELLOW}{msg}{Style.RESET_ALL}")

def print_error(msg):
    print(f"{Fore.RED}{msg}{Style.RESET_ALL}")

def print_success(msg):
    print(f"{Fore.GREEN}{msg}{Style.RESET_ALL}")

def render_yaml():
    ORG_, ENV_, APP_, env_config_dir, tgt_proj_dir = set_vars()
    src = os.getenv("SRC")
    tgt = os.getenv("TGT")

    if src == "" :
        print_error("FATAL ::: SRC directory not specified")
        exit(1)
    
    if tgt == "" or tgt is None: 
        tgt = src


    for subdir, _dirs, files in os.walk(src):
        for file in files:
            current_file_path = os.path.join(subdir, file)
            if current_file_path.endswith(".yaml"):
                print("working on: " + current_file_path)
                print(src, tgt, current_file_path)

                yaml_filename = os.path.join(src, current_file_path)
                json_filename = os.path.join(tgt, current_file_path.replace(".yaml", ".json"))

                with open(yaml_filename, encoding="utf-8") as file:
                    cnf = yaml.load(file, Loader=yaml.Loader)
                
                with open(json_filename, 'w') as file:
                    json.dump(cnf, file, indent=4)


def set_vars():
    try:
        ENV_ = os.getenv("ENV")
        ORG_ = os.getenv("ORG")
        ORG_DIR_ = os.getenv("ORG_DIR")
        APP_ = os.getenv("APP")
        TGT_ = os.getenv("TGT")         # where we get tpl files
        SRC_ = os.getenv("SRC")         # where we get the config file

        product_dir = os.path.join(__file__, "..", "..", "..", "..", "..")
        product_dir = os.path.abspath(product_dir)
        
        if TGT_ == "" or TGT_ is None: 
            tgt_proj_dir = os.path.join(f"/var/{ORG_DIR_}", "infra")
        else:
            tgt_proj_dir = os.path.join(f"/var/{ORG_DIR_}", f"{TGT_}")

        if SRC_ == "" or SRC_ is None: 
            env_config_dir = os.path.join(f"/var/{ORG_DIR_}", "infra", "cnf", "env", f"{ORG_}", f"{APP_}")
        else:
            env_config_dir = os.path.join(f"/var/{ORG_DIR_}", f"{SRC_}", "cnf", "env", f"{ORG_}", f"{APP_}")


    except IndexError as error:
        raise Exception("ERROR in set_vars: ", str(error)) from error

    return ORG_, ENV_, APP_, env_config_dir, tgt_proj_dir


def get_cnf(env_config_dir,ENV_):
    try:

        json_cnf_file = os.path.join(env_config_dir, f"{ENV_}.env.json")
        yaml_cnf_file = json_cnf_file.replace('json', 'yaml')

        # If YAML exists, dump it into JSON and use it.
        if os.path.exists(yaml_cnf_file):
            print(f"tpl_gen.py ::: using config json file: {yaml_cnf_file}")
            with open(yaml_cnf_file, encoding="utf-8") as file:
                cnf = yaml.load(file, Loader=yaml.Loader)

            # backwards compatible and also useful for jq
            with open(json_cnf_file, 'w') as file:
                json.dump(cnf, file, indent=4)
        else:  # otherwise use json
            print(f"tpl_gen.py ::: using config json file: {json_cnf_file}")
            with open(json_cnf_file, encoding="utf-8") as file:
                cnf = json.load(file)
        
        #pprintjson(cnf)

    except IndexError as error:
        raise Exception("ERROR in set_vars: ", str(error)) from error

    return cnf



def do_generate(ORG_, ENV_, APP_, cnf, tgt_proj_dir):

    for pathname in [os.path.join(tgt_proj_dir, "src", "tpl")]:  # directory this structure is enforced
        for subdir, _dirs, files in os.walk(pathname):
            for file in files:
                current_file_path = os.path.join(subdir, file)
                if current_file_path.endswith(".tpl"):
                    try:
                        print (f"START ::: working on tpl file: {current_file_path}")
                        with open(current_file_path, "r", encoding="utf-8") as current_file:
                            print(current_file_path)
                            str_tpl = current_file.read()
                            obj_tpl = Environment(loader=BaseLoader) \
                                .from_string(str_tpl)

                            # custom filters
                            obj_tpl.globals["include_file"] = include_file
                            obj_tpl.globals["load_yaml"]    = load_yaml

                            args = os.environ.copy()
                            override_env(cnf)
                            args.update(cnf["env"])
                            rendered = obj_tpl.render(args)

                            tgt_file_path = current_file_path.replace("/src/tpl", "", 1) \
                                .replace(".tpl", "") \
                                .replace(r"%env%", ENV_) \
                                .replace(r"%org%", ORG_) \
                                .replace(r"%app%", APP_)

                            if not os.path.exists(os.path.dirname(tgt_file_path)):
                                os.makedirs(os.path.dirname(tgt_file_path))
                            
                            print (f"START ::: generating tgt_file_path:  {tgt_file_path}")

                            with open(tgt_file_path, "w", encoding="utf-8") as tgt_file:
                                tgt_file.write(rendered + os.linesep)
                                msg = f"STOP  ::: File \"{tgt_file_path}\" rendered with success."
                            print_success(msg)


                    except exceptions.UndefinedError as error:
                        msg = "WARNING: Missing variable in json config in file: " + \
                            f"\"{current_file_path}\" - {error}"
                        print_warn(msg)

                    except Exception as error:
                        print_error(f"RENDERING EXCEPTION: \n{error}")
                        raise error

    print("STOP generating templates")

# allow environment variables to override configuration
# Warning: this is an important feature, users now need
# to be aware of their environment.
def override_env(cnf):
    # it only makes sense to talk about overriding variables on step level
    # since nested variables within steps are flattened to environment level
    # variables, i.e. :
    #     cnf["steps"]["001-step-name"]["AWS_PROFILE"]
    #     becomes AWS_PROFILE, thus no need to override
    #     cnf["aws"]["AWS_PROFILE"], since it won't be considered

    for step in cnf["env"]["steps"]:
        for step_var in cnf["env"]["steps"][step]:
            # checks if it is defined as environment variable
            # if it's not, preserves the value of itself.
            cnf["env"]["steps"][step][step_var] = os.getenv(step_var, cnf["env"]["steps"][step][step_var])

# Jinja2 custom filters
def include_file(filename):
    '''
    Include the raw contents of specified filename or return None if it doesn't exist.
    '''
    filepath = os.path.join(os.getcwd(), filename)
    content  = ""
    if os.path.exists(filepath):
        fp = open(filename, "r")
        content = fp.read()
        fp.close()
    return content

def load_yaml(filename):
    '''
    Return contents of yaml file as variables
    '''
    filepath  = os.path.join(os.getcwd(), filename)
    with open(filepath, encoding="utf-8") as file:
        yaml_file = yaml.load(file, Loader=yaml.Loader)
    
    return yaml_file


if __name__ == "__main__":
    main()
