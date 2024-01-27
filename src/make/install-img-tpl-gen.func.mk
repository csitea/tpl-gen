# src/make/clean-install-dockers.func.mk
# Keep all (clean and regular) docker install functions in here.

.PHONY: do-setup-tpl-gen  ## @-> setup the whole local tpl-gen environment for python no cache
do-setup-tpl-gen:
	$(call build-img,$(product),--no-cache,${TPL_GEN_PORT})
	make do-start-tpl-gen

.PHONY: do-setup-tpl-gen-cached  ## @-> setup the whole local tpl-gen environment for python
do-setup-tpl-gen-cached:
	$(call build-img,$(product),,${TPL_GEN_PORT})
	make do-start-tpl-gen

.PHONY: do-build-tpl-gen  ## @-> setup the whole local tpl-gen environment for python no cache
do-build-tpl-gen:
	$(call build-img,$(product),--no-cache,${TPL_GEN_PORT})

.PHONY: do-start-tpl-gen  ## @-> only start the containers
do-start-tpl-gen:
	$(call start-img,$(product),--no-cache,${TPL_GEN_PORT})

.PHONY: do-stop-tpl-gen
do-stop-tpl-gen:
	CONTAINER_NAME=$(PRODUCT)
	$(call stop-and-remove-docker-container)
