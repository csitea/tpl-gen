#!/bin/bash
set -x
test -z "${APPUSR:-}" && APPUSR=appusr


# ./run -a do_check_install_py_modules
# cd "$PRODUCT_DIR/src/python/tpl-gen/" ;
# source .venv/bin/activate;
# poetry run python "tpl_gen/tpl_gen.py"
set -x

venv_path="/${BASE_DIR}/${ORG_DIR}/${PRODUCT}/src/python/tpl-gen/.venv"
test -d $venv_path && sudo rm -vr $venv_path
cp -vr /home/$APPUSR$venv_path $venv_path
perl -pi -e "s|/home/$APPUSR||g" $venv_path/bin/activate
# source /home/$APPUSR/opt/spe/tpl-gen/src/python/tpl-gen/.venv/bin/python

echo "source /${BASE_DIR}/${ORG_DIR}/${PRODUCT}/src/python/${PRODUCT}/.venv/bin/activate" >> /home/$APPUSR/.bashrc
# /home/appusr/.local/share/pypoetry/venv/bin/activate 
# -> /home/appusr/.local/share/pypoetry/venv/bin/activate

cd /${BASE_DIR}/${ORG_DIR}/${PRODUCT}/

trap : TERM INT; sleep infinity & wait
