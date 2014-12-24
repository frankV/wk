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
@click.option('--name', envvar='wk_name', default='.wk',
              metavar='NAME', help='wk project name')
@click.option('--config', nargs=2, multiple=True,
              metavar='KEY VALUE', help='Overrides a config key/value pair.')
@click.option('--verbose', '-v', is_flag=True, help='verbose ouput')
@click.version_option('1.0')
@click.pass_context
def cli(ctx, name, config, verbose):
    """
    Create a wk object and remember it as as the context object.  From
    this point onwards other commands can refer to it by using the
    @wk_ctx decorator.
    """
    ctx.obj = WK(name)
    ctx.obj.verbose = verbose
    for key, value in config:
        ctx.obj.set_config(key, value)


@cli.command()
@wk_ctx
def setup(wk, *args, **kwargs):
    """
    """
    if not os.getenv('WK_HOME'):
        click.secho('please set your wk home directory', fg='red')
        click.secho('  $ export WK_HOME=~/.wk', fg='red')
        exit()

    cwd = os.getcwd()

    click.secho('wk setup project', fg='blue', bold=True)

    click.secho('enter project name,', fg='green', nl=False)
    wk.name = click.prompt('', type=str, default=os.path.basename(os.path.normpath(cwd)).lower())

    click.secho('enter project directory,', fg='green', nl=False)
    directory = click.prompt('', type=str, default=cwd)
    wk.set_config('directory', directory)

    if click.confirm(click.style('VirtualEnv?', fg='green'), default=True):
        wk.set_config('venv', True)

        if os.getenv('WORKON_HOME'):
            if click.confirm(click.style('From existing?', fg='green')):
                wk.set_config('venv_existing', True)
                venvs = os.walk(os.getenv('WORKON_HOME')).next()[1]
                for index, env in enumerate(venvs):
                    print '%s: %s' % (index, env)
                click.secho('enter number', fg='green', nl=False)
                i = click.prompt('', type=int)
                wk.set_config('venv_directory', os.path.join(os.getenv('WORKON_HOME'), venvs[i]))
            else:
                click.secho('virtualenv name,', fg='green', nl=False)
                venv = click.prompt('', type=str, default=wk.name)
                    # need a callback for this
                subprocess.call(['virtualenv', wk.name], cwd=os.getenv('WORKON_HOME'))
                wk.set_config('venv_directory', os.path.join(os.getenv('WORKON_HOME'), wk.name))

        # If the user has a preferred home for their environment storage, we place the env there
        # as the name of the project lowercased.
        # Otherwise, defaults to the project directory with the generic name, 'venv'.
        elif not os.getenv('WORKON_HOME'):
            wk.set_config('venv_existing', False)
            click.secho('virtualenv name,', fg='green', nl=False)
            venv = click.prompt('', type=str, default=wk.name)
            # need a callback for this
            subprocess.call(['virtualenv', 'venv'], cwd=directory)
            wk.set_config('venv_directory', os.path.join(directory, venv))

        click.pause()
        print wk.name
        print wk.config