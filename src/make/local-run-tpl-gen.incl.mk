# usage: include it in your Makefile by:
# include lib/make/tpl-gen.mk

.PHONY: tpl-gen ## @-> apply the environment cnf file into the templates
tpl-gen: demand_var-ENV demand_var-ORG demand_var-APP
	cd $(PYTHON_DIR) && poetry run main

.PHONY: do-tpl-gen ## @-> apply the environment cnf file into the templates on the tpl-gen container
do-tpl-gen: demand_var-ORG demand_var-ENV demand_var-APP
	docker exec -e ORG=$(ORG) -e APP=$(APP) -e ENV=$(ENV) -e STEP=$(STEP) -e TPL_SRC=$(TPL_SRC) -e CNF_SRC=$(CNF_SRC) -e TGT=$(TGT) $(ORG)-${PRODUCT}-tpl-gen-con make tpl-gen

.PHONY: run-tpl-gen ## @-> starts container, renders tpl-gen and destroyes container
run-tpl-gen: demand_var-ORG demand_var-ENV demand_var-APP
	$(call run-img,$(product),,${TPL_GEN_PORT}, make $(product))

.PHONY: yaml-to-json-file ## @-> render yaml file
yaml-to-json-file:
	cd $(PYTHON_DIR) && poetry run render

.PHONY: do-yaml-to-json-file ## @-> renders yaml file
do-yaml-to-json-file:
	docker exec -e TGT=$(TGT) -e SRC=$(SRC) $(ORG)-${PRODUCT}-tpl-gen-con make yaml-to-json-file

# eof file: src/make/local-setup-tasks.incl.mk
