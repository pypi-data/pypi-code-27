import logging
from pathlib import Path

import appdirs

import click

from munch import Munch

import pkg_resources

from ptpython import repl

from . import util
from .config import cfg, configure_logging
from .distribution import Distribution
from .requirement import Requirement

VERSION = pkg_resources.get_distribution("distinfo").version

log = logging.getLogger(__name__)


@click.command()
@click.argument(
    "source_dir",
    nargs=1, default=".",
    type=click.Path(exists=True, file_okay=False),
)
@click.option(
    "-i", "--interactive",
    is_flag=True,
    help="Launch interactive shell",
)
@click.option(
    "-f", "--fmt",
    type=click.Choice(util.DUMPERS.keys()),
    default=util.DEFAULT_DUMPER,
    help="Output format",
)
@click.option("-c", "--color", is_flag=True, help="Force colored output")
@click.option("-p", "--pretty", is_flag=True, help="Pretty print output")
@click.option("-o", "--output", help="Output to file")
@click.option("-r", "--requires", is_flag=True, help="Print requires")
@click.option("--include", help="Include metadata keys")
@click.option("--exclude", help="Exclude metadata keys")
@click.version_option(VERSION)
def main(source_dir, **options):
    """
    Extract metadata from Python source distributions
    """

    options = Munch(options)

    if options.color:
        cfg.logging.config.isatty = True
    configure_logging()

    dist = Distribution(source_dir)

    if options.interactive:
        namespace = dict(
            Distribution=Distribution,
            Requirement=Requirement,
            dist=dist,
            dump=util.dump,
            dumps=util.dumps,
        )
        click.secho("distinfo shell %s:" % VERSION, fg="white", bold=True)
        cachedir = Path(appdirs.user_cache_dir("distinfo", "distinfo"))
        cachedir.mkdir(parents=True, exist_ok=True)
        repl.embed(
            namespace,
            configure=repl.run_config,
            history_filename=cachedir / "history",
        )
    else:
        if options.requires:
            obj = dist.requires
        else:
            obj = dist.metadata
            if options.include:
                obj = {k: v for k, v in obj.items() if k in options.include.split(",")}
            if options.exclude:
                obj = {k: v for k, v in obj.items() if k not in options.exclude.split(",")}
        kwargs = Munch(fmt=options.fmt)
        if options.pretty and options.fmt == "json":
            kwargs.indent = 2
        dump = util.dumps(obj, **kwargs)
        if options.output:
            with open(options.output, "w") as stream:
                stream.write(dump)
        else:
            print(dump)
