#!/bin/bash 

do_set_vars_on_suse(){
   export OS=suse
   export host_name="$(cat /proc/sys/kernel/hostname)"
}
