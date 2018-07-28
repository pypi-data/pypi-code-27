#-*- coding:utf-8 -*-
#pylint:disable=missing-docstring,unused-import,no-member,line-too-long,no-name-in-module,redefined-outer-name
import hashlib
import os
import random
import shutil
import string
import mock
import pytest
from Crypto.PublicKey import RSA
import farine.settings
from farine.tests.fixtures import amqp_factory, message_factory, queue_factory

def gen_str(length=15):
    """
    Generate a string of `length`.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in xrange(length))

def hash_key(key):
    """
    Return the key using the gitolite hash.
    """
    return hashlib.md5(key.strip().split()[1]).hexdigest()

@pytest.fixture()
def key_factory():
    def factory():
        return RSA.generate(1024).publickey().exportKey('OpenSSH')
    return factory

@pytest.fixture(autouse=True, scope='function')
def settings(tmpdir):
    farine.settings.load()
    farine.settings.frasage['gitolite'] = str(tmpdir)
    os.makedirs(os.path.join(str(tmpdir), 'keydir'))
    os.makedirs(os.path.join(str(tmpdir), 'conf', 'repos'))
    os.makedirs(os.path.join(str(tmpdir), 'conf', 'groups'))

@pytest.fixture()
def git():
    """
    Git service fixture.
    """
    with mock.patch('pyolite.git.Frasage.commit', mock.MagicMock()):
        import frasage.service
        yield frasage.service.Frasage()

@pytest.fixture()
def user_factory(key_factory, git):
    """
    Factory for user creation.
    """
    def factory(key=None):
        username = gen_str()
        key = key or key_factory()
        body = {'user':username, 'key':key, 'user_creation': True}
        git.create_key(body, mock.Mock())
        return username
    return factory

@pytest.fixture()
def repo_factory(group_factory, git):
    """
    Factory for repo creation.
    """
    def factory(group=None):
        name = gen_str()
        group = group or group_factory()
        body = {'repo':name, 'organization':group}
        git.create_repo(body, mock.Mock())
        return name
    return factory

@pytest.fixture()
def group_factory(git):
    """
    Factory for group creation.
    """
    def factory(users=None):
        users = users or []
        name = gen_str()
        git.olite.groups.create(name)
        for user in users:
            git.olite.groups.user_add(name, user)
        return name
    return factory
