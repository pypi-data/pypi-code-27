import os
import re
import sys
import argparse

import requests_html


apbase_url = 'https://www.anime-planet.com'

login_ajax_url = 'https://www.anime-planet.com/ajaxDelegator.php?mode=login'
logout_ajax_url = 'https://www.anime-planet.com/login.php?logout=true'

anime_url_form = 'https://www.anime-planet.com/anime/{}'
anime_eps_url_form = 'https://www.anime-planet.com/api/list/update/anime/{id}/{eps}/{token}'

export_url = 'https://www.anime-planet.com/users/export_list.php'

AP_CONF_PATH = '~/.animeplanet.conf'


class AnimePlanetSession:

    def __init__(self, old_session=None):
        if old_session:
            self.session = old_session
        else:
            self.session = requests_html.HTMLSession()
            self.session.max_redirects = 5

        self._pages = {}

    def login(self, user, password):
        data = {
            'usr': user,
            'pwd': password,
        }

        r = self.session.post(login_ajax_url, data=data)

        assert r.html.html == 'Success'
        self._reset_pages()

    @property
    def token(self):
        m = re.search("var TOKEN = '(.*?)';", self.home.html)
        return m.group(1)

    def logout(self):
        data = {'key': self.token}

        r = self.session.post(logout_ajax_url, data=data, allow_redirects=False)
        self._reset_pages()
        return r

    def _reset_pages(self):
        self._pages = {}

    def get_cached_page(self, url):
        if url not in self._pages:
            self._pages[url] = self.session.get(url).html

        return self._pages[url]

    @property
    def home(self):
        return self.get_cached_page(apbase_url)

    def _siteuser_html(self):
        return self.home.find('div#siteUser')[0].html

    @property
    def logged(self):
        loggedin_divs = self.home.find('div.loggedIn')
        return bool(loggedin_divs)

    def logged_user(self):
        loggedin_divs = self.home.find('div.loggedIn')
        if not loggedin_divs:
            return None

        login = loggedin_divs[0]
        return login.find('a')[0].attrs["title"]

    @property
    def anime_json(self):
        export_list_page = self.get_cached_page(export_url)
        forms = export_list_page.find('form.pure-form')
        anime_export_path = forms[0].attrs['action']

        total_path = apbase_url + anime_export_path

        r = self.session.get(total_path)

        return r.json()

    def set_episodes(self, anime_base_name, eps):
        anime_id = self.anime_basename_to_id(anime_base_name)
        url = anime_eps_url_form.format(id=anime_id, eps=eps, token=self.token)
        return self.session.get(url)

    def anime_basename_to_id(self, base_name):
        url = anime_url_form.format(base_name)

        anime_page = self.get_cached_page(url)
        return int(anime_page.find('form.myListBar')[0].attrs['data-id'])


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--password')

    subparsers = parser.add_subparsers(dest='action')
    subparsers.required = True

    subp_eps = subparsers.add_parser('set-episodes', help='Set number of watched episodes')
    subp_eps.add_argument('anime_basename', help='Anime to modify.')
    subp_eps.add_argument('number_of_episodes', help='Number of watched episodes', type=int)

    return parser.parse_args()


def main():
    args = parse_args()

    if args.user is None or args.password is None:
        confpath = os.path.expanduser(AP_CONF_PATH)
        try:
            with open(confpath, 'r') as fd:
                user, password = fd.read().split(',', maxsplit=1)

        except IOError:
            print('Error. Credentials found neither in CLI arguments, nor in config file.')
            sys.exit(1)
    else:
        user = args.user
        password = args.password

    apses = AnimePlanetSession()
    apses.login(user, password)

    if args.action == 'set-episodes':
        apses.set_episodes(args.anime_basename, args.number_of_episodes)

    apses.logout()


if __name__ == '__main__':
    main()
