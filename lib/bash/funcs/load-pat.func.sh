#!/bin/bash
#------------------------------------------------------------------------------
# @description Load a Personal Access Token (PAT) from a file into the
#              corresponding environment variable.
#
# Supports two PAT file formats:
#   1. Shell export format:  export CONFLUENCE_PAT="token-value"
#      → file is sourced directly; the export attribute is then removed
#   2. Raw token format:     token-value
#      → first line is read into the PAT variable
#
# @param $1  service name: CONFLUENCE or JIRA  (required)
#
# @example  do_load_pat CONFLUENCE || return 11
# @example  do_load_pat JIRA       || return 11
#
# Environment consumed:
#   CONFLUENCE_PAT_FILE  path to the Confluence PAT file
#   JIRA_PAT_FILE        path to the JIRA PAT file
#
# Shell variable produced, NOT exported:
#   CONFLUENCE_PAT  (when service=CONFLUENCE)
#   JIRA_PAT        (when service=JIRA)
# The token is a plain shell variable: the action reads it in-process, and no
# child process (python, terraform, curl, ...) inherits it in its environment,
# where `ps eww` would show it. An inherited, already exported <SERVICE>_PAT
# and the aliases an export-format file may set (<SERVICE>_API_TOKEN,
# <SERVICE>_TOKEN, <SERVICE>_PERSONAL_ACCESS_TOKEN) are un-exported too.
#------------------------------------------------------------------------------

do_load_pat() {
  local service="${1:-}"
  if [[ -z "$service" ]]; then
    do_log "ERROR do_load_pat requires a service argument: CONFLUENCE or JIRA"
    return 11
  fi
  local rc=0 name
  _do_load_pat_read "$service" || rc=$?
  for name in "${service}_PAT" "${service}_API_TOKEN" "${service}_TOKEN" \
    "${service}_PERSONAL_ACCESS_TOKEN"; do
    # shellcheck disable=SC2163 # un-export the variable that $name names
    export -n "$name"
  done
  return $rc
}

# The reader behind do_load_pat: sets <SERVICE>_PAT, exports nothing itself
_do_load_pat_read() {
  local service="$1"
  local pat_var="${service}_PAT"
  local pat_file_var="${service}_PAT_FILE"
  local pat_file="${!pat_file_var:-}"

  # Already loaded — nothing to do
  if [[ -n "${!pat_var:-}" ]]; then
    return 0
  fi

  if [[ -z "$pat_file" ]]; then
    do_log "ERROR ${pat_file_var} is not set — cannot load ${pat_var}"
    return 11
  fi

  if [[ ! -f "$pat_file" ]]; then
    do_log "ERROR ${pat_var} not set and PAT file not found: ${pat_file}"
    return 11
  fi

  local first_line
  first_line=$(head -1 "$pat_file")

  if [[ "$first_line" == export* ]]; then
    # Shell export format — source the file to honour all export statements
    # shellcheck source=/dev/null
    source "$pat_file"
  else
    # Raw token format — the first line is the PAT value
    printf -v "$pat_var" '%s' "$first_line"
  fi

  if [[ -z "${!pat_var:-}" ]]; then
    do_log "ERROR ${pat_var} is still empty after loading ${pat_file}"
    return 11
  fi
}
# run-bsh ::: v3.7.0
