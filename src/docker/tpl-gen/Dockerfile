FROM python:3.8.3-alpine




ARG UID
ARG GID
ARG BASE_DIR
ARG PRODUCT
ARG ORG_DIR
ARG PRODUCT_DIR
ARG APPUSR
ARG APPGRP
ARG HOME_PRODUCT_DIR
ARG MOUNT_WORK_DIR
ARG DOCKER_SHELL
ARG DOCKER_HOME
ARG RUN_SCRIPT
ARG DOCKER_INIT_SCRIPT

ENV MODULE='tpl-gen'
ENV BASE_DIR=$BASE_DIR
ENV ORG=$ORG
ENV PRODUCT=$PRODUCT
ENV ORG_DIR=$ORG_DIR
ENV PRODUCT_DIR=$PRODUCT_DIR
ENV EDITOR="vim"
ENV APPUSR=$APPUSR
ENV APPGRP=$APPGRP
ENV PS1='`date "+%F %T"` \u@\h  \w \n\n  '
ENV HOME_PRODUCT_DIR=$HOME_PRODUCT_DIR
ENV MOUNT_WORK_DIR=$MOUNT_WORK_DIR
ENV DOCKER_SHELL=$DOCKER_SHELL
ENV DOCKER_HOME=$DOCKER_HOME
ENV RUN_SCRIPT=$RUN_SCRIPT
ENV DOCKER_INIT_SCRIPT=$DOCKER_INIT_SCRIPT


VOLUME $MOUNT_WORK_DIR

# STOP ::: arg vars


# START ::: install OS utils
RUN apk update && apk upgrade && apk add --no-cache \
    bash binutils vim perl jq wget curl zip unzip busybox-extras su-exec sudo shadow

# STOP ::: install OS utils


# START ::: install src utils
RUN apk update && apk upgrade && apk add --no-cache \
    build-base gcc openssl-dev python3-dev libmagic ttf-freefont \
    python3-dev jpeg-dev zlib-dev coreutils libffi-dev util-linux

# START ::: install src utils



# START ::: install python pip
RUN wget https://bootstrap.pypa.io/get-pip.py ; sudo python3 get-pip.py ; sudo rm -v get-pip.py


# STOP ::: install python pip


# START ::: add-os-user
RUN test -z $(getent group $GID | cut -d: -f1) || \
        groupmod -g $((GID+1000)) $(getent group $GID | cut -d: -f1)

# create a APPGRP and APPUSR
RUN set -x ; addgroup -g "$GID" -S "$APPGRP" && \
  adduser \
  --disabled-password \
  -g "$GID" \
  -D \
  -s "$DOCKER_SHELL" \
  -h "$DOCKER_HOME" \
  -u "$UID" \
  -G "$APPGRP" "$APPUSR" && exit 0 ; exit 1


RUN echo "$APPUSR ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN echo "export PS1=\"$PS1\"" >> $DOCKER_HOME/.bashrc && \
  sudo chown -R $APPUSR:$APPGRP $DOCKER_HOME && \
  sudo chmod -R 0775 $DOCKER_HOME

# ensure the default shell for this user is the bash bin
RUN usermod -s /bin/bash $APPUSR


USER $APPUSR

# STOP  ::: add-os-user


# START ::: install-poetry
# Set the Poetry version
ENV POETRY_VERSION=1.5.0

# Check if Poetry is installed and install it if necessary
RUN poetry --version >/dev/null 2>&1 \
    && poetry_version=$(poetry --version | sed -n 's/Poetry version \(.*\)/\1/p') \
    && test "$poetry_version" = "$POETRY_VERSION" \
    || (curl -sSL https://install.python-poetry.org | python - \
        && chmod 775 $HOME/.local/share/pypoetry/venv/bin/poetry )

RUN echo 'export PATH=$PATH:$HOME/.local/bin/' >> $HOME/.bashrc

ENV PATH="${PATH}:/home/${APPUSR}/.local/bin/"

# set the default shell as bash and not sh
SHELL ["/bin/bash", "-c"]

# STOP  ::: install-poetry



# START ::: copy-proj-dir

COPY --chown=$APPUSR:$APPGRP . ${HOME_PRODUCT_DIR}
COPY --chown=$APPUSR:$APPGRP ./src/bash/run/run.sh ${HOME_PRODUCT_DIR}/src/bash/run/run.sh

# Create the 'run' symlink
RUN ln -sfn ${HOME_PRODUCT_DIR}/src/bash/run/run.sh ${HOME_PRODUCT_DIR}/run

# STOP  ::: copy-proj-dir




# Iterate over each pyproject.toml file
RUN find $HOME_PRODUCT_DIR/src/python/ -name "pyproject.toml" -print0 | \
    while IFS= read -r -d '' f; do \
        tgt_dir=$(dirname "$f"); \
        echo "Working on tgt_dir: $tgt_dir"; \
        cd "$tgt_dir"; \
        if [ ! -z "${MODULE:-}" ] && [[ "$tgt_dir" == *"$MODULE"* ]]; then \
            test -f poetry.lock && rm -vf poetry.lock; \
            test -d .venv && rm -rv .venv; \
            poetry config virtualenvs.create true; \
            poetry install -vvv; \
            if [ $? -ne 0 ]; then \
                echo "FATAL: failed to install $tgt_dir py modules"; \
                exit 1; \
            fi; \
        fi; \
        cd -; \
    done



WORKDIR $HOME_PRODUCT_DIR

RUN chmod 0755 "$HOME_PRODUCT_DIR/src/bash/scripts/docker-init-${MODULE}.sh"

CMD exec /bin/bash -c "$HOME_PRODUCT_DIR/src/bash/scripts/docker-init-${MODULE}.sh"




