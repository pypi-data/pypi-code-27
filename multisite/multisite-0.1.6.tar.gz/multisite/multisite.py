import os
import json
import zipfile
import tarfile
import git
import string
import mistune
import shutil
import sys

PYTHON3 = sys.version_info[0] == 3


def sanitize(str):
    valid_chars = set("-_.()%s%s" % (string.ascii_letters, string.digits))
    return ''.join(
        c for c in str
        if c in valid_chars
    )


def extract_zip(src, dest):
    zip_ref = zipfile.ZipFile(src, 'r')
    zip_ref.extractall(dest)
    zip_ref.close()


def extract_tarball(src, dest):
    tar = tarfile.open(src)
    tar.extractall(dest)
    tar.close()


def import_archive(src, dest):
    os.makedirs(dest, exist_ok=True)
    if src.endswith('.zip'):
        extract_zip(src, dest)
        return
    elif (
        src.endswith('.tar') or
        src.endswith('.tar.gz') or
        src.endswith('.tar.bz2')
    ):
        extract_tarball(src, dest)
        return
    elif src.endswith('.tar.xz'):
        if PYTHON3:
            extract_tarball(src, dest)
            return
    raise ValueError('{} is not a recognized archive format'.format(src))


def import_git(remote_url, dest, remote_name='origin', branch_name='master'):
    # clone git repository to ./<name>/
    repo = git.Repo.init(dest)
    origin = repo.create_remote(remote_name, remote_url)
    origin.fetch()
    g = git.cmd.Git(dest)
    g.checkout(branch_name)
    g.pull(remote_name, branch_name)


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
            else:
                raise OSError('{} is not a directory'.format(source))
        elif source_type == 'archive':
            import_archive(source, default_location)
        elif source_type == 'git':
            # clone git repository to ./<name>/
            site['remote'] = kwargs.get('git_remote', 'origin')
            site['branch'] = kwargs.get('git_branch', 'master')
            import_git(
                source,
                default_location,
                site['remote'],
                site['branch']
            )
        self.sites[name] = site
        self.__save__()

    def page(self, path, exts=['html', 'md']):
        def serve(fpath):
            with open(fpath) as f:
                contents = f.read()
            _, ext = os.path.splitext(fpath)
            if ext == '.md':
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
        path = path.strip('/')
        if path == '':
            return self.homepage()
        path_parts = path.split('/', 1)
        name = path_parts.pop(0)
        if name not in self.sites:
            return self.not_found()
        if path_parts:
            path = path_parts.pop()
            ext = os.path.splitext(path)[1]
            if ext == '':
                exts = ['html', 'md']
            else:
                exts = None
        else:
            path = 'index'
            exts = ['html', 'md']
        filepath = os.path.join(self.sites[name]['location'], path)
        contents = self.page(filepath, exts)
        if contents is None:
            return self.not_found()
        return 200, contents

    def make_static(self, target_directory='html'):
        if os.path.isdir(target_directory):
            shutil.rmtree(target_directory)
        os.makedirs(target_directory)
        for filename in (f for f in os.listdir('.') if os.path.isfile(f)):
            filename, ext = os.path.splitext(filename)
            if ext in ('.html', '.md'):
                dest = os.path.join(
                    target_directory,
                    '{}.html'.format(filename)
                )
                contents = self.page(filename)
                if contents is not None:
                    with open(dest, 'w') as f:
                        f.write(contents)
        for name, site in self.sites.items():
            dirpath = os.path.join(target_directory, name)
            for dirpath, dirnames, filenames in os.walk(site['location']):
                dirpath = dirpath.lstrip('./')
                if any(d.startswith('.') for d in dirpath.split(os.path.sep)):
                    continue
                for filename in filenames:
                    filename, ext = os.path.splitext(filename)
                    if ext in ('.html', '.md'):
                        src = os.path.join(dirpath, filename)
                        if dirpath != '' and filename == 'index':
                            dest = os.path.join(
                                target_directory,
                                '{}.html'.format(name)
                            )
                        else:
                            dest_dir = os.path.join(target_directory, dirpath)
                            os.makedirs(dest_dir, exist_ok=True)
                            dest = os.path.join(
                                dest_dir,
                                '{}.html'.format(filename)
                            )
                        contents = self.page(src)
                        if contents is not None:
                            with open(dest, 'w') as f:
                                f.write(contents)
