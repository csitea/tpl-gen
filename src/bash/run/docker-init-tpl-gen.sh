#!/bin/bash

set -x

test -z ${PRODUCT:-} && PRODUCT='tpl-gen'

venv_path="$PRODUCT_DIR/src/python/tpl-gen/.venv"
home_venv_path="$HOME_PRODUCT_DIR/src/python/tpl-gen/.venv"
venv_path="$PRODUCT_DIR/src/python/tpl-gen/.venv"


test -d $venv_path && sudo rm -r $venv_path
cp -vr $home_venv_path $venv_path

perl -pi -e "s|/home/$APPUSR||g" $venv_path/bin/activate


echo "source $PRODUCT_DIR/src/python/tpl-gen/.venv/bin/activate" >> ~/.bashrc

echo "cd /opt/${ORG_DIR:-}/${PRODUCT:-}" >> ~/.bashrc


trap : TERM INT; sleep infinity & wait

