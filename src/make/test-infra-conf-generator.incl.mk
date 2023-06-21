.PHONY: do-test-tpl-gen ## @-> starts container, renders tpl-gen and destroyes container
do-test-tpl-gen: demand_var-ORG
	docker exec $(ORG)-tpl-gen-tpl-gen-con /bin/bash -c "cd $(PRODUCT_DIR)/src/python/tpl-gen && poetry run pytest -v"


