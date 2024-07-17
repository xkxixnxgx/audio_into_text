pre-commit:
	poetry run pre-commit run --all-files --color auto

migrate:
	docker-compose run --rm server python manage.py migrate

makemigrations:
	docker-compose run --rm server python manage.py makemigrations

createsuperuser:
	docker-compose run --rm server python manage.py createsuperuser

collectstatic:
	docker-compose run --rm server python manage.py collectstatic --noinput

rebuild:
	docker-compose build server --no-cache

run:
	poetry run python media_to_text/manage.py runserver

run_gunicorn:
	gunicorn media_to_text.media_to_text.wsgi --bind 0.0.0.0:8010

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f server

into_server:
	docker-compose exec server bash
