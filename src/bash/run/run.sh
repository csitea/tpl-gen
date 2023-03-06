#!/usr/bin/env bash
# install by:
# wget https://github.com/csitea/run.sh/archive/refs/tags/current.zip && unzip -o current.zip -d . && mv -v run.sh-current my-app
# usage: ./run --help

main(){
  do_flush_screen
  do_set_vars "$@"  # is inside, unless --help flag is present
  ts=$(date "+%Y%m%d_%H%M%S")
  main_log_dir=~/var/log/$PRODUCT/; mkdir -p $main_log_dir
  main_exec "$@" \
     > >(tee $main_log_dir/$RUN_UNIT.$ts.out.log) \
    2> >(tee $main_log_dir/$RUN_UNIT.$ts.err.log)
}


main_exec(){
   do_resolve_os
   do_check_install_min_req_bins
   do_load_functions

   test -z ${actions:-} && actions=' do_print_usage '
   do_run_actions "$actions"
   do_finalize

}


#------------------------------------------------------------------------------
# the "reflection" func - identify the the funcs per file
#------------------------------------------------------------------------------
get_function_list () {
   env -i PATH=/bin:/usr/bin:/usr/local/bin bash --noprofile --norc -c '
      source "'"$1"'"
      typeset -f |
      grep '\''^[^{} ].* () $'\'' |
      awk "{print \$1}" |
      while read -r fnc_name; do
         type "$fnc_name" | head -n 1 | grep -q "is a function$" || continue
            echo "$fnc_name"
            done
            '
}


do_read_cmd_args() {

   while [[ $# -gt 0 ]]; do
      case "$1" in
         -a|--actions) shift && actions="${actions:-}${1:-} " && shift ;;
         -h|--help) actions=' do_print_usage ' && ENV='dev' && shift ;;
         *) echo FATAL unknown "cmd arg: '$1' - invalid cmd arg, probably a typo !!!" && shift && exit 1
    esac
  done
   shift $((OPTIND -1))

}


do_run_actions(){
   actions=$1
   actions_found=0
      cd $PRODUCT_DIR
      actions="$(echo -e "${actions}"|sed -e 's/^[[:space:]]*//')"  #or how-to trim leading space
      run_funcs=''
      while read -d ' ' arg_action ; do
         while read -r fnc_file ; do
            #debug func fnc_file:$fnc_file
            while read -r fnc_name ; do
               #debug fnc_name:$fnc_name
               action_name=`echo $(basename $fnc_file)|sed -e 's/.func.sh//g'`
               action_name=`echo do_$action_name|sed -e 's/-/_/g'`
               # debug  action_name: $action_name
               test "$action_name" != "$arg_action" && continue
               source $fnc_file
               actions_found=$((actions_found+1))
               test "$action_name" == "$arg_action" && run_funcs="$(echo -e "${run_funcs}\n$fnc_name")"
            done< <(get_function_list "$fnc_file")
         done < <(find "src/bash/run/" "lib/bash/funcs" -type f -name '*.func.sh'|sort)

      done < <(echo "$actions")

   echo ${actions} ${actions_found}
   test $actions_found -eq 0 && {
      do_log "FATAL action(s) requested: \"$actions\" NOT found !!!"
      do_log "FATAL 1. check the spelling of your action"
      do_log "FATAL 2. check the available actions by: ENV=lde ./run --help"
      do_log "FATAL the run failed !"
      exit 1
   }

   run_funcs="$(echo -e "${run_funcs}"|sed -e 's/^[[:space:]]*//;/^$/d')"
   while read -r run_func ; do
      cd $PRODUCT_DIR
      do_log "INFO START ::: running action :: $run_func"
      echo $run_func
      $run_func
      if [[ "${exit_code:-}" != "0" ]]; then
        msg="FATAL failed to run action: $run_func !!!"
        do_log $msg
        exit $exit_code
      fi
      do_log "INFO STOP ::: running function :: $run_func"
   done < <(echo "$run_funcs")

}


do_flush_screen(){
   printf "\033[2J";printf "\033[0;0H"
}


#------------------------------------------------------------------------------
# purpose: to pass msgs and print them to a log file and terminal
#  - with datetime
#  - the type of msg - INFO, ERROR, DEBUG, WARNING
# usage:
# do_log "INFO some info message"
# do_log "ERROR some error message"
# do_log "DEBUG some debug message"
# do_log "WARNING some warning message"
# depts:
#  - PRODUCT_DIR - the root dir of the sfw project
#  - PRODUCT - the name of the software project dir
#  - host_name - the short hostname of the host / container running on
#------------------------------------------------------------------------------
do_log(){

  print_ok() {
      GREEN_COLOR="\033[0;32m"
      DEFAULT="\033[0m"
      echo -e "${GREEN_COLOR} ✔ [OK] ${1:-} ${DEFAULT}"
  }

  print_warning() {
      YELLOW_COLOR="\033[33m"
      DEFAULT="\033[0m"
      echo -e "${YELLOW_COLOR} ⚠ ${1:-} ${DEFAULT}"
  }

   print_info() {
      BLUE_COLOR="\033[0;34m"
      DEFAULT="\033[0m"
      echo -e "${BLUE_COLOR} ℹ ${1:-} ${DEFAULT}"
  }

  print_fail() {
      RED_COLOR="\033[0;31m"
      DEFAULT="\033[0m"
      echo -e "${RED_COLOR} ❌ [NOK] ${1:-}${DEFAULT}"
  }

  type_of_msg=$(echo $*|cut -d" " -f1)
  msg="$(echo $*|cut -d" " -f2-)"
  log_dir="${PRODUCT_DIR:-}/dat/log/bash" ; mkdir -p $log_dir
  log_file="$log_dir/${PRODUCT:-}."$(date "+%Y%m%d")'.log'
  msg=" [$type_of_msg] `date "+%Y-%m-%d %H:%M:%S %Z"` [${PRODUCT:-}][@${host_name:-}] [$$] $msg "
  case "$type_of_msg" in
    'FATAL') print_fail "$msg" | tee -a $log_file ;;
    'ERROR') print_fail "$msg" | tee -a $log_file ;;
    'WARNING') print_warning "$msg" | tee -a $log_file ;;
    'INFO') print_info "$msg" | tee -a $log_file ;;
    'OK') print_ok "$msg" | tee -a $log_file ;;
    *) echo "$msg" | tee -a $log_file ;;
  esac

}


do_check_install_min_req_bins(){

   while read -r f; do source $f; done < <(find $PRODUCT_DIR/lib/bash/funcs/ -type f)

   which perl > /dev/null 2>&1 || {
      run_os_func install_bins perl
   }
   which jq > /dev/null 2>&1 || {
      run_os_func install_bins jq
   }
   which make > /dev/null 2>&1 || {
      # this will not work properly - google how-to install make on <<my-operating-system>>
      run_os_func install_bins make
   }
}


do_set_vars(){
   set -u -o pipefail
   do_read_cmd_args "$@"
   export host_name="$(hostname -s)"
   export exit_code=1 # assume failure for each action, enforce return code usage
   unit_run_dir=$(perl -e 'use File::Basename; use Cwd "abs_path"; print dirname(abs_path(@ARGV[0]));' -- "$0")
   export RUN_UNIT=$(cd $unit_run_dir ; basename `pwd` .sh)
   export PRODUCT_DIR=$(cd $unit_run_dir/../../.. ; echo `pwd`)
   export ORG_DIR=$(echo $PRODUCT_DIR|xargs dirname | xargs basename)
   export BASE_DIR=$(cd $unit_run_dir/../../../../.. && echo `pwd`)
   do_ensure_logical_link
   export PRODUCT=$(basename $PRODUCT_DIR)
   ENV="${ENV:=lde}" # <- remove this one IF you want to enforce the caller to provide the ENV var
   cd $PRODUCT_DIR
   # workaround for github actions running on docker
   test -z ${GROUP:-} && export GROUP=$(id -gn)
   test -z ${GROUP:-} && export GROUP=$(ps -o group,supgrp $$|tail -n 1|awk '{print $1}')
   test -z ${USER:-} && export USER=$(id -un)
   test -z ${UID:-} && export UID=$(id -u)
   test -z ${GID:-} && export GID=$(id -g)
}



# ensure that the <<PRODUCT_DIR>>/run is a logical link and not a regular file
# if the run.sh is not under the src/bash/run dir terrible things happen ...
# this one is especially problematic in Dockerfile's ADD command
do_ensure_logical_link(){

   if [[ "$unit_run_dir" != */src/bash/run ]]; then
      echo "
         you probably unzipped into a new app/tool and forgot to run the following cmd:
         rm -v run; ln -sfn src/bash/run/run.sh run
         so that ls -al run should look like:
         lrwx------  1 osuser  osgroup 2022-01-01 20:40 run -> src/bash/run/run.sh
         !!!
         or you are running within a Dockerfile and calling directly PRODUCT_DIR/run
         which MIGHT work, but better to call PRODUCT_DIR/src/bash/run/run.sh
      "
      export PRODUCT_DIR=$(cd $unit_run_dir ; echo `pwd`)
      export ORG_DIR=$(echo $PRODUCT_DIR|xargs dirname | xargs basename)
      export BASE_DIR=$(cd $unit_run_dir/../.. && echo `pwd`)
      echo PRODUCT_DIR: $PRODUCT_DIR
      echo ORG_DIR: $ORG_DIR
      echo BASE_DIR: $BASE_DIR
   fi

}


do_finalize(){

  do_log "OK $RUN_UNIT's run completed"
  cat << EOF_FIN_MSG
  :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
         $RUN_UNIT run completed
  :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
EOF_FIN_MSG
  exit $exit_code
}


do_load_functions(){
    while read -r f; do source $f; done < <(ls -1 $PRODUCT_DIR/lib/bash/funcs/*.func.sh)
    while read -r f; do source $f; done < <(ls -1 $PRODUCT_DIR/src/bash/run/*.func.sh)
 }


run_os_func(){
   func_to_run=$1 ; shift ;

   if [[ -z "$OS" ]]; then
      echo "your OS distro is not supported!!!"
      exit 1
   else
      "do_"$OS"_""$func_to_run" "$@"
   fi

}


do_resolve_os(){
   if [[ $(uname -s) == *"Linux"* ]]; then
       distro=$(cat /etc/os-release|egrep '^ID='|cut -d= -f2 | tr -d '"')
       if [[ $distro == 'ubuntu' ]] || [[ $distro == "pop" ]]; then
         export OS='ubuntu'
       elif [[ $distro == "alpine" ]]; then
         export OS='alpine'
       elif [[ $distro == 'manjaro' ]]; then
         export OS='manjaro'
       elif [[ "$distro" == "opensuse-tumbleweed" ]]; then
         export OS="suse"
         echo "your Linux distro has limited support !!!"
       else
          echo "your Linux distro is not supported !!!"
          exit 1
       fi
   elif [[ $(uname -s) == *"Darwin"* ]]; then
         export OS=mac
   else
      echo "your OS distro is not supported !!!"
      exit 1
   fi
   source "$PRODUCT_DIR"'/lib/bash/funcs/set-vars-on-'"$OS"'.func.sh' ; 'do_set_vars_on_'"$OS"
}

main "$@"
