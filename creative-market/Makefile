all: check

setup:
	brew cask install chromedriver || 0
	cd downloader && pipenv install --dev

check:
	pipenv run yapf downloader.py --in-place
	pipenv run mypy downloader.py --ignore-missing-imports
	pipenv run pylint downloader.py

run:
	pipenv run python3 downloader.py

test:
	pipenv run pytest -m 'not email and not redis_queue'

test-redis-queue:
	docker-compose run worker pytest -m 'redis_queue'

deploy:
	cd .. && git subtree push --prefix creative-market heroku master

.PHONY: setup check run test deploy
