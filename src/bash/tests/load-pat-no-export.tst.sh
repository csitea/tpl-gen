#!/bin/bash
#------------------------------------------------------------------------------
# Purpose:
# Test that do_load_pat never exports the token: no child process of an
# action (python, terraform, curl and what they start) finds it in its
# environment, where `ps eww` shows it, while the action's own shell has it:
#   - raw-token file, export-format file that also sets an alias
#     (<SERVICE>_API_TOKEN), and an inherited, already exported <SERVICE>_PAT:
#     a child shell sees nothing, the loading shell has the token
#   - a missing PAT file still returns 11 and leaves nothing exported
#   - do_validate_params, the ./run path that calls do_load_pat for an empty
#     *_PAT param: the action's shell has the token, a child does not
# Only dummy tokens, HOME points at a temp dir, no network.
# Exit 0 when every check passes, 1 otherwise.
#------------------------------------------------------------------------------

cd "$(dirname "${BASH_SOURCE[0]}")/../../.." || exit 1
PROJ_DIR=$(pwd)
FUNCS="$PROJ_DIR/lib/bash/funcs"

fails=0
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
TOK=dummy-tok-7f3a9c

check_eq() {
  local what="$1" got="$2" want="$3"
  if [[ "$got" == "$want" ]]; then
    echo "  ok    $what"
  else
    echo "  FAIL  $what (got '$got', wanted '$want')"
    fails=$((fails + 1))
  fi
}

# load <service> [VAR=value ...]: run do_load_pat in a clean shell, print
# "<rc>|<token in this shell>|<count of the token in a child shell's env>"
load() {
  local svc="$1"; shift
  # shellcheck disable=SC2016 # the script expands in the child shell
  env -u CONFLUENCE_PAT -u JIRA_PAT -u CONFLUENCE_PAT_FILE -u JIRA_PAT_FILE \
    -u JIRA_API_TOKEN -u CONFLUENCE_API_TOKEN HOME="$T/home" "$@" bash -c '
      do_log() { :; }
      source "$1"
      do_load_pat "$2"; rc=$?
      v="${2}_PAT"
      printf "%s|%s|%s" "$rc" "${!v:-}" "$(env | grep -c "$3")"' \
    _ "$FUNCS/load-pat.func.sh" "$svc" "$TOK"
}

mkdir -p "$T/home"
printf '%s\n' "$TOK" > "$T/raw.tok"
printf 'export JIRA_PAT="%s"\nexport JIRA_API_TOKEN="%s"\n' "$TOK" "$TOK" > "$T/export.tok"

echo "--- do_load_pat: the token stays in the loading shell ---"
check_eq "raw file: loaded, not in a child's env" \
  "$(load CONFLUENCE CONFLUENCE_PAT_FILE="$T/raw.tok")" "0|$TOK|0"
check_eq "export file with an alias: loaded, neither name in a child's env" \
  "$(load JIRA JIRA_PAT_FILE="$T/export.tok")" "0|$TOK|0"
check_eq "inherited exported PAT: kept, un-exported" \
  "$(load CONFLUENCE CONFLUENCE_PAT="$TOK")" "0|$TOK|0"
check_eq "missing file: rc 11, an inherited alias un-exported" \
  "$(load JIRA JIRA_PAT_FILE="$T/none.tok" JIRA_API_TOKEN="$TOK")" "11||0"

echo "--- do_validate_params: an empty *_PAT param is loaded, not exported ---"
cat > "$T/fixture-action.func.sh" <<'FIX'
#!/bin/bash
#------------------------------------------------------------------------------
# @description A fixture action that needs a PAT
# @param JIRA_PAT (required) - the Jira token
# @example ./run -a do_fixture_action
#------------------------------------------------------------------------------
do_fixture_action() { :; }
FIX
# shellcheck disable=SC2016 # the script expands in the child shell
got=$(env -u JIRA_PAT -u JIRA_API_TOKEN HOME="$T/home" JIRA_PAT_FILE="$T/export.tok" \
  bash -c '
    do_log() { :; }
    for f in "$1"/parse-metadata.func.sh "$1"/load-pat.func.sh "$1"/validate-params.func.sh; do
      source "$f"
    done
    do_validate_params "$2"; rc=$?
    printf "%s|%s|%s" "$rc" "${JIRA_PAT:-}" "$(env | grep -c "$3")"' \
  _ "$FUNCS" "$T/fixture-action.func.sh" "$TOK")
check_eq "required JIRA_PAT: validated from the file, not in a child's env" "$got" "0|$TOK|0"

echo ""
if [[ $fails -eq 0 ]]; then
  echo "PASS load-pat-no-export"
  exit 0
fi
echo "FAIL load-pat-no-export: $fails check(s)"
exit 1
