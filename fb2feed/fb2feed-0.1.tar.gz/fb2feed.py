import mechanicalsoup
from feedgen.feed import FeedGenerator
import pytz
import datetime
import asyncio
from aiohttp import ClientSession
from urllib.parse import urlparse
from xdg import XDG_CONFIG_HOME
import os, sys, configparser

__version__ = "0.1"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15"
MAX_CONCURRENT_REQUESTS = 100

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()


async def bound_fetch(sem, url, session, media_dir):
    async with sem:
        destination = url_filename(url)
        full_path = os.path.join(media_dir, destination)
        os.makedirs(media_dir, exist_ok=True)
        if os.path.isfile(full_path):
            return

        data = await fetch(url, session)
        f = open(full_path, 'wb')
        f.write(data)
        f.close()

def url_filename(url):
    parsed = urlparse(url)
    return os.path.basename(parsed.path)

async def page_to_atom(browser, page_id, root_dir, media_dir, media_url_slug):
    tasks = []
    sem = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    async with ClientSession() as session:

        fb_url = 'https://www.facebook.com/%s/posts' % page_id
        browser.open(fb_url)
        page = browser.get_current_page()

        fg = FeedGenerator()
        fg.generator("Fb2Feed", version=__version__)
        fg.id(fb_url)
        fg.title(page.title.text.split('-')[0].strip().title())

        # profile_section = page.find_all('a', attrs={"aria-label": "Profile picture"})
        # print(profile_section)
        # fg.logo()
        updated = False

        for wrapper in page.select('div.userContentWrapper'):
            abbr = wrapper.select('abbr')[0]

            post_url = browser.absolute_url(abbr.parent.attrs["href"])
            post_id = abbr.attrs['data-utime']

            timestamp = datetime.datetime.utcfromtimestamp(int(post_id))
            timestamp = timestamp.replace(tzinfo=pytz.utc)

            if not updated:
                fg.updated(timestamp)
                updated = True

            txt = ''.join([ div.text for div in wrapper.select('div.userContent') ])
            if not txt:
                continue

            imgs = []
            for link in wrapper.find_all('a', attrs={'rel': 'theater'}):
                try:
                    img_url = link.attrs['data-ploi']
                except KeyError:
                    continue

                tasks.append(asyncio.ensure_future(bound_fetch(sem, img_url, session, media_dir)))
                imgs.append('<img src="%s%s"/>' % (media_url_slug, url_filename(img_url)))

            # TODO: cache videos, somehow.

            txt += ''.join(imgs)

            fe = fg.add_entry()
            fe.author(name=page_id, email="%s.facebook.no-reply@fb2feed.org" % page_id)
            fe.id(post_url)
            fe.link(href=post_url, rel="alternate")
            fe.published(timestamp)
            fe.updated(timestamp)
            fe.title(txt[:50])
            fe.description(txt)

        await asyncio.gather(*tasks)
        fg.atom_file(os.path.join(root_dir, '%s.atom.xml' % page_id))

def main(*args):
    config = configparser.ConfigParser()
    config.read(os.path.join(XDG_CONFIG_HOME, 'fb2feed.ini'))
    page_ids = config.sections()
    root_dir = config['DEFAULT']['root_directory']
    media_dir = config['DEFAULT']['media_directory']
    media_url_slug = config['DEFAULT']['media_url_slug']

    browser = mechanicalsoup.StatefulBrowser()
    browser.set_user_agent(USER_AGENT)

    tasks = [asyncio.ensure_future(page_to_atom(browser, page_id, root_dir, media_dir, media_url_slug))
             for page_id in page_ids]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
