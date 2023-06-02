import os
from .console_utils import print_info


def interpolate_path(cnf_vars, tpl_src_dir, tgt_output_dir, expandable_file_path):
    for key, value in cnf_vars.items():
        print_info(f"searching key: {key}: replacing: {value}")
        pkey = "%" + key + "%"  # percentage variable name aka percentage key

        if "%step%" not in expandable_file_path:
            tgt_file_path = (
                expandable_file_path.replace(tpl_src_dir, tgt_output_dir)
                .replace("/src/tpl", "", 1)
                .replace(".tpl", "")
                .replace(pkey, value)
            )
        else:
            if "%step%" in expandable_file_path and STEP_ is None:
                # TODO
                raise StepNotDefinedInShellError(f"STEP_ is not defined")

            tgt_file_path = (
                expandable_file_path.replace(tpl_src_dir, tgt_output_dir)
                .replace("/src/tpl", "", 1)
                .replace(".tpl", "")
                .replace(pkey, value)
            )

    return tgt_file_path


def expand_path(
    ORG_, APP_, ENV_, STEP_, tpl_src_dir, tgt_output_dir, expandable_file_path
):
    if "%step%" not in expandable_file_path:
        tgt_file_path = (
            expandable_file_path.replace(tpl_src_dir, tgt_output_dir)
            .replace("/src/tpl", "", 1)
            .replace(".tpl", "")
            .replace(r"%org%", ORG_)
            .replace(r"%app%", APP_)
            .replace(r"%env%", ENV_)
        )
    else:
        if "%step%" in expandable_file_path and STEP_ is None:
            raise StepNotDefinedInShellError("STEP_ is not defined")

        tgt_file_path = (
            expandable_file_path.replace(tpl_src_dir, tgt_output_dir)
            .replace("/src/tpl", "", 1)
            .replace(".tpl", "")
            .replace(r"%org%", ORG_)
            .replace(r"%app%", APP_)
            .replace(r"%env%", ENV_)
            .replace(r"%step%", STEP_)
        )

    return tgt_file_path


def load_yaml(filename):
    """
    Return contents of yaml file as variables
    """
    filepath = os.path.join(os.getcwd(), filename)
    print_info(f"INFO: filename is {filename}")
    print_info(f"INFO: filepath is {filepath}")
    with open(filepath, encoding="utf-8") as file:
        yaml_file = yaml.load(file, Loader=yaml.Loader)

    return yaml_file
