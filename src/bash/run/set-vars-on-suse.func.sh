#!/bin/bash

do_set_vars_on_suse() {

  # add any Suse Linux specific vars settings here
  export HOST_NAME="$(cat /proc/sys/kernel/hostname)"
}
