#!/bin/bash
#------------------------------------------------------------------------------
# usage example:
# source lib/bash/funcs/require-var.func.sh
# do_require_var ORG ${ORG:-}
# do_require_var APP ${APP:-}
# do_require_var ENV ${ENV:-}
#------------------------------------------------------------------------------
do_require_var() {
  # Input validation
  if [[ $# -ne 2 ]]; then
    printf " [ERROR] %s \n" "do_require_var: requires 2 arguments (ENV_VAR_NAME and ENV_VAR_VALUE)"
    return 1
  fi

  # Declare local variables
  local ENV_VAR_NAME=$1
  local ENV_VAR_VALUE=$2

  # Define logging function
  do_simple_log() {
    local TYPE_OF_MSG=$1
    local MSG=$2
    printf " [%s] %s [%d] %s \n" "$TYPE_OF_MSG" "$(date "+%Y-%m-%d %H:%M:%S %Z")" "$$" "$MSG"
  }

  # Check if the environment variable is set
  if [[ -z "${ENV_VAR_VALUE}" ]]; then
    do_simple_log 'FATAL' "The environment variable '${ENV_VAR_NAME}' does not have a value!"
    do_simple_log 'INFO' "In the calling shell, do 'export ${ENV_VAR_NAME}=your-${ENV_VAR_NAME}-value'"
    return 1
  fi

  # Return the value of the environment variable
  echo "${ENV_VAR_VALUE}"
}

