ifneq (,$(wildcard ./.env))
    include .env
    export
endif


.PHONY: test

test:
	docker compose down
	docker compose up -d --wait
	alembic upgrade head
	pytest -xvv tests --cov=core --cov=projects --cov=profiles --cov=users
