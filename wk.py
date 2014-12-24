import os
import sys
import pip
import subprocess

import click


class WK(object):

    def __init__(self, name):
        self.name = name
        self.config = {}
        self.verbose = False

    def set_config(self, key, value):
        self.config[key] = value
        if self.verbose:
            click.echo('  config[%s] = %s' % (key, value), file=sys.stderr)

    def __repr__(self):
        return '<WK %r>' % self.name


wk_ctx = click.make_pass_decorator(WK)


@click.group()
@click.option('--wk-name', envvar='wk_name', default='.wk',
              metavar='NAME', help='Changes wk project name.')
@click.option('--config', nargs=2, multiple=True,
              metavar='KEY VALUE', help='Overrides a config key/value pair.')
@click.option('--verbose', '-v', is_flag=True, help='verbose ouput')
@click.version_option('1.0')
@click.pass_context
def cli(ctx, wk_name, config, verbose):
    """
    Create a wk object and remember it as as the context object.  From
    this point onwards other commands can refer to it by using the
    @wk_ctx decorator.
    """
    ctx.obj = WK(os.path.abspath(wk_name))
    ctx.obj.verbose = verbose
    for key, value in config:
        ctx.obj.set_config(key, value)


@cli.command()
@wk_ctx
def setup(*args, **kwargs):
    """
    """
    cwd = os.getcwd()

    click.secho('wk setup project', fg='blue', bold=True)

    click.secho('enter project name,', fg='green', nl=False)
    name = click.prompt('', type=str, \
                        default=os.path.basename(os.path.normpath(cwd)).lower())

    click.secho('enter project directory,', fg='green', nl=False)
    directory = click.prompt('', type=str, default=cwd)

    if click.confirm('VirtualEnv?'):
        if click.confirm('From existing?'):
            # os.system('source /usr/local/bin/virtualenvwrapper.sh')
            subprocess.call('v', shell=True)
            click.pause()
        click.secho('using project name: %s' % name.lower(), fg='green', nl=True)
        # maybe I should search the pwd for a requirements.txt file?
        
        # If the user has a preferred home for their environment storage, we place the env there
        # as the name of the project lowercased.
        # Otherwise, defaults to the project directory with the generic name, 'venv'.
        virtualenv_dir = os.getenv('WORKON_HOME')
        if virtualenv_dir:
            subprocess.Popen(['virtualenv', name], cwd=virtualenv_dir)
        else:
            subprocess.Popen(['virtualenv', 'venv'], cwd=directory)

        click.pause()