# usage: include it in your Makefile by:
# include lib/make/tpl-gen.mk

.PHONY: tpl-gen ## @-> apply the environment cnf file into the templates
tpl-gen:
	cd /opt/$(ORG)/tpl-gen/src/python/tpl-gen && source .venv/bin/activate && poetry run python3 tpl_gen/tpl_gen.py

.PHONY: convert-yaml-to-json ## @-> apply the environment cnf file into the templates
convert-yaml-to-json:
	cd /opt/$(ORG)/tpl-gen/src/python/tpl-gen && source .venv/bin/activate && poetry run python3 tpl_gen/convert_yaml_to_json.py

.PHONY: do-tpl-gen ## @-> apply the environment cnf file into the templates on the tpl-gen container
do-tpl-gen:
	docker exec -e ORG=$(ORG) -e CNF_SRC=$(CNF_SRC)  -e TPL_SRC=$(TPL_SRC) -e TGT=$(TGT) -e DATA_PATH=$(DATA_KEY_PATH) $(ORG)-${PRODUCT}-tpl-gen-con make ${PRODUCT}

.PHONY: do-convert-yaml-to-json ## @-> apply the environment cnf file into the templates on the tpl-gen container
do-convert-yaml-to-json:
	docker exec -e ORG=$(ORG) -e CNF_SRC=$(CNF_SRC)  -e TPL_SRC=$(TPL_SRC) -e TGT=$(TGT) -e DATA_PATH=$(DATA_KEY_PATH) $(ORG)-${PRODUCT}-tpl-gen-con make convert-yaml-to-json


.PHONY: run-tpl-gen ## @-> starts container, renders tpl-gen and destroyes container
run-tpl-gen:
	$(call run-img,$(product),,${TPL_GEN_PORT}, make $(product))



# eof file: src/make/local-setup-tasks.incl.mk
