all: build

setup:
	brew cask install chromedriver || 0
	cd downloader && pipenv install --dev

build:
	pipenv run yapf downloader.py --in-place
	pipenv run mypy downloader.py --ignore-missing-imports
	pipenv run pylint downloader.py

run:
	pipenv run python3 downloader.py

test:
	pipenv run pytest

deploy:
	cd .. && git subtree push --prefix creative-market heroku master

.PHONY: setup build run test deploy
