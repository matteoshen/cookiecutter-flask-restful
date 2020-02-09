.PHONY: init init-migration build run db-migrate test tox mysql-create mysql-cleanup

init:  build run
	docker-compose exec web myapi db upgrade
	docker-compose exec web myapi init
	@echo "Init done, containers running"

build:
	docker-compose build

run:
	docker-compose up -d

db-migrate:
	docker-compose exec web myapi db migrate

db-upgrade:
	docker-compose exec web myapi db upgrade

test:
	docker-compose run -v $(PWD)/tests:/code/tests:ro web tox -e test

tox:
	docker-compose run -v $(PWD)/tests:/code/tests:ro web tox -e py37

lint:
	docker-compose run web tox -e lint

mysql-create:
	mysql/create-instance.sh

mysql-cleanup:
	mysql/cleanup.sh
