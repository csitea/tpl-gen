#!/bin/bash
#------------------------------------------------------------------------------
# usage example:
# source $PRODUCT/lib/bash/funcs/export-json-section-vars.sh
# do_export_json_section_vars cnf/env/dev.env.json '.env.db'
# dependencies: 
# jq
#------------------------------------------------------------------------------
do_export_json_section_vars(){

   json_file="$1"
   shift 1;
   test -f "$json_file" || do_log "FATAL the json_file: $json_file does not exist !!! Nothing to do"
   test -f "$json_file" || exit 1

   section="$1"
   test -z "$section" && do_log "FATAL the section in do_export_json_section_vars is empty !!! Nothing to do !!!"
   test -z "$section" && exit 1
   shift 1;

   sensitiveness="${1:-}"
   shift 1;

   do_log "INFO exporting vars from cnf $json_file: "
   while read -r l ; do
      key=$(echo $l|cut -d':' -f1|tr a-z A-Z)
      val=$(echo $l|cut -d':' -f2)

      #val="${val/#\~/$HOME}" # for some reason does not work !!
      val=$(echo $val|perl -ne 's|~|'$HOME'|g;print')
      eval "$(echo -e 'export '$key=\"\"$val\"\")"

      # does not echo sensitive values
      if [[ "${sensitiveness}" == "" ]]; then
         do_log "INFO ${key}=${val}"
      else
         do_log "WARNING SENSITIVE ${key}=*****************"
      fi

   done < <(cat "$json_file"| jq -r "$section"'|keys_unsorted[] as $key|"\($key):\"\(.[$key])\""')

}
