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
define build-img
	@clear

	$(eval NO_CACHE=${2})
	$(eval PORT_COMMAND=-p ${3}:${3})

	# these variables bellow cannot be moved to root Makefile
	# since they are arguments of this function.
	NO_CACHE=$(or $(2),$(2))
	PORT_COMMAND=$(or $(3),$(3))
	$(eval IMAGE_NAME=$(ROOT_DOCKER_NAME)-$(1)-img)
	$(eval CONTAINER_NAME=$(ROOT_DOCKER_NAME)-$(1)-con)
	$(eval PORT_COMMAND=`echo "$(PORT_COMMAND)"|perl -ne 's/-p ://g;print'`)

	@echo -e "\n\n START ::: running the docker build by:"

	@DOCKER_BUILDKIT=${DOCKER_BUILDKIT} docker build . -t $(IMAGE_NAME) $(NO_CACHE) \
		--build-arg UID=${UID} \
		--build-arg GID=${GID} \
		--build-arg BASE_PATH=${BASE_PATH} \
		--build-arg ORG_DIR=${ORG_DIR} \
		--build-arg PROJ=${PROJ} \
		--build-arg PROJ_PATH=${PROJ_PATH} \
		--build-arg APPUSR=${APPUSR} \
		--build-arg APPGRP=${APPGRP} \
		--build-arg HOME_PROJ_PATH=${HOME_PROJ_PATH} \
		--build-arg MOUNT_WORK_DIR=${MOUNT_WORK_DIR} \
		--build-arg DOCKER_HOME=${DOCKER_HOME} \
		--build-arg RUN_SCRIPT=${RUN_SCRIPT} \
		--build-arg DOCKER_INIT_SCRIPT=${DOCKER_INIT_SCRIPT} \
		-f src/docker/$(1)/Dockerfile.x86_64
	@echo -e "\n\n STOP  ::: running the docker build."
	@echo -e "\n\n"
	@sleep 1

	# only remove after build successfully, to avoid leaving user without
	# a working container not a built image
	$(call stop-and-remove-docker-container,$1)

endef

# 	@clear
define start-img


	$(eval NO_CACHE=${2})
	$(eval PORT_COMMAND=-p ${3}:${3})

	# these variables bellow cannot be moved to root Makefile
	# since they are arguments of this function.
	NO_CACHE=$(or $(2),$(2))
	PORT_COMMAND=$(or $(3),$(3))
	$(eval IMAGE_NAME=$(ROOT_DOCKER_NAME)-$(1)-img)
	$(eval CONTAINER_NAME=$(ROOT_DOCKER_NAME)-$(1)-con)
	$(eval PORT_COMMAND=`echo "$(PORT_COMMAND)"|perl -ne 's/-p ://g;print'`)

	@echo -e "\n\n You MIGHT have even up to 1min for the container to start properly !!!"
	@echo -e "\n\n START ::: spawning the docker container by:"

	@DOCKER_BUILDKIT=${DOCKER_BUILDKIT} docker run -it -d --restart=always $(PORT_COMMAND) \
		-v $(MOUNT_WORK_DIR):$(MOUNT_WORK_DIR) \
		-v $(HOST_AWS_DIR):$(DOCKER_AWS_DIR) \
		-v $(HOST_SSH_DIR):$(DOCKER_SSH_DIR) \
		-v $(HOST_KUBE_DIR):$(DOCKER_KUBE_DIR) \
		--name $(CONTAINER_NAME) $(IMAGE_NAME) ;
	@echo -e "\nSTOP  ::: spawnning the docker container \n"

	@echo -e "before attaching run: docker logs $(CONTAINER_NAME) \| tail -n 10"
	@echo -e "to attach run: \ndocker exec -it $(CONTAINER_NAME) /bin/bash"
	@echo -e "to get help run: \ndocker exec -it $(CONTAINER_NAME) ./run --help"
	@echo -e "to suppress docker build logging: export DOCKER_BUILDKIT=0"
	@echo -e "\n\n"
endef

define run-img

	@clear

	$(eval NO_CACHE=${2})
	$(eval PORT_COMMAND=-p ${3}:${3})
	$(eval COMMAND=${4})

	# these variables bellow cannot be moved to root Makefile
	# since they are arguments of this function.
	NO_CACHE=$(or $(2),$(2))
	PORT_COMMAND=$(or $(3),$(3))
	$(eval IMAGE_NAME=$(ROOT_DOCKER_NAME)-$(1)-img)
	$(eval CONTAINER_NAME=$(ROOT_DOCKER_NAME)-$(1)-con)
	$(eval PORT_COMMAND=`echo "$(PORT_COMMAND)"|perl -ne 's/-p ://g;print'`)

	DOCKER_BUILDKIT=${DOCKER_BUILDKIT} docker run --rm $(PORT_COMMAND) \
		-v $(MOUNT_WORK_DIR):$(MOUNT_WORK_DIR) \
		-v $(HOST_AWS_DIR):$(DOCKER_AWS_DIR) \
		-v $(HOST_SSH_DIR):$(DOCKER_SSH_DIR) \
		-v $(HOST_KUBE_DIR):$(DOCKER_KUBE_DIR) \
		-e CNF_SRC=$(CNF_SRC)  -e TPL_SRC=$(TPL_SRC) -e TGT=$(TGT) \
		--name $(CONTAINER_NAME) $(IMAGE_NAME) $(COMMAND) ;
endef


define stop-and-remove-docker-container
	-@echo "Stoping & Removing the $(CONTAINER_NAME) IF it is running"
	-@docker container stop $(shell docker ps -aqf "name=${CONTAINER_NAME}") 2> /dev/null
	-@docker container rm $(shell docker ps -aqf "name=${CONTAINER_NAME}") 2> /dev/null
endef

