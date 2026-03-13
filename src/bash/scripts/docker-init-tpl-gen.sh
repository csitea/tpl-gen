#!/bin/bash

PROJ_PATH=$(echo $PROJ_PATH | perl -ne "s|/home/$APPUSR||g;print")
BASE_PATH=$(echo $BASE_PATH | perl -ne "s|/home/$APPUSR||g;print")

home_venv_path="$HOME_PROJ_PATH/src/python/$MODULE/.venv"
venv_path="$PROJ_PATH/src/python/$MODULE/.venv"

if [ -d "$venv_path" ]; then
  rm -r "$venv_path"
fi

# echo running find $home_venv_path \| tail -n 10
# find $home_venv_path | tail -n 10
# todo remove me ^^^^

# test -d $venv_path && sudo rm -r $venv_path
# do not use this one ^^^^!!! Big GOTCHA !!!
if [ -d "$home_venv_path" ]; then
  cp -r $home_venv_path $venv_path
  perl -pi -e "s|/home/$APPUSR||g" $venv_path/bin/activate
else
  # CI fallback: no pre-existing .venv — create one via poetry install
  cd "$PROJ_PATH/src/python/$MODULE"
  poetry config virtualenvs.create true
  poetry config virtualenvs.in-project true
  poetry install --no-interaction
  cd "$PROJ_PATH"
fi

# if it points to PROJ_PATH it will always be broken
echo "source $PROJ_PATH/src/python/$MODULE/.venv/bin/activate" >>~/.bashrc
echo "source $PROJ_PATH/src/python/$MODULE/.venv/bin/activate" >>~/.profile

echo 'export PATH=$PATH:$PROJ_PATH/src/python/$MODULE/.venv/bin/' >>~/.bashrc
echo 'export PATH=$PATH:$PROJ_PATH/src/python/$MODULE/.venv/bin/' >>~/.profile

echo "cd $PROJ_PATH" >>~/.bashrc
echo "cd $PROJ_PATH" >>~/.profile

cd $PROJ_PATH

trap : TERM INT
sleep infinity &
wait
