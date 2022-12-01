# Makefile
# usage: run the "make" command in the root, than make <<cmd>>...
include $(wildcard lib/make/*.mk)
include $(wildcard src/make/*.mk)

# get those from the env when in azure, otherwise get locally
BUILD_NUMBER := $(if $(BUILD_NUMBER),$(BUILD_NUMBER),"0")
COMMIT_SHA := $(if $(COMMIT_SHA),$(COMMIT_SHA),$$(git rev-parse --short HEAD))
COMMIT_MESSAGE := $(if $(COMMIT_MESSAGE),$(COMMIT_MESSAGE),$$(git log -1  --pretty='%s'))

SHELL = bash
PRODUCT := $(shell basename $$PWD)
PP_NAME := $(shell cd ../../ && basename $$PWD)
ORG_DIR := $(shell basename $(dir $(abspath $(dir $$PWD))))
PRODUCT_DIR := $(HOME)/$(PP_NAME)/$(PRODUCT)
PROCESSOR_ARCHITECTURE := $(shell uname -m)
product := $(shell echo `basename $$PWD`|tr '[:upper:]' '[:lower:]')
ORG := $(shell basename $(dir $(abspath $(dir $$PWD))))


.PHONY: install ## @-> install both the devops-ter and the tpl-gen containers
install:
	@clear 
	make clean-install-tpl-gen

