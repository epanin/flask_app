start:
	poetry run flask --app lesson_ws.router --debug run --port 8000

gunicorn:
	poetry run gunicorn --workers=4 --bind=127.0.0.1:8000 lesson_ws.router:app
