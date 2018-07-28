#-*- coding:utf-8 -*-
"""
Unit tests for the service module.
"""
#pylint:disable=wildcard-import,unused-wildcard-import,redefined-outer-name,unused-argument,invalid-name,line-too-long
import os
import glob
import mock
from .fixtures import *

def test_create_key_user(key_factory, git, tmpdir):
    """
    Try to create a key to a new user:
    must succeed.
    """
    user = gen_str()
    key = key_factory()
    assert not os.path.exists('{}/keydir/{}/'.format(str(tmpdir), user))
    body = {'user': user, 'key':key, 'user_creation': True}
    created = git.create_key(body, mock.Mock())
    assert created is True
    assert os.path.exists('{}/keydir/{}/'.format(str(tmpdir), user))
    assert len(glob.glob('{}/keydir/{}/*/{}.pub'.format(str(tmpdir), user, user))) == 1

def test_create_key_simple_ok(user_factory, key_factory, git, tmpdir):
    """
    Try to create a key to an user:
    must succeed.
    """
    user = user_factory()
    assert len(glob.glob('{0}/keydir/{1}/*/{1}.pub'.format(str(tmpdir), user))) == 1
    key = key_factory()
    body = {'user':user, 'key':key}
    created = git.create_key(body, mock.Mock())
    assert created is True
    assert len(glob.glob('{0}/keydir/{1}/*/{1}.pub'.format(str(tmpdir), user))) == 2

def test_create_key_simple_idempotent(user_factory, key_factory, git, tmpdir):
    """
    Try to create a key twice to an user:
    must succeed (the second time will be ignored).
    """
    user = user_factory()
    key = key_factory()
    body = {'user':user, 'key':key}
    assert len(glob.glob('{0}/keydir/{1}/*/{1}.pub'.format(str(tmpdir), user))) == 1
    created = git.create_key(body, mock.Mock())
    assert created is True
    assert len(glob.glob('{0}/keydir/{1}/*/{1}.pub'.format(str(tmpdir), user))) == 2
    created = git.create_key(body, mock.Mock())
    assert created is True
    assert len(glob.glob('{0}/keydir/{1}/*/{1}.pub'.format(str(tmpdir), user))) == 2

def test_delete_key_simple(user_factory, key_factory, git, tmpdir):
    """
    Try to delete a key:
    must succeed.
    """
    key = key_factory()
    md5key = hash_key(key)
    user = user_factory(key)
    assert os.path.exists('{0}/keydir/{1}/'.format(str(tmpdir), user))
    assert os.path.exists('{0}/keydir/{1}/{2}/{1}.pub'.format(str(tmpdir), user, md5key))
    body = {'user':user, 'key':key}
    delete = git.delete_key(body, mock.Mock())
    assert delete is True
    assert not os.path.exists('{0}/keydir/{1}/{2}/{1}.pub'.format(str(tmpdir), user, md5key))

def test_delete_key_inexistant(user_factory, key_factory, git, tmpdir):
    """
    Try to delete a key that doesn't exist:
    must succeed.
    """
    key = key_factory()
    md5key = hash_key(key)
    user = user_factory()
    assert not os.path.exists('{0}/keydir/{1}/{2}/{1}.pub'.format(str(tmpdir), user, md5key))
    body = {'user':user, 'key':key}
    delete = git.delete_key(body, mock.Mock())
    assert delete is True
    assert not os.path.exists('{0}/keydir/{1}/{2}/{1}.pub'.format(str(tmpdir), user, md5key))

def test_create_repo_simple(group_factory, git, tmpdir):
    """
    Try to create a repo adding one user:
    must succeed.
    """
    group = group_factory()
    repo = gen_str()
    body = {'repo': repo, 'organization':group}
    assert git.create_repo(body, mock.Mock()) is True
    assert os.path.exists('{0}/conf/repos/{1}.conf'.format(str(tmpdir), repo))
    assert """repo {0}
       RW+         =        @{1}""".format(repo, group) == open('{0}/conf/repos/{1}.conf'.format(str(tmpdir), repo)).read().strip()

def test_create_repo_simple_idempotent(group_factory, git, tmpdir):
    """
    Try to create twice a repo with the same group:
    must succeed.
    """
    group = group_factory()
    repo = gen_str()
    body = {'repo': repo, 'organization':group}
    git.create_repo(body, mock.Mock())
    git.create_repo(body, mock.Mock())
    assert """repo {0}
       RW+         =        @{1}""".format(repo, group) == open('{0}/conf/repos/{1}.conf'.format(str(tmpdir), repo)).read().strip()

def test_delete_repo_simple(repo_factory, git, tmpdir):
    """
    Try to delete a repo:
    must succeed.
    """
    repo = repo_factory()
    assert os.path.exists('{0}/conf/repos/{1}.conf'.format(str(tmpdir), repo))
    body = {'repo': repo}
    deleted = git.delete_repo(body, mock.Mock())
    assert deleted is True
    assert not os.path.exists('{0}/conf/repos/{1}.conf'.format(str(tmpdir), repo))

def test_delete_repo_inexistant(repo_factory, git, tmpdir):
    """
    Try to delete a repo inexistant:
    must succeed.
    """
    assert not os.path.exists('{0}/conf/repos/i-dont-exist.conf'.format(str(tmpdir)))
    body = {'repo': 'i-dont-exist'}
    deleted = git.delete_repo(body, mock.Mock())
    assert deleted is True
    assert not os.path.exists('{0}/conf/repos/i-dont-exist.conf'.format(str(tmpdir)))

def test_delete_user_one_key(user_factory, git, tmpdir):
    """
    Try to delete an user which only have one key and no repo:
    must succeed.
    """
    user = user_factory()
    assert os.path.exists('{0}/keydir/{1}/'.format(str(tmpdir), user))
    deleted = git.delete_user({'user':user}, mock.Mock())
    assert deleted is True
    assert not os.path.exists('{0}/keydir/{1}/'.format(str(tmpdir), user))

def test_delete_user_inexistant(user_factory, git, tmpdir):
    """
    Try to delete an user twice:
    must succeed.
    """
    user = user_factory()
    git.delete_user({'user':user}, mock.Mock())
    deleted = git.delete_user({'user':user}, mock.Mock())
    assert deleted is True

def test_delete_user_two_keys(user_factory, key_factory, git, tmpdir):
    """
    Try to delete an user which have two keys and no repo:
    must succeed.
    """
    user = user_factory()
    git.create_key({'user':user, 'key':key_factory()}, mock.Mock())
    deleted = git.delete_user({'user':user}, mock.Mock())
    assert deleted is True
    assert not os.path.exists('{0}/keydir/{1}/'.format(str(tmpdir), user))

def test_add_member(user_factory, group_factory, git, tmpdir):
    """
    Add a member to an organization.
    """
    user = user_factory()
    group = group_factory()
    body = {'account':user, 'organization':group}
    git.create_member(body, mock.Mock())
    assert open('{0}/conf/groups/{1}.conf'.format(str(tmpdir), group)).read() == "@{} = {}\n".format(group, user)

def test_add_member_multi(user_factory, group_factory, git, tmpdir):
    """
    Add several members to an organization.
    """
    user1 = user_factory()
    group = group_factory()
    body = {'account':user1, 'organization':group}
    git.create_member(body, mock.Mock())
    assert open('{0}/conf/groups/{1}.conf'.format(str(tmpdir), group)).read() == "@{} = {}\n".format(group, user1)
    #
    user2 = user_factory()
    body = {'account':user2, 'organization':group}
    git.create_member(body, mock.Mock())
    user3 = user_factory()
    body = {'account':user3, 'organization':group}
    git.create_member(body, mock.Mock())
    assert open('{0}/conf/groups/{1}.conf'.format(str(tmpdir), group)).read() == "@{0} = {1}\n@{0} = {2}\n@{0} = {3}\n".format(group, user1, user2, user3)

def test_add_member_idempotent(user_factory, group_factory, git, tmpdir):
    """
    Add twice a member to an organization.
    """
    user = user_factory()
    group = group_factory()
    body = {'account':user, 'organization':group}
    git.create_member(body, mock.Mock())
    assert open('{0}/conf/groups/{1}.conf'.format(str(tmpdir), group)).read() == "@{} = {}\n".format(group, user)
    #
    git.create_member(body, mock.Mock())
    assert open('{0}/conf/groups/{1}.conf'.format(str(tmpdir), group)).read() == "@{} = {}\n".format(group, user)

def test_add_member_invalid(group_factory, git, tmpdir):
    """
    Add a non existing member a member to an organization.
    """
    group = group_factory()
    body = {'account':'user', 'organization':group}
    git.create_member(body, mock.Mock())
    assert open('{0}/conf/groups/{1}.conf'.format(str(tmpdir), group)).read() == ""

def test_delete_member_on_orga(user_factory, group_factory, git, tmpdir):
    """
    Try to delete an user which is on an organization which contains another user.
    must succeed.
    """
    user1 = user_factory()
    user2 = user_factory()
    group = group_factory(users=[user1, user2])
    assert user1 in open('{0}/conf/groups/{1}.conf'.format(str(tmpdir), group)).read().strip()
    assert user2 in open('{0}/conf/groups/{1}.conf'.format(str(tmpdir), group)).read().strip()
    deleted = git.delete_user({'user':user1}, mock.Mock())
    assert deleted is True
    assert not os.path.exists('{0}/keydir/{1}/'.format(str(tmpdir), user1))
    assert user1 not in open('{0}/conf/groups/{1}.conf'.format(str(tmpdir), group)).read().strip()
    assert user2 in open('{0}/conf/groups/{1}.conf'.format(str(tmpdir), group)).read().strip()

def test_delete_organization(group_factory, git, tmpdir):
    """
    Delete an organization.
    """
    group = group_factory()
    assert os.path.exists('{0}/conf/groups/{1}.conf'.format(str(tmpdir), group))
    git.delete_organization({'organization':group}, mock.Mock())
    assert not os.path.exists('{0}/conf/groups/{1}.conf'.format(str(tmpdir), group))

def test_delete_organization_not_exist(group_factory, git, tmpdir):
    """
    Delete an organization which does not exist.
    """
    assert git.delete_organization({'organization':'group'}, mock.Mock())

def test_delete_organization_in_repo(group_factory, git, tmpdir):
    """
    Delete an organization.
    """
    group = group_factory()
    repo = gen_str()
    body = {'repo': repo, 'organization':group}
    git.create_repo(body, mock.Mock())
    assert os.path.exists('{0}/conf/groups/{1}.conf'.format(str(tmpdir), group))
    assert os.path.exists('{0}/conf/repos/{1}.conf'.format(str(tmpdir), repo))
    assert group in open('{0}/conf/repos/{1}.conf'.format(str(tmpdir), repo)).read().strip()
    ###
    git.delete_organization({'organization':group}, mock.Mock())
    assert not os.path.exists('{0}/conf/groups/{1}.conf'.format(str(tmpdir), group))
    assert os.path.exists('{0}/conf/repos/{1}.conf'.format(str(tmpdir), repo))
    assert group not in open('{0}/conf/repos/{1}.conf'.format(str(tmpdir), repo)).read().strip()
