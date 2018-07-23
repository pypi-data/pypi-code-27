import os
import json
import zipfile
import tarfile
import git
import string
import mistune


def sanitize(str):
    valid_chars = set("-_.()%s%s" % (string.ascii_letters, string.digits))
    return ''.join(
        c for c in str
        if c in valid_chars
    )


class Multisite(object):
    def __init__(self, config_file=None):
        self.config_file = config_file or 'multisite.json'
        if os.path.isfile(self.config_file):
            with open(self.config_file) as f:
                self.sites = json.load(f)
        else:
            self.sites = {}
            self.__save__()
        self.update(force=False)

    def __save__(self):
        with open(self.config_file, 'w') as f:
            f.write(json.dumps(self.sites, indent=2))

    def update(self, name=None, force=True):
        for _name, site in self.sites.items():
            if name is not None and name != _name:
                continue
            if not (site['auto_update'] or force):
                continue
            source_type = site['source_type']
            if source_type is None:
                continue
            if source_type == 'git':
                # pull latest from git repository
                g = git.cmd.Git(site['location'])
                g.checkout(site['branch'])
                g.pull(site['remote'], site['branch'], '-f')

    def add_site(
        self,
        name,
        source=None,
        source_type='local',
        auto_update=False,
        **kwargs
    ):
        default_location = os.path.join(os.path.curdir, name)
        site = {
            'name': name,
            'source': source,
            'location': default_location,
            'source_type': source_type,
            'auto_update': auto_update
        }
        if source_type == 'local':
            if os.path.isdir(source):
                # map /<name>/* to source directory
                site['location'] = source
        elif source_type == 'archive':
            os.makedirs(default_location)
            if source.endswith('.zip'):
                # extract zipfile to ./<name>/
                zip_ref = zipfile.Zipfile(source, 'r')
                zip_ref.extractall(default_location)
                zip_ref.close()
            elif (
                source.endswith('.tar') or
                source.endswith('.tar.gz') or
                source.endswith('.tar.bz2') or
                source.endswith('.tar.xz')
            ):
                # extract tarball to ./<name>/
                tar = tarfile.open(source)
                tar.extractall(default_location)
                tar.close()
        elif source_type == 'git':
            # clone git repository to ./<name>/
            site['remote'] = kwargs.get('git_remote', 'origin')
            site['branch'] = kwargs.get('git_branch', 'master')
            repo = git.Repo.init(default_location)
            origin = repo.create_remote(site['remote'], source)
            origin.fetch()
            g = git.cmd.Git(default_location)
            g.checkout(site['branch'])
            g.pull(site['remote'], site['branch'])
        self.sites[name] = site
        self.__save__()

    def page(self, path, exts=['html', 'md']):
        def serve(fpath):
            with open(fpath) as f:
                contents = f.read()
            if ext == 'md':
                contents = mistune.Markdown()(contents)
            return contents
        if exts is None and os.path.isfile(path):
            return serve(path)
        for ext in exts:
            fpath = '.'.join((path, ext))
            if os.path.isfile(fpath):
                return serve(fpath)

    def not_found(self):
        return 404, self.page('404') or '404: Page not found'

    def homepage(self):
        contents = self.page('index')
        if contents is None:
            return self.not_found()
        return 200, contents

    def get(self, path):
        path = path.lstrip('/')
        if path == '':
            return self.homepage()
        path_parts = path.split('/', 1)
        name = path_parts.pop(0)
        if name not in self.sites:
            return self.not_found()
        if path_parts:
            path = path_parts.pop()
            exts = None
        else:
            path = 'index'
            exts = ['html', 'md']
        filepath = os.path.join(self.sites[name]['location'], path)
        contents = self.page(filepath, exts)
        if contents is None:
            return self.not_found()
        return 200, contents
