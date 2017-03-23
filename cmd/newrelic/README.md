> # py-kit:newrelic
>
> Get transactions from your New Relic accounts for three months.

```bash
$ virtualenv .virtenv
$ v+
$(.virtenv) pip install -r requirements.txt
$(.virtenv) echo /transaction/id | python report.py -c config.yml -u USER -p PASS ACCOUNT1 ACCOUNT2
```
