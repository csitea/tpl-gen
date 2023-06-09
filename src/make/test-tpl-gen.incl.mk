# usage: include it in your Makefile by:
# include lib/make/tpl-gen.mk

# .PHONY: tpl-gen ## @-> apply the environment cnf file into the templates
# tpl-gen: demand_var-ENV demand_var-ORG demand_var-APP
# 	cd $(PYTHON_DIR) && poetry test start

# .PHONY: do-tpl-gen ## @-> apply the environment cnf file into the templates on the tpl-gen container
# do-tpl-gen: demand_var-ORG demand_var-ENV demand_var-APP
# 	docker exec -e TPL_SRC=$(TPL_SRC) -e CNF_SRC=$(CNF_SRC) -e ORG=$(ORG) -e APP=$(APP) -e ENV=$(ENV) -e TGT=$(TGT) -e SRC=$(SRC) $(ORG)-${PRODUCT}-tpl-gen-con make ${PRODUCT}

.PHONY: do-test-tpl-gen ## @-> starts container, renders tpl-gen and destroyes container
do-test-tpl-gen: demand_var-ORG
	docker exec $(ORG)-tpl-gen-tpl-gen-con /bin/bash -c "cd $(PRODUCT_DIR)/src/python/tpl-gen && poetry run pytest -v"


# .PHONY: test-yaml-to-json-file ## @-> render yaml file
# test-yaml-to-json-file:
# 	cd $(PYTHON_DIR) && poetry test render

# .PHONY: do-yaml-to-json-file ## @-> renders yaml file
# do-yaml-to-json-file:
# 	docker exec -e TGT=$(TGT) -e SRC=$(SRC) $(ORG)-${PRODUCT}-tpl-gen-con make yaml-to-json-file

# eof file: src/make/local-setup-tasks.incl.mk
