#!/bin/bash

do_suse_install_bins(){
	zypper install -y \
		"$@"
}
