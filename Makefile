install:
	poetry install

dev:
	poetry run python manage.py runserver


start:
	poetry run gunicorn task_manager.wsgi