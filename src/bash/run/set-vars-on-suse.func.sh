#!/bin/bash

do_set_vars_on_suse(){

   # add any Suse Linux specific vars settings here 
   export host_name="$(cat /proc/sys/kernel/hostname)"
}
