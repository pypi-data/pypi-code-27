import argparse
import itertools
import logging
import pathlib

import consumers
import git
import github
import gitlab


GITLAB_URL = 'https://gitlab.com'


def get_gitlab_groups(name, api):
    try:
        yield api.users.list(username=name)[0]
    except (gitlab.GitlabGetError, IndexError):
        pass

    try:
        group = api.groups.get(name)
    except gitlab.GitlabGetError:
        return

    yield group

    groups = [group]
    while groups:
        subgroups = []
        for group in groups:
            for subgroup in group.subgroups.list(
                    all_available=True, as_list=False):
                subgroup = api.groups.get(subgroup.id)
                yield subgroup
                subgroups.append(subgroup)
        groups = subgroups


def get_gitlab_project(path, api):
    try:
        return api.projects.get(path)
    except gitlab.GitlabGetError:
        pass


def get_gitlab_projects(path, api):
    project = get_gitlab_project(path, api)
    if project:
        yield project

    for group in get_gitlab_groups(path, api):
        yield from group.projects.list(all_available=True, as_list=False)


def get_gitlab_repos(path, token):
    api = gitlab.Gitlab(GITLAB_URL, private_token=token)

    for project in get_gitlab_projects(path, api):
        yield project.path_with_namespace, project.ssh_url_to_repo


def get_github_repos(path, token):
    api = github.Github(token)

    repos = []
    if '/' in path:
        repo = api.get_repo(path)
        if repo:
            repos.append(repo)
    else:
        repos = api.get_user(path).get_repos()

    for repo in repos:
        yield repo.full_name, repo.ssh_url


def download_repos(repos, directory):
    errors = []
    logger = logging.getLogger()

    for path, url in repos:
        local_path = pathlib.Path(directory, path)
        logger.info('Backing up %s', local_path)
        try:
            if local_path.exists():
                repo = git.Repo(local_path)
                for remote in repo.remotes:
                    remote.fetch()
                if repo.branches:
                    repo.remote().pull()
            else:
                git.Repo.clone_from(url, local_path)
        except Exception as e:
            logger.exception(e)
            errors.append(local_path)
    return errors


PROVIDER_FUNCTIONS = {
    'github': get_github_repos,
    'gitlab': get_gitlab_repos
}


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s %(processName)s %(message)s')

    logging.info('Begin')

    parser = argparse.ArgumentParser(
            description='Clone all the repos belonging to a user.')
    parser.add_argument('-d', '--directory', default='.')
    parser.add_argument('-t', '--token', required=True)
    parser.add_argument('-p', '--provider', choices=PROVIDER_FUNCTIONS.keys())
    parser.add_argument('paths', nargs='*')
    args = parser.parse_args()

    repos = itertools.chain(*[
        PROVIDER_FUNCTIONS[args.provider](path, args.token)
        for path in args.paths
    ])

    with consumers.Pool(download_repos, args=[args.directory]) as pool:
        for path, url in repos:
            pool.put(path, url)

    for error in itertools.chain(*pool.results):
        logging.error(error)

    logging.info('Done')


if __name__ == '__main__':
    main()
