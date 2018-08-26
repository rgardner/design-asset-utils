# Creative Market

This tool is intended to automate syncing the 6 free goods offered by Creative
Market each week.


## Usage

```sh
$ cd downloader
$ pipenv install
$ pipenv run ./downloader.py
```


## Development

Complete the one-time setup:

```sh
$ cd downloader
$ # install dependencies
$ make setup
$ # edit necessary environment variables
$ cp .env.example .env
$ vim .env
```

Then, run `make` to validate the Python code and `make run` to run the program.


## Creative Market Terms of Service

This is compliant with Creative Market's Terms of Service ([August 24,
2018](https://web.archive.org/web/20180824022212/creativemarket.com/terms))
([permalink](https://creativemarket.com/terms)).
