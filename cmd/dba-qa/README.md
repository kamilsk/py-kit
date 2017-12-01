> # py-kit:dba-qa
>
> Check your DBA team's work.

[![Patreon](https://img.shields.io/badge/patreon-donate-orange.svg)](https://www.patreon.com/octolab)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](../../LICENSE)

```bash
$ virtualenv .virtenv
$ v+
$(.virtenv) pip install -r requirements.txt
$(.virtenv) python check.py -c config.yml --env=prod INFRADB-123
```
