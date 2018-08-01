import os
import sys
import errno
import click
from .config import Config
from .multilogger import MultiLogger
from .monitoring import Monitoring
from .sources.file import FileSource


@click.command()
@click.option('--dry-run', '-n', is_flag=True, help='Output what would happen.')
@click.option('--config', '-c', default='~/.xtransfer.yaml', help='Configuration file.')
@click.argument('profile', required=True)
def main(profile, dry_run, config):
    """A file transfer cli to rule them all."""

    xtransfer_config = Config(config_filename=config)
    logger = MultiLogger(loggers=xtransfer_config.loggers).getLogger()
    monitoring = Monitoring(profile=profile, options=xtransfer_config.monitoring)

    if profile not in xtransfer_config.profiles:
        logger.critical("profile %s not found in configuration %s" % (
            profile, config))
        monitoring.unknown(
            message="profile %s not found in configuration %s" %
            (profile, config))
        sys.exit(1)

    logger.warning("profile %s running" % profile)

    if dry_run:
        logger.warning("dry_run enabled")

    run_profile = xtransfer_config.profiles[profile]

    if 'src' not in run_profile:
        logger.critical("profile %s has no src configuration" % profile)

        monitoring.unknown(
            message="profile %s has no src configuration" % profile)
        sys.exit(1)

    run_src = run_profile['src']
    if len(run_src) > 1:
        logger.critical(
            "profile %s src configuration must only contain 1 src type"
            % profile)

        monitoring.unknown(
            message="profile %s src configuration must only contain 1 src type"
            % profile)
        sys.exit(1)

    working_directory = os.path.join(xtransfer_config.work_dir, profile)
    try:
        if not os.path.isdir(working_directory):
            logger.warning("creating working directory %s" % working_directory)
            try:
                os.makedirs(working_directory)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

    except (IOError, OSError):
        logger.critical(
            "permission denied whilst creating working directory %s"
            % working_directory)

        monitoring.unknown(
            message="permission denied whilst creating %s"
            % working_directory)
        sys.exit(1)

    if 'file' in run_src:
        working_files = FileSource(dry_run=dry_run,
                                   work_dir=working_directory,
                                   **run_src['file']).get()

    print(working_files)
    pass
