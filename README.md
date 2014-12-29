wk -- project automation
=================

The things you'll need are a global installation of [click](http://click.pocoo.org/3/) and to install `wk` in editable mode. So from your `wk` project directory, run

```shell
$ pip install click
$ pip install --editable .
```

The last step is to setup the wk project directory. I borrowed this idea from virtualenv wrapper and rvm. It works for them, so it should be fine in this case. Add this line to your .bashrc file, it will instruct wk to load and save from the specified directory: `export WK_HOME=$HOME/.wk`
Now you'll be able to run wk anywhere on your terminal.

```shell
$ wk
Usage: wk [OPTIONS] COMMAND [ARGS]...

  Create a wk object and remember it as as the context object.  From this
  point onwards other commands can refer to it by using the @wk_ctx
  decorator.

Options:
  --name NAME         wk project name
  --config KEY VALUE  Overrides a config key/value pair.
  -v, --verbose       verbose ouput
  --version           Show the version and exit.
  --help              Show this message and exit.

Commands:
  load
  setup

```