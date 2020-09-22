DOCKER_IMAGE := farey
DOCKER_WORKSPACE = /app

.PHONY: help

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v frgrep | sed -e 's/\\$$//' | sed -e 's/##//'

image:		## Build base image
	@docker build -f docker/Dockerfile -t $(DOCKER_IMAGE) .

pytest:		## Run unit tests
	@docker run --rm -it \
		-v $(PWD):$(DOCKER_WORKSPACE) \
		$(DOCKER_IMAGE) pytest
