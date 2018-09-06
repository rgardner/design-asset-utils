# Creative Market

This tool is intended to automate syncing the 6 free goods offered by Creative
Market each week.


## Usage

Install dependencies:

```sh
$ cd creative-market
$ pipenv install --dev
$ # edit necessary environment variables
$ cp .env.example .env
$ vim .env
```

To sync the 6 free goods offered by Creative Market to your Dropbox:

```sh
$ make run
```

To validate that the script succeeded, check your Dropbox, or:

```sh
$ make test
```

`checker` validates that Creative Market thinks you've synced your 6 free
goods, and optionally, sends an email if an error occurred:

```sh
$ pipenv run python checker.py --send-email-on-error
```

And finally, to run some validations on the Python scripts:

```sh
$ make check
```


## Creative Market Terms of Service

This is compliant with Creative Market's Terms of Service ([August 24,
2018](https://web.archive.org/web/20180824022212/creativemarket.com/terms))
([permalink](https://creativemarket.com/terms)).
