import os
from tpl_gen import generate_code, set_vars


def test_main():

    ORG_, ENV_, APP_, STEP_, cnf_src_dir, tpl_src_dir , tgt_output_dir, product_dir = set_vars()
    cnf_src_dir = product_dir
    tpl_src_dir = product_dir
    tgt_output_dir = product_dir

    generate_code()


    gen_file_p = os.path.join(product_dir, "src" , "nodejs" , "%site%")

    assert gen_file_p == '/opt/csi/tpl-gen/src/nodejs/re-01'
