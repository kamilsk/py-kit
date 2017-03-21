> # py-kit:newrelic
>
> Get transactions for three months.

```bash
$ virtualenv .virtenv
$ v+
$(.virtenv) pip install -r requirements.txt
$(.virtenv) echo /transaction/id | python crawler.py scrap -u USER -p PASS -c config.yml ACCOUNT1 ACCOUNT2
```
