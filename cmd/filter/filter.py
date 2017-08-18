import click
import mysql.connector

from mysql.connector.errors import DatabaseError, OperationalError

import os
import sys
import yaml


@click.command()
@click.option('-c', '--config', help='yaml configuration', type=click.File(), default='config.local.yml')
@click.option('-e', '--env', help='environment', default='staging')
@click.option('-h', '--host', help='host', default='')
@click.argument('issues', nargs=-1)
def filter(config, env, host, issues):
    """
    :param file config:
    :param str env:
    :param str host:
    :param tuple issues:

    :return:
    """
    cfg = yaml.load(config)
    cur = [item for item in list(cfg['environments']) if str(item['name']).lower() == env.lower()].pop()
    con = [item for item in cur['connections'] if str(item['host']).lower().find(host) == 0].pop()

    cnx = None
    try:
        cnx = mysql.connector.connect(**dict(con))
    except OperationalError:
        print 'assertion for host %s fails' % con['con'], 'time out'
        exit(1)
    except DatabaseError, err:
        print 'database error "%s" at host %s' % (err, con['host'])
        exit(1)
    cursor = cnx.cursor(buffered=True, dictionary=True)

    path = os.path.dirname(os.path.realpath(__file__)) + '/issue'

    issue = issues[0]
    sql = open(path + '/' + str(issue).upper() + '.sql', 'r')
    query = sql.read()
    assertion = (lambda q: (lambda r: r is None))(query)

    for line in sys.stdin:
        line = line.strip()
        try:
            cursor.execute(query, [line])
            if assertion(cursor.fetchone()):
                print line
        except OperationalError:
            print 'assertion for host %s fails' % con['con'], 'time out'
            exit(1)
        except DatabaseError, err:
            print 'database error "%s" at host %s' % (err, con['host'])
            exit(1)

    cursor.close()
    cnx.close()


if __name__ == '__main__':
    filter()
