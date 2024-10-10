.SILENT: clean

COMPOSE := @docker compose -f docker-compose.yml

ARG=


build:
	$(COMPOSE) build

up:
	@echo "Server up..."
	$(COMPOSE) up

debug:
	@echo "Launchings Server for debbugging..."
	$(COMPOSE) run --service-ports nql

clean:
	@echo "Cleaning containers ..."
	docker ps -aq | xargs docker stop
	docker ps -aq | xargs docker rm

bash:
	@echo "Opening a shell session"
	$(COMPOSE) run --rm chainlit bash

lock:
	$(COMPOSE) run --rm chainlit poetry lock

prod_build:
	aws-vault exec nlq --no-session -- ./build.sh $(STAGE)