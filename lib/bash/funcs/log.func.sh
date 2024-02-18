#!/bin/bash

do_log() {
  print_ok() {
    GREEN_COLOR="\033[0;32m"
    DEFAULT_COLOR="\033[0m"
    echo -e "${GREEN_COLOR} ✔ [OK] ${1:-} ${DEFAULT_COLOR}"
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
    echo -e "${RED_COLOR} ❌ [NOK] ${1:-}${DEFAULT_COLOR}"
  }

  type_of_msg=$(echo $* | cut -d" " -f1)
  action=$(echo $* | cut -d" " -f2)
  rest_of_msg=$(echo $* | cut -d" " -f3-)
  test -z ${host_name:-} && export host_name=$(hostname -s)
  [ -z "${PROJ_PATH}" ] &&
    export PROJ_PATH=$(cd $(dirname $(perl -e 'use File::Basename; use Cwd "abs_path"; print dirname(abs_path($ARGV[0]))' -- "$0"))/../../.. && pwd)
  [ -z "${PROJ}" ] && export PROJ=$(basename $PROJ_PATH)

  # Check if the action is START or STOP and adjust the length
  if [[ "$action" == "START" || "$action" == "STOP" ]]; then
    # Adjust the length of 'START' or 'STOP' token for alignment
    formatted_action=$(printf "%-5s" "$action") # 5 characters wide, adjust as needed
    msg=" [$type_of_msg] $(date "+%Y-%m-%d %H:%M:%S %Z") [${PROJ:-}][@${host_name:-}] [$$] $formatted_action $rest_of_msg"
  else
    # Handle other types of messages without formatting the action
    msg=" [$type_of_msg] $(date "+%Y-%m-%d %H:%M:%S %Z") [${PROJ:-}][@${host_name:-}] [$$] $action $rest_of_msg"
  fi

  log_dir="${PROJ_PATH:-}/dat/log/bash"
  mkdir -p $log_dir || mkdir -p $HOME/var/log/$PROJ && log_dir=$HOME/var/log/$PROJ
  log_file="$log_dir/${PROJ:-}."$(date "+%Y%m%d")'.log'

  case "$type_of_msg" in
  'FATAL') print_fail "$msg" | tee -a $log_file ;;
  'ERROR') print_fail "$msg" | tee -a $log_file ;;
  'WARNING') print_warning "$msg" | tee -a $log_file ;;
  'INFO') print_info "$msg" | tee -a $log_file ;;
  'OK') print_ok "$msg" | tee -a $log_file ;;
  *) echo "$msg" | tee -a $log_file ;;
  esac
}
#------------------------------------------------------------------------------
# do_log: A truly reusable logging function.
#------------------------------------------------------------------------------
# PURPOSE:
# To output messages to both the terminal and a log file, each message is
# prefixed with a timestamp, the type of message (INFO, ERROR, DEBUG, WARNING),
# and other relevant metadata.
#
# DEPENDENCIES:
# - Requires the following environment variables:
#   * PROJ_PATH: The root directory of the software project.
#   * PROJ: The name of the software project directory. If not set, it is derived from PROJ_PATH.
#   * host_name: The short hostname of the host/container. Automatically set if not provided.
# - Relies on external commands: `hostname`, `perl`, `dirname`.
#
# USAGE:
# ----------------
# Source the script before using the function:
# source ./lib/bash/funcs/log.func.sh
#
# Example calls:
# do_log "INFO Some informational message"
# do_log "ERROR An error occurred"
# do_log "DEBUG Debugging data: x = $x"
# do_log "WARNING Warning: Configuration file not found"
#
# LOG FILE:
# - Messages are logged to a file named `<PROJ>.<date>.log` in the directory
#   `$PROJ_PATH/dat/log/bash`. If this directory is not writable, it falls back to
#   `$HOME/var/log/$PROJ`.
# - The log file includes the date, message type, project name, hostname, process ID,
#   and the message itself.
#
# NOTES:
# - The function dynamically adjusts the message layout for START and STOP actions
#   for better readability.
# - Color-coding is used for terminal output: green for OK, yellow for WARNING,
#   blue for INFO, and red for ERROR/FATAL messages.
#------------------------------------------------------------------------------

# eof file: lib/bash/funcs/log.func.sh
