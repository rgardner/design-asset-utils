# Design Asset Utils

This project is intended to help manage design assets, such as those
available in [Creative Market][creative-market].

## Creative Market

**This project has been archived because [Creative Market][creative-market] now
uses Google ReCAPTCHA, which prevents the scraper from accessing the site.**

This project is a Python app deployed to Heroku to log into
<creativemarket.com> and click the "Sync to Dropbox" button on the 6 free
goods each day. The script's novelty lies in using a Jupyter Notebook to
scrape the site, making it easier to develop the web scraping code. It even
captures a screenshot and shows it in the notebook when a scraping error
occurs. It uses `jupyter nbconvert --execute` to run the notebook from the
command line, so this same notebook is also used on the server. Heroku
doesn't natively support cron jobs, so `clock.py` is run continuously, which
uses [apscheduler][apscheduler] to run the _downloader_ and _checker_
scripts.

[apscheduler]: https://pypi.org/project/APScheduler/

### Creative Market Terms of Service

This is compliant with Creative Market's Terms of Service ([August 24,
2018](https://web.archive.org/web/20180824022212/creativemarket.com/terms))
([permalink](https://creativemarket.com/terms)) because it:

- does not "[copy], [distribute], or [disclose] any part of the Service in any medium"
- does not "use the Service in a manner that sends more request messages to the
  Creative Market servers than a human can reasonably produce in the same
  period of time by using a conventional online web browser"

[creative-market]: https://creativemarket.com/
