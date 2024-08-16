#!/bin/bash

do_set_vars_on_suse() {
  export OS=suse
  export HOST_NAME="$(cat /proc/sys/kernel/hostname)"
}
