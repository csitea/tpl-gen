# usage: include it in your Makefile by:
# include lib/make/tpl-gen.mk

.PHONY: tpl-gen ## @-> apply the environment cnf file into the templates
tpl-gen:
	cd ${TPG_PROJ_PATH} && source .venv/bin/activate && poetry run python3 tpl_gen/tpl_gen.py

.PHONY: convert-yaml-to-json ## @-> apply the environment cnf file into the templates
convert-yaml-to-json:
	cd ${TPG_PROJ_PATH} && source .venv/bin/activate && poetry run python3 tpl_gen/convert_yaml_to_json.py

# .PHONY: do-tpl-gen ## @-> apply the environment cnf file into the templates on the tpl-gen container
# do-tpl-gen:
# 	docker exec -e ORG=$(ORG) -e CNF_SRC=$(CNF_SRC) -e TPL_SRC=$(TPL_SRC) -e TGT=$(TGT) -e DATA_PATH=$(DATA_KEY_PATH) $(ORG)-${PROJ}-tpl-gen-con make ${PROJ}
# broken !!!

.PHONY: do-convert-yaml-to-json ## @-> apply the environment cnf file into the templates
do-convert-yaml-to-json:
	docker exec -e ORG=$(ORG) -e CNF_SRC=$(CNF_SRC) -e TPL_SRC=$(TPL_SRC) -e TGT=$(TGT) -e DATA_PATH=$(DATA_KEY_PATH) $(ORG)-${PROJ}-tpl-gen-con make convert-yaml-to-json


.PHONY: run-tpl-gen ## @-> starts container, renders tpl-gen and destroyes container
run-tpl-gen:
	$(call run-img,$(PROJ),,${TPL_GEN_PORT}, make $(PROJ))



# eof file: src/make/local-setup-tasks.incl.mk
