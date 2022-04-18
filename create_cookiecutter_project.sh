#!/bin/zsh
cookiecutter \
--output-dir ~/repos \
--debug-file \
/tmp/cookiecutter.log \
--directory python \
git@gitlab.com:jar1/cookiecutters.git \
AUTHOR="Jamil André RAICHOUNI" \
EMAIL=raichouni@gmail.com \
GIT_BASE_URL=git@gitlab.com:jar1 \
DOCKER_REGISTRY=registry.gitlab.com/jar1/docker-images \
WEBAPP=no
