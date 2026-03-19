#!/usr/bin/env bash
# install by:
# wget https://github.com/csitea/run.sh/archive/refs/tags/current.zip && unzip -o current.zip -d . && mv -v run.sh-current my-app
# usage: ./run --help

set -E  # Ensure ERR trap is inherited by functions

# Global Error Handler
error_handler() {
  local exit_code=$?
  local line_no=$1
  local cmd="$2"
  if [ $exit_code -ne 0 ]; then
    do_log "FATAL Command '$cmd' failed at line $line_no with status $exit_code."
    exit $exit_code
  fi
}

# Execution Wrapper
execute_step() {
  local func_name=$1
  do_log "INFO START ::: running action :: $func_name"

  "$func_name"
  local status=$?

  if [ $status -eq 0 ]; then
    do_log "INFO STOP ::: running function :: $func_name"
  else
    do_log "FATAL failed to run action: $func_name with status $status !!!"
    exit $status
  fi
}

trap 'error_handler ${LINENO} "$BASH_COMMAND"' ERR

main() {
  do_flush_screen
  do_set_vars_v205 "$@" # is inside, unless --help flag is present
  ts=$(date "+%Y%m%d_%H%M%S")
  main_log_dir=~/var/log/$PROJ/

  mkdir -p $main_log_dir
  main_exec "$@" \
    > >(tee $main_log_dir/$PROJ.$ts.out.log) \
    2> >(tee $main_log_dir/$PROJ.$ts.err.log)
}

main_exec() {
  do_resolve_os
  do_check_install_min_req_bins
  do_load_functions

  test -z ${actions:-} && actions=' do_print_usage '
  do_run_actions "$actions"
  do_finalize

}

#------------------------------------------------------------------------------
# the "reflection" func - identify the the funcs per file
#------------------------------------------------------------------------------
get_function_list() {
  env -i PATH=/bin:/usr/bin:/usr/local/bin bash --noprofile --norc -c '
      source "'"$1"'"
      typeset -f |
      grep '\''^[^{} ].* () $'\'' |
      awk "{print \$1}" |
      while read -r fnc_name; do
         type "$fnc_name" | head -n 1 | grep -q "is a function$" || continue
            echo "$fnc_name"
            done
            '
}

do_read_cmd_args() {

  while [[ $# -gt 0 ]]; do
    case "$1" in
    -a | --actions) shift && actions="${actions:-}${1:-} " && shift ;;
    -h | --help) actions=' do_print_usage ' && ENV='dev' && shift ;;
    *) echo FATAL unknown "cmd arg: '$1' - invalid cmd arg, probably a typo !!!" && shift && exit 1 ;;
    esac
  done
  shift $((OPTIND - 1)) || true

}

do_run_actions() {
  actions=$1
  actions_found=0
  cd $PROJ_PATH
  actions="$(echo -e "${actions}" | sed -e 's/^[[:space:]]*//')" #or how-to trim leading space
  run_funcs=''
  while read -d ' ' arg_action; do
    while read -r fnc_file; do
      # Skip files that don't match the action name BEFORE spawning subprocess
      action_name=$(basename "$fnc_file" .func.sh)
      action_name="do_${action_name//-/_}"
      test "$action_name" != "$arg_action" && continue

      # Only call get_function_list for matching files
      while read -r fnc_name; do
        do_log "DEBUG Sourcing $fnc_file for action $arg_action"
        source $fnc_file
        actions_found=$((actions_found + 1))
        run_funcs="$(echo -e "${run_funcs}\n$fnc_name")"
      done < <(get_function_list "$fnc_file")
    done < <(find "src/bash/run/" "lib/bash/funcs" -type f -name '*.func.sh' | sort)

  done < <(echo "$actions")

  echo ${actions} ${actions_found}
  test $actions_found -eq 0 && {
    do_log "FATAL action(s) requested: \"$actions\" NOT found !!!"
    do_log "FATAL 1. check the spelling of your action"
    do_log "FATAL 2. check the available actions by: ENV=lcl ./run --help"
    do_log "FATAL the run failed !"
    exit 1
  }

  run_funcs="$(echo -e "${run_funcs}" | sed -e 's/^[[:space:]]*//;/^$/d')"
  while read -r run_func; do
    cd $PROJ_PATH
    execute_step "$run_func"
  done < <(echo "$run_funcs")

}

do_flush_screen() {
  printf "\033[2J"
  printf "\033[0;0H"
}

#------------------------------------------------------------------------------
# purpose: to pass msgs and print them to a log file and terminal
#  - with datetime
#  - the type of msg - INFO, ERROR, DEBUG, WARNING
# usage:
# do_log "INFO some info message"
# do_log "ERROR some error message"
# do_log "DEBUG some debug message"
# do_log "WARNING some warning message"
# depts:
#  - PROJ_PATH - the root dir of the sfw project
#  - PROJ - the name of the software project dir
#  - host_name - the short hostname of the host / container running on
#------------------------------------------------------------------------------
do_log() {
  print_ok() {
    GREEN_COLOR="\033[0;32m"
    DEFAULT_COLOR="\033[0m"
    echo -e "${GREEN_COLOR} ✔ ${1:-} ${DEFAULT_COLOR}"
  }

  print_warning() {
    YELLOW_COLOR="\033[33m"
    DEFAULT_COLOR="\033[0m"
    echo -e "${YELLOW_COLOR} ⚠ ${1:-} ${DEFAULT_COLOR}"
  }

  print_info() {
    BLUE_COLOR="\033[0;34m"
    DEFAULT_COLOR="\033[0m"
    echo -e "${BLUE_COLOR} ℹ ${1:-} ${DEFAULT_COLOR}"
  }

  print_fail() {
    RED_COLOR="\033[0;31m"
    DEFAULT_COLOR="\033[0m"
    echo -e "${RED_COLOR} ✘ ${1:-}${DEFAULT_COLOR}"
  }

  print_debug() {
    GRAY_COLOR="\033[0;37m"
    DEFAULT_COLOR="\033[0m"
    echo -e "${GRAY_COLOR} ⚙ ${1:-}${DEFAULT_COLOR}"
  }

  type_of_msg=$(echo $* | cut -d" " -f1)
  action=$(echo $* | cut -d" " -f2)
  rest_of_msg=$(echo $* | cut -d" " -f3-)
  test -z ${HOST_NAME:-} && export HOST_NAME=$(hostname -s)
  [ -z "${PROJ_PATH}" ] &&
    export PROJ_PATH=$(cd $(dirname $(perl -e 'use File::Basename; use Cwd "abs_path"; print dirname(abs_path($ARGV[0]))' -- "$0"))/../../.. && pwd)
  [ -z "${PROJ}" ] && export PROJ=$(basename $PROJ_PATH)

  # Pad [TYPE] to 9 chars (longest is [WARNING]) so dates align vertically
  local padded_type
  [[ "$type_of_msg" == "WARNING" ]] && type_of_msg="WARN"
  padded_type=$(printf "%-7s" "[$type_of_msg]")

  # Check if the action is START or STOP and adjust the length
  if [[ "$action" == "START" || "$action" == "STOP" ]]; then
    # Adjust the length of 'START' or 'STOP' token for alignment
    formatted_action=$(printf "%-5s" "$action") # 5 characters wide, adjust as needed
    msg="${padded_type} $(date "+%Y-%m-%d %H:%M:%S %Z") [${PROJ:-}][@${HOST_NAME:-}] [$$] $formatted_action $rest_of_msg"
  else
    # Handle other types of messages without formatting the action
    msg="${padded_type} $(date "+%Y-%m-%d %H:%M:%S %Z") [${PROJ:-}][@${HOST_NAME:-}] [$$] $action $rest_of_msg"
  fi

  log_dir="${PROJ_PATH:-}/dat/log/bash"
  mkdir -p "$log_dir" 2>/dev/null || { log_dir="$HOME/var/log/${PROJ:-}"; mkdir -p "$log_dir" 2>/dev/null; }
  log_file="$log_dir/${PROJ:-}."$(date "+%Y%m%d")'.log'

  case "$type_of_msg" in
  'FATAL') print_fail "$msg" | tee -a "$log_file" 2>/dev/null ;;
  'ERROR') print_fail "$msg" | tee -a "$log_file" 2>/dev/null ;;
  'WARNING'|'WARN') print_warning "$msg" | tee -a "$log_file" 2>/dev/null ;;
  'INFO') print_info "$msg" | tee -a "$log_file" 2>/dev/null ;;
  'OK') print_ok "$msg" | tee -a "$log_file" 2>/dev/null ;;
  'DEBUG') print_debug "$msg" | tee -a "$log_file" 2>/dev/null ;;
  *) echo " · $msg" | tee -a "$log_file" 2>/dev/null ;;
  esac
}

do_check_install_min_req_bins() {

  while read -r f; do source $f; done < <(find $PROJ_PATH/lib/bash/funcs/ -type f)

  which perl >/dev/null 2>&1 || {
    run_os_func install_bins perl
  }
  which jq >/dev/null 2>&1 || {
    run_os_func install_bins jq
  }
  which make >/dev/null 2>&1 || {
    # this will not work properly - google how-to install make on <<my-operating-system>>
    run_os_func install_bins make
  }
}

do_set_vars_v205() {
  set -u -o pipefail

  # Read command line arguments
  do_read_cmd_args "$@"

  # Set basic variables
  declare -gx host_name="$(hostname -s)" && export host_name

  # Determine directory paths
  unit_run_dir=$(perl -e 'use File::Basename; use Cwd "abs_path"; print dirname(abs_path(@ARGV[0]));' -- "$0")

  declare -gx RUN_UNIT="$(cd "$unit_run_dir" && basename "$(pwd)").sh" && export RUN_UNIT
  declare -gx PROJ_PATH="$(cd "$unit_run_dir/../../.." && pwd)" && export PROJ_PATH
  declare -gx APP_PATH="$(cd "$unit_run_dir/../../../.." && pwd)" && export APP_PATH
  declare -gx ORG_PATH="$(cd "$unit_run_dir/../../../../.." && pwd)" && export ORG_PATH
  declare -gx BASE_PATH="$(cd "$unit_run_dir/../../../../../.." && pwd)" && export BASE_PATH

  # Ensure logical link
  do_ensure_logical_link

  # Set project name
  declare -gx PROJ="$(basename "$PROJ_PATH")"
  export PROJ

  # Set environment
  declare -gx ENV="${ENV:-lcl}"
  export ENV

  # Set log directory and file
  declare -gx LOG_DIR="${PROJ_PATH:-}/dat/log/bash" && export LOG_DIR
  mkdir -p "$LOG_DIR"
  declare -gx LOG_FILE="$LOG_DIR/${PROJ:-}.$(date "+%Y%m%d").log" && export LOG_FILE

  # Change to project directory
  cd "$PROJ_PATH"

  # Log paths
  do_log "INFO using: BASE_PATH: $BASE_PATH"
  do_log "INFO using: ORG_PATH: $ORG_PATH"
  do_log "INFO using: APP_PATH: $APP_PATH"
  do_log "INFO using: PROJ_PATH: $PROJ_PATH"
  do_log "INFO using: LOG_DIR: $LOG_DIR"
  do_log "INFO using: LOG_FILE: $LOG_FILE"

  # Set user and group information
  declare -gx GROUP="${GROUP:-$(id -gn 2>/dev/null || ps -o group,supgrp $$ | tail -n 1 | awk '{print $1}')}" && export GROUP
  declare -gx USER="${USER:-$(id -un)}" && export USER

  # Set UID and GID only if they're not already set (and likely readonly)
  if ! declare -p UID >/dev/null 2>&1; then
    declare -gx UID="$(id -u)" && export UID
  fi
  if ! declare -p GID >/dev/null 2>&1; then
    declare -gx GID="$(id -g)" && export GID
  fi

  # Set OS
  declare -gx OS="${OS:-$(uname -s | tr '[:upper:]' '[:lower:]')}" && export OS

  # Print out all declared variables
  echo "Declared variables:"
  compgen -A variable | { grep -E '^(host_name|RUN_UNIT|PROJ_PATH|APP_PATH|ORG_PATH|BASE_PATH|PROJ|ENV|GROUP|USER|UID|GID|OS|LOG_DIR|LOG_FILE)$' || true; } | while read -r var; do
    echo "$var"
  done

  # Generate REQUIRED_VARS array
  REQUIRED_VARS=(host_name RUN_UNIT PROJ_PATH APP_PATH ORG_PATH BASE_PATH PROJ ENV GROUP USER UID GID OS LOG_DIR LOG_FILE)
  echo "REQUIRED_VARS: ${REQUIRED_VARS[*]}"
}
# REQUIRED_VARS=(host_name RUN_UNIT PROJ_PATH APP_PATH ORG_PATH BASE_PATH PROJ ENV GROUP USER UID GID OS)
# do_require_run_vars "${REQUIRED_VARS[@]}"
do_require_run_vars() {
  local var_list=("$@")
  local set_vars=()
  local unset_vars=()

  for var in "${var_list[@]}"; do
    if [[ -v $var && -n "${!var}" ]]; then
      set_vars+=("$var=${!var}")
    else
      unset_vars+=("$var")
    fi
  done

  if [[ ${#unset_vars[@]} -gt 0 ]]; then
    echo "FATAL: The following variables are not set or empty:" >&2
    printf '%s\n' "${unset_vars[@]}" >&2
    return 1
  fi

  printf "All required variables are set and non-empty:\n"
  printf '%s\n' "${set_vars[@]}" | sort
  return 0
}

# Usage example:
# check_variables "${REQUIRED_VARS[@]}"
# Usage example:
# do_set_vars_v205 "$@"

# ensure that the <<PROJ_PATH>>/run is a logical link and not a regular file
# if the run.sh is not under the src/bash/run dir terrible things happen ...
# this one is especially problematic in Dockerfile's ADD command
do_ensure_logical_link() {

  if [[ "$unit_run_dir" != */src/bash/run ]]; then
    echo "
         you probably unzipped into a new app/tool and forgot to run the following cmd:
         rm -v run; ln -sfn src/bash/run/run.sh run
         so that ls -al run should look like:
         lrwx------  1 osuser  osgroup 2022-01-01 20:40 run -> src/bash/run/run.sh
         !!!
         or you are running within a Dockerfile and calling directly PROJ_PATH/run
         which MIGHT work, but better to call PROJ_PATH/src/bash/run/run.sh
      "
    export PROJ_PATH=$(
      cd $unit_run_dir
      echo $(pwd)
    )
    export ORG_DIR=$(echo $PROJ_PATH | xargs dirname | xargs basename)
    export BASE_PATH=$(cd $unit_run_dir/../.. && echo $(pwd))
    echo PROJ_PATH: $PROJ_PATH
    echo ORG_DIR: $ORG_DIR
    echo BASE_PATH: $BASE_PATH
  fi

}

do_finalize() {

  do_log "OK $RUN_UNIT's run completed"
  cat <<EOF_FIN_MSG
  :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
         $RUN_UNIT run completed
  :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
EOF_FIN_MSG
  exit 0
}

do_load_functions() {
  while read -r f; do source $f; done < <(ls -1 $PROJ_PATH/lib/bash/funcs/*.func.sh)
  while read -r f; do source $f; done < <(ls -1 $PROJ_PATH/src/bash/run/*.func.sh)
}

run_os_func() {
  func_to_run=$1
  shift

  if [[ -z "$OS" ]]; then
    echo "your OS distro is not supported!!!"
    exit 1
  else
    "do_"$OS"_""$func_to_run" "$@"
  fi

}

do_resolve_os() {
  if [[ $(uname -s) == *"Linux"* ]]; then
    distro=$(grep '^ID=' /etc/os-release | cut -d= -f2 | tr -d '"')
    case "$distro" in
    ubuntu | pop) export OS='ubuntu' ;;
    alpine) export OS='alpine' ;;
    manjaro) export OS='manjaro' ;;
    fedora) export OS='fedora' ;;
    debian) export OS='debian' ;;
    opensuse-tumbleweed | opensuse-leap | suse)
      export OS='suse'
      echo "your Linux distro has limited support !!!"
      ;;
    *)
      echo "your Linux distro is not supported !!!"
      exit 1
      ;;
    esac
  elif [[ $(uname -s) == *"Darwin"* ]]; then
    export OS='mac'
  else
    echo "your OS distro is not supported !!!"
    exit 1
  fi
  source "$PROJ_PATH"'/lib/bash/funcs/set-vars-on-'"$OS"'.func.sh'
  'do_set_vars_on_'"$OS"
}

# usage:
# checks the return code of the last command and exits with the proper
# quit_on "restoring the mysql dump to the server"
quit_on() {
  rv=$?
  if [ $rv -ne 0 ]; then
    do_log "FATAL Error: Failed in $1"
    exit $rv
  fi
}

main "$@"

# Version: 2.0.5
# VersionHistory:
# 2.0.5 - 2024-08-14 - set GUID and UID only if they are not already set
# 2.0.4 - 2024-08-13 - versioned required vars api , all exported vars in CAPS
# 2.0.3 - 2024-07-25 - fix the base path resolution bug
# 2.0.2 - 2024-07-22 - remove the kin functions
# 2.0.1 - 2024-07-17 - add the quit_on func to the base vars
# 2.0.0 - 2024-04-09 - added the explict levels up docs to the base vars
