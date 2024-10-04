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
	$(COMPOSE) run --rm nql bash

lock:
	$(COMPOSE) run --rm nql poetry lock