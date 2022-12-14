# usage: include it in your Makefile by:
# include lib/make/tpl-gen.mk

.PHONY: tpl-gen ## @-> apply the environment cnf file into the templates
tpl-gen: demand_var-ENV demand_var-ORG demand_var-APP
	cd /opt/$(ORG_DIR)/$(PRODUCT)/src/python/tpl-gen && poetry run start

.PHONY: do-tpl-gen ## @-> apply the environment cnf file into the templates on the tpl-gen container
do-tpl-gen: demand_var-ORG demand_var-ENV demand_var-APP
	docker exec -e APP=$(APP) -e ENV=$(ENV) -e ORG=$(ORG) -e TGT=$(TGT) -e SRC=$(SRC) ${PRODUCT}-tpl-gen-con make tpl-gen

.PHONY: render-yaml ## @-> render yaml file
render-yaml: 
	cd /opt/$(ORG_DIR)/$(PRODUCT)/src/python/tpl-gen && poetry run render

.PHONY: do-render-yaml ## @-> renders yaml file
do-render-yaml:
	docker exec -e TGT=$(TGT) -e SRC=$(SRC) ${PRODUCT}-tpl-gen-con make render-yaml

# eof file: src/make/local-setup-tasks.incl.mk
