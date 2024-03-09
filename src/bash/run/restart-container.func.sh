#!/bin/bash

do_restart_container() {

  PROJ=$(echo $(basename $PROJ_PATH) | tr '[:upper:]' '[:lower:]')
  MODULE=${MODULE:-$PROJ}

  docker container stop $(docker ps -aqf "name=${org_path}-${PROJ}-${PROJ}-con") 2>/dev/null
  docker container rm $(docker ps -aqf "name=${org_path}-${PROJ}-${PROJ}-con") 2>/dev/null

  PORT_COMMAND=""
  docker container ls

  DOCKER_BUILDKIT=1 docker run -it -d --restart=always ${PORT_COMMAND:-} \
    -v ${BASE_PATH}/${ORG_PATH}:${BASE_PATH}/${ORG_PATH} \
    -v $HOME/.aws:/home/${USER}/.aws \
    -v $HOME/.ssh:/home/${USER}/.ssh \
    -v $HOME/.kube:/home/${USER}/.kube \
    --name ${PROJ}-${MODULE}-con ${org_path}-${PROJ}-${MODULE}-img
  echo -e "\nSTOP  ::: spawnning the docker container \n"

  echo -e "to get help run: \ndocker exec -it ${org_path}-${PROJ}-${MODULE}-con ./run --help"
  echo -e "some containers are slow to start !!! Thus, use :\n docker logs ${org_path}-${PROJ}-${MODULE}-con"
  echo -e "to check the container's logs "
  echo -e "to attach run: \ndocker exec -it ${org_path}-${PROJ}-${MODULE}-con /bin/bash"
  echo -e "to debug re-run using DOCKER_BUILDKIT=0"
  echo -e "\n\n"

  export exit_code=$?
}
