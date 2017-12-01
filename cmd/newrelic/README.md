> # py-kit:newrelic
>
> Get transactions from your New Relic accounts for three months.

[![Patreon](https://img.shields.io/badge/patreon-donate-orange.svg)](https://www.patreon.com/octolab)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](../../LICENSE)

```bash
$ virtualenv .virtenv
$ v+
$(.virtenv) pip install -r requirements.txt
$(.virtenv) echo /transaction/id | python report.py -c config.yml -u USER -p PASS ACCOUNT1 ACCOUNT2
```
