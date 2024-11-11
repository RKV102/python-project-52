install:
	poetry install

start-dev:
	poetry run python manage.py runserver

start-production:
	poetry run gunicorn task_manager.wsgi:application

configure:
	poetry config virtualenvs.in-project true

lint:
	poetry run flake8

test:
	poetry run coverage run manage.py test

cover:
	poetry run coverage lcov

migrate:
	poetry run python manage.py makemigrations && \
	poetry run python manage.py migrate