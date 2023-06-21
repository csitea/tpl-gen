# src/make/clean-install-dockers.func.mk
# Keep all (clean and regular) docker install functions in here.

.PHONY: clean-install-tpl-gen  ## @-> setup the whole local tpl-gen environment for python no cache
clean-install-tpl-gen:
	$(call build-img,$(product),--no-cache,${TPL_GEN_PORT})
	make start-tpl-gen

.PHONY: install-tpl-gen  ## @-> setup the whole local tpl-gen environment for python
install-tpl-gen:
	$(call build-img,$(product),,${TPL_GEN_PORT})
	make start-tpl-gen

.PHONY: build-tpl-gen  ## @-> setup the whole local tpl-gen environment for python no cache
build-tpl-gen:
	$(call build-img,$(product),--no-cache,${TPL_GEN_PORT})

.PHONY: start-tpl-gen  ## @-> setup the whole local tpl-gen environment for python no cache
start-tpl-gen:
	$(call start-img,$(product),--no-cache,${TPL_GEN_PORT})

.PHONY: stop-tpl-gen
stop-tpl-gen:
	CONTAINER_NAME=$(PRODUCT)
	$(call stop-and-remove-docker-container)
