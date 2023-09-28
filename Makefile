PYTHON_INTERPRETER = python3

## clean
clean: .clean-build .clean-pyc .clean-test

.clean-build:
	rm -rf dist/

.clean-pyc:
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '*.pyo' -exec rm -rf {} +
	find . -name '*~' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +

.clean-test:
	rm -rf .tox/
	rm -rf .coverage
	rm -rf htmlcov/

## dev environment
## deps
deps-dev:
	@echo "Installing necessary dependencies for web"
	$(PYTHON_INTERPRETER) -m pip install -U -r app/requirements.txt

# run the dev environment
POSTGRES_USERNAME = dummy
POSTGRES_PASSWORD = dummy
POSTGRES_HOST = localhost
POSTGRES_PORT = 5432
POSTGRES_DATABASE = tts
CURRENT_DIR = $(shell pwd)
DB_CHECK_PARAMS = $(POSTGRES_USERNAME) $(POSTGRES_PASSWORD) $(POSTGRES_HOST) $(POSTGRES_PORT) $(POSTGRES_DATABASE)
DB_PARAMS = PGUSER=dummy PGPASSWORD='$(POSTGRES_PASSWORD)' APP_ENV=dev
DB_CMD_PARAMS = -h "$(POSTGRES_HOST)" -U "$(POSTGRES_USERNAME)" -p "$(POSTGRES_PORT)"

## bring up docker containers for local dev-setup
.PHONY: docker-compose
docker-compose:
	mkdir -p ./app/db-data
	docker-compose -f docker-compose.yml up -d


## db related actions like check, create, migrate and seed db
.PHONY: check-db
check-db:
	@echo "check and ensure postgres is up and running"
	until $(PYTHON_INTERPRETER) $(CURRENT_DIR)/app/dockerconf/check_postgres.py $(DB_CHECK_PARAMS); do \
  		printf "." ; \
  		sleep 2 ; \
  	done

.PHONY: create-db
create-db: check-db

ifeq ($(shell $(DB_PARAMS) psql -t -A $(DB_CMD_PARAMS) -c \
	"SELECT 1 FROM pg_catalog.pg_database WHERE datname ='$(POSTGRES_DATABASE)'"), 1)
	printf "Database $(POSTGRES_DATABASE) already present, Hence not creating new one\n"
else
	printf "Creating Database $(POSTGRES_DATABASE)\n"
	$(DB_PARAMS) createdb $(DB_CMD_PARAMS) "$(POSTGRES_DATABASE)"
	$(DB_PARAMS) psql -t -A  $(DB_CMD_PARAMS) -d "$(POSTGRES_DATABASE)" \
		-c "GRANT ALL PRIVILEGES ON DATABASE $(POSTGRES_DATABASE) TO $(POSTGRES_USERNAME)"
endif

.PHONY: migrate-db
migrate-db:
	$(PYTHON_INTERPRETER) -m web.migrate db upgrade

.PHONY: seed-db
seed-db:
	$(DB_PARAMS) psql -t -A $(DB_CMD_PARAMS) -d "$(POSTGRES_DATABASE)" -f "./migrations/data.sql"


## setup the dev-docker environment
.PHONY: dev-docker-env-up
dev-docker-env-up:
	docker-compose up -d
	@echo "dev docker environment is up !!"

.PHONY: dev-docker-env-down
dev-docker-env-down:
	docker-compose down
	@echo "dev docker environment is down !!"


## locally running without docker
.PHONY: local-app
local-app:
	export APP_NAME=web ; \
	export APP_ENV=dev ; \
	export PORT=8080; \
	export METRICS_PORT=8081; \
    gunicorn -c app/config/gunicorn.conf.dev.py web.run:app
