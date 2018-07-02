"""
Update MSL packages.
"""
import sys
import subprocess
from pkg_resources import parse_version

from colorama import Fore

from . import utils, _PKG_NAME


def update(*names, **kwargs):
    """Update MSL packages.

    MSL packages can be updated from PyPI packages_ (only if a release has been
    uploaded to PyPI) or from GitHub repositories_.

    .. note::
       If the MSL packages_ are available on PyPI then PyPI is used as the default
       URI_ to update the package. If you want to force the update to occur
       from the ``master`` branch of the GitHub `repository <https://github.com/MSLNZ>`_
       then set ``branch='master'``. If the package is not available on PyPI
       then the ``master`` branch is used as the default update URI_.

    .. _repositories: https://github.com/MSLNZ
    .. _packages: https://pypi.org/search/?q=msl-
    .. _URI: https://en.wikipedia.org/wiki/Uniform_Resource_Identifier

    Parameters
    ----------
    *names : :class:`tuple` of :class:`str`
        The name(s) of the MSL package(s) to update. If empty then
        update **all** MSL packages (except for the **MSL Package Manager** --
        in which case use ``pip install -U msl-package-manager``).
    **kwargs
        yes : :class:`bool`, default :data:`False`
            If :data:`True` then don't ask for confirmation before updating.
            The default is to ask before updating.
        branch : :class:`str`, default :data:`None`
            The name of a GitHub branch to use for the update. If :data:`None`, and no
            `tag` value has also been specified, then updates the package using the
            ``master`` branch.
        tag : :class:`str`, default :data:`None`
            The name of a GitHub tag to use for the update.
        update_cache : :class:`bool`, default :data:`False`
            The information about the MSL packages_ that are available on PyPI and about
            the repositories_ that are available on GitHub are cached to use for subsequent
            calls to this function. After 24 hours the cache is automatically updated. Set
            `update_cache` to be :data:`True` to force the cache to be updated when you call
            this function.

        .. attention::
           Cannot specify both a `branch` and a `tag` simultaneously.

        .. important::
           If you specify a `branch` or a `tag` then the update will be forced.
    """
    # Python 2.7 does not support named arguments after using *args
    # we can define yes=False, branch=None, tag=None, update_cache=False in the function signature
    # if we choose to drop support for Python 2.7
    utils._check_kwargs(kwargs, {'yes', 'branch', 'tag', 'update_cache'})

    yes = kwargs.get('yes', False)
    branch = kwargs.get('branch', None)
    tag = kwargs.get('tag', None)
    update_cache = kwargs.get('update_cache', False)

    zip_name = utils._get_github_zip_name(branch, tag)
    if zip_name is None:
        return

    pkgs_installed = utils.installed()

    pkgs_github = utils.github(update_cache)
    pkgs_pypi = utils.pypi(update_cache)
    if not pkgs_github and not pkgs_pypi:
        return

    names = utils._check_msl_prefix(*names)
    if not names:
        names = [pkg for pkg in pkgs_installed if pkg != _PKG_NAME]
    elif _PKG_NAME in names:
        utils.log.warning('Use "pip install -U {}" to update the MSL Package Manager'.format(_PKG_NAME))
        del names[names.index(utils._PKG_NAME)]

    w = [0, 0]
    pkgs_to_update = {}
    for name in names:

        err_msg = 'Cannot update {}: '.format(name)

        if name not in pkgs_installed:
            utils.log.error(err_msg + 'package not installed')
            continue

        if name not in pkgs_github and name not in pkgs_pypi:
            utils.log.error(err_msg + 'package not found on GitHub or PyPI')
            continue

        installed_version = pkgs_installed[name]['version']

        # use PyPI to update the package (only if the package is available on PyPI)
        using_pypi = name in pkgs_pypi and tag is None and branch is None

        if tag is not None:
            if tag in pkgs_github[name]['tags']:
                pkgs_to_update[name] = (installed_version, '[tag:{}]'.format(tag), using_pypi)
            else:
                utils.log.error(err_msg + 'a "{}" tag does not exist'.format(tag))
                continue
        elif branch is not None:
            if branch in pkgs_github[name]['branches']:
                pkgs_to_update[name] = (installed_version, '[branch:{}]'.format(branch), using_pypi)
            else:
                utils.log.error(err_msg + 'a "{}" branch does not exist'.format(branch))
                continue
        else:
            if using_pypi:
                version = pkgs_pypi[name]['version']
            else:
                version = pkgs_github[name]['version']

            if not version:
                # a version number must exist on PyPI, so if this occurs it must be for a github repo
                utils.log.error(err_msg + 'the github repository does not contain a release')
                continue
            elif parse_version(version) > parse_version(installed_version):
                pkgs_to_update[name] = (installed_version, version, using_pypi)
            else:
                utils.log.warning('The {} package is already the latest [{}]'.format(name, installed_version))
                continue

        w = [max(w[0], len(name)), max(w[1], len(installed_version))]

    if pkgs_to_update:
        pkgs_to_update = utils._sort_packages(pkgs_to_update)

        msg = '\nThe following MSL packages will be {}UPDATED{}:\n'.format(Fore.CYAN, Fore.RESET)
        for pkg in pkgs_to_update:
            local, remote, _ = pkgs_to_update[pkg]
            pkg += ': '
            msg += '\n  ' + pkg.ljust(w[0]+2) + local.ljust(w[1]) + ' --> ' + remote

        utils.log.info(msg)
        if not (yes or utils._ask_proceed()):
            return

        utils.log.info('')

        exe = [sys.executable, '-m', 'pip', 'install']
        options = ['--upgrade', '--force-reinstall', '--no-deps'] + ['--quiet'] * utils._NUM_QUIET
        for pkg in pkgs_to_update:
            if pkgs_to_update[pkg][2]:
                utils.log.debug('Updating {} from PyPI'.format(pkg))
                package = [pkg]
            else:
                utils.log.debug('Updating {} from GitHub/{}'.format(pkg, zip_name))
                package = ['https://github.com/MSLNZ/{}/archive/{}.zip'.format(pkg, zip_name)]
            subprocess.call(exe + options + package)
    else:
        utils.log.info('No MSL packages to update')
