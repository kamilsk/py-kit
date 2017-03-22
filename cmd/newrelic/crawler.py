import click
import requests

import os
import sys
import time
import yaml


class Scrapper(object):
    LOGIN_URL = 'https://login.newrelic.com/login'
    TIME_WINDOW_URL = 'https://rpm.newrelic.com/set_time_window'
    TRANSACTION_URL = 'https://rpm.newrelic.com/accounts/%d/applications/%d/transactions/table.csv?type=all'

    def __init__(self, session):
        self.session = session

    def login(self, login, password):
        print self.session.post(self.LOGIN_URL, data={
            'login[email]': login,
            'login[password]': password})

    def set_time_window(self, ts):
        return self.session.get(self.TIME_WINDOW_URL, data={
            'back': '',
            'tw[dur]': 'last_7_days',
            'tw[end]': str(ts)})

    def get_last_n_week_csv_data(self, csv_url, path, filename, n=13):
        start = int(time.time())
        if not os.path.exists(path):
            os.makedirs(path, 0777)
        for i in range(n):
            time.sleep(0.1)
            self.set_time_window(start - (i*604800))
            resp = self.session.get(csv_url)
            f = open(path + '/' + str(i) + '-' + filename, 'w')
            f.write(resp.content)
            f.close()


@click.command()
@click.option('-u', '--username', help='username', envvar='NEW_RELIC_USER')
@click.option('-p', '--password', help='password', envvar='NEW_RELIC_PASS')
@click.option('-c', '--config', help='yaml configuration', type=click.File())
@click.option('--skip', help='skip download part', is_flag=True)
@click.option('--debug', help='add verbosity', is_flag=True)
@click.argument('accounts', nargs=-1)
def scrap(username, password, config, skip, debug, accounts):
    """
    :param str username:
    :param str password:
    :param file config:
    :param bool skip:
    :param bool debug:
    :param list accounts:
    :return:
    """
    if not skip:
        cfg = yaml.load(config)

        scrapper = Scrapper(requests.Session())
        scrapper.login(username, password)

        if len(accounts) == 0:
            accounts = [str(dict(item)['name']) for item in list(cfg['accounts'])]

        for account in accounts:
            current = [item for item in list(cfg['accounts']) if account.lower() == item['name'].lower()]
            if len(current) > 0:
                item = current[0]
                for app in list(item['apps']):
                    scrapper.get_last_n_week_csv_data(
                        scrapper.TRANSACTION_URL % (item['id'], app['id']),
                        './report/%s' % account.lower(),
                        '%s.csv' % app['name'])
            else:
                print 'account %s not found' % account
    pipeline = [
        'grep -rnw ./report/*/*.csv -e "%s"',
        'awk -F "," \'{print $1"\t\t"$3}\'',
    ]
    for criteria in sys.stdin:
        cmd = ' | '.join(pipeline) % criteria.strip()
        if debug:
            print 'executed: %s' % cmd
        os.system(cmd)


if __name__ == '__main__':
    scrap()
