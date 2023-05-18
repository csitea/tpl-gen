#!/bin/bash
#
# create a kind of morphed clone module of the source module specified
# usage:
# to "morph" the run.sh into a foo-bar module do:
# SRC_MODULE=run.sh TGT_MODULE=foo-bar ./run -a do_morph_module
# to "morph" the foo-bar into a foo-baz module do:
# SRC_MODULE=foo-bar TGT_MODULE=foo-baz ./run -a do_morph_module
#
do_morph_module(){

  do_require_var SRC_MODULE ${SRC_MODULE:-} ; do_require_var TGT_MODULE ${TGT_MODULE:-} ;

  # echo produce the $BASE_DIR/$ORG_DIR/$SRC_MODULE.zip
  MODULE=$SRC_MODULE do_zip_me_as_module

  # mkdir -p $BASE_DIR/$ORG_DIR/$TGT_MODULE ; cd $BASE_DIR/$ORG_DIR/$TGT_MODULE
  test -d $BASE_DIR/$ORG_DIR/$TGT_MODULE && rm -r $BASE_DIR/$ORG_DIR/$TGT_MODULE
  mkdir -p $BASE_DIR/$ORG_DIR/$TGT_MODULE ; cd $_ ;
  sudo chmod 0775 src/bash/run/run.sh ; ln -sfn src/bash/run/run.sh run
  unzip -o $BASE_DIR/$ORG_DIR/$SRC_MODULE.zip -d .
  cp -v $PRODUCT_DIR/cnf/lst/$SRC_MODULE.include.lst $BASE_DIR/$ORG_DIR/$TGT_MODULE/cnf/lst/$TGT_MODULE.include.lst
  cp -v $PRODUCT_DIR/cnf/lst/$SRC_MODULE.exclude.lst $BASE_DIR/$ORG_DIR/$TGT_MODULE/cnf/lst/$TGT_MODULE.exclude.lst

  # Action !!! do search and replace src & tgt module into the new dir
  test $SRC_MODULE != 'run.sh' && STR_TO_SRCH=$SRC_MODULE STR_TO_REPL=$TGT_MODULE \
    DIR_TO_MORPH=$BASE_DIR/$ORG_DIR/$TGT_MODULE do_morph_dir

  SRC_MODULE_UNDERSCORED=$(echo ${SRC_MODULE:-}|perl -ne 's|-|_|g;print')
  TGT_MODULE_UNDERSCORED=$(echo ${TGT_MODULE:-}|perl -ne 's|-|_|g;print')
  do_log DEBUG SRC_MODULE_UNDERSCORED: $SRC_MODULE_UNDERSCORED
  do_log DEBUG TGT_MODULE_UNDERSCORED: $TGT_MODULE_UNDERSCORED
  sleep 1

  # Action !!! do search and replace src & tgt module into the new dir UNDERSCORED
  test $SRC_MODULE != 'run.sh' && STR_TO_SRCH=$SRC_MODULE_UNDERSCORED STR_TO_REPL=$TGT_MODULE_UNDERSCORED \
    DIR_TO_MORPH=$BASE_DIR/$ORG_DIR/$TGT_MODULE do_morph_dir

  cd $PRODUCT_DIR

  # TODO: !!!
  exit_code="0"
}
