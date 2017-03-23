import click
import mysql.connector

import os
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
        query = sql.read()

        # TODO hard code
        assertion = (lambda q: (lambda r: r['total'] == 0))(query)

        for conn in item['connections']:
            cnx = mysql.connector.connect(**dict(conn))
            cursor = cnx.cursor(dictionary=True)
            cursor.execute(query)

            for row in cursor.fetchall():
                if not assertion(row):
                    # TODO hard code
                    print 'assertion for host %s fails' % conn['host']
                    exit(1)
                else:
                    print 'assertion for host %s is successful' % conn['host']

            cnx.close()


if __name__ == '__main__':
    check()
