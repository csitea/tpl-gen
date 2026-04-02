#!/bin/bash

#------------------------------------------------------------------------------
# @description Set vars on mac.
#------------------------------------------------------------------------------
do_set_vars_on_mac() {

  # add any mac OS specific vars settings here
  export HOST_NAME=$(hostname -s)
}
