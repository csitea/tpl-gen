#!/bin/bash

function resolve_dirname() {
    local path_in_the_base_dir="$1"
    # OBS !!! this resolves the directory which is holding
    perl -e 'use File::Basename; use Cwd "abs_path"; print dirname(abs_path(@ARGV[0]));' -- "$path_in_the_base_dir"
}

