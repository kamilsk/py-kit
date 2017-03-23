> # py-kit:dba-qa
>
> Check your DBA team's work.

```bash
$ virtualenv .virtenv
$ v+
$(.virtenv) pip install -r requirements.txt
$(.virtenv) python check.py -c config.yml --env=prod INFRADB-123
```
