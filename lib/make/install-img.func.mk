# usage: include it in your Makefile
# include lib/make/install-img.func.mk
# call it by:
# install-web-node:
# 	$(call install-img,web-node,--no-cache,80)
# install-api-node:
# 	$(call install-img,api-node,,,linux_user)

# do not set variables here !!! 

include lib/make/demand-var.func.mk


# iss-2209082055 https://pythonspeed.com/articles/docker-build-problems-mac/
define install-img
	@clear
	$(call stop-and-remove-docker-container,$1)

	$(eval NO_CACHE=${2})
	$(eval PORT_COMMAND=-p ${3}:${3})

	NO_CACHE=$(or $(2),$(2))
	PORT_COMMAND=$(or $(3),$(3))
	APPUSR=$(eval APPUSR=`echo appusr`)
	APPUSR=$(or $(4),$(APPUSR))
	$(eval PORT_COMMAND=`echo "$(PORT_COMMAND)"|perl -ne 's/-p ://g;print'`)
	


	@echo -e "\n\n START ::: running the docker build by:"
	@echo DOCKER_BUILDKIT=${DOCKER_BUILDKIT} docker build . -t ${org_dir}-${product}-$(1)-img $(NO_CACHE) \
		--build-arg UID=$(shell id -u) \
		--build-arg GID=$(shell id -g) \
		--build-arg BASE_DIR=${BASE_DIR} \
		--build-arg ORG_DIR=${ORG_DIR} \
		--build-arg PRODUCT=${PRODUCT} \
		-f src/docker/$(1)/Dockerfile.${PROCESSOR_ARCHITECTURE}
	@echo -e "\n\n"
	@sleep 3


	DOCKER_BUILDKIT=${DOCKER_BUILDKIT} docker build . -t ${org_dir}-${product}-$(1)-img $(NO_CACHE) \
		--build-arg UID=$(shell id -u) \
		--build-arg GID=$(shell id -g) \
		--build-arg BASE_DIR=${BASE_DIR} \
		--build-arg ORG_DIR=${ORG_DIR} \
		--build-arg PRODUCT=${PRODUCT} \
		-f src/docker/$(1)/Dockerfile.${PROCESSOR_ARCHITECTURE}
	@echo -e "\n\n STOP  ::: running the docker build."
	@echo -e "\n\n"
	@sleep 1

	@echo -e "\n\n You MIGHT have even up to 1min for the container to start properly !!!"
	@echo -e "\n\n START ::: spawning the docker container by:"
	@echo docker run -it -d --restart=always $(PORT_COMMAND) \
		-v $(BASE_DIR)/$(ORG_DIR):$(BASE_DIR)/$(ORG_DIR) \
		-v $$HOME/.aws:/home/$(APPUSR)/.aws \
		-v $$HOME/.ssh:/home/$(APPUSR)/.ssh \
		-v $$HOME/.kube:/home/$(APPUSR)/.kube \
		--name ${org_dir}-${product}-$(1)-con ${org_dir}-${product}-${1}-img ;
	@echo -e "\n\n"
	@sleep 1


	DOCKER_BUILDKIT=${DOCKER_BUILDKIT} docker run -it -d --restart=always $(PORT_COMMAND) \
		-v $(BASE_DIR)/$(ORG_DIR):$(BASE_DIR)/$(ORG_DIR) \
		-v $$HOME/.aws:/home/${APPUSR}/.aws \
		-v $$HOME/.ssh:/home/${APPUSR}/.ssh \
		-v $$HOME/.kube:/home/${APPUSR}/.kube \
		--name ${org_dir}-${product}-$(1)-con ${org_dir}-${product}-${1}-img ;
	@echo -e "\nSTOP  ::: spawnning the docker container \n"


	@echo -e "before attaching run: docker logs ${org_dir}-${product}-${1}-con \| tail -n 10"
	@echo -e "to attach run: \ndocker exec -it ${org_dir}-${product}-${1}-con /bin/bash"
	@echo -e "to get help run: \ndocker exec -it ${org_dir}-${product}-${1}-con ./run --help"
	@echo -e "to suppress docker build logging: export DOCKER_BUILDKIT=0"
	@echo -e "\n\n"
endef


define stop-and-remove-docker-container
	-@echo "STOPPing & REMOVing the ${org_dir}-${product}-${1}-con IF it is running"
	-@docker container stop $(shell docker ps -aqf "name=${org_dir}-${product}-${1}-con") 2> /dev/null
	-@docker container rm $(shell docker ps -aqf "name=${org_dir}-${product}-${1}-con") 2> /dev/null
endef

