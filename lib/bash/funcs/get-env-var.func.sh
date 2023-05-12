#!/bin/env bash


# ORG=$(do_get_env_var 'ORG')
# APP=$(do_get_env_var 'APP')
# ENV=$(do_get_env_var 'ENV')
#
do_get_env_var() {
  # Input validation
  if [[ $# -ne 1 ]]; then
    printf " [ERROR] %s \n" "do_get_env_var: requires 1 argument (ENV_VAR_NAME)"
    return 1
  fi

  # Declare local variables
  local ENV_VAR_NAME=$1
  local ENV_VAR_VALUE=${!ENV_VAR_NAME}

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

