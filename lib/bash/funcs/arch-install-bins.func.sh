#!/bin/bash

do_arch_install_bins(){
	sudo pacman -S --noconfirm \
		"$@"
}
