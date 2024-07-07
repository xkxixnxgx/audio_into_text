pre-commit:
	poetry run pre-commit run --all-files --color auto

migrate:
	poetry run python audio_into_text/manage.py migrate

makemigrations:
	poetry run python audio_into_text/manage.py makemigrations

createsuperuser:
	poetry run python audio_into_text/manage.py createsuperuser

run:
	poetry run python audio_into_text/manage.py runserver 8010
