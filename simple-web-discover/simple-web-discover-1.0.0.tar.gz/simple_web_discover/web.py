import asks
from asks.response_objects import Response
from asks.errors import TooManyRedirects
import trio
import click
from click import Path

from functools import partial
import logging
from typing import Set

asks.init("trio")

log = logging.getLogger(__name__)


class MockResponse:
    def __init__(self, url: str, status_code: int) -> None:
        """Used if the request returns a TooManyRedirection error."""
        self.url = url
        self.status_code = status_code


async def get_and_verify(session: asks.Session, status_codes: Set[int], end_path: str, **kwargs):
    try:
        response = await get_url(session, end_path, **kwargs)
    except Exception:
        log.debug("Failed to get URL %s/%s", session.base_location, end_path, exc_info=True)
        return

    if response.status_code in status_codes:
        print_response(response)


async def get_url(session: asks.Session, end_path: str, **kwargs):
    log.debug("Sending request to path: %s/%s", session.base_location, end_path)
    try:
        response = await session.get(path=end_path, max_redirects=0, timeout=2)
        return response
    except TooManyRedirects:
        return MockResponse(f"{session.base_location}{end_path}", 301)


async def async_main(session: asks.Session, wordlist_path: Path, status_codes: Set[int], **kwargs):
    # First get the base URL path
    try:
        first_response: Response = await get_url(session, end_path="", **kwargs)
    except Exception:
        log.debug("Failed to get first request for %s", session.base_location)
    else:
        if first_response.status_code in status_codes:
            print_response(first_response)

    # Then get the URLs from the file
    with open(wordlist_path) as wordlist:
        for line in wordlist:
            async with trio.open_nursery() as nursery:
                nursery.start_soon(partial(get_and_verify, session, status_codes,
                                           end_path=line.strip(),
                                           **kwargs))


def print_response(response: Response):
    """Echos details of the response colored by status code."""
    fg_color = None

    if 200 <= response.status_code < 300:
        fg_color = "green"
    if 300 <= response.status_code < 400:
        fg_color = "yellow"
    if 400 <= response.status_code < 600:
        fg_color = "red"

    click.secho(f"{response.url} - {response.status_code} - {len(response.content)} bytes", fg=fg_color)
