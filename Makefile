compose = docker compose

.PHONY: build up run

build:
    $(compose) build

up:
	$(compose) up

