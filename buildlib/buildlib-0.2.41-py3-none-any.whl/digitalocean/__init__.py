import os
import requests
from typing import Optional, List, Pattern, Union
from cmdi import command, CmdResult, set_result, strip_args

API_V2_URL = 'https://api.digitalocean.com/v2'
TOKEN_NAME = 'DIGITALOCEAN_TOKEN'

if not TOKEN_NAME in os.environ:
    os.environ[TOKEN_NAME] = ''


class cmd:

    @staticmethod
    @command
    def set_access_token_envvar(token: str, **cmdargs) -> CmdResult:
        return set_access_token_envvar(**strip_args(locals()))

    @staticmethod
    @command
    def get_volumes(
        name_contains: Optional[List[str]] = None,
        region: Optional[str] = 'fra1',
        **cmdargs
    ) -> CmdResult:
        return get_volumes(**strip_args(locals()))

    @staticmethod
    @command
    def create_volume(
        name: str,
        size_gb: Optional[int] = None,
        description: Optional[str] = '',
        region: Optional[str] = 'fra1',
        snapshot_id: Optional[str] = None,
        **cmdargs
    ) -> CmdResult:
        return create_volume(**strip_args(locals()))

    @staticmethod
    @command
    def delete_volume(volume_id: str, **cmdargs) -> CmdResult:
        return delete_volume(**strip_args(locals()))

    @staticmethod
    @command
    def get_volume_snapshots(
        volume_id: Optional[str] = None,
        name_contains: Optional[List[str]] = None,
        region: Optional[str] = 'fra1',
        **cmdargs
    ) -> CmdResult:
        return get_volume_snapshots(**strip_args(locals()))

    @staticmethod
    @command
    def create_volume_snapshot(
        name: str, volume_id: str, **cmdargs
    ) -> CmdResult:
        return create_volume_snapshot(**strip_args(locals()))

    @staticmethod
    @command
    def delete_snapshot(snapshot_id: str, **cmdargs) -> CmdResult:
        return delete_snapshot(**strip_args(locals()))


def set_access_token_envvar(token: str):
    os.environ[TOKEN_NAME] = token


def get_volumes(
    name_contains: Optional[List[str]] = None,
    region: Optional[str] = 'fra1',
) -> List[dict]:

    headers = {"Authorization": f"Bearer {os.environ[TOKEN_NAME]}"}
    params = {'region': region}

    r = requests.get(
        f'{API_V2_URL}/volumes',
        headers=headers,
        params=params,
    )

    r.raise_for_status()

    data = r.json()

    if not 'volumes' in data:
        return []

    if name_contains:

        filtered = []

        for vol in data['volumes']:
            if all([substr in vol['name'] for substr in name_contains]):
                filtered.append(vol)

        return filtered

    else:
        return data['volumes']


def create_volume(
    name: str,
    size_gb: Optional[int] = None,
    description: Optional[str] = '',
    region: Optional[str] = 'fra1',
    snapshot_id: Optional[str] = None,
) -> dict:

    headers = {
        "Authorization": f"Bearer {os.environ[TOKEN_NAME]}",
        "Content-Type": "application/json",
    }

    data = {
        "size_gigabytes": size_gb,
        "name": name,
        "description": description,
        "region": region,
    }

    if snapshot_id:
        data['snapshot_id'] = snapshot_id

    r = requests.post(
        f'{API_V2_URL}/volumes',
        headers=headers,
        json=data,
    )

    r.raise_for_status()

    return r.json()['volume']


def delete_volume(volume_id: str) -> None:
    """
    This deletes a snapshot of both kinds: "volume" and "droplet".
    """

    headers = {"Authorization": f"Bearer {os.environ[TOKEN_NAME]}"}

    r = requests.delete(
        f'{API_V2_URL}/volumes/{volume_id}',
        headers=headers,
    )

    r.raise_for_status()


def get_volume_snapshots(
    volume_id: Optional[str] = None,
    name_contains: Optional[List[str]] = None,
    region: Optional[str] = 'fra1',
) -> List[dict]:

    headers = {"Authorization": f"Bearer {os.environ[TOKEN_NAME]}"}
    params = {'region': region}

    if volume_id:
        r = requests.get(
            f'{API_V2_URL}/volumes/{volume_id}/snapshots',
            headers=headers,
            params=params,
        )
    else:
        r = requests.get(
            f'{API_V2_URL}/snapshots',
            headers=headers,
            params=params,
        )

    r.raise_for_status()

    data = r.json()

    if not 'snapshots' in data:
        return []

    if name_contains:

        filtered = []

        for snap in data['snapshots']:
            if all([substr in snap['name'] for substr in name_contains]):
                filtered.append(snap)

        return filtered

    else:
        return data['snapshots']


def create_volume_snapshot(name: str, volume_id: str) -> dict:

    headers = {
        "Authorization": f"Bearer {os.environ[TOKEN_NAME]}",
        "Content-Type": "application/json",
    }
    data = {'name': name}

    r = requests.post(
        f'{API_V2_URL}/volumes/{volume_id}/snapshots',
        headers=headers,
        json=data,
    )

    r.raise_for_status()

    return r.json()['snapshot']


def delete_snapshot(snapshot_id: str) -> None:
    """
    This deletes a snapshot of both kinds: "volume" and "droplet".
    """

    headers = {"Authorization": f"Bearer {os.environ[TOKEN_NAME]}"}

    r = requests.delete(
        f'{API_V2_URL}/snapshots/{snapshot_id}',
        headers=headers,
    )

    r.raise_for_status()
