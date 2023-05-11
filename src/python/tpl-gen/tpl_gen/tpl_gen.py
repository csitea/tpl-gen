#!/usr/bin/env python3

import time
import os
import shutil
import json
import yaml
from jinja2 import Environment, BaseLoader, exceptions
from pprintjson import pprintjson
from colorama import Fore, Style

class StepNotDefinedError(Exception):
    pass


def main():
    ORG_, ENV_, APP_, STEP_, cnf_src_dir, tpl_src_dir , tgt_output_dir  = set_vars()
    cnf = get_cnf(cnf_src_dir,ORG_,APP_,ENV_)
    print(cnf)
    exit(0)
    # # if the caller defines a step the step MUST have configuration
    # if STEP_ is not None and STEP_ != "" and cnf["steps"][STEP_] is None:
    #     raise StepNotDefinedError("STEP_ is not defined")

    do_generate(ORG_, ENV_ , APP_ , STEP_, cnf, tpl_src_dir, tgt_output_dir)

def print_warn(msg):
    print(f"{Fore.YELLOW}{msg}{Style.RESET_ALL}")

def print_error(msg):
    print(f"{Fore.RED}{msg}{Style.RESET_ALL}")

def print_success(msg):
    print(f"{Fore.GREEN}{msg}{Style.RESET_ALL}")


# generate the *.json files from the *.yaml files
def render_yaml():
    print ("START ::: render_yaml")
    ORG_, ENV_, APP_, STEP_, cnf_src_dir, tpl_src_dir , tgt_output_dir = set_vars()
    cnf_src_dir = os.getenv("CNF_SRC")
    tgt_dir = os.getenv("TGT")

    if cnf_src_dir == "" :
        print_error("FATAL ::: SRC directory not specified")
        exit(1)

    if tgt_dir == "" or tgt_dir is None:
        tgt_dir = cnf_src_dir

    # Get the HOME environment variable
    home_dir = os.environ['HOME']

    # Define the directories you want to iterate through
    dirs_to_iterate = [
        os.path.join(home_dir, '.aws'),
        os.path.join(home_dir, '.ssh'),
        cnf_src_dir
    ]

    for cdir in dirs_to_iterate:
        for subdir, _dirs, files in os.walk(cdir):
            for file in files:
                current_tpl_file = os.path.join(subdir, file)
                if current_tpl_file.endswith(".yaml"):
                    # print("working on: " + current_tpl_file)
                    # print("src_dir: " + cnf_src_dir)
                    # print("tgt_dir: " + tgt_dir)
                    # print("current_tpl_file; " + current_tpl_file)

                    yaml_filename = os.path.join(cnf_src_dir, current_tpl_file)
                    json_filename = os.path.join(tgt_dir, current_tpl_file.replace(".yaml", ".json"))
                    print ( f"rendered yaml into json_file: {json_filename}" )

                    with open(yaml_filename, encoding="utf-8") as file:
                        cnf = yaml.load(file, Loader=yaml.Loader)

                    with open(json_filename, 'w') as file:
                        json.dump(cnf, file, indent=4)
    print ("STOP  ::: render_yaml")


def set_vars():
    try:

        ORG_DIR_ = os.getenv("ORG_DIR")
        ORG_ = os.getenv("ORG")
        APP_ = os.getenv("APP")
        ENV_ = os.getenv("ENV")
        STEP_ = os.getenv("STEP") or None

        CNF_SRC_ = os.getenv("CNF_SRC")         # where we get the structured env configuration files
        TPL_SRC_ = os.getenv("TPL_SRC")         # where we get the tpl files

        tgt_output_dir = os.getenv("TGT")         # where we get tpl files

        product_dir = os.path.join(__file__, "..", "..", "..", "..", "..")
        product_dir = os.path.abspath(product_dir)

        base_dir = os.path.join(__file__, "..", "..", "..", "..", "..","..", "..")
        base_dir = os.path.abspath(base_dir)


        if tgt_output_dir == "" or tgt_output_dir is None:
            tgt_output_dir = os.path.join(f"{base_dir}",f"{ORG_DIR_}", f"{ORG_}-{APP_}-infra-conf")

        if CNF_SRC_ == "" or CNF_SRC_ is None:
            cnf_src_dir = os.path.join(f"{base_dir}",f"{ORG_DIR_}", f"{ORG_}-{APP_}-infra-conf", f"{APP_}")
        else:
            cnf_src_dir = CNF_SRC_

        if TPL_SRC_ == "" or TPL_SRC_ is None:
            tpl_src_dir = os.path.join(f"{base_dir}",f"{ORG_DIR_}", f"{ORG_}-{APP_}-infra-app")
        else:
            tpl_src_dir = TPL_SRC_



    except IndexError as error:
        raise Exception("ERROR in set_vars: ", str(error)) from error

    return ORG_, ENV_, APP_, STEP_, cnf_src_dir, tpl_src_dir , tgt_output_dir



def get_cnf(cnf_src_dir,ORG_,APP_,ENV_):

    try:
        json_cnf_file = os.path.join(cnf_src_dir, f"{APP_}", f"{ENV_}.env.json")
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

    except IndexError as error:
        raise Exception("ERROR in set_vars: ", str(error)) from error

    return cnf


def expand_path(ORG_, APP_, ENV_, STEP_, tpl_src_dir, tgt_output_dir,expandable_file_path):


    if "%step%" not in expandable_file_path:
        tgt_file_path = expandable_file_path.replace(tpl_src_dir,tgt_output_dir) \
            .replace("/src/tpl", "", 1) \
            .replace(".tpl", "") \
            .replace(r"%org%", ORG_) \
            .replace(r"%app%", APP_) \
            .replace(r"%env%", ENV_)
    else:
        if '%step%' in expandable_file_path and STEP_ is None:
            raise StepNotDefinedError("STEP_ is not defined")

        tgt_file_path = expandable_file_path.replace(tpl_src_dir,tgt_output_dir) \
            .replace("/src/tpl", "", 1) \
            .replace(".tpl", "") \
            .replace(r"%org%", ORG_) \
            .replace(r"%app%", APP_) \
            .replace(r"%env%", ENV_) \
            .replace(r"%step%", STEP_)

    return tgt_file_path


def do_generate(ORG_, ENV_, APP_, STEP_, cnf , tpl_src_dir, tgt_output_dir):
    print("START ::: generating templates")

    for pathname in [os.path.join(tpl_src_dir, "src", "tpl")]:  # directory this structure is enforced
        for subdir, _dirs, files in os.walk(pathname):

            current_dir_path = os.path.join(tpl_src_dir, subdir)
            # print(f"START ::: {current_dir_path}")
            if os.path.isdir(current_dir_path) and '%step%' in current_dir_path:
                tgt_dir_path = expand_path(ORG_,APP_,ENV_,STEP_,tpl_src_dir,tgt_output_dir,current_dir_path)
                print(f"tgt_dir_path: {tgt_dir_path}")
                # Remove the directory if it exists
                if os.path.exists(tgt_dir_path) and os.path.isdir(tgt_dir_path):
                    shutil.rmtree(tgt_dir_path)
                os.makedirs(tgt_dir_path)
            # print(f"STOP  ::: ${current_dir_path}")

            for file in files:
                current_tpl_file = os.path.join(subdir, file)
                # print("current_tpl_file: " + str(current_tpl_file))

                if current_tpl_file.endswith(".tpl"):
                    tgt_file_path = expand_path(ORG_,APP_,ENV_,STEP_,tpl_src_dir,tgt_output_dir,current_tpl_file)

                    try:
                        print (f"START ::: working on tpl file: {current_tpl_file}")

                        with open(current_tpl_file, "r", encoding="utf-8") as current_file:

                            str_tpl = current_file.read()
                            obj_tpl = Environment(loader=BaseLoader) \
                                .from_string(str_tpl)

                            # pass in globally available functions, objects & data
                            obj_tpl.globals["include_file"] = include_file
                            obj_tpl.globals["load_yaml"]    = load_yaml

                            args = os.environ.copy()
                            cnf = override_env(cnf)
                            args.update(cnf["env"])
                            rendered = obj_tpl.render(args)
                            tgt_file_path = current_tpl_file
                            tgt_file_path = expand_path(ORG_,APP_,ENV_,STEP_,tpl_src_dir,tgt_output_dir,current_tpl_file)

                            if not os.path.exists(os.path.dirname(tgt_file_path)):
                                os.makedirs(os.path.dirname(tgt_file_path))

                            print (f"START ::: generating tgt_file_path:  {tgt_file_path}")

                            if STEP_ is not None:
                                if STEP_ in tgt_file_path or '%step%' in tgt_file_path:
                                    with open(tgt_file_path, "w", encoding="utf-8") as tgt_file:
                                        tgt_file.write(rendered + os.linesep)
                                        msg = f"STOP  ::: File \"{tgt_file_path}\" rendered with success."
                            else:
                                with open(tgt_file_path, "w", encoding="utf-8") as tgt_file:
                                    tgt_file.write(rendered + os.linesep)
                                    msg = f"STOP  ::: File \"{tgt_file_path}\" rendered with success."


                    except exceptions.UndefinedError as error:
                        msg = "WARNING: Missing variable in json config in file: " + \
                            f"\"{current_tpl_file}\" - {error}"
                        print_warn(msg)

                    except Exception as error:
                        print_error(f"RENDERING EXCEPTION: \n{error}")
                        raise error

    print("STOP  ::: generating templates")


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

    return cnf


# Jinja2 custom filters
def include_file(filename):
    '''
    Include the raw contents of csicified filename or return None if it doesn't exist.
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
