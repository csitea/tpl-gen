#!/bin/bash

MODULE='tpl-gen'


test -z ${PRODUCT:-} && PRODUCT=${MODULE:-}

PRODUCT_DIR=$(echo $PRODUCT_DIR|perl -ne "s|/home/$APPUSR||g;print")
BASE_DIR=$(echo $BASE_DIR|perl -ne "s|/home/$APPUSR||g;print")

home_venv_path="$HOME_PRODUCT_DIR/src/python/$MODULE/.venv"
venv_path="$PRODUCT_DIR/src/python/$MODULE/.venv"

if [ -d "$venv_path" ]; then
  rm -r "$venv_path"
fi

cd $PRODUCT_DIR/src/python/$MODULE && poetry install
perl -pi -e "s|/home/$APPUSR||g" $venv_path/bin/activate


# if it points to PRODUCT_DIR it will always be broken
echo "source $PRODUCT_DIR/src/python/$MODULE/.venv/bin/activate" >> ~/.bashrc
echo "source $PRODUCT_DIR/src/python/$MODULE/.venv/bin/activate" >> ~/.profile
# cd "$PRODUCT_DIR/src/python/$MODULE && poetry install"

echo "cd $PRODUCT_DIR" >> ~/.bashrc


trap : TERM INT; sleep infinity & wait