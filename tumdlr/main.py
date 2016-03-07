import logging
import os
import click
from configparser import ConfigParser

from tumdlr import PLUGIN_DIR
from tumdlr.config import load_config


CONTEXT_SETTINGS = dict(auto_envvar_prefix='TUMDLR', max_content_width=100)


class Context(object):
    """
    CLI Context
    """
    def __init__(self):
        self.cookiejar      = None
        self.config         = load_config('tumdlr')
        self.config_path    = None
        self.log            = None
        self.cache          = True
        self.database       = NotImplemented


class CommandLine(click.MultiCommand):

    def list_commands(self, ctx):
        """
        Get a list of all available commands

        Args:
            ctx: Context

        Returns:
            list
        """
        commands = []
        for filename in os.listdir(PLUGIN_DIR):
            if filename.endswith('.py') and not filename.startswith('__'):
                commands.append(filename[:-3])

        commands.sort()
        return commands

    def get_command(self, ctx, name):
        """
        Fetch a command module

        Args:
            ctx:        Context
            name(str):  Command name
        """
        ns = {}

        filename = os.path.join(PLUGIN_DIR, name + '.py')
        with open(filename) as f:
            code = compile(f.read(), filename, 'exec')
            eval(code, ns, ns)

        return ns['cli']


pass_context = click.make_pass_decorator(Context, ensure=True)


@click.command(cls=CommandLine, context_settings=CONTEXT_SETTINGS)
@click.option('-c', '--config', type=click.Path(dir_okay=False, resolve_path=True), envvar='TUMDLR_CONFIG_PATH',
              default='~/.config/tumdlr/tumdlr.conf', help='Path to the TumDLR configuration file')
@click.option('-q', '--quiet', help='Silence all output except for fatal errors', is_flag=True)
@click.option('-d', '--debug', help='Output information used for debugging', is_flag=True)
@pass_context
def cli(ctx, config, quiet, debug):
    """
    Tumblr Downloader CLI utility

    Args:
        ctx(Context)
        config(str)
        quiet(bool)
        debug(bool)
    """
    # Logging setup
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.ERROR if quiet else logging.WARN

    ctx.log = logging.getLogger('tumdlr')
    ctx.log.setLevel(log_level)

    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(logging.Formatter('[%(levelname)s] %(name)s: %(message)s'))
    ctx.log.addHandler(ch)


if __name__ == '__main__':
    cli()
