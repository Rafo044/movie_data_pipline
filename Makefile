
up:
	docker compose up -d --build

down:
	docker compose down --volumes

logs:
	docker compose logs

start:
	docker compose start


stop:
	docker compose stop


venv:
	python3 -m venv venv
	source venv/bin/activate


install:
	pip install -r requirements.txt



jetstream:
	python3 jetstream/jetstream.py


omdb_publisher:
	python3 omdb/omdb_publisher.py


tvdb_publisher:
	python3 tvdb/tvdb_publisher.py


subscriber:
	python3 subscriber/subscriber.py
