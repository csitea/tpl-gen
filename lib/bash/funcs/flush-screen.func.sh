#!/bin/bash

#------------------------------------------------------------------------------
# usage example:
# source $PROJ_PATH/lib/bash/funcs/flush-screen.sh
# do_flush_screen
#------------------------------------------------------------------------------
do_flush_screen() {
  printf "\033[2J"
  printf "\033[0;0H"
}
