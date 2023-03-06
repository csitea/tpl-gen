#!/bin/bash

do_set_vars(){
   set -u -o pipefail
   do_read_cmd_args "$@"
   export host_name="$(hostname -s)"
   export exit_code=1 # assume failure for each action, enforce return code usage
   unit_run_dir=$(perl -e 'use File::Basename; use Cwd "abs_path"; print dirname(abs_path(@ARGV[0]));' -- "$0")
   export RUN_UNIT=$(cd $unit_run_dir ; basename `pwd` .sh)
   export PRODUCT_DIR=$(cd $unit_run_dir/../../.. ; echo `pwd`)
   export ORG_DIR=$(echo $PRODUCT_DIR|xargs dirname | xargs basename)
   export BASE_DIR=$(cd $unit_run_dir/../../../../.. && echo `pwd`)
   do_ensure_logical_link
   export PRODUCT=$(basename $PRODUCT_DIR)
   ENV="${ENV:=lde}" # <- remove this one IF you want to enforce the caller to provide the ENV var
   cd $PRODUCT_DIR
   # workaround for github actions running on docker
   test -z ${GROUP:-} && export GROUP=$(id -gn)
   test -z ${GROUP:-} && export GROUP=$(ps -o group,supgrp $$|tail -n 1|awk '{print $1}')
   test -z ${USER:-} && export USER=$(id -un)
   test -z ${UID:-} && export UID=$(id -u)
   test -z ${GID:-} && export GID=$(id -g)
}

set -x

do_set_vars

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

