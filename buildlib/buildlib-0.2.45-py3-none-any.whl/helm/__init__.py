from typing import Optional, List, Pattern, Union
from cmdi import command, CmdResult, strip_args
import subprocess as sp


def parse_option(
    flag: str,
    val: Union[List[str], bool],
    sep: 'str' = '',
) -> list:
    """"""
    if flag in ['', None]:
        flag = []
    else:
        flag = [flag]

    if type(val) == str:
        return flag + [val]
    if type(val) == list:
        return flag + [sep.join(val)]
    elif type(val) == bool and val is True:
        return flag
    else:
        return []


class cmd:

    @staticmethod
    @command
    def install(
        chart: str,  # [CHART]
        namespace: List[str],  # --namespace
        name: Optional[str],  # --name
        force: bool = False,  # --force
        values: Optional[str] = None,  # -f, --values
        version: Optional[str] = None,  # --version
        **cmdargs
    ) -> CmdResult:
        return install(**strip_args(locals()))

    @staticmethod
    @command
    def upgrade(
        release: str,  # [RELEASE]
        chart: str,  # [CHART]
        namespace: List[str],  # --namespace
        force: bool = False,  # --force
        recreate_pods: bool = False,  # --recreate-pods
        **cmdargs
    ) -> CmdResult:
        return upgrade(**strip_args(locals()))


def install(
    chart: str,  # [CHART]
    namespace: List[str],  # --namespace
    name: Optional[str],  # --name
    force: bool = False,  # --force
    values: Optional[str] = None,  # -f, --values
    version: Optional[str] = None,  # --version
) -> None:
    """
    helm install mw/mw-adminer --version 0.0.1 --name mw-adminer --namespace mw -f values.yaml
    """
    options = [
        *parse_option(flag='', val=chart, sep=''),
        *parse_option(flag='--namespace', val=namespace, sep=','),
        *parse_option(flag='--name', val=name, sep=','),
        *parse_option(flag='--force', val=force, sep=''),
        *parse_option(flag='--values', val=values, sep=''),
        *parse_option(flag='--version', val=version, sep=''),
    ]

    cmd = ['helm', 'install'] + options

    print(cmd)

    sp.run(cmd, check=True)


def upgrade(
    release: str,  # [RELEASE]
    chart: str,  # [CHART]
    namespace: List[str],  # --namespace
    force: bool = False,  # --force
    recreate_pods: bool = False,  # --recreate-pods
) -> None:
    """
    helm upgrade logcenter chart --force --recreate-pods --namespace mw-prod
    """
    options = [
        *parse_option(flag='', val=release, sep=''),
        *parse_option(flag='', val=chart, sep=''),
        *parse_option(flag='--namespace', val=namespace, sep=','),
        *parse_option(flag='--force', val=force, sep=''),
        *parse_option(flag='--recreate-pods', val=recreate_pods, sep=''),
    ]

    cmd = ['helm', 'upgrade'] + options

    print(cmd)

    sp.run(cmd, check=True)
