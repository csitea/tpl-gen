#!/bin/bash
#------------------------------------------------------------------------------
# Purpose:
# to search for a string and replace it with another recursively in a dir
# both in dir and file paths and their contents
# Prerequisites: setting vars in the caller shell
# export DIR_TO_MORPH=<<the-dir-to-search-and-replace-in-recursively>>
# export STR_TO_SRCH=<<the-string-to-search-for>>
# export STR_TO_REPL=<<the-string-to-replace-with>>
# while read -r f ; do cp -v $f $(echo $f|perl -ne 's#func#help#g;print'|perl -ne
# 's#src#doc#g;print'|perl -ne 's#bash#txt#g;print'|perl -ne 's#help.sh#help.txt#g;print') ; done <
# <(find src/bash/run/ -type f)
#------------------------------------------------------------------------------
do_morph_dir(){

  # set -x
  # some initial checks the users should set the vars in their shells !!!
  do_require_var DIR_TO_MORPH $DIR_TO_MORPH
  do_require_var STR_TO_SRCH $STR_TO_SRCH
  do_require_var STR_TO_REPL $STR_TO_REPL

  do_log "INFO DIR_TO_MORPH: $DIR_TO_MORPH"
  do_log "INFO STR_TO_SRCH:\"$STR_TO_SRCH\" " ;
  do_log "INFO STR_TO_REPL:\"$STR_TO_REPL\" " ;
  sleep 2

  do_log "INFO START :: search and replace in non-binary files"
  #search and replace ONLY in the txt files and omit the binary files
  while read -r file ; do (
    #debug do_log doing find and replace in $file
    do_log "DEBUG working on file: $file"
    do_log "DEBUG searching for $STR_TO_SRCH , replacing with :: $STR_TO_REPL"

        # we do not want to mess with out .git dir
        # or how-to check that a string contains another string
        case "$file" in
          *.git*)
          continue
          ;;
        esac
    perl -pi -e "s|\Q$STR_TO_SRCH\E|$STR_TO_REPL|g" "$file"
  );
  done < <(find $DIR_TO_MORPH -type f -not -path "*/.venv/*" -not -exec file {} \; | grep text | cut -d: -f1)

  do_log "INFO STOP  :: search and replace in non-binary files"

  #search and repl %var_id% with var_id_val in deploy_tmp_dir
  do_log "INFO search and replace in dir and file paths DIR_TO_MORPH:$DIR_TO_MORPH"
    # rename the dirs according to the pattern
    while read -r dir ; do (
        echo $dir|perl -nle '$o=$_;s#'"\Q$STR_TO_SRCH\E"'#'"$STR_TO_REPL"'#g;$n=$_;`mkdir -p $n` ;'
    );
    done < <(find $DIR_TO_MORPH -type d -not -path "*/.venv/*" \
        -not -path "/*node_modules/*" |grep -v '.git')

    # rename the files according to the pattern
    while read -r file ; do (
        echo $file | perl -nle '$o=$_;s|'"\Q$STR_TO_SRCH\E"'|'"$STR_TO_REPL"'|g;$n=$_;rename($o,$n) unless -e $n ;'
    );
    done < <(find $DIR_TO_MORPH -type f -not -path "*/.venv/*" \
        -not -path "*/node_modules/*" |grep -v '.git')

    while read -r dir ; do (
        rm -rv $dir
    );
    done < <(find $DIR_TO_MORPH -type d -not -path "*/.venv/*" -not -path "/*node_modules/*" \
        | grep -v '.git'|grep "$STR_TO_SRCH")


    export exit_code=0

}

#eof file: src/bash/run/morph-dir.func.sh
