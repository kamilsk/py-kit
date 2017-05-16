import click
import mysql.connector

from mysql.connector.errors import OperationalError

import os
import sys
import yaml


@click.command()
@click.option('-c', '--config', help='yaml configuration', type=click.File(), default='config.local.yml')
@click.option('-e', '--env', help='environment', default='staging')
@click.option('--debug', help='add verbosity', is_flag=True)
@click.argument('issues', nargs=-1)
def check(config, env, debug, issues):
    """
    :param file config:
    :param str env:
    :param bool debug:
    :param list issues:

    :return:
    """
    cfg = yaml.load(config)
    current = [item for item in list(cfg['environments']) if str(item['name']).lower() == env.lower()]
    item = {}
    if len(current) > 0:
        item = current[0]
    else:
        print 'environment %s not found' % env
        exit(1)
    path = os.path.dirname(os.path.realpath(__file__)) + '/issue'
    for issue in issues:
        sql = open(path + '/' + str(issue).upper() + '.sql', 'r')
        queries = sql.read().split(';')

        for conn in item['connections']:
            try:
                cnx = mysql.connector.connect(**dict(conn))
                cursor = cnx.cursor(dictionary=True)

                if len(queries) > 1:
                    for query in queries[:-1]:
                        cursor.execute(query)

                query = queries[-1]

                # TODO hard code
                assertion = (lambda q: (lambda r: r['total'] == 0))(query)

                cursor.execute(query)

                for row in cursor.fetchall():
                    if not assertion(row):
                        # TODO hard code
                        print 'assertion for host %s fails' % conn['host'], row
                    else:
                        print 'assertion for host %s is successful' % conn['host']

                cnx.close()
            except OperationalError:
                print 'assertion for host %s fails' % conn['host'], 'time out'


if __name__ == '__main__':
    check()