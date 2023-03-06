#!/bin/bash

MODULE='tpl-gen'


test -z ${PRODUCT:-} && PRODUCT=${MODULE:-}

PRODUCT_DIR=$(echo $PRODUCT_DIR|perl -ne "s|/home/$APPUSR||g;print")
BASE_DIR=$(echo $BASE_DIR|perl -ne "s|/home/$APPUSR||g;print")

venv_path="$PRODUCT_DIR/src/python/$MODULE/.venv"
home_venv_path="$HOME_PRODUCT_DIR/src/python/$MODULE/.venv"
venv_path="$PRODUCT_DIR/src/python/$MODULE/.venv"

echo running find $home_venv_path \| tail -n 10
find $home_venv_path | tail -n 10
# todo remove me ^^^^


# test -d $venv_path && sudo rm -r $venv_path
# do not use this one ^^^^!!! Big GOTCHA !!!
cp -vr $home_venv_path $venv_path
perl -pi -e "s|/home/$APPUSR||g" $venv_path/bin/activate


echo "source $PRODUCT_DIR/src/python/$MODULE/.venv/bin/activate" >> ~/.bashrc

echo "cd $PRODUCT_DIR" >> ~/.bashrc


trap : TERM INT; sleep infinity & wait

