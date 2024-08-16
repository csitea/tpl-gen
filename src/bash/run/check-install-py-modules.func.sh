#!/bin/bash

# install the poetry for every python component project on the first level
# of the src/python dir
do_check_install_py_modules() {

  set -x

  which poetry >/dev/null 2>&1 || {
    do_check_install_poetry
  }

  while read -r f; do
    tgt_dir=$(dirname $f)
    echo working on tgt_dir: $tgt_dir
    cd "$tgt_dir" || do_log "FATAL
        do_check_install_py_modules ::: the tgt_dir: $tgt_dir does not exist" && exit 1

    # if we want to filter by a sub component
    if [[ ! -z "${MODULE:-}" ]]; then
      if [[ "$tgt_dir" == *"$MODULE"* ]]; then
        test -f poetry.lock && rm -vf poetry.lock
        test -d .venv && rm -rv .venv
        poetry env use python3.8
        poetry config virtualenvs.create true
        poetry config virtualenvs.in $tgt_dir/.venv
        poetry config settings.virtualenvs.in-project true
        poetry config --list
        sleep 10
        poetry intall cleo
        poetry install -vvv
        poetry -vvv update
        test $? -ne "0" && do_log "FATAL failed to install $tgt_dir py modules" && exit 1
      fi
    fi
    cd -
  done < <(find $PROJ_PATH/src/python/ -name pyproject.toml)

  export EXIT_CODE=0
}
