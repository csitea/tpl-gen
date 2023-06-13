  .PHONY: do-generate-conf-for-%task% ## @-> run the provision step %task%
do-generate-conf-for-%task%: demand_var-ENV demand_var-ORG demand_var-APP
	docker exec -e ORG=$(ORG) -e APP=$(APP) -e ENV=$(ENV) -e TPL_SRC=${BASE_DIR}/$(ORG)/$(ORG)-$(APP)-infra-app -e CNF_SRC=${BASE_DIR}/$(ORG)/$(ORG)-$(APP)-infra-conf -e TGT=${BASE_DIR}/$(ORG)/$(ORG)-$(APP)-infra-conf $(ORG)-tpl-gen-tpl-gen-con /bin/bash -c 'cd ${BASE_DIR}/$(ORG)/tpl-gen && make yaml-to-json-file'
	docker exec -e ORG=$(ORG) -e APP=$(APP) -e ENV=$(ENV) -e TPL_SRC=${BASE_DIR}/$(ORG)/$(ORG)-$(APP)-infra-app -e CNF_SRC=${BASE_DIR}/$(ORG)/$(ORG)-$(APP)-infra-conf -e TGT=${BASE_DIR}/$(ORG)/$(ORG)-$(APP)-infra-conf $(ORG)-tpl-gen-tpl-gen-con /bin/bash -c 'cd ${BASE_DIR}/$(ORG)/tpl-gen && make tpl-gen'

