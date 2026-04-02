#!/bin/bash

#------------------------------------------------------------------------------
# @description Set vars on ubuntu.
#------------------------------------------------------------------------------
do_set_vars_on_ubuntu() {

  # add any ubuntu specific vars settings here
  export HOST_NAME=$(hostname -s)
}
