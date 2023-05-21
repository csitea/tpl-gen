#!/bin/bash
#
# create a component zip file to be unzipped to the component project back
# usage:
# MODULE=run.sh ./run -a do_zip_me_as_module
do_zip_me_as_module() {
  mkdir -p "$PRODUCT_DIR/cnf/lst/"
  cd "$PRODUCT_DIR"
  do_require_var MODULE "${MODULE:-}"

  # Path to the exclude file containing the glob patterns
  exclude_file="$PRODUCT_DIR/cnf/lst/$MODULE.exclude.lst"

  # Contains the files to be included while packaging
  component_include_list_fle="$PRODUCT_DIR/cnf/lst/$MODULE.include.lst"

  zip_file="$BASE_DIR/$ORG_DIR/$MODULE.zip"
  test -f "$zip_file" && rm -v "$zip_file"

  while read -r file; do
    excluded=false

    # Check if the file matches any of the exclude patterns
    while IFS= read -r pattern; do
      if [[ $file == *$pattern* ]]; then
        excluded=true
        break
      fi
    done < "$exclude_file"

    # Only add the file to the zip if it is not excluded
    if ! $excluded; then
      # if the file or symlink still exists in the bigger project, add it
      if [ -f "$PRODUCT_DIR/$file" ] || [ -L "$PRODUCT_DIR/$file" ]; then
        zip -y "$zip_file" "$file"
      fi

      # if the file does not exist, remove it from the list file
      test -f "$file" || perl -pi -e 's|^'"$file"'\n\r||gm' "$component_include_list_fle"
    fi
  done < "$component_include_list_fle"

  do_log "INFO produced the $zip_file file"

  test -f "$component_include_list_fle" && export exit_code="0"
}
