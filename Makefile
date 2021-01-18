# include .env

# DOCKER
# -----------------------------------------------------------------------------
bash:
	docker exec -it django bash

build:
	docker-compose -f local.yml build --force-rm --no-cache

down:
	docker-compose -f local.yml down --remove-orphans

down_reset:
	docker-compose -f local.yml down -v --rmi all --remove-orphans

logs:
	docker-compose -f local.yml logs --tail all -f

logs-django:
	docker-compose -f local.yml logs --tail all  django

ps:
	docker-compose -f local.yml ps

remove:
	docker-compose -f local.yml rm

start:
	docker-compose -f local.yml start

stop:
	docker-compose -f local.yml stop

top:
	docker-compose -f local.yml top

up:
	docker-compose -f local.yml up -d

# PYTHON
# -----------------------------------------------------------------------------
pipenv-install:
	@echo "> pipenv install && pipenv lock"

	docker exec -it django pip install -r requirements.txt

# DJANGO
# -----------------------------------------------------------------------------
createsuperuser:
	@echo "> ./manage.py createsuperuser"

	docker-compose -f local.yml run --rm django python manage.py createsuperuser

check:
	docker-compose -f local.yml run --rm django python manage.py check

showmigrations:
	@echo "> ./manage.py showmigrations"

	docker-compose -f local.yml run --rm django python manage.py showmigrations


makemigrations:
	@echo "> ./manage.py makemigrations"

	docker-compose -f local.yml run --rm django python manage.py makemigrations

migrate:
	@echo "> ./manage.py migrate"

	docker-compose -f local.yml run --rm django python manage.py migrate


shell:
	@echo "> ./manage.py shell"

	docker-compose -f local.yml run --rm django python manage.py shell

dbshell:
	@echo "> ./manage.py dbshell"

	docker-compose -f local.yml run --rm django python manage.py dbshell

debug:
	@echo "> ./manage.py debug"

	docker-compose -f local.yml run --rm --service-ports django

# -----------------------------------------------------------------------------
#  Rebuild all.
rebuild: down build

#Restart all
restart: stop start logs
