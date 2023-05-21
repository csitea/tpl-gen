# Makefile
# usage: run the "make" command in the root, than make <<cmd>>...
include $(wildcard lib/make/*.mk)
include $(wildcard src/make/*.mk)

# set ALL of your global variables here, setting vars in functions outsite the funcs does not work
BUILD_NUMBER := $(if $(BUILD_NUMBER),$(BUILD_NUMBER),"0")
COMMIT_SHA := $(if $(COMMIT_SHA),$(COMMIT_SHA),$$(git rev-parse --short HEAD))
COMMIT_MESSAGE := $(if $(COMMIT_MESSAGE),$(COMMIT_MESSAGE),$$(git log -1  --pretty='%s'))
DOCKER_BUILDKIT := $(or 0,$(shell echo $$DOCKER_BUILDKIT))



SHELL := /bin/bash
.SHELLFLAGS := -c

PRODUCT := $(shell basename $$PWD)
product := $(shell echo `basename $$PWD`|tr '[:upper:]' '[:lower:]')
PROCESSOR_ARCHITECTURE := $(shell uname -m)
ORG_DIR := $(shell basename $(dir $(abspath $(dir $$PWD))))
org_dir := $(shell echo `basename $(dir $(abspath $(dir $$PWD)))|tr '[:upper:]' '[:lower:]'`)
BASE_DIR := $(shell source $$PWD/lib/bash/funcs/resolve-dirname.func.sh ; resolve_dirname $$PWD"/../" )
PRODUCT_DIR := $$PWD
PYTHON_DIR := $(PRODUCT_DIR)/src/python/$(product)

APPUSR := appusr
APPGRP := appgrp
ROOT_DOCKER_NAME = ${product}
MOUNT_WORK_DIR := $(BASE_DIR)/$(ORG_DIR)
HOST_AWS_DIR := $(HOME)/.aws
DOCKER_AWS_DIR := /home/${APPUSR}/.aws
HOST_SSH_DIR := $(HOME)/.ssh
DOCKER_SSH_DIR := /home/${APPUSR}/.ssh
HOST_KUBE_DIR := $(HOME)/.kube
DOCKER_KUBE_DIR := /home/${APPUSR}/.kube

# dockerfile variables
PRODUCT_DIR := $(BASE_DIR)/$(ORG_DIR)/$(PRODUCT)
HOME_PRODUCT_DIR := "/home/$(APPUSR)$(BASE_DIR)/$(ORG_DIR)/$(PRODUCT)"
DOCKER_HOME := /home/$(APPUSR)
DOCKER_SHELL := /bin/$(SHELL)
RUN_SCRIPT := $(HOME_PRODUCT_DIR)/run
DOCKER_INIT_SCRIPT := $(HOME_PRODUCT_DIR)/src/bash/run/docker-init-$(PRODUCT).sh

UID := $(shell id -u)
GID := $(shell id -g)

TPL_GEN_PORT=


.PHONY: install ## @-> install both the tf-runner and the tpl-gen containers
install:
	@clear
	make clean-install-$(product)


