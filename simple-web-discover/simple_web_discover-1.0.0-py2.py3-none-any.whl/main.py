from functools import partial
import logging
from typing import Set

import asks
import click
import click_log
import trio

from simple_web_discover.web import async_main
from simple_web_discover.web import log as web_log

log = logging.getLogger(__name__)


def validate_status_codes(ctx, param, status_codes: str) -> Set[int]:
    try:
        codes = status_codes.split(",")

        codes = {int(code.strip()) for code in codes}

    except Exception:
        raise click.BadParameter("Status codes are not integers split by commas")

    return codes


@click.command()
@click.argument("url")
@click.argument("wordlist", metavar="PATH_TO_WORDLIST", type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.option("--status-codes", callback=validate_status_codes, default="200", help="Comma separated list of status codes to show", show_default=True)
@click.option("--connections", type=int, default=1, help="Number of concurrent connections to use", show_default=True)
@click.option("--timeout", type=int, default=2, help="Number of seconds to wait for request before timing out", show_default=True)
@click_log.simple_verbosity_option(log, show_default=True)
def main(url: str, wordlist: click.Path, status_codes: Set[str], connections: int, timeout: int):
    if not url.endswith("/"):
        url = f"{url}/"

    # Not entirely satisfied with this implementation of click-log. I think we can just use the handlers and formatters
    click_log.basic_config(log)
    web_log.level = log.level
    click_log.basic_config(web_log)

    log.debug("Debug logging turned on")
    session = asks.Session(url, connections=connections)  # Connection pool with the base URL
    log.info("Running wordlist on base URL %s with %d connections and status codes %s.", url, connections, status_codes)

    trio.run(partial(async_main, session, wordlist, status_codes, timeout=timeout))


if __name__ == "__main__":
    main()
