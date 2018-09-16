all: check

setup:
	brew cask install chromedriver || 0
	cd downloader && pipenv install --dev

check:
	pipenv run yapf *.py --in-place
	pipenv run mypy *.py --ignore-missing-imports
	pipenv run pylint *.py

run:
	$(eval OUTPUT_FILENAME := $(shell date "+%y%m%d_%H%M%S_downloader"))
	pipenv run jupyter nbconvert --execute downloader.ipynb --output $(OUTPUT_FILENAME)

test:
	pipenv run pytest -m 'not email'

deploy:
	cd .. && git subtree push --prefix creative-market heroku master

.PHONY: setup check run test deploy
