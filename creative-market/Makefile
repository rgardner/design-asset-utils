all: check

setup:
	brew cask install chromedriver || 0
	cd downloader && pipenv install --dev

check:
	pipenv run yapf *.py --in-place
	pipenv run mypy *.py --ignore-missing-imports
	pipenv run pylint *.py

run:
	pipenv run python3 downloader.py

test:
	pipenv run pytest -m 'not email'

deploy:
	cd .. && git subtree push --prefix creative-market heroku master

.PHONY: setup check run test deploy
