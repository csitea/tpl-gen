#!/bin/bash


PRODUCT_DIR=$(echo $PRODUCT_DIR|perl -ne "s|/home/$APPUSR||g;print")
BASE_DIR=$(echo $BASE_DIR|perl -ne "s|/home/$APPUSR||g;print")


home_venv_path="$HOME_PRODUCT_DIR/src/python/$MODULE/.venv"
venv_path="$PRODUCT_DIR/src/python/$MODULE/.venv"

if [ -d "$venv_path" ]; then
  rm -r "$venv_path"
fi

# echo running find $home_venv_path \| tail -n 10
# find $home_venv_path | tail -n 10
# todo remove me ^^^^

# test -d $venv_path && sudo rm -r $venv_path
# do not use this one ^^^^!!! Big GOTCHA !!!
cp -r $home_venv_path $venv_path
perl -pi -e "s|/home/$APPUSR||g" $venv_path/bin/activate


# if it points to PRODUCT_DIR it will always be broken
echo "source $PRODUCT_DIR/src/python/$MODULE/.venv/bin/activate" >> ~/.bashrc
echo "source $PRODUCT_DIR/src/python/$MODULE/.venv/bin/activate" >> ~/.profile

echo "cd $PRODUCT_DIR" >> ~/.bashrc


trap : TERM INT; sleep infinity & wait

