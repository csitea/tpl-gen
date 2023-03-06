# Makefile
# usage: run the "make" command in the root, than make <<cmd>>...
include $(wildcard lib/make/*.mk)
include $(wildcard src/make/*.mk)

# set ALL of your global variables here, setting vars in functions outsite the funcs does not work
BUILD_NUMBER := $(if $(BUILD_NUMBER),$(BUILD_NUMBER),"0")
COMMIT_SHA := $(if $(COMMIT_SHA),$(COMMIT_SHA),$$(git rev-parse --short HEAD))
COMMIT_MESSAGE := $(if $(COMMIT_MESSAGE),$(COMMIT_MESSAGE),$$(git log -1  --pretty='%s'))
DOCKER_BUILDKIT := $(or 0,$(shell echo $$DOCKER_BUILDKIT))


SHELL = bash
PRODUCT := $(shell basename $$PWD)
product := $(shell echo `basename $$PWD`|tr '[:upper:]' '[:lower:]')
PROCESSOR_ARCHITECTURE := $(shell uname -m)
ORG_DIR := $(shell basename $(dir $(abspath $(dir $$PWD))))
org_dir := $(shell echo ${ORG_DIR}|tr '[:upper:]' '[:lower:]')
BASE_DIR := $(shell cd ../../ && echo $$PWD)
PRODUCT_DIR := $(shell echo $$PWD)


.PHONY: install ## @-> install both the tpl-gen and the tpl-gen containers
install:
	@clear
	make clean-install-tpl-gen




