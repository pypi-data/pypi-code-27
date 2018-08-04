import glob

import click

from github import Github


class GithubRelease(object):
    def __init__(self, github):
        self.github = github


@click.group(
    context_settings={
        'auto_envvar_prefix': 'GITHUB_RELEASE_CICD',
    },
)
@click.option(
    '--token',
    help='GitHub API token.',
    envvar='TOKEN',
    required=True,
)
@click.option(
    '--repo',
    help='GitHub repository name.',
    envvar='REPO',
    required=True,
)
@click.version_option()
@click.pass_context
def cli(ctx, token, repo):
    """Manage GitHub releases."""

    ctx.obj = Github(token).get_user().get_repo(repo)


@cli.command()
@click.option(
    '--tag',
    help='Release tag.',
    envvar='TAG',
    required=True,
)
@click.option(
    '--name',
    help='Release name.',
    envvar='NAME',
)
@click.option(
    '--message',
    help='Release message.',
    envvar='MESSAGE',
    required=True,
)
@click.option(
    '--draft',
    help='Release is a draft.',
    envvar='DRAFT',
    default=False,
)
@click.option(
    '--prerelease',
    help='Release is a prerelease.',
    envvar='PRERELEASE',
    default=False,
)
@click.option(
    '--target',
    help='Release commit target.',
    envvar='TARGET',
)
@click.option(
    '--assets',
    help='Release assets to upload.',
    envvar='ASSETS',
)
@click.pass_obj
def create(repo, tag, name, message, draft, prerelease, target, assets):
    """Create release."""

    if not name:
        name = tag

    release = repo.create_git_release(
        tag=tag,
        name=tag,
        message=message,
        target_commitish=target,
    )

    for item in glob.glob(assets):
        release.upload_asset(item)
