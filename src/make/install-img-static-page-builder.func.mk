# src/make/clean-install-dockers.func.mk
# Keep all (clean and regular) docker install functions in here.

.PHONY: clean-install-static-page-builder  ## @-> setup the whole local static-page-builder environment for python no cache
clean-install-static-page-builder:
	$(call build-img,static-page-builder,--no-cache,4200)
	make start-static-page-builder

.PHONY: install-static-page-builder  ## @-> setup the whole local static-page-builder environment for python
install-static-page-builder:
	$(call build-img,static-page-builder,,4200)
	make start-static-page-builder

.PHONY: build-static-page-builder  ## @-> setup the whole local static-page-builder environment for python no cache
build-static-page-builder:
	$(call build-img,static-page-builder,--no-cache,4200)

.PHONY: start-static-page-builder  ## @-> setup the whole local static-page-builder environment for python no cache
start-static-page-builder:
	$(call start-img,static-page-builder,--no-cache,4200)

.PHONY: stop-static-page-builder
stop-static-page-builder:
	CONTAINER_NAME=static-page-builder
	$(call stop-and-remove-docker-container)
