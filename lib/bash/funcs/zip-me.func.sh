#!/bin/bash
#------------------------------------------------------------------------------
# usage example:
# source $PRODUCT/lib/bash/funcs/export-json-section-vars.sh
# ./run -a do_zip_me
# binary dependencies:
# zip
#------------------------------------------------------------------------------
do_zip_me(){
   
   # remove any pre-existing zip file 
   test -f ../$(basename `pwd`).zip && rm -v ../$(basename `pwd`).zip ; 
   
   # zip everything except the .git, .terraform, .venv and node_modules dirs
   zip -r ../$(basename `pwd`).zip  . -x '.git/*' -x '*/.terraform/*' -x '*/.venv/*' -x '*/node_modules/*' --symlinks
   rv=$?


   echo -e "\n\n to unzip run the following cmd:"
   echo -e "\n mkdir -p /tmp/whatever-tgt_dir ; unzip -o $(cd ..; echo `pwd`)/$(basename `pwd`).zip -d /tmp/whatever-tgt_dir \n\n"

   
   export exit_code=$rv

}
