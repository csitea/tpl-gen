#!/bin/bash
#
# create a component zip file to be unzipped to the component project back
# usage:
# MODULE=run.sh ./run -a do_zip_me_as_module
#
do_zip_me_as_module(){

   mkdir -p $PRODUCT_DIR/cnf/lst/
   cd $PRODUCT_DIR
   do_require_var MODULE ${MODULE:-}

   # contains the files to be included while packaging
   component_include_list_fle=$PRODUCT_DIR/cnf/lst/$MODULE.include.lst

   zip_file=$BASE_DIR/$ORG_DIR/$MODULE.zip
   test -f $zip_file && rm -v $zip_file


   while read -r f; do

      # if the file or symlink still exists in the bigger project add it
      if [ -f "$PRODUCT_DIR/$f" ] || [ -L "$PRODUCT_DIR/$f" ]; then
        zip -y $zip_file $f
      fi

      # if the file does not exist, remove it from the list file
      test -f $f || perl -pi -e 's|^'"$f"'\n\r||gm' $component_include_list_fle

   done < <(cat $component_include_list_fle)

   do_log "INFO produced the $zip_file file"

   test -f $component_include_list_fle && export exit_code="0"

}
