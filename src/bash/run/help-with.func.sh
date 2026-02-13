#!/bin/bash
#------------------------------------------------------------------------------
# Purpose:
# To provide documentation for shell action functions by searching for
# functions containing a keyword and displaying their comments.
#
# Usage:
# SRCH=push ./run -a do_help_with
# SRCH=pull ./run -a do_help_with
# SRCH=gcp ./run -a do_help_with
#
# With pager for long output:
# SRCH=gcp ./run -a do_help_with 2>&1 | less
#
# Note: The variable must be on the SAME LINE before ./run (inline assignment)
#------------------------------------------------------------------------------
do_help_with() {
  local keyword="${SRCH:-}"

  if [[ -z "$keyword" ]]; then
    do_log "ERROR SRCH is not set"
    do_log "INFO Usage: SRCH=<keyword> ./run -a do_help_with"
    do_log "INFO Example: SRCH=push ./run -a do_help_with"
    do_log "INFO Example: SRCH=gcp ./run -a do_help_with 2>&1 | less"
    export EXIT_CODE=1
    return 1
  fi

  do_log "INFO Searching for functions containing: '$keyword'"
  echo ""

  local found_count=0
  local func_dirs=("src/bash/run" "lib/bash/funcs")

  for func_dir in "${func_dirs[@]}"; do
    local search_path="$PROJ_PATH/$func_dir"
    [[ ! -d "$search_path" ]] && continue

    while read -r func_file; do
      [[ -z "$func_file" ]] && continue

      # Extract function names from the file (exclude private functions starting with _)
      while read -r func_name; do
        [[ -z "$func_name" ]] && continue
        [[ "$func_name" =~ ^_ ]] && continue  # Skip private functions

        # Check if function name contains the keyword (case insensitive)
        if echo "$func_name" | grep -qi "$keyword"; then
          found_count=$((found_count + 1))

          # Get relative path from PROJ_PATH
          local rel_path="${func_file#$PROJ_PATH/}"

          echo "=============================================================================="
          echo "Function:  $func_name"
          echo "File:      $rel_path"
          echo "=============================================================================="

          # Find the line number where the function is defined
          local func_line
          func_line=$(grep -n "^${func_name}[[:space:]]*()[[:space:]]*{" "$func_file" | head -1 | cut -d: -f1)

          if [[ -z "$func_line" ]]; then
            echo "  (No documentation found)"
            echo ""
            continue
          fi

          # Read backwards from the function line to collect comments
          local comments=()
          local line_num=$((func_line - 1))

          while [[ $line_num -gt 0 ]]; do
            local line
            line=$(sed -n "${line_num}p" "$func_file")

            # Stop if we hit a non-comment, non-empty line (excluding shebang)
            if [[ ! "$line" =~ ^[[:space:]]*# && -n "$line" ]]; then
              break
            fi

            # Skip empty lines but continue looking
            if [[ -z "$line" ]]; then
              line_num=$((line_num - 1))
              continue
            fi

            # Skip shebang
            if [[ "$line" =~ ^#! ]]; then
              line_num=$((line_num - 1))
              continue
            fi

            # Add comment to array (we'll reverse later)
            comments+=("$line")
            line_num=$((line_num - 1))
          done

          # Print comments in correct order (reverse the array)
          if [[ ${#comments[@]} -gt 0 ]]; then
            for ((i=${#comments[@]}-1; i>=0; i--)); do
              echo "  ${comments[i]}"
            done
          else
            echo "  (No documentation found)"
          fi

          echo ""
        fi
      done < <(grep -E '^[a-zA-Z_][a-zA-Z0-9_]*\s*\(\)\s*\{' "$func_file" 2>/dev/null | \
               sed 's/[[:space:]]*().*$//')
    done < <(find "$search_path" -type f -name '*.func.sh' 2>/dev/null)
  done

  if [[ $found_count -eq 0 ]]; then
    do_log "WARNING No functions found containing '$keyword'"
    do_log "INFO Try a different keyword or check available actions with: ./run --help"
  else
    do_log "INFO Found $found_count function(s) matching '$keyword'"
  fi

  export EXIT_CODE=0
}
