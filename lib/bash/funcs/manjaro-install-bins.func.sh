#!/bin/bash

do_manjaro_install_bins(){
	sudo pacman -S --noconfirm \
		"$@"
}
