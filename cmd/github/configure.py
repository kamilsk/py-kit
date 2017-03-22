import click

import yaml


@click.command()
@click.option('-c', '--config', help='yaml configuration', type=click.File(), default='config.local.yml')
@click.option('-t', '--token', help='access token', envvar='GITHUB_TOKEN')
@click.option('--debug', help='add verbosity', is_flag=True)
@click.argument('projects', nargs=-1)
def configure(config, token, debug, projects):
    """
    :param str token:
    :param file config:
    :param bool debug:
    :param list projects:
    :return:
    """
    cfg = yaml.load(config)
    print cfg


if __name__ == '__main__':
    configure()
