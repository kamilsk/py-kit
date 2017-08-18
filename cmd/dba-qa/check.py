import click
import mysql.connector

from mysql.connector.errors import DatabaseError, OperationalError

import os
import yaml


@click.command()
@click.option('-c', '--config', help='yaml configuration', type=click.File(), default='config.local.yml')
@click.option('-e', '--env', help='environment', default='staging')
@click.argument('issues', nargs=-1)
def check(config, env, issues):
    """
    :param file config:
    :param str env:
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
                cursor = cnx.cursor(buffered=True, dictionary=True)

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
            except DatabaseError, err:
                print 'database error "%s" at host %s' % (err, conn['host'])


if __name__ == '__main__':
    check()
